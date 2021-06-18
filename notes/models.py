from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class BotUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	chat_id = models.IntegerField(null=True, unique=True)
	activation_token = models.CharField(max_length=100, null=True, unique=True)
	# Make it as a choicefield - Telegram, Whastapp..
	platform = models.CharField(max_length=100, default='telegram', blank=False)

	def __str__(self):
		return f"BotUser<{self.id}>: {self.platform} - User<{self.user.id}> {self.user.username}"

class Tag(models.Model):
	name = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"Tag<{self.id}>: {self.name}"

class Note(models.Model):
	text = models.TextField()
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)
	tags = models.ManyToManyField(Tag)
	bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	class Meta:
		ordering = ('-created',)
		
	@property
	def tags_list(self):
		note_tags = self.tags.all()
		return note_tags
		
	def __str__(self):
		return f"Note:<{self.id}> <{self.text}> <{self.bot_user}>"

	def get_absolute_url(self):
		return reverse("account:notes")



