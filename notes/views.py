import json
import requests
import dotenv
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note, BotUser, Tag
from .forms import NoteForm, NoteUpdateForm
from .utils import extract_hash_tags

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')


# Create your views here.
def activate_bot(text, chat_id):
	separate_strings = text.split()
	if separate_strings[0].startswith('/code') == True and len(separate_strings[1]) == 5:
		bot_activation_token = separate_strings[1]
		if BotUser.objects.filter(activation_token=bot_activation_token).exists():
			bot_user = BotUser.objects.get(activation_token=bot_activation_token)
			bot_user.chat_id = chat_id
			bot_user.save()
			message = "You have successfully activated your account!"
			url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(API_KEY, chat_id, message)
			requests.get(url)
			return True
		else:
			message = "Yo, Activation has failed! \nTo activate your account send a message to me starting with:\n/code followed by activation_token received from the website.\nExample:\n/code sW2ax"
			url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(API_KEY, chat_id, message)
			requests.get(url)
			return False


@csrf_exempt
def telegram_webhook(request):
	if request.method == "POST":
		data = request.body.decode("utf8")
		update = json.loads(data)
		message = update.get('message')
		if message:
			text = message['text']
			chat_id = message['chat']['id']
			print(chat_id)
			if BotUser.objects.filter(chat_id=chat_id, platform='telegram').exists():
				string_tags = extract_hash_tags(text)
				bot_user = BotUser.objects.get(chat_id=chat_id, platform='telegram')
				user = bot_user.user
				note = Note.objects.create(text=text, user=user)
				user_tags = user.tag_set.all()
				user_tags_list = user_tags.values_list('name', flat=True)
				new_tags = []
				for string_tag in string_tags:
					if string_tag not in user_tags_list:
						new_tags.append(string_tag)
						Tag.objects.create(name=string_tag, user=user)
				note_tags = Tag.objects.filter(user=user, name__in=string_tags)
				if not note_tags:
					if Tag.objects.filter(user=user, name='#untagged').exists():
						default_tag = Tag.objects.get(user=user, name='#untagged')
					else:
						default_tag = Tag.objects.create(user=user, name='#untagged')
					note.tags.add(default_tag)
				else:
					note.tags.add(*note_tags)
					note.save()

			else:
				chat_id = str(chat_id)
				activate_bot(text, chat_id)
	return HttpResponse(status=200)

#CRUD note on website

def create_note(request):
	context = {}
	form = NoteForm(request.POST or None)
	if form.is_valid():
		cd_text = form.cleaned_data.get('text')
		cd_tags = form.cleaned_data.get('tags')
		new_note = Note.objects.create(user=request.user, text=cd_text)
		for tag in cd_tags:
			new_note.tags.add(tag)
			return redirect('account:notes')
	context['form'] = form
	return render(request, 'create_note.html', context)

class NoteUpdateView(UpdateView):
	model = Note
	form_class = NoteUpdateForm
	template_name_suffix = '_update_form'

	def get_queryset(self):
		qs = super(NoteUpdateView, self).get_queryset()
		return qs.filter(user=self.request.user)

	
class NoteDeleteView(DeleteView):
	model = Note
	success_url = reverse_lazy('account:notes')

	def get_queryset(self):
		qs = super(NoteDeleteView, self).get_queryset()
		return qs.filter(user=self.request.user)

def post_list_by_tag(request, tag_name=None):
	notes_list = Note.objects.filter(user=request.user)
	tag = None

	if tag_name:
		tag = get_object_or_404(Tag, name=tag_name, user=request.user)
		notes_list = Note.objects.filter(tags=tag)
	return render(request, 'notes/list_by_tag.html', {'tag':tag, 'notes_list':notes_list})


