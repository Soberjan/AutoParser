from rest_framework import serializers

from examples.w10.app2.models import App2Model

class App2Serializer(serializers.ModelSerializer):
    class Meta:
        model = App2Model
        fields = ["id","title","description", ]