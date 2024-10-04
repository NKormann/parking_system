from rest_framework import serializers
from .models import Customer, Vehicle, Plan, CustomerPlan, Contract, ContractRule, ParkMovement

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', allow_null=True
    )
    class Meta:
        model = Vehicle
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class CustomerPlanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)

    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer')
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), source='plan')

    class Meta:
        model = CustomerPlan
        fields = '__all__'

class ContractRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractRule
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    contract_rules = ContractRuleSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'

class ParkMovementSerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.plate', read_only=True)
    customer_card_id = serializers.CharField(source='vehicle.customer.card_id', read_only=True)

    class Meta:
        model = ParkMovement
        fields = '__all__'
