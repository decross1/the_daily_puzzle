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
from .serializers import (
    PuzzleSerializer, PlayerProgressSerializer, StumpTallySerializer, 
    DifficultyHistorySerializer, LeaderboardSerializer, PuzzleStatsSerializer,
    PuzzleSubmissionSerializer, PuzzleSubmissionResponseSerializer,
    PuzzleGenerationRequestSerializer
)
from ai_services.manager import puzzle_service
import asyncio

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_daily_puzzle(request):
    """Get today's puzzle"""
    today = timezone.now().date()
    
    try:
        # Find today's puzzle by looking for puzzle with today's date in the ID
        puzzle = Puzzle.objects.get(id=today.strftime('%Y-%m-%d'), is_active=True)
        
        serializer = PuzzleSerializer(puzzle)
        return Response(serializer.data)
        
    except Puzzle.DoesNotExist:
        logger.warning(f"No puzzle found for {today.strftime('%Y-%m-%d')}")
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
    
    # Validate submission data
    submission_serializer = PuzzleSubmissionSerializer(data=request.data)
    if not submission_serializer.is_valid():
        return Response(submission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    submitted_answer = submission_serializer.validated_data['answer']
    solve_time = submission_serializer.validated_data.get('solve_time')
    
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
    
    # solve_time is already extracted from validated data above
    
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
    
    # Use response serializer for consistency
    response_data = {
        'is_correct': is_correct,
        'attempts': progress.attempts,
        'solved': progress.solved,
        'solve_time': progress.solve_time,
        'message': 'Correct! Well done!' if is_correct else 'Not quite right, try again!'
    }
    
    response_serializer = PuzzleSubmissionResponseSerializer(response_data)
    return Response(response_serializer.data)

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
    
    leaderboard_data = {
        'daily_leaderboard': daily_leaders,
        'all_time_leaderboard': all_time_data
    }
    
    serializer = LeaderboardSerializer(leaderboard_data)
    return Response(serializer.data)

@api_view(['GET'])
def get_stump_tally(request):
    """Get AI model stump tally"""
    tallies = StumpTally.objects.all().order_by('-successful_stumps')
    serializer = StumpTallySerializer(tallies, many=True)
    
    # Sort by stump_rate in Python since it's a property
    tally_data = serializer.data
    tally_data.sort(key=lambda x: x.get('stump_rate', 0), reverse=True)
    
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
    
    serializer = PlayerStatsSerializer(stats_data)
    return Response(serializer.data)

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
    
    # Allow any user for testing visual puzzles
    # if not request.user.is_staff:
    #     return Response(
    #         {'error': 'Permission denied'}, 
    #         status=status.HTTP_403_FORBIDDEN
    #     )
    
    try:
        # Get request parameters
        category = request.data.get('category', 'art')
        difficulty = float(request.data.get('difficulty', 0.5))
        visual_puzzle = request.data.get('visual_puzzle', True)
        
        # Prepare constraints for visual puzzles
        constraints = {
            'visual_puzzle': visual_puzzle
        }
        
        # Generate puzzle using our sophisticated system
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            puzzle_data = loop.run_until_complete(
                puzzle_service.generate_daily_puzzle(
                    timezone.now().date(), 
                    category, 
                    difficulty
                )
            )
            
            # Format response for frontend
            response_data = {
                'success': True,
                'puzzle': {
                    'id': puzzle_data.get('id'),
                    'category': puzzle_data.get('category'),
                    'difficulty': puzzle_data.get('difficulty'),
                    'question': puzzle_data.get('question'),
                    'solution': puzzle_data.get('solution'),
                    'explanation': puzzle_data.get('explanation'),
                    'hints': puzzle_data.get('hints', []),
                    'visual_content': puzzle_data.get('visual_content'),
                    'interaction_type': puzzle_data.get('interaction_type'),
                    'puzzle_type': puzzle_data.get('puzzle_type'),
                    'puzzle_format': puzzle_data.get('puzzle_format', 'text'),
                    'visual_elements': puzzle_data.get('visual_elements', {}),
                    'estimated_solve_time': puzzle_data.get('estimated_solve_time', 180),
                    'generator_model': puzzle_data.get('generator_model'),
                    'difficulty_justification': puzzle_data.get('difficulty_justification')
                },
                'validation': puzzle_data.get('validator_results', {}),
                'message': f'Generated {category} puzzle with difficulty {difficulty}'
            }
            
            return Response(response_data)
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Puzzle generation failed: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Puzzle generation failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])  # Allow unauthenticated access for testing
def generate_visual_art_puzzle(request):
    """Generate visual art puzzle specifically for frontend testing"""
    
    try:
        difficulty = float(request.data.get('difficulty', 0.5))
        puzzle_type = request.data.get('puzzle_type', 'auto')  # 'color_theory', 'composition', etc.
        
        # Import the visual puzzle generator
        from ai_services.visual_art_puzzles import generate_visual_art_puzzle
        from ai_services.difficulty_framework import ArtDifficultyCalibrator
        
        # Generate difficulty factors
        calibrator = ArtDifficultyCalibrator()
        difficulty_factors = calibrator.generate_difficulty_factors(difficulty)
        
        # Generate visual puzzle
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            puzzle_data = loop.run_until_complete(
                generate_visual_art_puzzle(difficulty_factors)
            )
            
            # Add metadata
            puzzle_data.update({
                'id': f'test-{timezone.now().strftime("%Y%m%d-%H%M%S")}',
                'category': 'art',
                'difficulty': difficulty,
                'generator_model': 'visual_puzzle_system',
                'created_at': timezone.now().isoformat()
            })
            
            return Response({
                'success': True,
                'puzzle': puzzle_data,
                'message': 'Visual art puzzle generated successfully'
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Visual puzzle generation failed: {str(e)}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Visual puzzle generation failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    
    stats_data = {
        'total_puzzles': total_puzzles,
        'total_attempts': total_attempts,
        'total_solves': total_solves,
        'overall_solve_rate': total_solves / total_attempts if total_attempts > 0 else 0,
        'category_stats': category_stats
    }
    
    serializer = PuzzleStatsSerializer(stats_data)
    return Response(serializer.data)

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