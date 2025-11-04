from rest_framework import routers
from .views import ComponentViewSet, RequirementViewSet

router = routers.DefaultRouter()
router.register(r"components", ComponentViewSet)
router.register(r"requirements", RequirementViewSet)

urlpatterns = router.urls
