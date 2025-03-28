from django.apps import apps
from django.contrib import admin
from .models import Product
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.utils.html import format_html


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.list_select_related = [x.name for x in model._meta.fields if isinstance(
            x, (ManyToOneRel, ForeignKey, OneToOneField,))]

        # self.search_fields=[model.p]
        super(ListAdminMixin, self).__init__(model, admin_site)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image',
        'name',
        'price',
        'shop_name',
        'shop_type',
        'd_rate_nums',
    ]
    list_display_links = ("image", "name",)
    list_filter = ('name', 'price', 'shop_name','shop_type')
    list_select_related = True
    list_per_page = 20
    list_max_show_all = 200
    list_editable = ()
    search_fields = [
        'name'
    ]
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    preserve_filters = True
    inlines = []

    def image(self, obj):
        return format_html('<img src="{cover}" width=150 height=150>', cover=obj.image_link.url)
    image.short_description = '封面'


admin.site.register(Product, ProductAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
