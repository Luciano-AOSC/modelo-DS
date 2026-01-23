"""Compatibility shim for unpickling models trained with `modeling` module."""

from src import modeling as _modeling

__all__ = [name for name in dir(_modeling) if not name.startswith("_")]

for name in __all__:
    globals()[name] = getattr(_modeling, name)
