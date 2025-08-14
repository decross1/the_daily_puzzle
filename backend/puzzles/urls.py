from django.urls import path
from . import views

urlpatterns = [
    path('puzzle/daily/', views.get_daily_puzzle, name='daily-puzzle'),
    path('puzzle/submit/', views.submit_puzzle_answer, name='submit-answer'),
    path('puzzle/history/', views.get_puzzle_history, name='puzzle-history'),
    path('puzzle/generate/', views.generate_puzzle_manually, name='generate-puzzle'),
    path('puzzle/visual-art/', views.generate_visual_art_puzzle, name='visual-art-puzzle'),
    
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
    path('stump-tally/', views.get_stump_tally, name='stump-tally'),
    path('stats/', views.get_player_stats, name='player-stats'),
]