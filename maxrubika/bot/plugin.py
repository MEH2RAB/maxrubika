"""
Complete Plugin Management System for Rubika Bot
This module provides a robust plugin system with auto-discovery and dependency management
"""
from __future__ import annotations

import inspect
import logging
import os
import importlib.util
from dataclasses import dataclass, field
from typing import (
    Any, Dict, List, Optional, Set, Tuple,
    Type, Mapping
)

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    try:
        import importlib_metadata
    except ImportError:
        importlib_metadata = None

logger = logging.getLogger(__name__)

_UNNAMED = "unnamed"

@dataclass(frozen=True)
class PluginMeta:
    """
    Plugin metadata containing all information about a plugin.

    required_permissions is declarative metadata only (it is exposed via
    get_plugin_info); the manager does not enforce it.
    """
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = "Unknown"
    homepage: Optional[str] = None
    dependencies: Tuple[str, ...] = ()
    required_permissions: Tuple[str, ...] = ()
    default_config: Mapping[str, Any] = field(default_factory=dict)
    enabled_by_default: bool = False

class Plugin:
    """
    Base class that all plugins must inherit from.
    """
    meta = PluginMeta(name=_UNNAMED)

    def __init__(self, bot, *, config: Optional[Mapping[str, Any]] = None):
        self.bot = bot
        self.config = self._merge_config(config)
        self._is_ready = False

    @classmethod
    def identifier(cls) -> str:
        """Get unique plugin identifier."""
        if cls.meta and cls.meta.name and cls.meta.name != _UNNAMED:
            return cls.meta.name
        return cls.__name__.lower()

    async def setup(self) -> None:
        """Setup hook - called when plugin is enabled."""
        logger.info("Setting up plugin: %s", self.meta.name)
        self._is_ready = True

    async def teardown(self) -> None:
        """Teardown hook - called when plugin is disabled."""
        logger.info("Tearing down plugin: %s", self.meta.name)
        self._is_ready = False

    def configure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and modify config before saving."""
        return config

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        return self.config.get(key, default)

    def update_config(self, config: Optional[Mapping[str, Any]]) -> None:
        """Replace the current config (merged with the plugin's defaults)."""
        self.config = self._merge_config(config)

    def _merge_config(self, override: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
        """Merge default config with user config."""
        defaults = getattr(self.meta, "default_config", None) or {}
        merged = dict(defaults)

        if override:
            merged.update(override)

        configured = self.configure(merged)
        if configured is None:
            return merged
        if not isinstance(configured, dict):
            raise TypeError("Plugin.configure() must return a dict")

        return configured

    @property
    def is_ready(self) -> bool:
        """Is the plugin ready to work?"""
        return self._is_ready

class PluginLoadError(Exception):
    """Raised when plugin loading fails."""
    pass

class PluginDefinitionError(Exception):
    """Raised when plugin definition is invalid."""
    pass

class PluginManager:
    """
    Plugin Manager - handles registration, discovery, and lifecycle management
    """
    def __init__(
        self,
        bot,
        *,
        auto_discover: bool = True,
        plugins_dir: Optional[str] = "plugins",
        plugin_configs: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        self.bot = bot
        self.plugins_dir = plugins_dir
        self._registry: Dict[str, Type[Plugin]] = {}
        self._instances: Dict[str, Plugin] = {}
        self._enabled: Dict[str, Plugin] = {}
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._sources: Dict[str, str] = {}
        self._enabling_stack: Set[str] = set()

        if plugin_configs:
            for name, config in plugin_configs.items():
                self._configs[self._normalize(name)] = config

        if auto_discover:
            self.discover_plugins()

    def discover_plugins(self) -> List[str]:
        """Automatically discover plugins from various sources."""
        discovered = []

        if self.plugins_dir:
            discovered.extend(self._discover_from_directory())

        discovered.extend(self._discover_from_entry_points())

        return discovered

    @staticmethod
    def _load_module(file_path: str, module_name: str):
        """Execute a plugin file and return its module object."""
        spec = importlib.util.spec_from_file_location(
            f"plugins.{module_name}", file_path
        )
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Cannot load module from {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _plugin_classes_in(module) -> List[Type[Plugin]]:
        """Plugin subclasses defined in this module (not merely imported)."""
        classes = []
        for item_name in dir(module):
            item = getattr(module, item_name)
            if (
                inspect.isclass(item)
                and issubclass(item, Plugin)
                and item is not Plugin
                and item.__module__ == module.__name__
            ):
                classes.append(item)
        return classes

    def _discover_from_directory(self) -> List[str]:
        """Discover plugins from directory."""
        discovered = []

        if not self.plugins_dir or not os.path.isdir(self.plugins_dir):
            return discovered

        for file in sorted(os.listdir(self.plugins_dir)):
            if not file.endswith('.py') or file.startswith('__'):
                continue

            module_name = file[:-3]
            file_path = os.path.abspath(os.path.join(self.plugins_dir, file))
            try:
                module = self._load_module(file_path, module_name)
            except Exception as e:
                logger.error("Failed to load %s: %s", file, e)
                continue

            for item in self._plugin_classes_in(module):
                try:
                    identifier = self.register_plugin(item)
                except PluginDefinitionError as e:
                    logger.warning("Failed to register %s: %s", item.__name__, e)
                    continue
                self._sources[identifier] = file_path
                discovered.append(identifier)
                logger.info("Discovered plugin %s from %s", identifier, file)

        return discovered

    def _discover_from_entry_points(self) -> List[str]:
        """Discover plugins from entry points."""
        discovered = []

        if importlib_metadata is None:
            return discovered

        try:
            entry_points = importlib_metadata.entry_points()

            if hasattr(entry_points, 'select'):
                plugin_entry_points = entry_points.select(group='rubika.plugins')
            else:
                plugin_entry_points = entry_points.get('rubika.plugins', [])

            for entry_point in plugin_entry_points:
                try:
                    plugin_cls = entry_point.load()
                    identifier = self.register_plugin(plugin_cls)
                    discovered.append(identifier)
                    logger.info("Discovered plugin %s from entry point.", identifier)
                except Exception as e:
                    logger.error("Failed to load entry point %s: %s", entry_point.name, e)

        except Exception as e:
            logger.debug("Failed to read entry points: %s", e)

        return discovered

    @staticmethod
    def _prepare_class(plugin_cls: Type[Plugin], identifier: str) -> None:
        """Give a plugin without its own name a meta matching its identifier."""
        meta = getattr(plugin_cls, "meta", None)
        if meta is None or not meta.name or meta.name == _UNNAMED:
            plugin_cls.meta = PluginMeta(name=identifier)

    def register_plugin(
        self,
        plugin_cls: Type[Plugin],
        name: Optional[str] = None
    ) -> str:
        """Register a new plugin."""
        if not inspect.isclass(plugin_cls) or not issubclass(plugin_cls, Plugin):
            raise PluginDefinitionError("Must inherit from Plugin class.")

        identifier = (name or plugin_cls.identifier()).strip().lower()
        if not identifier:
            raise PluginDefinitionError("Plugin identifier cannot be empty.")

        if identifier in self._registry:
            raise PluginDefinitionError(f"Plugin {identifier} already registered.")

        self._prepare_class(plugin_cls, identifier)

        self._registry[identifier] = plugin_cls
        logger.debug("Plugin %s registered successfully.", identifier)

        return identifier

    def unregister_plugin(self, identifier: str) -> bool:
        """Remove a plugin from registry. Enabled plugins cannot be removed."""
        key = self._normalize(identifier)

        if key in self._enabled:
            return False

        removed = self._registry.pop(key, None) is not None
        self._instances.pop(key, None)
        self._sources.pop(key, None)

        if removed:
            logger.debug("Plugin %s unregistered.", identifier)
        return removed

    def _enabled_dependents(self, key: str) -> List[str]:
        """Enabled plugins that list `key` among their dependencies."""
        dependents = []
        for other_key, instance in self._enabled.items():
            deps = getattr(instance.meta, "dependencies", None) or ()
            if key in {self._normalize(d) for d in deps}:
                dependents.append(other_key)
        return dependents

    async def enable(self, identifier: str) -> Plugin:
        """Enable a plugin (and, first, its dependencies)."""
        key = self._normalize(identifier)

        plugin_cls = self._registry.get(key)
        if not plugin_cls:
            raise PluginLoadError(f"Plugin {identifier} not registered.")

        if key in self._enabled:
            return self._enabled[key]

        if key in self._enabling_stack:
            raise PluginLoadError(f"Circular dependency detected in plugin {identifier}.")

        self._enabling_stack.add(key)
        try:
            instance = self._instances.get(key)
            if instance is None:
                try:
                    instance = plugin_cls(self.bot, config=self._configs.get(key))
                except Exception as e:
                    raise PluginLoadError(
                        f"Failed to instantiate plugin {identifier}: {e}"
                    ) from e
                self._instances[key] = instance

            await self._enable_dependencies(plugin_cls)

            try:
                await instance.setup()
            except Exception as e:
                raise PluginLoadError(f"Plugin {identifier} setup failed: {e}") from e

            self._enabled[key] = instance
            logger.info("Plugin %s enabled.", identifier)
            return instance
        except BaseException:
            failed = self._instances.pop(key, None)
            if failed is not None:
                failed._is_ready = False
            raise
        finally:
            self._enabling_stack.discard(key)

    async def enable_many(self, identifiers: List[str]) -> List[Plugin]:
        """Enable multiple plugins."""
        results = []
        for identifier in identifiers:
            results.append(await self.enable(identifier))
        return results

    async def enable_all(self) -> List[Plugin]:
        """Enable all registered plugins; one failure does not stop the rest."""
        enabled = []
        for identifier in self.registered_plugins:
            try:
                enabled.append(await self.enable(identifier))
            except Exception as e:
                logger.error("Failed to enable %s: %s", identifier, e)
        return enabled

    async def enable_defaults(self) -> List[Plugin]:
        """Enable every registered plugin whose meta has enabled_by_default=True."""
        enabled = []
        for identifier in self.registered_plugins:
            if not getattr(self._registry[identifier].meta, "enabled_by_default", False):
                continue
            try:
                enabled.append(await self.enable(identifier))
            except Exception as e:
                logger.error("Failed to enable %s: %s", identifier, e)
        return enabled

    async def disable(self, identifier: str) -> bool:
        """Disable a plugin. Refused while other enabled plugins depend on it."""
        key = self._normalize(identifier)
        instance = self._enabled.get(key)

        if not instance:
            return False

        dependents = self._enabled_dependents(key)
        if dependents:
            logger.warning(
                "Cannot disable %s: required by %s", identifier, ", ".join(dependents)
            )
            return False

        try:
            await instance.teardown()
        except Exception as e:
            logger.error("Failed to disable %s: %s", identifier, e)
            return False

        self._enabled.pop(key, None)
        logger.info("Plugin %s disabled", identifier)
        return True

    async def disable_all(self) -> None:
        """Disable all plugins in reverse order (dependents before dependencies)."""
        for identifier in reversed(self.enabled_plugins):
            await self.disable(identifier)

    async def reload(self, identifier: str) -> Plugin:
        """
        Reload a plugin: disable it, drop its instance and, when it came from
        a file in plugins_dir, re-execute that file so code changes take effect.
        """
        key = self._normalize(identifier)
        if key not in self._registry:
            raise PluginLoadError(f"Plugin {identifier} not registered.")

        if key in self._enabled and not await self.disable(key):
            raise PluginLoadError(
                f"Cannot reload {identifier}: it could not be disabled "
                f"(is another enabled plugin depending on it?)."
            )

        self._instances.pop(key, None)

        source = self._sources.get(key)
        if source:
            module_name = os.path.splitext(os.path.basename(source))[0]
            try:
                module = self._load_module(source, module_name)
            except Exception as e:
                raise PluginLoadError(f"Failed to reload module for {identifier}: {e}") from e

            for cls in self._plugin_classes_in(module):
                if cls.identifier().strip().lower() == key:
                    self._prepare_class(cls, key)
                    self._registry[key] = cls
                    break
            else:
                raise PluginLoadError(
                    f"Plugin {identifier} not found after reloading {source}."
                )

        return await self.enable(key)

    async def _enable_dependencies(self, plugin_cls: Type[Plugin]) -> None:
        """Enable plugin dependencies."""
        dependencies = getattr(plugin_cls.meta, "dependencies", None) or ()

        for dep in dependencies:
            try:
                await self.enable(dep)
            except PluginLoadError as e:
                raise PluginLoadError(
                    f"Failed to enable dependency {dep} for {plugin_cls.meta.name}: {e}"
                ) from e

    def _normalize(self, identifier: str) -> str:
        """Normalize plugin identifier."""
        return identifier.strip().lower()

    @property
    def registered_plugins(self) -> List[str]:
        """List of registered plugins."""
        return list(self._registry.keys())

    @property
    def enabled_plugins(self) -> List[str]:
        """List of enabled plugins (in enable order)."""
        return list(self._enabled.keys())

    def get_plugin(self, identifier: str) -> Optional[Plugin]:
        """Get plugin instance (if enabled)."""
        return self._enabled.get(self._normalize(identifier))

    def get_all_plugins(self) -> Dict[str, Plugin]:
        """Get all enabled plugins."""
        return self._enabled.copy()

    def is_registered(self, identifier: str) -> bool:
        """Is plugin registered?"""
        return self._normalize(identifier) in self._registry

    def is_enabled(self, identifier: str) -> bool:
        """Is plugin enabled?"""
        return self._normalize(identifier) in self._enabled

    def set_config(self, identifier: str, config: Dict[str, Any]) -> None:
        """Set plugin configuration."""
        key = self._normalize(identifier)
        self._configs[key] = config

        instance = self._instances.get(key)
        if instance is not None:
            instance.update_config(config)

    def get_config(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get plugin configuration."""
        return self._configs.get(self._normalize(identifier))

    def get_plugin_info(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get complete plugin information."""
        key = self._normalize(identifier)
        plugin_cls = self._registry.get(key)

        if not plugin_cls:
            return None

        instance = self._instances.get(key)
        meta = plugin_cls.meta

        return {
            'name': meta.name,
            'version': meta.version,
            'description': meta.description,
            'author': meta.author,
            'homepage': meta.homepage,
            'dependencies': meta.dependencies,
            'required_permissions': meta.required_permissions,
            'enabled_by_default': meta.enabled_by_default,
            'enabled': key in self._enabled,
            'ready': instance.is_ready if instance else False,
            'config': self._configs.get(key, {})
        }

def create_plugin(
    name: str,
    version: str = "1.0.0",
    description: str = "",
    author: str = "Unknown",
    dependencies: Tuple[str, ...] = ()
):
    """
    Decorator for quick plugin creation

    Example:
    @create_plugin("greeter", version="1.0.0")
    class GreeterPlugin(Plugin):
        async def setup(self):
            await self.bot.send_message("Hello World!")
    """
    def decorator(cls):
        cls.meta = PluginMeta(
            name=name,
            version=version,
            description=description,
            author=author,
            dependencies=dependencies
        )
        return cls
    return decorator