from django import forms
from django.forms import inlineformset_factory

from .models import Blank, BlankMeta, Furniture


class BlankForm(forms.ModelForm):
    class Meta:
        model = Blank
        fields = "__all__"


class BlankMetaForm(forms.ModelForm):
    class Meta:
        model = BlankMeta
        fields = '__all__'


class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = "__all__"


BlankMetaInlineFormset = inlineformset_factory(
    Blank,
    BlankMeta,
    form=BlankMetaForm,
    extra=0,
    max_num=10,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    can_delete=False,
    # max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

FurnitureInlineFormset = inlineformset_factory(
    Blank,
    Furniture,
    form=FurnitureForm,
    extra=4,
    max_num=4,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    can_delete=False,
    # max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)
