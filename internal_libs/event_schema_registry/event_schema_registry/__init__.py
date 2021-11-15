try:
    from validator import validate, generate_event
except ImportError:
    from .validator import validate, generate_event

__all__ = [
    'validate',
    'generate_event',
]
