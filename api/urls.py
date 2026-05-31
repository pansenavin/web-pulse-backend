from django.urls import path
from api.users.views import RegisterView, LoginView, LogoutView, ProfileView
from api.monitoring.views import WebsiteListView, WebsiteDetailView, TogglePauseView, ActivityLogView
from api.notifications.views import NotificationPreferenceView, NotificationHistoryView

urlpatterns = [
    # Auth & Users
    path('userauth/register', RegisterView.as_view(), name='register'),
    path('userauth/login', LoginView.as_view(), name='login'),
    path('userauth/logout', LogoutView.as_view(), name='logout'),
    path('userauth/profile', ProfileView.as_view(), name='profile'),
    
    # Monitoring
    path('websites/add', WebsiteListView.as_view(), name='add_website'),
    path('websites/list', WebsiteListView.as_view(), name='list_websites'),
    path('websites/update/<int:pk>', WebsiteDetailView.as_view(), name='update_website'),
    path('websites/delete/<int:pk>', WebsiteDetailView.as_view(), name='delete_website'),
    path('websites/get/<int:pk>', WebsiteDetailView.as_view(), name='get_website'),
    path('websites/togglePause/<int:pk>', TogglePauseView.as_view(), name='toggle_pause'),
    path('websites/activity', ActivityLogView.as_view(), name='activity'),
    
    # Notifications
    path('notifications/preferences', NotificationPreferenceView.as_view(), name='notification_preferences'),
    path('notifications/history', NotificationHistoryView.as_view(), name='notification_history'),
]
