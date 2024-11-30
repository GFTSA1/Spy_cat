from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cats.models import Cat, Mission, Target


class UpdateAfterCreationMixin:

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        updatable_fields = self.Meta.updatable_fields

        if self.instance:
            for field_name in self.Meta.fields:
                if field_name in updatable_fields:
                    continue

                kwargs.setdefault(field_name, {})
                kwargs[field_name]["read_only"] = True

        return kwargs


class CatSerializer(UpdateAfterCreationMixin, serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ['id', 'name', 'experience', 'breed', 'salary']
        updatable_fields = ['salary']


class TargetSerializer(UpdateAfterCreationMixin, serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']
        updatable_fields = ['notes', 'is_completed']


class MissionSerializer(UpdateAfterCreationMixin, serializers.ModelSerializer):
        targets = TargetSerializer(many=True)

        class Meta:
            model = Mission
            fields = ['id', 'cat', 'targets', 'is_completed']
            updatable_fields = ['cat', 'targets', 'is_completed']

        def create(self, validated_data):
            targets_data = validated_data.pop('targets')
            if not targets_data:
                raise ValidationError(
                    'Field targets cannot be empty'
                )

            if len(targets_data) > 3:
                raise ValidationError(
                    'There could not be more than 3 targets'
                )

            mission = Mission.objects.create(**validated_data)

            for target_data in targets_data:
                target = Target.objects.create(**target_data)
                mission.targets.add(target)

            return mission
