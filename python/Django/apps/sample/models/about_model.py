from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .category_model import Category

class About(models.Model):
    """
    サンプルモデル。

    このモデルは、idを更新するためのモデルです。

    フィールド:
    - id: 投稿のID。
    - context: 投稿のテキスト。
    - created_at: 作成日時。
    - updated_at: 更新日時。
    """

    # Django は自動的に id フィールドを作成するため、明示的に定義する必要はありません
    # id = models.CharField(_('id'), max_length=255)

    context = models.CharField(_('context'), max_length=255)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('about')
        verbose_name_plural = _('abouts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.context