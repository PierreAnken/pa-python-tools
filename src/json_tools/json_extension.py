"""
Module providing a custom JSON encoder and decoder to handle sets, datetimes, dates, and integer keys in dictionaries.
"""

import json
from datetime import datetime, date


class CustomJSONEncoder(json.JSONEncoder):
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
        """
        if isinstance(obj, dict):
            return {f"__int__{k}" if isinstance(k, int) else k: self._encode_nested(v) for k, v in obj.items()}
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
        if isinstance(k, str) and k.startswith("__int__"):
            new_dict[int(k.replace("__int__", ""))] = v
        else:
            new_dict[k] = v
    return new_dict
