from django import template

register = template.Library()

@register.filter(name='private')
def private(dic, attribute):
    # return getattr(obj, attribute)
    return dic[attribute]