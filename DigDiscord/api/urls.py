from api.views import (
    ChannelsFrequency,
    ChannelViewSet,
    DistributionUserMessage,
    GenericCounter,
    LinksFrequency,
    LinkViewSet,
    MessageViewSet,
    ModelReferenceViewSet,
    ScoreUserGeneralMessage,
    ServerViewSet,
    UserViewSet,
    WordBattle,
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
router.register(
    r"distribution",
    DistributionUserMessage,
    basename="distributionusermessage",
)

router.register(r"wordbattle", WordBattle, basename="wordbattle"),

router.register(r"links", LinksFrequency, basename="linksfrequency")
router.register(r"channels", ChannelsFrequency, basename="channelsfrequency")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"<str:objectname>/counter", GenericCounter.as_view()),
]
