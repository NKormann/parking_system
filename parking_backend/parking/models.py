from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.plate

class Plan(models.Model):
    description = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return self.description

class CustomerPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.plan.description}"

class Contract(models.Model):
    description = models.CharField(max_length=50)
    max_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.description

class ContractRule(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_rules')
    until = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.contract.description} - Até {self.until} min"


class ParkMovement(models.Model):
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.plate} - Entrada: {self.entry_date}"
