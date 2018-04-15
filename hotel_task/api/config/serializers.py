from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import APIException

from hotel_task.models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('parameter', 'value')

    def validate(self, attrs):
        parameter = attrs.get('parameter', '')
        value = attrs.get('value', '')

        parameter_options = Config.PARAMETERS.get(parameter)
        if parameter_options is None:
            raise Http404()

        type_, converter, _= parameter_options
        try:
            converter(value)
        except ValueError:
            raise APIException(f'Wrong value. Type of value should be <{type_}>', 400)

        return attrs
