from api.views import (
    ChannelsFrequency,
    ChannelViewSet,
    GenericCounter,
    LinksFrequency,
    LinkViewSet,
    MessageViewSet,
    ModelReferenceViewSet,
    ScoreUserGeneralMessage,
    ServerViewSet,
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
router.register(
    r"score", ScoreUserGeneralMessage, basename="scoreusergeneralmessage"
)
router.register(r"links", LinksFrequency, basename="linksfrequency")

router.register(r"channels", ChannelsFrequency, basename="channelsfrequency")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"<str:objectname>/counter", GenericCounter.as_view()),
]
