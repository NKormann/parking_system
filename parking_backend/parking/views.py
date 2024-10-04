from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from .models import (
    Customer,
    Vehicle,
    Plan,
    CustomerPlan,
    Contract,
    ContractRule,
    ParkMovement,
)
from .serializers import (
    CustomerSerializer,
    VehicleSerializer,
    PlanSerializer,
    CustomerPlanSerializer,
    ContractSerializer,
    ContractRuleSerializer,
    ParkMovementSerializer,
)
from .services import enter_vehicle, exit_vehicle

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def create(self, request, *args, **kwargs):
        plate = request.data.get('plate')
        customer_id = request.data.get('customer')

        try:
            vehicle = Vehicle.objects.filter(plate=plate).first()
            if vehicle:
                if vehicle.customer is None and customer_id is None:
                    serializer = self.get_serializer(vehicle)
                    return Response(serializer.data)
                elif vehicle.customer is not None:
                    return Response({'error': 'Veículo já cadastrado para um cliente.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class CustomerPlanViewSet(viewsets.ModelViewSet):
    queryset = CustomerPlan.objects.all()
    serializer_class = CustomerPlanSerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ContractRuleViewSet(viewsets.ModelViewSet):
    queryset = ContractRule.objects.all()
    serializer_class = ContractRuleSerializer

class ParkMovementViewSet(viewsets.ModelViewSet):
    queryset = ParkMovement.objects.all()
    serializer_class = ParkMovementSerializer

    def create(self, request, *args, **kwargs):
        plate = request.data.get('plate')
        card_id = request.data.get('card_id')

        try:
            park_movement = enter_vehicle(plate=plate, card_id=card_id)
            serializer = self.get_serializer(park_movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        park_movement = self.get_object()
        try:
            park_movement = exit_vehicle(park_movement)
            serializer = self.get_serializer(park_movement)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def exit(self, request, pk=None):
        """
        Endpoint para registrar a saída de um veículo.
        """
        try:
            park_movement = ParkMovement.objects.get(pk=pk, exit_date__isnull=True)
            updated_movement = exit_vehicle(park_movement)
            serializer = ParkMovementSerializer(updated_movement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParkMovement.DoesNotExist:
            return Response({'error': 'Movimento de estacionamento não encontrado ou já finalizado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
