from django.db import models
from catalog.modules.services.utils import unique_slugify

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """ Модель продукта """
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=255, verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='id категории')
    price = models.IntegerField(verbose_name='цена продукта')
    date_of_creation = models.DateTimeField(verbose_name='дата создания')
    date_of_change = models.DateTimeField(verbose_name='дата последнего изменения')
    user = models.ForeignKey('users.user', on_delete=models.PROTECT, verbose_name='id пользователя')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'user'


class Category(models.Model):
    """ Модель категории продукта """
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=255, verbose_name='описание')

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Version(models.Model):
    """ Модель версии продукта """
    id_product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='id продукта')
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=150, verbose_name='наименование')
    publication = models.BooleanField(default=False, verbose_name='признак публикации')

    def __str__(self):
        return f'{self.version_name}'

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продукта'


class Blog(models.Model):
    """ Модель статьи (блога) """
    name = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=255, verbose_name='url')
    content = models.CharField(max_length=1000, verbose_name='содержимое')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    date_of_creation = models.DateTimeField(verbose_name='дата создания')
    publication = models.BooleanField(default=False, verbose_name='признак публикации')
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.name}'

    def delete(self, using=None, keep_parents=False):
        """ Удаление статьи """
        self.publication = False
        self.save()

    def save(self, *args, **kwargs):
        """ Сохранение полей модели при их отсутствии заполнения """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
