from django.db.models import get_models, get_app
from django.contrib import admin

app_models = get_app(".".join(__name__.split('.')[:-1]))
for model in get_models(app_models):
    admin.site.register(model)
