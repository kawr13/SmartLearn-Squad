from django.urls import path
from .views import get_events, cabinets_view, update_calend, user_full, user_full_view, VideoArchView, SendToEmailView

app_name = 'cabinet'


urlpatterns = [
    path('get_events/<int:cabinet_id>/', get_events, name='get_events'),
    path('cabinets/<int:cab_id>/', cabinets_view, name='cabinet'),
    path('get_updates/<int:cabinet_id>/', update_calend, name='get_update'),
    path('userfull_info_cab/<int:cabinet_id>/', user_full, name='userfull_info_cab'),
    path('userfull_detailed/<int:post_id>/', user_full_view, name='userfull_detailed'),
    path('records_cab/<int:cabinet_id>/', VideoArchView.as_view(), name='records_cab'),
    path('send_mail/<int:cabinet_id>/', SendToEmailView.as_view(), name='send_mail'),
    path('send_mail/<int:cabinet_id>/', SendToEmailView.as_view(), name='send_mail_post'),

]
