# from django.http import HttpResponse, JsonResponse

# from django.views.decorators.csrf import csrf_exempt

# from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from examples.w10.app2.models import App2Model
from examples.w10.app2.serializers import App2Serializer


@extend_schema_view(
    list=extend_schema(summary="all app2 models", description="Description for list"),
    create=extend_schema(
        summary="create app2 model", description="Description for create"
    ),
    retrieve=extend_schema(
        summary="retrieve app2 models", description="Description for retrieve"
    ),
    update=extend_schema(
        summary="update app2 models", description="Description for update"
    ),
    destroy=extend_schema(
        summary="destroy app2 models", description="Description for destroy"
    ),
    partial_update=extend_schema(
        summary="patch app2 models", description="Description for patch"
    ),
)
class App2ViewSet(viewsets.ModelViewSet):
    """Model app2 example."""

    queryset = App2Model.objects.all()
    serializer_class = App2Serializer

    # def retrieve2(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # django-filter


# @csrf_exempt
# def app2_list(request):
#     if request.method == "GET":
#         models = App2Model.objects.all()
#         serializer = App2Serializer(models, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = App2Serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def app2_detail(request, pk):
#     try:
#         model = App2Model.objects.get(pk=pk)
#     except App2Model.DoesNotExist:
#         return HttpResponse(status=404)


#     if request.method == "GET":
#         serializer = App2Serializer(model)
#         return JsonResponse(serializer.data)
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = App2Serializer(model, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == "DELETE":
#         model.delete()
#         return HttpResponse(status=204)
