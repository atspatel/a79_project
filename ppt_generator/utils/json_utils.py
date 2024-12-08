from django.contrib import admin
from django.db import models
import json
from django.forms.widgets import Textarea


class PrettyJSONWidget(Textarea):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update(
            {"style": "height: 200px; width: 80%;"}
        )  # Adjust size as needed

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value:
            try:
                parsed = json.loads(value)
                return json.dumps(parsed, indent=4)  # Pretty-print JSON
            except json.JSONDecodeError:
                return value  # Return as is if it fails to parse
        return value

    def render(self, name, value, attrs=None, renderer=None):
        # Ensure the value is always pretty-printed when rendered
        if value:
            try:
                parsed = json.loads(value)
                value = json.dumps(parsed, indent=4)  # Pretty-print JSON
            except json.JSONDecodeError:
                pass  # If it can't parse, just use the raw value
        return super().render(name, value, attrs, renderer)


class BaseJsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": PrettyJSONWidget},  # Apply to all JSONFields
    }
