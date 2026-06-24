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

@dataclass(frozen=True)
class PluginMeta:
    """
    Plugin metadata containing all information about a plugin.
    """
    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = "Unknown"
    homepage: Optional[str] = None
    dependencies: Tuple[str, ...] = ()
    required_permissions: List[str] = field(default_factory=list)
    default_config: Mapping[str, Any] = field(default_factory=dict)
    enabled_by_default: bool = False

class Plugin:
    """
    Base class that all plugins must inherit from.
    """
    meta = PluginMeta(name="unnamed")

    def __init__(self, bot, *, config: Optional[Mapping[str, Any]] = None):
        self.bot = bot
        self.config = self._merge_config(config)
        self._is_ready = False

    @classmethod
    def identifier(cls) -> str:
        """Get unique plugin identifier."""
        if cls.meta and cls.meta.name and cls.meta.name != "unnamed":
            return cls.meta.name
        return cls.__name__.lower()

    async def setup(self) -> None:
        """Setup hook - called when plugin is enabled."""
        logger.info(f"Setting up plugin: {self.meta.name}")
        self._is_ready = True

    async def teardown(self) -> None:
        """Teardown hook - called when plugin is disabled."""
        logger.info(f"Tearing down plugin: {self.meta.name}")
        self._is_ready = False

    def configure(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and modify config before saving."""
        return config

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        return self.config.get(key, default)

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

    def _discover_from_directory(self) -> List[str]:
        """Discover plugins from directory."""
        discovered = []

        if not os.path.exists(self.plugins_dir):
            return []

        for file in os.listdir(self.plugins_dir):
            if file.endswith('.py') and not file.startswith('__'):
                module_name = file[:-3]
                try:
                    file_path = os.path.abspath(os.path.join(self.plugins_dir, file))
                    spec = importlib.util.spec_from_file_location(
                        f"plugins.{module_name}",
                        file_path
                    )
                    if spec is None or spec.loader is None:
                        continue

                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if (inspect.isclass(item) and 
                            issubclass(item, Plugin) and 
                            item != Plugin):
                            try:
                                identifier = self.register_plugin(item)
                                discovered.append(identifier)
                                logger.info(f"Discovered plugin {identifier} from {file}")
                            except PluginDefinitionError as e:
                                logger.warning(f"Failed to register {item_name}: {e}")

                except Exception as e:
                    logger.error(f"Failed to load {file}: {e}")

        return discovered

    def _discover_from_entry_points(self) -> List[str]:
        """Discover plugins from entry points."""
        discovered = []

        if importlib_metadata is None:
            return discovered

        try:
            entry_points = importlib_metadata.entry_points()
            plugin_entry_points = []

            if hasattr(entry_points, 'select'):
                plugin_entry_points = entry_points.select(group='rubika.plugins')
            else:
                plugin_entry_points = entry_points.get('rubika.plugins', [])

            for entry_point in plugin_entry_points:
                try:
                    plugin_cls = entry_point.load()
                    identifier = self.register_plugin(plugin_cls)
                    discovered.append(identifier)
                    logger.info(f"Discovered plugin {identifier} from entry point.")
                except Exception as e:
                    logger.error(f"Failed to load entry point {entry_point.name}: {e}")

        except Exception as e:
            logger.debug(f"Failed to read entry points: {e}")

        return discovered

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

        if not hasattr(plugin_cls, 'meta') or not plugin_cls.meta.name:
            plugin_cls.meta = PluginMeta(name=identifier)

        self._registry[identifier] = plugin_cls
        logger.debug(f"Plugin {identifier} registered successfully.")

        return identifier

    def unregister_plugin(self, identifier: str) -> bool:
        """Remove a plugin from registry."""
        key = self._normalize(identifier)

        if key in self._enabled:
            return False

        removed = self._registry.pop(key, None) is not None
        self._instances.pop(key, None)
        self._enabled.pop(key, None)

        if removed:
            logger.debug(f"Plugin {identifier} unregistered.")
        return removed
    
    async def enable(self, identifier: str) -> Plugin:
        """Enable a plugin."""
        key = self._normalize(identifier)

        plugin_cls = self._registry.get(key)
        if not plugin_cls:
            raise PluginLoadError(f"Plugin {identifier} not registered.")

        instance = self._instances.get(key)
        if not instance:
            try:
                instance = plugin_cls(
                    self.bot,
                    config=self._configs.get(key)
                )
                self._instances[key] = instance
            except Exception as e:
                raise PluginLoadError(f"Failed to instantiate plugin {identifier}: {e}")

        if key in self._enabled:
            return instance

        if key in self._enabling_stack:
            raise PluginLoadError(f"Circular dependency detected in plugin {identifier}.")

        self._enabling_stack.add(key)
        try:
            await self._enable_dependencies(plugin_cls)
            await instance.setup()
            self._enabled[key] = instance
            logger.info(f"Plugin {identifier} enabled.")
            return instance
        finally:
            self._enabling_stack.discard(key)

    async def enable_many(self, identifiers: List[str]) -> List[Plugin]:
        """Enable multiple plugins."""
        results = []
        for identifier in identifiers:
            results.append(await self.enable(identifier))
        return results

    async def enable_all(self) -> List[Plugin]:
        """Enable all registered plugins."""
        enabled = []
        for identifier in self.registered_plugins:
            try:
                enabled.append(await self.enable(identifier))
            except PluginLoadError as e:
                logger.error(f"Failed to enable {identifier}: {e}")
        return enabled

    async def disable(self, identifier: str) -> bool:
        """Disable a plugin."""
        key = self._normalize(identifier)
        instance = self._enabled.get(key)

        if not instance:
            return False

        try:
            await instance.teardown()
            self._enabled.pop(key, None)
            logger.info(f"Plugin {identifier} disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable {identifier}: {e}")
            return False

    async def disable_all(self) -> None:
        """Disable all plugins."""
        for identifier in self.enabled_plugins:
            await self.disable(identifier)

    async def reload(self, identifier: str) -> Plugin:
        """Reload a plugin."""
        await self.disable(identifier)
        return await self.enable(identifier)
    
    async def _enable_dependencies(self, plugin_cls: Type[Plugin]) -> None:
        """Enable plugin dependencies."""
        dependencies = getattr(plugin_cls.meta, "dependencies", None) or ()

        for dep in dependencies:
            try:
                await self.enable(dep)
            except PluginLoadError as e:
                raise PluginLoadError(
                    f"Failed to enable dependency {dep} for {plugin_cls.meta.name}: {e}"
                )

    def _normalize(self, identifier: str) -> str:
        """Normalize plugin identifier."""
        return identifier.strip().lower()

    @property
    def registered_plugins(self) -> List[str]:
        """List of registered plugins."""
        return list(self._registry.keys())

    @property
    def enabled_plugins(self) -> List[str]:
        """List of enabled plugins."""
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

        if key in self._instances:
            instance = self._instances[key]
            instance.config = instance._merge_config(config)

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

        return {
            'name': plugin_cls.meta.name,
            'version': plugin_cls.meta.version,
            'description': plugin_cls.meta.description,
            'author': plugin_cls.meta.author,
            'dependencies': plugin_cls.meta.dependencies,
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