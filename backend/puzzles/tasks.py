from celery import shared_task
from django.utils import timezone
from django.db.models import Q
import logging
import asyncio
import random
from datetime import date

from .models import Puzzle, PlayerProgress, StumpTally, DifficultyHistory
from ai_services.manager import puzzle_service

logger = logging.getLogger(__name__)

@shared_task
def generate_daily_puzzle():
    """
    Daily task to generate new puzzle at 00:00 UTC
    """
    logger.info("Starting daily puzzle generation...")
    
    today = timezone.now().date()
    puzzle_id = today.strftime('%Y-%m-%d')
    
    # Check if puzzle already exists
    if Puzzle.objects.filter(id=puzzle_id).exists():
        logger.info(f"Puzzle for {puzzle_id} already exists")
        return f"Puzzle {puzzle_id} already exists"
    
    # Choose a random category for today's puzzle
    category = random.choice(['math', 'word', 'art'])
    
    # Get current difficulty for this category
    difficulty = get_current_difficulty(category)
    
    try:
        # Generate puzzle using async service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        puzzle_data = loop.run_until_complete(
            puzzle_service.generate_daily_puzzle(today, category, difficulty)
        )
        
        # Create puzzle in database
        puzzle = Puzzle.objects.create(
            id=puzzle_data['id'],
            category=puzzle_data['category'],
            difficulty=puzzle_data['difficulty'],
            generator_model=puzzle_data['generator_model'],
            puzzle_content={
                'question': puzzle_data['question'],
                'media_url': puzzle_data.get('media_url'),
                'hints': puzzle_data.get('hints', []),
                'estimated_solve_time': puzzle_data.get('estimated_solve_time', 180)
            },
            solution=puzzle_data['solution'],
            generator_solution=puzzle_data.get('explanation', ''),
            validator_results=puzzle_data.get('validator_results', {}),
            is_active=True
        )
        
        logger.info(f"Successfully generated puzzle {puzzle.id} by {puzzle.generator_model}")
        return f"Generated puzzle {puzzle.id}"
        
    except Exception as e:
        logger.error(f"Failed to generate daily puzzle: {str(e)}")
        return f"Failed to generate puzzle: {str(e)}"
    finally:
        loop.close()


def get_current_difficulty(category: str) -> float:
    """Get the current difficulty level for a category"""
    
    # Try to get the most recent difficulty from DifficultyHistory
    latest_history = DifficultyHistory.objects.filter(category=category).first()
    if latest_history:
        return latest_history.difficulty
    
    # Default to mid-level difficulty
    return 0.5

@shared_task
def evaluate_daily_results():
    """
    Daily task to evaluate puzzle results and adjust difficulty at 23:59 UTC
    """
    logger.info("Starting daily puzzle evaluation...")
    
    yesterday = timezone.now().date() - timezone.timedelta(days=1)
    puzzle_id = yesterday.strftime('%Y-%m-%d')
    
    try:
        puzzle = Puzzle.objects.get(id=puzzle_id, is_active=True)
    except Puzzle.DoesNotExist:
        logger.warning(f"No puzzle found for {puzzle_id}")
        return f"No puzzle found for {puzzle_id}"
    
    # Check if community solved the puzzle
    community_solved = puzzle.successful_solves > 0
    
    # Update stump tally
    update_stump_tally(puzzle, community_solved)
    
    # Adjust difficulty for this category
    adjust_difficulty(puzzle.category, community_solved)
    
    # Check for community save achievement
    if community_solved:
        award_community_save_achievement(puzzle)
    
    logger.info(f"Puzzle {puzzle.id} evaluation complete. Community solved: {community_solved}")
    return f"Evaluated puzzle {puzzle.id}"

def update_stump_tally(puzzle, community_solved):
    """Update the stump tally for the generator model"""
    
    tally, created = StumpTally.objects.get_or_create(
        ai_model=puzzle.generator_model,
        category=puzzle.category,
        defaults={
            'total_generated': 0,
            'successful_stumps': 0
        }
    )
    
    tally.total_generated += 1
    
    if not community_solved:
        tally.successful_stumps += 1
        logger.info(f"{puzzle.generator_model} successfully stumped the community!")
    
    tally.save()

def award_community_save_achievement(puzzle):
    """Award community save achievement to first solver on potential stump days"""
    
    # Find the first person to solve this puzzle
    first_solve = PlayerProgress.objects.filter(
        puzzle=puzzle,
        solved=True
    ).order_by('solved_at').first()
    
    if first_solve and puzzle.successful_solves <= 3:  # Only if very few people solved it
        # TODO: Implement PlayerStats model for achievements
        logger.info(f"Would award community save to {first_solve.user.username}")
        # stats, created = PlayerStats.objects.get_or_create(user=first_solve.user)
        # stats.community_saves += 1
        # stats.save()

@shared_task
def cleanup_old_puzzles():
    """
    Weekly task to clean up old puzzle data (optional)
    Keep puzzles but remove detailed attempt data older than 30 days
    """
    cutoff_date = timezone.now().date() - timezone.timedelta(days=30)
    cutoff_id = cutoff_date.strftime('%Y-%m-%d')
    
    # Delete old player progress (keep puzzle records for history)
    deleted_count = PlayerProgress.objects.filter(
        puzzle__id__lt=cutoff_id
    ).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old player progress records")
    return f"Cleaned up {deleted_count} records"

@shared_task
def test_ai_models():
    """
    Test task to verify AI model connectivity
    """
    # TODO: Implement AI model testing when PuzzleGenerationService is ready
    logger.info("AI model connectivity test - not yet implemented")
    return "AI model testing not yet implemented"
    
    # generator = PuzzleGenerationService()
    # 
    # # Test Claude
    # test_puzzle = generator.claude_client.generate_math_puzzle(0.5)
    # 
    # if test_puzzle:
    #     logger.info("Claude API test successful")
    #     return "Claude API working"
    # else:
    #     logger.error("Claude API test failed")
    #     return "Claude API failed"

def adjust_difficulty(category, community_solved):
    """Adjust difficulty for a category based on community performance"""
    from django.db.models import Q
    
    # Get current difficulty for this category (default to 0.5)
    current_difficulty = 0.5
    
    # Try to get the most recent difficulty from DifficultyHistory
    latest_history = DifficultyHistory.objects.filter(category=category).first()
    if latest_history:
        current_difficulty = latest_history.difficulty
    
    # Enhanced difficulty adjustment for art puzzles using solve rate
    if category == 'art':
        new_difficulty, adjustment_reason = adjust_art_difficulty_with_feedback(
            current_difficulty, community_solved
        )
    else:
        # Standard difficulty adjustment for math/word puzzles
        if community_solved:
            # Make it harder
            new_difficulty = min(1.0, current_difficulty + 0.05)
            adjustment_reason = "Community solved - increased difficulty"
        else:
            # Make it easier
            new_difficulty = max(0.0, current_difficulty - 0.05)
            adjustment_reason = "Community stumped - decreased difficulty"
    
    # Save the difficulty adjustment
    DifficultyHistory.objects.create(
        category=category,
        date=timezone.now().date(),
        difficulty=new_difficulty,
        previous_difficulty=current_difficulty,
        adjustment_reason=adjustment_reason
    )
    
    logger.info(f"Adjusted {category} difficulty from {current_difficulty} to {new_difficulty}: {adjustment_reason}")
    return new_difficulty


def adjust_art_difficulty_with_feedback(current_difficulty, community_solved):
    """Enhanced difficulty adjustment for art puzzles using sophisticated feedback"""
    
    # TODO: Get actual solve rate data from puzzle statistics
    # For now, use community_solved as a proxy
    estimated_solve_rate = 0.6 if community_solved else 0.2
    
    # Use our sophisticated difficulty calibrator's feedback mechanism
    from ai_services.difficulty_framework import ArtDifficultyCalibrator
    
    calibrator = ArtDifficultyCalibrator()
    
    # Generate current difficulty factors
    current_factors = calibrator.generate_difficulty_factors(current_difficulty)
    
    # Adjust factors based on solve rate feedback
    adjusted_factors = calibrator.adjust_for_performance(current_factors, estimated_solve_rate)
    
    # Calculate new difficulty
    new_difficulty = adjusted_factors.calculate_composite_difficulty()
    
    # Ensure reasonable bounds and incremental changes
    max_change = 0.1  # Limit dramatic swings
    if abs(new_difficulty - current_difficulty) > max_change:
        if new_difficulty > current_difficulty:
            new_difficulty = current_difficulty + max_change
        else:
            new_difficulty = current_difficulty - max_change
    
    # Determine adjustment reason
    if estimated_solve_rate > 0.7:
        reason = f"High solve rate ({estimated_solve_rate:.1%}) - increased difficulty via sophisticated calibration"
    elif estimated_solve_rate < 0.3:
        reason = f"Low solve rate ({estimated_solve_rate:.1%}) - decreased difficulty via sophisticated calibration"
    else:
        reason = f"Moderate solve rate ({estimated_solve_rate:.1%}) - minor difficulty adjustment"
    
    return new_difficulty, reason