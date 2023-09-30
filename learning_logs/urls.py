"""DEFINES URL PATTERN FOR LEARNING_LOGS."""

from django.urls import path
from . import views
app_name='learning_logs'

urlpatterns = [
    #Home page
    path('',views.index,name='index'),
    #  page that show all the topics
    path('topics/',views.topics,name='topics'),

    # detailed view for each topic.
    path('topics/<int:topic_id>/',views.topic,name='topic'),

    # Page for adding new topic
    path('new_topic/',views.new_topic,name='new_topic'),

    # Page for adding new entry
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),

    # page for editing the entry
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
]
