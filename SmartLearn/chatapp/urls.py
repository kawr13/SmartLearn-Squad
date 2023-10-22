from django.urls import path


app_name = 'chatapp'
#
#
#
urlpatterns = [
    path('get_events/<int:cabinet_id>/', name='get_events'),
]
