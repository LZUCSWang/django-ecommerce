from django import template
import hashlib
from urllib.parse import urlencode
from django.conf import settings

register = template.Library()

@register.filter
def gravatar(email, size=40):
    """
    返回Gravatar头像或默认头像
    """
    # 使用identicon作为默认头像样式,它会根据email生成独特的几何图案
    default = "identicon"
    
    if not email:
        # 如果没有email,生成一个随机但固定的头像
        email = str(hash(email or 'default_avatar'))
    
    # 生成头像hash
    gravatar_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    
    # 构建Gravatar URL参数
    params = {
        's': str(size),  # 图片大小
        'd': default,    # 默认头像类型
        'r': 'g'        # 评级
    }
    
    # 返回Gravatar URL
    return f"https://secure.gravatar.com/avatar/{gravatar_hash}?{urlencode(params)}"