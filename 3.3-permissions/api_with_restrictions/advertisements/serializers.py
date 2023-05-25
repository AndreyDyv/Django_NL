from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)
        read_only_fields = ('username', )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля 'creator' по-умолчанию.
        # Текущий пользователь (user) является создателем объявления, изменить или переопределить его через API нельзя.
        # Обратите внимание на `context` – он выставляется автоматически через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if self.context['request'].method == 'POST':
            if Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count() > 10:
                raise ValidationError('Превышено максимальное число открытых объявлений')
        return data

