from django.utils import timezone
from django.db import transaction
from .models import Vehicle, Customer, CustomerPlan, Contract, ContractRule, ParkMovement
from rest_framework.exceptions import ValidationError

def get_vehicle_by_plate_or_card(plate=None, card_id=None):
    if plate:
        try:
            vehicle = Vehicle.objects.get(plate=plate)
            return vehicle
        except Vehicle.DoesNotExist:
            # Veículo não cadastrado
            vehicle = Vehicle.objects.create(plate=plate)
            return vehicle
    elif card_id:
        try:
            customer = Customer.objects.get(card_id=card_id)
            vehicle = Vehicle.objects.filter(customer=customer).first()
            if not vehicle:
                raise ValidationError('Cliente não possui veículo cadastrado.')
            return vehicle
        except Customer.DoesNotExist:
            raise ValidationError('CARD_ID não cadastrado.')
    else:
        raise ValidationError('É necessário fornecer a placa ou o CARD_ID.')

def is_vehicle_in_parking(vehicle):
    return ParkMovement.objects.filter(vehicle=vehicle, exit_date__isnull=True).exists()

def calculate_parking_fee(park_movement):
    duration = (park_movement.exit_date - park_movement.entry_date).total_seconds() / 60  # duração em minutos

    # Verificar se é mensalista
    if park_movement.vehicle.customer and CustomerPlan.objects.filter(customer=park_movement.vehicle.customer).exists():
        return 0.0  # Mensalistas não são cobrados
    else:
        # Cálculo para rotativos
        contract = Contract.objects.first()
        if not contract:
            raise ValidationError('Nenhum contrato de cálculo encontrado.')

        rules = ContractRule.objects.filter(contract=contract).order_by('until')
        for rule in rules:
            if duration <= rule.until:
                return rule.value

        # Se não encontrar uma regra adequada, aplica o valor máximo
        if contract.max_value:
            return contract.max_value
        else:
            raise ValidationError('Não foi possível calcular o valor. Verifique as regras do contrato.')

def enter_vehicle(plate=None, card_id=None):
    with transaction.atomic():
        vehicle = get_vehicle_by_plate_or_card(plate, card_id)

        if is_vehicle_in_parking(vehicle):
            raise ValidationError('Veículo já está no pátio.')

        # Criar movimento de entrada
        park_movement = ParkMovement.objects.create(vehicle=vehicle)
        return park_movement

def exit_vehicle(park_movement):
    with transaction.atomic():
        if park_movement.exit_date:
            raise ValidationError('Movimento já finalizado.')

        park_movement.exit_date = timezone.now()
        park_movement.value = calculate_parking_fee(park_movement)
        park_movement.save()
        return park_movement
