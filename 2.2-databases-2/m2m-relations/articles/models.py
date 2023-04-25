from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tags = models.ManyToManyField('Tag', through='Scope')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

class Tag(models.Model):

    name = models.CharField(max_length=25, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Scope(models.Model):

    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    articles = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        constraints = [
            models.UniqueConstraint(fields=('tags', 'articles'), name='main-tag')
        ]
        ordering = ['-is_main', 'tags']


