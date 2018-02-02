from django import template
from datetime import timedelta
import datetime

register = template.Library()

import os


@register.filter
def filename(value):
    return os.path.basename(value.file.name)