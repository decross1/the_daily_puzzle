from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
import logging

from .models import Puzzle, PlayerProgress, StumpTally, DifficultyHistory
# from .serializers import PuzzleSerializer, PlayerProgressSerializer, StumpTallySerializer
# from services.puzzle_generator import PuzzleGenerationService

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_daily_puzzle(request):
    """Get today's puzzle"""
    today = timezone.now().date()
    
    try:
        # Find today's puzzle by looking for puzzle with today's date in the ID
        puzzle = Puzzle.objects.get(id=today.strftime('%Y-%m-%d'), is_active=True)
        
        # For now, return basic puzzle data without serializer
        puzzle_data = {
            'id': puzzle.id,
            'category': puzzle.category,
            'difficulty': puzzle.difficulty,
            'generator_model': puzzle.generator_model,
            'question': puzzle.puzzle_question,
            'media_url': puzzle.media_url,
            'total_attempts': puzzle.total_attempts,
            'solve_rate': puzzle.solve_rate,
            'created_at': puzzle.created_at,
        }
        
        return Response(puzzle_data)
        
    except Puzzle.DoesNotExist:
        # TODO: Try to generate today's puzzle using PuzzleGenerationService
        # For now, return an error
        return Response(
            {'error': 'No puzzle found for today. Puzzle generation not yet implemented.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_puzzle_answer(request):
    """Submit an answer to today's puzzle"""
    today = timezone.now().date()
    
    try:
        puzzle = Puzzle.objects.get(id=today.strftime('%Y-%m-%d'), is_active=True)
    except Puzzle.DoesNotExist:
        return Response(
            {'error': 'No active puzzle found for today'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    user = request.user
    submitted_answer = request.data.get('answer', '').strip()
    
    if not submitted_answer:
        return Response(
            {'error': 'Answer is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create player progress for this puzzle
    progress, created = PlayerProgress.objects.get_or_create(
        puzzle=puzzle, 
        user=user,
        defaults={
            'attempts': 0,
            'solved': False
        }
    )
    
    # Check if user already solved this puzzle
    if progress.solved:
        return Response(
            {'error': 'You have already solved this puzzle'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Increment attempt count
    progress.attempts += 1
    
    # Get solve time from request (frontend should track this)
    solve_time = request.data.get('solve_time')  # seconds
    
    # Check if answer is correct (simple string comparison for now)
    # TODO: Implement more sophisticated answer checking
    is_correct = submitted_answer.lower().strip() == puzzle.solution.lower().strip()
    
    # Update progress
    if is_correct:
        progress.solved = True
        progress.solve_time = solve_time
        progress.solved_at = timezone.now()
        
        # Update puzzle stats
        puzzle.successful_solves += 1
        
    # Update puzzle total attempts
    puzzle.total_attempts += 1
    puzzle.save()
    progress.save()
    
    # TODO: Update player stats and streaks
    if is_correct:
        update_player_stats(user, puzzle, solve_time)
    
    return Response({
        'is_correct': is_correct,
        'attempts': progress.attempts,
        'solved': progress.solved,
        'solve_time': progress.solve_time,
        'message': 'Correct! Well done!' if is_correct else 'Not quite right, try again!'
    })

def update_player_stats(user, puzzle, solve_time):
    """Update player statistics after a correct solve"""
    # TODO: Implement comprehensive player stats tracking
    # This will be implemented when we add PlayerStats model
    # For now, just log the solve
    logger.info(f"User {user.username} solved puzzle {puzzle.id} in {solve_time}s")
    pass

@api_view(['GET'])
def get_leaderboard(request):
    """Get leaderboard data"""
    today = timezone.now().date()
    today_puzzle_id = today.strftime('%Y-%m-%d')
    
    # Daily leaderboard (fastest solves today)
    daily_leaders = []
    try:
        today_puzzle = Puzzle.objects.get(id=today_puzzle_id)
        daily_progress = PlayerProgress.objects.filter(
            puzzle=today_puzzle,
            solved=True,
            solve_time__isnull=False
        ).order_by('solve_time')[:10]
        
        daily_leaders = [
            {
                'username': progress.user.username,
                'solve_time': progress.solve_time,
                'attempts': progress.attempts,
                'rank': i + 1
            }
            for i, progress in enumerate(daily_progress)
        ]
    except Puzzle.DoesNotExist:
        pass
    
    # All-time leaders (most puzzles solved)
    # TODO: This will be more sophisticated with PlayerStats model
    all_time_leaders = (
        User.objects.annotate(
            total_solved=Count('playerprogress', filter=Q(playerprogress__solved=True)),
            avg_solve_time=Avg('playerprogress__solve_time', filter=Q(playerprogress__solved=True))
        )
        .filter(total_solved__gt=0)
        .order_by('-total_solved')[:10]
    )
    
    all_time_data = [
        {
            'username': user.username,
            'total_solved': user.total_solved,
            'avg_solve_time': user.avg_solve_time,
            'rank': i + 1
        }
        for i, user in enumerate(all_time_leaders)
    ]
    
    return Response({
        'daily_leaderboard': daily_leaders,
        'all_time_leaderboard': all_time_data
    })

@api_view(['GET'])
def get_stump_tally(request):
    """Get AI model stump tally"""
    tallies = StumpTally.objects.all()
    
    tally_data = [
        {
            'ai_model': tally.ai_model,
            'category': tally.category,
            'successful_stumps': tally.successful_stumps,
            'total_generated': tally.total_generated,
            'stump_rate': tally.stump_rate,
            'last_updated': tally.last_updated
        }
        for tally in tallies
    ]
    
    # Sort by stump_rate in Python since it's a property
    tally_data.sort(key=lambda x: x['stump_rate'], reverse=True)
    
    return Response(tally_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_stats(request):
    """Get current user's statistics"""
    user = request.user
    
    # Calculate user stats from PlayerProgress
    user_progress = PlayerProgress.objects.filter(user=user)
    total_solved = user_progress.filter(solved=True).count()
    total_attempts = user_progress.aggregate(total=Count('attempts'))['total'] or 0
    
    solved_progress = user_progress.filter(solved=True, solve_time__isnull=False)
    fastest_solve = solved_progress.order_by('solve_time').first()
    avg_solve_time = solved_progress.aggregate(avg=Avg('solve_time'))['avg']
    
    # Category breakdown
    math_solved = user_progress.filter(puzzle__category='math', solved=True).count()
    word_solved = user_progress.filter(puzzle__category='word', solved=True).count()
    art_solved = user_progress.filter(puzzle__category='art', solved=True).count()
    
    # TODO: Calculate streaks properly when we have date-based tracking
    current_streak = 0
    longest_streak = 0
    
    stats_data = {
        'total_solved': total_solved,
        'total_attempts': total_attempts,
        'fastest_solve': fastest_solve.solve_time if fastest_solve else None,
        'avg_solve_time': avg_solve_time,
        'math_solved': math_solved,
        'word_solved': word_solved,
        'art_solved': art_solved,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
    }
    
    return Response(stats_data)

@api_view(['GET'])
def get_puzzle_history(request):
    """Get recent puzzle history"""
    puzzles = Puzzle.objects.filter(is_active=True).order_by('-created_at')[:7]  # Last 7 puzzles
    
    puzzle_data = []
    for puzzle in puzzles:
        # Calculate difficulty band
        if puzzle.difficulty < 0.4:
            difficulty_band = 'Mini'
        elif puzzle.difficulty < 0.7:
            difficulty_band = 'Mid'
        else:
            difficulty_band = 'Beast'
            
        puzzle_info = {
            'id': puzzle.id,
            'category': puzzle.category,
            'difficulty': puzzle.difficulty,
            'difficulty_band': difficulty_band,
            'total_attempts': puzzle.total_attempts,
            'successful_solves': puzzle.successful_solves,
            'solve_rate': puzzle.solve_rate,
            'generator_model': puzzle.generator_model,
            'created_at': puzzle.created_at,
        }
        puzzle_data.append(puzzle_info)
    
    return Response({'puzzles': puzzle_data})

@api_view(['POST'])
def generate_puzzle_manually(request):
    """Manual puzzle generation endpoint (for testing)"""
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    category = request.data.get('category', 'math')
    difficulty = float(request.data.get('difficulty', 0.5))
    
    # TODO: Implement PuzzleGenerationService
    # For now, return a mock response
    mock_puzzle_data = {
        'category': category,
        'difficulty': difficulty,
        'question': f'Sample {category} puzzle at difficulty {difficulty}',
        'solution': 'sample_solution',
        'generator_model': 'mock'
    }
    
    return Response({
        'success': True,
        'puzzle': mock_puzzle_data,
        'message': 'Mock puzzle generated. Real AI integration coming soon.'
    })

# Additional utility endpoints

@api_view(['GET'])
def get_puzzle_stats(request):
    """Get overall puzzle statistics"""
    total_puzzles = Puzzle.objects.filter(is_active=True).count()
    total_attempts = Puzzle.objects.aggregate(total=Count('total_attempts'))['total'] or 0
    total_solves = Puzzle.objects.aggregate(total=Count('successful_solves'))['total'] or 0
    
    category_stats = {}
    for category, _ in Puzzle.CATEGORY_CHOICES:
        category_puzzles = Puzzle.objects.filter(category=category, is_active=True)
        category_stats[category] = {
            'total_puzzles': category_puzzles.count(),
            'avg_difficulty': category_puzzles.aggregate(avg=Avg('difficulty'))['avg'] or 0,
            'total_attempts': category_puzzles.aggregate(total=Count('total_attempts'))['total'] or 0,
            'total_solves': category_puzzles.aggregate(total=Count('successful_solves'))['total'] or 0,
        }
    
    return Response({
        'total_puzzles': total_puzzles,
        'total_attempts': total_attempts,
        'total_solves': total_solves,
        'overall_solve_rate': total_solves / total_attempts if total_attempts > 0 else 0,
        'category_stats': category_stats
    })

@api_view(['GET'])
def get_difficulty_history(request):
    """Get difficulty adjustment history"""
    category = request.GET.get('category', 'math')
    history = DifficultyHistory.objects.filter(category=category).order_by('-date')[:30]
    
    history_data = [
        {
            'date': entry.date,
            'difficulty': entry.difficulty,
            'previous_difficulty': entry.previous_difficulty,
            'adjustment_reason': entry.adjustment_reason,
        }
        for entry in history
    ]
    
    return Response({
        'category': category,
        'history': history_data
    })