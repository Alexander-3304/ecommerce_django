from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Наименование"), max_length=200, db_index=True
    )
    slug = models.SlugField(verbose_name=_("slug"), max_length=200, unique=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(verbose_name=_("Наименование"), max_length=200)
    description = models.TextField(verbose_name=_("Описание"), blank=True)
    new_price = models.DecimalField(verbose_name=_("Новая цена"), max_digits=10, decimal_places=2)
    old_price = models.DecimalField(verbose_name=_("Старая цена"), max_digits=10, decimal_places=2)
    slug = models.SlugField(verbose_name=_("slug"), max_length=200, unique=True)
    image = models.ImageField(
        verbose_name=_("Изображение"), upload_to="products", blank=True
    )
    images = models.ManyToManyField(
        to="ItemImage",
        verbose_name=_("Изображение"),
        blank=True,
        related_name="product_image",
    )
    stock = models.PositiveIntegerField(verbose_name=_("Наличие"), default=0)
    available = models.BooleanField(verbose_name=_("Доступен"), default=True)
    active = models.BooleanField(verbose_name=_("Активный"), default=True)
    in_stock = models.BooleanField(verbose_name=_("В продаже"), default=True)
    size = models.ForeignKey(
        to="ItemSize",
        verbose_name=_("Размер"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_size",
    )
    category = models.ForeignKey(
        to="Category",
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_category",
    )
    sale = models.ForeignKey(
        to="ItemSale",
        verbose_name=_("Скидка"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_sale",
    )
    updated_at = models.DateTimeField(verbose_name=_("Обновлён"), auto_now=True)
    created_at = models.DateTimeField(verbose_name=_("Создан"), auto_now_add=True)
    order = models.SmallIntegerField(default=0, db_index=True)
    class Meta:
        ordering = ("order", "name",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        index_together = (("id", "slug"),)
        db_table = "ustora_001"

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)


class ItemSet(models.Model):

    name = models.CharField(verbose_name=_("Наименование"), max_length=200)
    description = models.TextField(verbose_name=_("Описание"), blank=True)
    image = models.ImageField(
        verbose_name=_("Изображение"), upload_to="images/%Y/%m/%d", blank=True
    )

    set = models.ManyToManyField(
        to="Item",
        verbose_name=_("Наименование товаров"),
        related_name="item_set",
    )

    class Meta:
        verbose_name = _("Наименование списка товаров")
        verbose_name_plural = _("Наименования списка товаров")
        ordering = ("pk",)

        db_table = "ustora_001.ItemSet"

    def __str__(self) -> str:
        return f"{self.name}"


class ItemSale(models.Model):

    sale_begin = models.DateField(
        verbose_name=_("Начало скидки"), blank=True, null=True
    )
    sale_end = models.DateField(verbose_name=_("Конец скидки"), blank=True, null=True)
    sale_percent = models.DecimalField(
        verbose_name=_("Процент скидки"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sale_discount = models.DecimalField(
        verbose_name=_("Скидка"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    sale_price = models.DecimalField(
        verbose_name=_("Новая цена"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    sale_total = models.DecimalField(
        verbose_name=_("Общая стоимость"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ("product_sale", "sale_begin", "sale_end")
        db_table = "ustora_001.ItemSale"

    def __str__(self) -> str:
        return f"Скидка продукта {self.product_sale.name}"


class ItemSize(models.Model):

    category = models.ForeignKey(
        to="Category",
        verbose_name=_("Категория"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="size_category",
    )
    size = models.CharField(verbose_name=_("Размер"), max_length=200)

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
        ordering = ("category", "size")
        db_table = "ustora_001.ItemSize"

    def __str__(self) -> str:
        return f"Размер продукта {self.size} - {self.category}"


class ItemImage(models.Model):

    image = models.ImageField(
        verbose_name=_("Изображение"), upload_to="products/%Y/%m/%d", blank=True
    )
    alt = models.CharField(verbose_name=_("Подпись"), max_length=200, blank=True)
    description = models.TextField(verbose_name=_("Описание"), blank=True)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self) -> str:
        return f"Ссылка на изображение продукта {self.image}"