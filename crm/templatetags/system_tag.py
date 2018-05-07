from django import template
from datetime import timedelta
import datetime
from django.db.models import Avg,Sum

register = template.Library()

import os


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.assignment_tag
def get_container_number(obj,terminal,line):
	x=obj.filter(booking__company__name=terminal,
					booking__line__name=line)
	if x.count()==0:
		return 0
	else:
		return x[0]['number']

@register.assignment_tag
def sum(obj,field):
	# print (obj.strip())
	return obj.aggregate(Sum(field))