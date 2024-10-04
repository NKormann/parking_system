from django.urls import path, include
from rest_framework import routers
from .views import CustomerViewSet, VehicleViewSet, PlanViewSet, CustomerPlanViewSet, ContractViewSet, ContractRuleViewSet, ParkMovementViewSet

router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'vehicle', VehicleViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'customerplan', CustomerPlanViewSet)
router.register(r'contract', ContractViewSet)
router.register(r'contractrule', ContractRuleViewSet)
router.register(r'parkmovement', ParkMovementViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
