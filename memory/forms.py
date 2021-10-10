from django.forms import ModelForm, fields

from memory.models import Memory


class MemoryForm(ModelForm):

    class Meta:
        model = Memory
        fields = ['name', 'descripsion', ]
