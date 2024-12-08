from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from jsonschema import validate, ValidationError

from accounts.models import CustomUser, AbstractBaseModel

theme_schema = {
    "type": "object",
    "properties": {
        "fonts": {
            "type": "object",
            "properties": {
                "title_font": {
                    "type": "string",
                    "enum": ["Lucida Console", "Arial", "Times New Roman", "Verdana"],
                },
                "content_font": {
                    "type": "string",
                    "enum": ["Calibri", "Arial", "Helvetica", "Georgia"],
                },
            },
            "required": ["title_font", "content_font"],
        },
        "font_sizes": {
            "type": "object",
            "properties": {
                "title_size": {"type": "integer", "minimum": 10, "maximum": 100},
                "content_size": {"type": "integer", "minimum": 8, "maximum": 72},
            },
            "required": ["title_size", "content_size"],
        },
        "colors": {
            "type": "object",
            "properties": {
                "background_color": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 255},
                    "minItems": 3,
                    "maxItems": 3,
                },
                "title_color": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 255},
                    "minItems": 3,
                    "maxItems": 3,
                },
                "content_color": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0, "maximum": 255},
                    "minItems": 3,
                    "maxItems": 3,
                },
            },
            "required": ["background_color", "title_color", "content_color"],
        },
    },
    "required": ["fonts", "font_sizes", "colors"],
}


class Presentation(AbstractBaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    num_slides = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20),
        ],  # Restrict between 1 and 20
    )
    theme = models.JSONField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",  # Default status is 'pending'
    )

    def __str__(self):
        return f"{self.user} <> {self.topic}"

    def set_defaults(self, data, defaults):
        for key, value in defaults.items():
            if isinstance(
                value, dict
            ):  # If value is a dictionary, recursively set defaults
                data[key] = self.set_defaults(data.get(key, {}), value)
            else:
                data.setdefault(key, value)  # Set the default value if key is missing
        return data

    def set_default_theme(self):
        default_theme = {
            "fonts": {"title_font": "Lucida Console", "content_font": "Calibri"},
            "font_sizes": {"title_size": 28, "content_size": 18},
            "colors": {
                "background_color": [240, 248, 255],
                "title_color": [0, 51, 102],
                "content_color": [51, 51, 51],
            },
        }
        self.theme = self.set_defaults(self.theme, default_theme)

    def save(self, *args, **kwargs):
        self.set_default_theme()

        try:
            validate(instance=self.theme, schema=theme_schema)
        except ValidationError as e:
            raise ValueError(f"Invalid theme data: {e.message}")

        super(Presentation, self).save(*args, **kwargs)


class PresentationSlide(models.Model):
    # Layout names mapped to layout_id
    LAYOUT_NAMES = [
        ("Title Slide", 0),
        ("Title and Content", 1),
        ("Section Header", 2),
        ("Two Content", 3),
        ("Comparison", 4),
        ("Title Only", 5),
        ("Blank", 6),
        ("Content with Caption", 7),
        ("Picture with Caption", 8),
        ("Title and Vertical Text", 9),
        ("Vertical Title and Text", 10),
    ]
    LAYOUT_CHOICES = [(str(id), name) for name, id in LAYOUT_NAMES]

    presentation = models.ForeignKey(
        Presentation, related_name="slides", on_delete=models.CASCADE
    )
    layout_id = models.IntegerField(
        choices=[(id, name) for name, id in LAYOUT_NAMES], default=0
    )
    layout_name = models.CharField(
        max_length=50, choices=LAYOUT_CHOICES, default="Title Slide"
    )
    content = models.JSONField(
        default=list
    )  # Content as a list of objects {id, name, value}
    index = models.PositiveIntegerField()  # Slide index

    def __str__(self):
        return f"Slide {self.index} - {self.layout_name}"
