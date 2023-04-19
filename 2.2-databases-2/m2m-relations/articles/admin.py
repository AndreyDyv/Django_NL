from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            if 'is_main' in form.cleaned_data:
                counter += 1
        if counter > 1:
            raise ValidationError('Только один тэг может быть отмечен как главный')
        elif counter == 0:
            raise ValidationError('Отсутствует главный тэг')
        return super().clean()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['is_main']

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'text', 'published_at', 'image']

