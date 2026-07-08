"""
Data wrapper for easy access to nested dictionary data with JSON formatting.
"""
import json
from typing import Optional, Any

class Data:
    def __init__(self, data: dict):
        self._data = data

    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __getattr__(self, name: str):
        result = self._find_keys(name)
        if result is None:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'. "
                f"Available keys: {list(self._data.keys()) if isinstance(self._data, dict) else 'N/A'}"
            )
        return result

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(
                f"Key '{key}' not found. Available keys: {list(self._data.keys())}"
            )

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def _find_keys(self, keys, data=None):
        if data is None:
            data = self._data

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(data, dict):
            for key in keys:
                if key in data:
                    value = data[key]
                    if isinstance(value, dict):
                        return self.__class__(value)
                    elif isinstance(value, list):
                        return [self.__class__(item) if isinstance(item, dict) else item for item in value]
                    return value

            for value in data.values():
                if isinstance(value, (dict, list)):
                    result = self._find_keys(keys, value)
                    if result is not None:
                        return result

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    result = self._find_keys(keys, item)
                    if result is not None:
                        return result
        return None

    def _clean_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                k: self._clean_data(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self._clean_data(item) for item in data]
        return data

    def jsonify(self, indent: Optional[int] = None) -> str:
        return json.dumps(
            self._clean_data(self._data),
            indent=indent,
            ensure_ascii=False,
            default=str
        )

    @property
    def original_data(self):
        return self._data

    def to_dict(self) -> dict:
        return self._data

    def to_clean_dict(self) -> dict:
        return self._clean_data(self._data)

    def get(self, key: str, default=None):
        return self._data.get(key, default)