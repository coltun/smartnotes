import random, string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from account.forms import CustomLoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from notes.models import BotUser, Note, Tag
# Create your views here.

class CustomLoginView(LoginView):
	template_name = "registration/login.html"
	authentication_form = CustomLoginForm

class CustomLogoutView(LogoutView):
	template_name = "homepage.html"

@login_required
def display_notes(request):
	user = request.user
	all_notes = Note.objects.filter(user=request.user)
	user_tags = user.tag_set.all()
	filtered_tags_names = []
	

	if request.GET.getlist('tags'):
		filtered_tags_names =  request.GET.getlist('tags')
		all_notes = all_notes.filter(tags__name__in=filtered_tags_names)

	if request.GET.get('term'):
		search_term = request.GET.get('term')
		all_notes = all_notes.filter(text__icontains=search_term)
	
	return render(request, "notes.html", {'all_notes': all_notes, 'user_tags': user_tags, 'filtered_tags_names':filtered_tags_names})

def register(request):
	if request.method == "POST":
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.username = new_user.email
			new_user.set_password(user_form.cleaned_data['password2'])
			new_user.save()
			form = CustomLoginForm()
			
			return render(request, 'registration/login.html', {'form':form})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'user_form': user_form})

def homepage(request):
	return render(request, 'homepage.html')

def user_settings(request):
	return render(request, 'user_settings.html')

def user_instructions(request):
	if BotUser.objects.filter(user=request.user, platform='telegram').exists() == False:
		activation_token = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
		BotUser.objects.create(user=request.user, platform='telegram', activation_token=activation_token)
	bot_user = BotUser.objects.get(user=request.user)
	display_user_token = bot_user.activation_token
	return render(request, 'user_instructions.html', { 'display_user_token': display_user_token})
