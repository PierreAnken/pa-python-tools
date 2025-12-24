"""
Module providing a custom JSON encoder and decoder to handle sets, datetimes, dates, and integer keys in dictionaries.
"""

import json
from datetime import datetime, date


class TaggedJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that supports sets, datetimes, dates, and integer keys in dictionaries.
    """

    def encode(self, obj):
        """
        Encode the object, converting integer keys in dictionaries to strings with a prefix.
        Handles nested structures.
        """
        return super().encode(self._encode_nested(obj))

    def _encode_nested(self, obj):
        """
        Recursively process nested dictionaries, lists and tuples.
        Handles various key types for dictionaries.
        """
        if isinstance(obj, dict):
            new_dict = {}
            for k, v in obj.items():
                if isinstance(k, bool):
                    new_key = f"__bool__{k}"
                elif isinstance(k, int):
                    new_key = f"__int__{k}"
                elif isinstance(k, float):
                    new_key = f"__float__{k}"
                elif isinstance(k, (datetime, date)):
                    new_key = f"__{type(k).__name__}__{k.isoformat()}"
                else:
                    new_key = k
                new_dict[new_key] = self._encode_nested(v)
            return new_dict
        if isinstance(obj, list):
            return [self._encode_nested(v) for v in obj]
        if isinstance(obj, tuple):
            return {"__tuple__": [self._encode_nested(v) for v in obj]}
        return obj

    def default(self, obj):
        """
        Handle sets, datetimes, and dates during encoding.
        """
        if isinstance(obj, set):
            return {"__set__": list(obj)}
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        if isinstance(obj, date):
            return {"__date__": obj.isoformat()}
        return super().default(obj)


def tagged_decoder_hook(d):
    """
    Custom JSON decoder that restores sets, datetimes, and integer keys from their encoded format.
    """
    # Sets
    if "__set__" in d:
        return set(d["__set__"])

    # Tuples
    if "__tuple__" in d:
        return tuple(d["__tuple__"])

    # Datetimes
    if "__datetime__" in d:
        return datetime.fromisoformat(d["__datetime__"])

    # Dates
    if "__date__" in d:
        return date.fromisoformat(d["__date__"])

    # Tagged keys
    new_dict = {}
    for k, v in d.items():
        if isinstance(k, str):
            if k.startswith("__int__"):
                new_dict[int(k.replace("__int__", ""))] = v
            elif k.startswith("__float__"):
                new_dict[float(k.replace("__float__", ""))] = v
            elif k.startswith("__bool__"):
                new_dict[k.replace("__bool__", "") == "True"] = v
            elif k.startswith("__datetime__"):
                new_dict[datetime.fromisoformat(k.replace("__datetime__", ""))] = v
            elif k.startswith("__date__"):
                new_dict[date.fromisoformat(k.replace("__date__", ""))] = v
            else:
                new_dict[k] = v
        else:
            new_dict[k] = v
    return new_dict
