from api.views import (
    ChannelsFrequency,
    ChannelViewSet,
    DistributionUserMessage,
    GenericCounter,
    IsAuthentView,
    LinksFrequency,
    LinkViewSet,
    MessageViewSet,
    ModelReferenceViewSet,
    ScoreUserGeneralMessage,
    ServerViewSet,
    UserViewSet,
    Search,
    WordBattle,
    ProfileManager,
)
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

# from django.urls import path
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

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
router.register(r"search", Search, basename="search"),

router.register(r"links", LinksFrequency, basename="linksfrequency")
router.register(r"channels", ChannelsFrequency, basename="channelsfrequency")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"<str:objectname>/counter", GenericCounter.as_view()),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("hello/", IsAuthentView.as_view(), name="hello"),
    path("profile/", ProfileManager.as_view(), name="profile_manager"),
]

# schema_view = get_schema_view(
#   openapi.Info(
#      title="Snippets API",
#      default_version='v1',
#      description="Test description",
#      terms_of_service="https://www.google.com/policies/terms/",
#      contact=openapi.Contact(email="contact@snippets.local"),
#      license=openapi.License(name="BSD License"),
#   ),
#   public=True,
#   permission_classes=(permissions.AllowAny,),
#)

# urlpatterns = urlpatterns + [
#        path(r'swagger(?<str:format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#   path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#   path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#]
