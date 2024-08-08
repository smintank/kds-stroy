from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True, published_date__lte=timezone.now())


class Category(BaseModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
        unique=True
    )
    objects = models.Manager()
    published = PublishManager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class News(BaseModel):
    title = models.CharField("Заголовок", max_length=255)
    content = CKEditor5Field('Текст', config_name='extends')
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    published_date = models.DateTimeField(
        "Дата и время публикации", default=timezone.now
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name="Категория", null=True
    )

    objects = models.Manager()
    published = PublishManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsPhoto(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField(upload_to="news_photos/",
                              blank=False, null=False)

    def photo_preview(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.photo.url}" width="200">')
        return "No image"

    photo_preview.short_description = 'Photo Preview'

    def __str__(self):
        return f"Фото к новости {self.news.title}"
