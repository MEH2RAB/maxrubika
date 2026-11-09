from __future__ import annotations

import asyncio
import atexit
import concurrent.futures
import functools
import inspect
import threading
from contextlib import suppress
from typing import Any, AsyncGenerator, Generator, Optional, TypeVar

T = TypeVar("T")

class SyncLoop:
    def __init__(self, name: str = "sync-loop-worker") -> None:
        self._name = name
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._ready = threading.Event()
        self._lock = threading.Lock()
        self._closed = False

    def start(self) -> asyncio.AbstractEventLoop:
        with self._lock:
            if self._closed:
                raise RuntimeError("SyncLoop has been closed.")

            if self._thread is None or not self._thread.is_alive():
                self._ready.clear()
                self._thread = threading.Thread(
                    target=self._worker,
                    name=self._name,
                    daemon=True,
                )
                self._thread.start()

            ready = self._ready

        if not ready.wait(timeout=10.0):
            raise RuntimeError("SyncLoop worker failed to start in time.")

        loop = self._loop
        if loop is None or loop.is_closed():
            raise RuntimeError("SyncLoop worker did not initialize a loop.")
        return loop

    def run(self, coro) -> Any:
        if not inspect.iscoroutine(coro):
            raise TypeError(
                f"Expected a coroutine, got {type(coro).__name__}."
            )

        try:
            if threading.current_thread() is self._thread:
                raise RuntimeError(
                    "Cannot run a synchronous call from inside the SyncLoop worker."
                )
            loop = self.start()
        except BaseException:
            with suppress(Exception):
                coro.close()
            raise

        future = asyncio.run_coroutine_threadsafe(coro, loop)

        try:
            return future.result()
        except BaseException:
            with suppress(Exception):
                future.cancel()
            raise

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            loop = self._loop
            thread = self._thread

        if loop is not None and loop.is_running():
            with suppress(Exception):
                loop.call_soon_threadsafe(loop.stop)

        if thread is not None and thread.is_alive() \
                and thread is not threading.current_thread():
            thread.join(timeout=10.0)

        self._loop = None
        self._thread = None

    def _worker(self) -> None:
        loop = asyncio.new_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(
            thread_name_prefix=f"{self._name}-exec",
        )
        loop.set_default_executor(executor)
        asyncio.set_event_loop(loop)

        self._loop = loop
        self._ready.set()

        try:
            loop.run_forever()
        finally:
            self._shutdown(loop, executor)

    def _shutdown(
        self,
        loop: asyncio.AbstractEventLoop,
        executor: concurrent.futures.ThreadPoolExecutor,
    ) -> None:
        with suppress(Exception):
            pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for t in pending:
                t.cancel()
            if pending:
                loop.run_until_complete(asyncio.wait(pending, timeout=3.0))

        with suppress(Exception):
            loop.run_until_complete(
                asyncio.wait_for(loop.shutdown_asyncgens(), timeout=3.0)
            )

        with suppress(Exception):
            loop.run_until_complete(
                asyncio.wait_for(loop.shutdown_default_executor(), timeout=3.0)
            )

        with suppress(Exception):
            loop.close()

        with suppress(Exception):
            executor.shutdown(wait=False, cancel_futures=True)

_sync_loop = SyncLoop()
atexit.register(_sync_loop.close)

def close_sync_loop() -> None:
    _sync_loop.close()

def _has_running_loop() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True

def _run_sync(coro) -> Any:
    return _sync_loop.run(coro)

def _close_coro(coro) -> None:
    with suppress(Exception):
        coro.close()

def _sync_async_generator(
    agen: AsyncGenerator[T, None],
) -> Generator[T, None, None]:
    try:
        while True:
            try:
                async def _next():
                    return await agen.__anext__()
                yield _run_sync(_next())
            except StopAsyncIteration:
                return
    finally:
        async def _close():
            await agen.aclose()
        coro = _close()
        try:
            _run_sync(coro)
        except BaseException:
            _close_coro(coro)

def async_to_sync(obj: Any, name: str) -> None:
    raw = None
    for cls in obj.__mro__:
        if name in cls.__dict__:
            raw = cls.__dict__[name]
            break

    if raw is None:
        return

    if isinstance(raw, (staticmethod, classmethod)):
        func = raw.__func__
    else:
        func = raw

    is_coro = inspect.iscoroutinefunction(func)
    is_agen = inspect.isasyncgenfunction(func)
    if not (is_coro or is_agen):
        return

    bound = func

    if is_agen:
        @functools.wraps(bound)
        def wrapper(*args, **kwargs):
            agen = bound(*args, **kwargs)
            if _has_running_loop():
                return agen
            return _sync_async_generator(agen)
    else:
        @functools.wraps(bound)
        def wrapper(*args, **kwargs):
            coro = bound(*args, **kwargs)
            if _has_running_loop():
                return coro
            try:
                return _run_sync(coro)
            except BaseException:
                _close_coro(coro)
                raise

    if isinstance(obj, type) and isinstance(raw, staticmethod):
        setattr(obj, name, staticmethod(wrapper))
    elif isinstance(obj, type) and isinstance(raw, classmethod):
        setattr(obj, name, classmethod(wrapper))
    else:
        setattr(obj, name, wrapper)

def wrap_methods(source: Any) -> None:
    for name, method in inspect.getmembers(
        source,
        predicate=lambda m: (
            inspect.isfunction(m)
            or inspect.ismethod(m)
            or inspect.iscoroutinefunction(m)
            or inspect.isasyncgenfunction(m)
        ),
    ):
        if name.startswith("_"):
            continue
        async_to_sync(source, name)