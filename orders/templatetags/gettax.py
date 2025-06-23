from django import template
register=template.Library()

@register.simple_tag(name='gettax')

def gettotal(subtotal,rate):
    tax=subtotal*rate/100
    return tax
    