from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from hotel_task.api.config.serializers import ConfigSerializer
from hotel_task.models import Config


class ConfigViewSet(viewsets.ModelViewSet):
    """
    options:
    Returns list of configuration parameters

    list:
    Returns list of configuration parameters with current values

    retrieve:
    Return configuration parameter value
    <parameter> - name of the parameter

    update:
    Set configuration parameter value
    <parameter> - name of the parameter
    """

    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    lookup_url_kwarg = 'parameter'
    http_method_names = ('get', 'put', 'options')

    def options(self, request, *args, **kwars):
        list_parameters = [{'name': name, 'type': type_}
                           for name, (type_, _, _) in Config.PARAMETERS.items()]
        return Response({'parameters': list_parameters})

    def list(self, request, *args, **kwargs):
        parameters = []
        for name in Config.PARAMETERS:
            parameters.append(self.serializer_class(self.get_object(name)).data)
        return Response(parameters)

    def retrieve(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        param_name = self.kwargs[self.lookup_url_kwarg]
        if param_name in Config.PARAMETERS:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        else:
            raise Http404()

    def get_object(self, name=None):
        try:
            param_name = name or self.kwargs[self.lookup_url_kwarg]
            param_object = self.queryset.filter(
                parameter=param_name).latest()
        except Config.DoesNotExist:
            raise Http404()

        return param_object
