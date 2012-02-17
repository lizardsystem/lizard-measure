# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import datetime

from django import template
register = template.Library()

@register.filter
def format_date_string(date_string):
    dt = datetime.datetime.strptime(
        '2012-02-17 09:46:06.625306',
        '%Y-%m-%d %H:%M:%S.%f',
    )
    result = dt.strftime('%Y-%m-%d %H:%M')
    return result
