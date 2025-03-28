'''
 将queryset与model实例等进行序列化，转化成json格式，返回给用户(api接口)。
'''
from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['image_link', 'name']
