from django.db import models
from wagtail.wagtailcore.models import Page
from satchless.item import Item
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from django_prices.models import PriceField
from modelcluster.fields import ParentalKey


class Variant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = PriceField(currency='USD', max_digits=5, decimal_places=2)
    size = models.CharField(max_length=3, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    product = ParentalKey('product.Product', related_name='variants')

    def __str__(self):
        return self.name


class Product(Item, Page):
    description = RichTextField()

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.name

Product.content_panels = [
    FieldPanel('title'),
    FieldPanel('description'),
]
Product.variant_panels = [
    InlinePanel(Product, 'variants', label='Variants')
]

from wagtail.wagtailadmin.views.pages import PAGE_EDIT_HANDLERS
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
PAGE_EDIT_HANDLERS[Product] = TabbedInterface([
    ObjectList(Product.content_panels, heading='Product'),
    ObjectList(Product.promote_panels, heading='Promote'),
    ObjectList(Product.variant_panels, heading='Variants')
])
