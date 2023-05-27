from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourites
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavouritesSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated(), ]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly(), ]
        return []

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_anonymous:
            drafts = Advertisement.objects.filter(user=self.request.user, status='DRAFT')
            qs = qs.union(drafts)
        return qs

    @action(methods=('get', 'post'), detail=False, url_path='fav')
    def favourite(self, request):
        if self.request.user.is_anonymous:
            return Response({'error': 'У вас нет прав доступа к избранным заметкам'})
        if request.method == 'GET':
            qs = Favourites.objects.filter(user=self.request.user)
            serializer = FavouritesSerializer(qs, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            try:
                favourite_id = Advertisement.objects.get(pk=request.data.get('advertisement'))
            except ObjectDoesNotExist:
                return Response({'error': 'Объявления с таким id не существует'})
            if Favourites.objects.filter(user=self.request.user, advertisement=favourite_id).exists():
                return Response({'error': 'Объявление уже добавлено в "Избранное"'})
            else:
                favourite = Favourites.objects.create(user=self.request.user, advertisement=favourite_id)
                serializer = FavouritesSerializer((favourite,), many=True)
                return Response(serializer.data)
