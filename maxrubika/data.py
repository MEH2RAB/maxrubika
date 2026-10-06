import json
from typing import Optional, Set, Any, List, Union

_MISSING = object()

class Data:
    _EXCLUDED_KEYS: Set[str] = {'_client', '_memo', '_regex_match', 'client', 'track_id'}

    def __init__(self, data: Any):
        self._data = data
        self._memo = {}

    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def __getattr__(self, name: str):
        if (
            name in ('_data', '_memo')
            or (name.startswith('__') and name.endswith('__'))
        ):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

        result = self.find_keys(name, default=_MISSING)

        if result is _MISSING:
            if isinstance(self._data, dict):
                available = list(self._data.keys())
            elif isinstance(self._data, list):
                available = f"list of {len(self._data)} items"
            else:
                available = "N/A"

            raise AttributeError(
                f"'{type(self).__name__}' has no attribute '{name}'. "
                f"Available: {available}"
            )

        return result

    def __getitem__(self, key):
        if isinstance(self._data, dict):
            try:
                return self._convert_value(self._data[key])
            except KeyError:
                pass

            if isinstance(key, str):
                result = self.find_keys(key, default=_MISSING)
                if result is not _MISSING:
                    return result

            raise KeyError(
                f"Key '{key}' not found. "
                f"Available keys: {list(self._data.keys())}"
            ) from None

        if isinstance(self._data, list):
            if isinstance(key, str):
                result = self.find_keys(key, default=_MISSING)
                if result is not _MISSING:
                    return result

            try:
                return self._convert_value(self._data[key])
            except (IndexError, TypeError):
                raise IndexError(
                    f"Index '{key}' not found in list "
                    f"of length {len(self._data)}"
                ) from None

        raise TypeError(f"Cannot index '{type(self._data).__name__}'")

    def __setitem__(self, key, value):
        if isinstance(self._data, (dict, list)):
            self._data[key] = value
            return

        raise TypeError(
            f"Cannot set item on "
            f"'{type(self._data).__name__}' Data object"
        )

    def __contains__(self, key):
        if isinstance(self._data, (dict, list)):
            return key in self._data

        return False

    def __delitem__(self, key):
        if isinstance(self._data, (dict, list)):
            del self._data[key]
            return

        raise TypeError(
            f"Cannot delete item from "
            f"'{type(self._data).__name__}' Data object"
        )

    def __iter__(self):
        if isinstance(self._data, list):
            return (self._convert_value(item) for item in self._data)

        if isinstance(self._data, dict):
            return iter(self._data)

        raise TypeError(
            f"'{type(self._data).__name__}' object is not iterable"
        )

    def __len__(self) -> int:
        if isinstance(self._data, (dict, list)):
            return len(self._data)

        return 0

    def _convert_value(self, value: Any) -> Any:
        if type(value) is dict:
            return self.__class__(value)

        if type(value) is list:
            return [self._convert_value(item) for item in value]

        return value

    def find_keys(
        self,
        keys: Union[str, List[Any]],
        data: Any = None,
        default: Any = None,
    ) -> Any:
        if data is None:
            data = self._data

        target = self._normalize_keys(keys)

        if isinstance(data, list):
            stack = data[::-1]
        else:
            stack = [data]

        while stack:
            node = stack.pop()

            if type(node) is dict:
                for key in node:
                    if key in target:
                        return self._convert_value(node[key])

                for value in reversed(tuple(node.values())):
                    if type(value) is dict or type(value) is list:
                        stack.append(value)

            elif type(node) is list:
                for item in reversed(node):
                    if type(item) is dict or type(item) is list:
                        stack.append(item)

        return default

    def _normalize_keys(self, keys: Union[str, List[Any]]) -> frozenset:
        if isinstance(keys, str):
            return frozenset((keys,))

        if isinstance(keys, (list, tuple, set, frozenset)):
            return frozenset(keys)

        raise TypeError(
            "keys must be str, list, tuple or set, "
            f"got {type(keys).__name__}"
        )

    def _clean_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                key: self._clean_data(value)
                for key, value in data.items()
                if key not in self._EXCLUDED_KEYS
            }

        if isinstance(data, list):
            return [self._clean_data(item) for item in data]

        return data

    def jsonify(self, indent: Optional[int] = None) -> str:
        return json.dumps(
            self._clean_data(self._data),
            indent=indent,
            ensure_ascii=False,
            default=str,
        )

    @property
    def original_data(self):
        return self._data

    def to_dict(self):
        if isinstance(self._data, dict):
            return self._data.copy()

        if isinstance(self._data, list):
            return self._data.copy()

        return self._data

    def to_clean_dict(self):
        return self._clean_data(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        if not isinstance(self._data, dict):
            return default

        value = self._data.get(key, _MISSING)

        if value is _MISSING:
            return default

        return self._convert_value(value)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __eq__(self, other):
        if isinstance(other, Data):
            return self._data == other._data

        return self._data == other