from django.contrib import admin
from .models import Opinion, Product


class ProductUrlListFilter(admin.SimpleListFilter):
    parameter_name = 'product_url'

    def queryset(self, request, queryset):
        return queryset.filter(product__title__contains=self.value())


# admin.RelatedFieldListFilter
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('url',)


class OpinionAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'product_url', 'product_title', 'comments_num', 'stars_num',
                'source', 'using_duration', 'advantages', 'disadvantages', 'content')
    search_fields = ('content',)
    list_filter = ('using_duration', 'stars_num', 'source')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "product_title":
    #         kwargs["queryset"] = Opinion.objects.filter(product__title__contains=request.title)
    #     return super(OpinionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def product_url(self, obj):
        return obj.product.url

    def product_title(self, obj):
        return obj.product.title
    
    product_url.admin_order_field = 'product__url'
    product_title.admin_order_field = 'product__title'


admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Product, ProductAdmin)
