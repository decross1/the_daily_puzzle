from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PuzzleViewSet, DifficultyHistoryViewSet, PlayerProgressViewSet, StumpTallyViewSet

router = DefaultRouter()
router.register(r'puzzles', PuzzleViewSet)
router.register(r'difficulty-history', DifficultyHistoryViewSet)
router.register(r'progress', PlayerProgressViewSet)
router.register(r'stump-tally', StumpTallyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]