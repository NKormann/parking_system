from rest_framework import serializers
from .models import Customer, Vehicle, Plan, CustomerPlan, Contract, ContractRule, ParkMovement

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class CustomerPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPlan
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    contract_rules = serializers.PrimaryKeyRelatedField(many=True, queryset=ContractRule.objects.all())

    class Meta:
        model = Contract
        fields = '__all__'

class ContractRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractRule
        fields = '__all__'

class ParkMovementSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.plate', read_only=True)
    customer_card_id = serializers.CharField(source='vehicle.customer.card_id', read_only=True)

    class Meta:
        model = ParkMovement
        fields = '__all__'
