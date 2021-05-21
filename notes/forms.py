from django import forms
from .models import Note
from django.utils.translation import ugettext_lazy as _

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		exclude = ('created', 'updated', 'bot_user', 'user')
		labels = {
            'text': _('Note'),
        }

		widgets = {
			'text': forms.TextInput(attrs={'class': 'form-control'}),
			'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),

		}

class NoteUpdateForm(forms.ModelForm):
	class Meta:
		model = Note
		exclude = ('created', 'updated', 'bot_user', 'user')
		labels = {
            'text': _('Note'),
        }

		widgets = {
			'text': forms.TextInput(attrs={'class': 'form-control'}),
			'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),

		}
