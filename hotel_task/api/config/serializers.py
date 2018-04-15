from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import APIException

from hotel_task.models import Config


class ConfigSerializer(serializers.Serializer):
    parameter = serializers.CharField(read_only=True)
    value = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.parameter = kwargs.pop('parameter', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        value = attrs.get('value', '')
        assert self.parameter is not None

        parameter_options = Config.PARAMETERS.get(self.parameter)
        if parameter_options is None:
            raise Http404()

        type_, converter, _ = parameter_options
        try:
            converter(value)
        except ValueError:
            raise APIException(f'Wrong value. Type of value should be <{type_}>', 400)

        attrs['parameter'] = self.parameter
        return attrs
