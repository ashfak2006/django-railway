from django import template
register=template.Library()

@register.simple_tag(name='gettotal')

def gettotal(subtotal,shiping,tax,discount):
    total=subtotal+shiping+tax 
    if discount:
        total = total = discount
    return total
    