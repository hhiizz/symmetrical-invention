from django import template

register = template.Library()
@register.filter(name='range')
def numbercount(number):
    return range(1,number)



@register.filter(name='split')
def strsplit(str1,key):
    return str1.split(key)