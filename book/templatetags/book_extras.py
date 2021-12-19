# Author :Breeze_xylf
# Date :
from django import  template
from django.utils import timezone
import math
import requests

register = template.Library()

@register.inclusion_tag('book/inclusions/_pagination.html',takes_context=True)
def show_pagination(context):
    return {
        'page_objects': context['objects'],
        'search':context['search'],
        'order_by':context['orderby']
    }

@register.inclusion_tag('book/inclusions/_messages.html',takes_context=True)
def show_messages(context):
    return {
        'messages':context['messages'],
    }

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter('has_group')
def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
