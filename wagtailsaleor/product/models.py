from django.db import models
from wagtail.wagtailcore.models import Page
from satchless.item import StockedItem
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import (TabbedInterface, ObjectList,
                                                PageChooserPanel, FieldPanel,
                                                InlinePanel, MultiFieldPanel)
from wagtail.wagtailadmin.views.pages import PAGE_EDIT_HANDLERS
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable
from django_prices.models import PriceField
from modelcluster.fields import ParentalKey


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


class Picture(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class ProductPicture(Orderable, Picture):
    page = ParentalKey('product.Product', related_name='pictures')


class Variant(StockedItem, models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    price = PriceField(currency='USD', max_digits=5, decimal_places=2)
    size = models.CharField(max_length=3, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    product = ParentalKey('product.Product', related_name='variants')
    stock = models.IntegerField('In stock')

    def __str__(self):
        return self.name

    def get_stock(self):
        return self.stock


class Product(Page):
    description = RichTextField()

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.name

Product.content_panels = [
    FieldPanel('title'),
    FieldPanel('description'),
    InlinePanel(Product, 'pictures', label='Pictures')
]
Product.variant_panels = [
    InlinePanel(Product, 'variants', label='Variants')
]

PAGE_EDIT_HANDLERS[Product] = TabbedInterface([
    ObjectList(Product.content_panels, heading='Product'),
    ObjectList(Product.promote_panels, heading='Promote'),
    ObjectList(Product.variant_panels, heading='Variants')
])
