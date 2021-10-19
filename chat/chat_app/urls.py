from rest_framework import routers

from chat.chat_app import views

router = routers.SimpleRouter()
router.register(r'conversation', views.ConversationViewSet, 'conversation')
router.register(r'message', views.MessageViewSet, 'message')
router.register(r'participation', views.ParticipationViewSet, 'participation')
router.register(r'user', views.UserViewSet, 'user')

urlpatterns = router.urls
