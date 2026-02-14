from django import forms
from livestock.models import Category
from django.utils.translation import gettext_lazy as _

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['parent', 'name_ar', 'name_en', 'slug', 'description_ar', 'description_en', 'icon', 'order']
        widgets = {
            'description_ar': forms.Textarea(attrs={'rows': 3}),
            'description_en': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = _("Main Category (No Parent)")
        self.fields['parent'].queryset = Category.objects.all()
        
        # If editing, exclude self from parent options to avoid recursion options
        if self.instance.pk:
             self.fields['parent'].queryset = Category.objects.exclude(pk=self.instance.pk)
