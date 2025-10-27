from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    Postのカテゴリを表すモデル。

    フィールド:
    - name: カテゴリ名 (一意)。
    - slug: URLフレンドリーな一意の識別子。
    - description: カテゴリの説明 (任意)。
    - created_at: 作成日時。
    - updated_at: 更新日時。
    """

    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name