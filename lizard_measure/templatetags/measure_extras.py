# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import datetime

from django import template
register = template.Library()

@register.filter
def format_date_string(date_string):
    dt = datetime.datetime.strptime(
        date_string,
        '%Y-%m-%d %H:%M:%S.%f',
    )
    result = dt.strftime('%Y-%m-%d %H:%M')
    return result
