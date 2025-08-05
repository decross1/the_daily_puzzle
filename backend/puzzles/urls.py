from django.urls import path
from . import views

urlpatterns = [
    # Daily puzzle endpoints
    path('daily/', views.get_daily_puzzle, name='get_daily_puzzle'),
    path('submit/', views.submit_puzzle_answer, name='submit_puzzle_answer'),
    
    # Leaderboard and stats
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('stump-tally/', views.get_stump_tally, name='get_stump_tally'),
    path('stats/player/', views.get_player_stats, name='get_player_stats'),
    path('stats/overall/', views.get_puzzle_stats, name='get_puzzle_stats'),
    
    # Puzzle history and data
    path('history/', views.get_puzzle_history, name='get_puzzle_history'),
    path('difficulty-history/', views.get_difficulty_history, name='get_difficulty_history'),
    
    # Admin/testing endpoints
    path('generate/', views.generate_puzzle_manually, name='generate_puzzle_manually'),
]