from django import forms
from .models import Note
from django.utils.translation import ugettext_lazy as _

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		exclude = ('created', 'updated', 'bot_user', 'user', 'tags')
		labels = {'text': _('Note')}
		widgets = {
			'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Write your #tags in your note"}),
		}
