from django.contrib import admin
from django.apps import apps

# Get all models of your app
app = apps.get_app_config('RoomBookingWebsite') 

# Register each model automatically
for model_name, model in app.models.items():
    admin.site.register(model)
