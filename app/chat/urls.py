from django.urls import path

from chat.views import StartNewChat, RetrieveChat, MyChatsList, ReadAllMessage

urlpatterns = [
    path("chat/", StartNewChat.as_view(), name="start_new_chat"),
    path("chat/<int:pk>/", RetrieveChat.as_view(), name="retrieve_chat"),
    path("chat/my_chats/", MyChatsList.as_view(), name="user_all_chats_list"),
    path(
        "chat/<int:pk>/read_messages/",
        ReadAllMessage.as_view(),
        name="read_all_messages_from_user",
    ),
]
