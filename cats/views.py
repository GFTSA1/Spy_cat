from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

import requests
from cats.models import Cat, Mission, Target
from cats.serializers import CatSerializer, MissionSerializer, TargetSerializer


class CatsView(ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        request_cat_api = requests.get("https://api.thecatapi.com/v1/breeds")
        breeds_json = request_cat_api.json()
        breed_names = {breed["name"].lower() for breed in breeds_json}
        breed_for_validation = request.data.get('breed')

        if breed_for_validation.lower() in breed_names:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"error": f"The breed '{request.data.get('breed')}' is not a valid breed."},
                status=status.HTTP_400_BAD_REQUEST
            )


class MissionView(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat is not None:
            return Response(
                data={'Mission after assigning to a cat is not deletable'},
                status=400,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TargetView(ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    pagination_class = None

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        target = self.get_object()
        if target.is_completed is True:
            return Response(
                data={'Targets after completion is not editable.'},
                status=400,
            )
        if self.is_related_mission_completed(target):
            return Response(
                data={'Targets after mission completion is not editable.'},
                status=400,
            )

        serializer = self.get_serializer(target, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @classmethod
    def is_related_mission_completed(cls, target: Target):
        related_missions = Mission.objects.filter(targets__id=target.pk)
        if not related_missions:
            return False

        return related_missions.first().is_completed
