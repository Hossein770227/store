from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import  MinValueValidator , MaxValueValidator

from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(_("title"), max_length=150)
    description = models.CharField(_("description for category "), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Category ")
        verbose_name_plural = _("Categories")
        ordering = ['title'] 

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(_("name product"), max_length=150)
    slug = models.SlugField(max_length=150, unique=True,allow_unicode=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.PROTECT, related_name='products')
    short_description = models.CharField(_("short description for product"), max_length=255, blank=True)
    description = RichTextField()
    main_price = models.PositiveIntegerField(_("main price "))
    price_with_discount = models.PositiveIntegerField(_("price with discount "), blank=True, null=True)
    inventory = models.IntegerField(_("inventory "), validators = [MinValueValidator(0)])
    image = models.ImageField(_("product image"), upload_to='cover/', blank=True,)
    is_special_offer = models.BooleanField(_("is special offer"), null=True, blank=True, default=False)

    ate_time_modified = models.DateTimeField(_("date time modified"), auto_now=True)
    date_time_added = models.DateTimeField(_("date time added"), auto_now_add=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ['-date_time_added']
        indexes = [
            models.Index(fields=['name', 'category']),
        ]

    def clean(self):
        if self.price_with_discount and self.price_with_discount >= self.main_price:
            raise ValidationError(_("Discount price must be less than main price."))
            
    def percent_discount(self):
        if self.price_with_discount:
            if self.main_price == 0:
                return 0 
            return ((self.main_price - self.price_with_discount) / self.main_price) * 100
        return 0
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])


    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Color Name"))

    def __str__(self):
        return self.name


class Features(models.Model):
    SMALL_SIZE ='S'
    MEDIUM_SIZE = 'M'
    LARGE_SIZE = 'L'
    BIG_SIZE = 'XL'
    CHOICE_SIZE =(
        (SMALL_SIZE, 'small'),
        (MEDIUM_SIZE, 'medium'),
        (LARGE_SIZE, 'large'),
        (BIG_SIZE, 'very large')

    )
    product = models.ForeignKey(Product, verbose_name=_(""), on_delete=models.CASCADE, related_name='feature')
    weight = models.PositiveSmallIntegerField(
                _("weight product"), 
                validators=[MinValueValidator(1), MaxValueValidator(1000)]
                )
    size = models.CharField(_("size"), max_length=3, choices=CHOICE_SIZE, default=LARGE_SIZE)
    colors = models.ManyToManyField(Color, verbose_name=_("Colors"))

    class Meta:
        verbose_name = _("feature")
        verbose_name_plural = _("features")
        constraints = [
            models.UniqueConstraint(fields=['product'], name='one_feature_per_product')
        ]

    
class Comment(models.Model):
    RATING_CHOICES = [
        ('5', "⭐⭐⭐⭐⭐"),
        ('4', "⭐⭐⭐⭐"),
        ('3', "⭐⭐⭐"),
        ('2', "⭐⭐"),
        ('1', "⭐"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField(_("email"), max_length=254, blank=True, null=True)
    text = models.TextField(_("comment text"))
    rating = models.CharField(
        _("rating"),
        max_length=10,
        choices=RATING_CHOICES,
        blank=True,
        default=None,
    )
    is_active = models.BooleanField(_("active ?"), default=True)
    ate_time_modified = models.DateTimeField(_("date time modified"), auto_now=True)
    date_time_added = models.DateTimeField(_("date time added"), auto_now_add=True)

    def __str__(self):
        return self.user.full_name
    