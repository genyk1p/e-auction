from modeltranslation.translator import translator, TranslationOptions
from .models import Information


class ProductTranslationOptions(TranslationOptions):
    fields = ('content', 'meta_tag_description')


translator.register(Information, ProductTranslationOptions)
