from tastypie.resources import ModelResource
from tastypie.resources import Resource
from django.db.models import get_app, get_models
from tastypie.api import Api
from tastypie import http
from django.http.response import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.authorization import Authorization

class CorsApi(Api):
    def top_level(self, *args, **kw):
        response = super(CorsApi, self).top_level(*args, **kw)
        response['Access-Control-Allow-Origin'] = '*'
        return response

class BaseCorsResource(Resource):
    """
    Class implementing CORS
    """
    def error_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).error_response(*args, **kwargs)
        return self.add_cors_headers(response, expose_headers=True)

    def add_cors_headers(self, response, expose_headers=False):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'content-type, authorization'
        if expose_headers:
            response['Access-Control-Expose-Headers'] = 'Location'
        return response

    def create_response(self, *args, **kwargs):
        """
        Create the response for a resource. Note this will only
        be called on a GET, POST, PUT request if
        always_return_data is True
        """
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        return self.add_cors_headers(response)

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(unicode.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = allows
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method

api = CorsApi(api_name='v1')
import yaml_def

def vklass(module_name, class_name, super_classes, fields=None):
    if module_name:
        initial_dict = { '__module__':module_name,}
    else:
        initial_dict = {}
    if fields is not None:
        initial_dict.update(fields)
    return type(class_name, super_classes, initial_dict)

app_models = get_app(".".join(__name__.split('.')[:-1]))
for model in get_models(app_models):
    klass = model.__name__
    meta = vklass(__name__ + '.' + klass, 'Meta', (), {
                                                            'queryset': model.objects.all(),
                                                            'authorization':Authorization(),
                                                            'always_return_data': True,
                                                        })
    res =  vklass(__name__, klass, (BaseCorsResource, ModelResource), {'Meta':meta})
    api.register(res())
    locals()[klass] = res

