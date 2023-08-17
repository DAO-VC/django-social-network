from django.urls import path

from chat.views import (
    StartNewChat,
    RetrieveChat,
    MyChatsList,
    ReadAllMessage,
    BanUser,
    StartupStartChat,
    InvestorStartChat,
    ChangeRoomStatus,
    StartupWorkteamRoom,
)

urlpatterns = [
    path("chat/", StartNewChat.as_view(), name="start_new_chat"),
    path("chat/<int:pk>/", RetrieveChat.as_view(), name="retrieve_chat"),
    path("chat/my_chats/", MyChatsList.as_view(), name="user_all_chats_list"),
    path(
        "chat/<int:pk>/read_messages/",
        ReadAllMessage.as_view(),
        name="read_all_messages_from_user",
    ),
    path("user/<int:pk>/ban/", BanUser.as_view(), name="ban_user_with_id"),
    path(
        "main/startup/candidates/<int:pk>/chat/",
        StartupStartChat.as_view(),
        name="new_chat_startup_to_professional",
    ),
    path(
        "main/offers/candidates/<int:pk>/chat/",
        InvestorStartChat.as_view(),
        name="new_chat_investor_to_startup",
    ),
    path(
        "main/startup/my_team/<int:pk>/chat/",
        StartupWorkteamRoom.as_view(),
        name="new_chat_startup_to_team_member",
    ),
    path(
        "chat/<int:pk>/status/", ChangeRoomStatus.as_view(), name="change_chat_status"
    ),
]
