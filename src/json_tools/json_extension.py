"""
Module providing a custom JSON encoder and decoder to handle sets, datetimes, and integer keys in dictionaries.
"""

import json
from datetime import datetime


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that supports sets, datetimes, and integer keys in dictionaries.
    """

    def encode(self, obj):
        """
        Encode the object, converting integer keys in dictionaries to strings with a prefix.
        Handles nested structures.
        """
        if isinstance(obj, dict):
            new_obj = {f"__int__{k}" if isinstance(k, int) else k: self._encode_nested(v) for k, v in obj.items()}
            return super().encode(new_obj)
        if isinstance(obj, list):
            return super().encode([self._encode_nested(v) for v in obj])
        return super().encode(obj)

    def _encode_nested(self, obj):
        """
        Recursively process nested dictionaries and lists.
        """
        if isinstance(obj, dict):
            return {f"__int__{k}" if isinstance(k, int) else k: self._encode_nested(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._encode_nested(v) for v in obj]
        return obj

    def default(self, obj):
        """
        Handle sets and datetimes during encoding.
        """
        if isinstance(obj, set):
            return {"__set__": list(obj)}
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        return super().default(obj)


def tagged_decoder_hook(d):
    """
    Custom JSON decoder that restores sets, datetimes, and integer keys from their encoded format.
    """
    # Sets
    if "__set__" in d:
        return set(d["__set__"])

    # Datetimes
    if "__datetime__" in d:
        return datetime.fromisoformat(d["__datetime__"])

    # Tagged keys
    new_dict = {}
    for k, v in d.items():
        if isinstance(k, str) and k.startswith("__int__"):
            new_dict[int(k.replace("__int__", ""))] = v
        else:
            new_dict[k] = v
    return new_dict
