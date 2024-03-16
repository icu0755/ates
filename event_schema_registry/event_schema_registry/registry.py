from importlib import import_module

from jsonschema import validate


class SchemaRegistry:
    @classmethod
    def validate_event(cls, data, event_name, *, version):
        try:
            package = import_module(f"registry.{event_name}.{version}")
        except ModuleNotFoundError:
            raise ValueError(f"wrong event name: {event_name}")
        validate(data, package.schema)
