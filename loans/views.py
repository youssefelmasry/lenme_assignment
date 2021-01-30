from functools import partial
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from loans.serializers import LoanSubmitSerializer, OfferSerializer

class LoanSubmitView(CreateAPIView):
    serializer_class = LoanSubmitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status":"Loan Submitted, Please Check for Offers"})


class OfferSubmitView(UpdateAPIView, CreateAPIView):

    serializer_class = OfferSerializer

    def get_queryset(self):
        query_set = OfferSerializer.Meta.model.objects.all()
        return query_set

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'user':request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    