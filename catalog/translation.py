from modeltranslation.translator import translator, TranslationOptions
from .models import Product, LabelText


class ProductTranslationOptions(TranslationOptions):
    fields = ('content', 'name', 'title', 'description')

class Label_TextTranslationOptions(TranslationOptions):
    fields = ('name',)
    # pass

translator.register(Product, ProductTranslationOptions)
translator.register(LabelText, Label_TextTranslationOptions)
