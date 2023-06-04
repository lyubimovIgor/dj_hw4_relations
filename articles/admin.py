from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tags = False
        for form in self.forms:
            if form.cleaned_data.get('is_main') and tags:
                raise ValidationError('Только один раздел может быть основным ')
            if form.cleaned_data.get('is_main') and not tags:
                tags = True
        if tags is False:
            raise ValidationError('Выберите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ['name']