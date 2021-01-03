from api.views import (
    ChannelViewSet,
    LinkViewSet,
    MessageViewSet,
    ModelReferenceViewSet,
    ServerViewSet,
    UserCounter,
    UserViewSet,
)
from django.urls import include, path
from rest_framework import routers

# from django.urls import path

router = routers.DefaultRouter()
router.register(r"channel", ChannelViewSet)
router.register(r"link", LinkViewSet)
router.register(r"message", MessageViewSet)
router.register(r"modelreference", ModelReferenceViewSet)
router.register(r"server", ServerViewSet)
router.register(r"user", UserViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"user/counter", UserCounter.as_view()),
]
