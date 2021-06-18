from django.urls import path
from notes import views
from notes.views import NoteUpdateView, NoteDeleteView

urlpatterns = [
	path('create_note/', views.create_note, name='create_note'),
	path('update_note/<int:pk>/', NoteUpdateView.as_view(), name='update_note'),
	path('delete_note/<int:pk>/', views.NoteDeleteView.as_view(), name='note_delete'),
	path('tag/<str:tag_name>/', views.post_list_by_tag, name='list_by_tag'),

	
    
	
	
	
]