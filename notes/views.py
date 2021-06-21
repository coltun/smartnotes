import json
import requests
import dotenv
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .models import Note, BotUser, Tag
from .forms import NoteForm
from .utils import extract_hash_tags

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

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
			if BotUser.objects.filter(chat_id=chat_id, platform='telegram').exists():
				string_tags = extract_hash_tags(text)
				for string_tag in string_tags:
					text = text.replace(string_tag, "")
				clean_text = " ".join(text.split())
				bot_user = BotUser.objects.get(chat_id=chat_id, platform='telegram')
				user = bot_user.user
				note = Note.objects.create(text=clean_text, user=user)
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
	user = request.user
	form = NoteForm(request.POST or None)
	if form.is_valid():
		text = form.cleaned_data.get('text')
		hashtags = extract_hash_tags(text)
		for hashtag in hashtags:
			text = text.replace(hashtag, "")
		clean_text = " ".join(text.split())
		note = Note.objects.create(text=clean_text, user=user)
		tags = []
		for hashtag in hashtags:
			tag, created = Tag.objects.get_or_create(name=hashtag, user=user)
			tags.append(tag)
		if not hashtags:
			tag, created = Tag.objects.get_or_create(name="#untagged", user=user)
			tags.append(tag)
		note.tags.clear()
		note.tags.add(*tags)
		note.save()
		return redirect('account:notes')
	context['form'] = form
	return render(request, 'create_note.html', context)

class NoteUpdateView(View):

	def get(self, request, pk, *args, **kwargs):
		note = get_object_or_404(Note, pk=pk, user=request.user)
		context = {
			'note': note,
			'tags': ' '.join([ tag.name for tag in note.tags.all()])
		}
		return render(request, 'notes/note_update_form.html', context)

	def post(self, request, pk, *args, **kwargs):
		user = request.user
		note = get_object_or_404(Note, pk=pk, user=request.user)
		note.text = request.POST.get('text', note.text)
		hashtags_string = request.POST.get('tags')
		hashtags = hashtags_string.split()
		tags = []
		for hashtag in hashtags:
			tag, created = Tag.objects.get_or_create(name=hashtag, user=user)
			tags.append(tag)
		if not hashtags:
			tag, created = Tag.objects.get_or_create(name="#untagged", user=user)
			tags.append(tag)
		note.tags.clear()
		note.tags.add(*tags)
		note.save()
		return redirect('account:notes')

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
	return render(request, 'notes/list_by_tag.html', {'tag': tag, 'notes_list': notes_list})


