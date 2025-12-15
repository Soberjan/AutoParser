from django.contrib import admin

from examples.w10.app2.models import App2Model

class App2Admin(admin.ModelAdmin):
    list_display = ["id","title","description", "created"]

admin.site.register(App2Model, App2Admin)
