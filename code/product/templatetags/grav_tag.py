import hashlib
from urllib.parse import urlencode

from django import template

register = template.Library()


# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
@register.filter
def gravatar(email, size=150):
    #url = gravatar_url(email, size)
    #return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
    return "https://www.gravatar.com/avatar/"+str(hashlib.md5(email.encode('utf-8')).hexdigest())+"?s="+str(size);