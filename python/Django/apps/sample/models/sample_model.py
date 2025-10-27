from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .category_model import Category

class Sample(models.Model):
    """
    サンプルモデル。

    このモデルは、ブログ投稿や記事などのデータを表現するために使用できます。

    フィールド:
    - title: 投稿のタイトル。
    - slug: URLフレンドリーな一意の識別子。
    - content: 投稿の本文。
    - excerpt: 投稿の要約 (任意)。
    - author: 投稿の作成者 (外部キー)。
    - category: 投稿のカテゴリ (外部キー、任意)。
    - is_published: 公開ステータス。
    - published_at: 公開日時 (任意)。
    - views_count: 閲覧数。
    - likes_count: いいね数。
    - created_at: 作成日時。
    - updated_at: 更新日時。
    """

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    content = models.TextField(_('content'))
    excerpt = models.TextField(_('excerpt'), blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='samples',
        verbose_name=_('author')
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='samples',
        verbose_name=_('category')
    )

    is_published = models.BooleanField(_('published'), default=False)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)

    views_count = models.IntegerField(_('views count'), default=0)
    likes_count = models.IntegerField(_('likes count'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('samples')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published', '-published_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title