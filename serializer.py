import json

from rest_framework import serializers


class CustomPKRelatedField(serializers.PrimaryKeyRelatedField):
    """A PrimaryKeyRelatedField derivative that uses named field for the display value."""

    def __init__(self, **kwargs):
        self.display_field = kwargs.pop("display_field", "name")
        super(CustomPKRelatedField, self).__init__(**kwargs)

    def display_value(self, instance):
        # Use a specific field rather than model stringification
        return getattr(instance, self.display_field)

