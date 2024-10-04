from django.contrib import admin
from .models import (
    Customer, Vehicle, Plan, CustomerPlan,
    Contract, ContractRule, ParkMovement
)

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Plan)
admin.site.register(CustomerPlan)
admin.site.register(Contract)
admin.site.register(ContractRule)
admin.site.register(ParkMovement)
