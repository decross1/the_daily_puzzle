import random
from typing import Dict, Any, Optional, List
from django.conf import settings
from datetime import date, datetime
from .base import PuzzleGenerationError
from .claude import Claude4PuzzleGenerator
import logging

logger = logging.getLogger(__name__)


class PuzzleGenerationService:
    """Service that manages puzzle generation across all AI models"""
    
    def __init__(self):
        self.generators = {
            'claude4': Claude4PuzzleGenerator(),
            # Will add GPT-5 and Gemini generators later
        }
        self.categories = settings.PUZZLE_CATEGORIES
        self.models = settings.AI_MODELS
    
    async def generate_daily_puzzle(
        self, 
        puzzle_date: date, 
        category: str, 
        difficulty: float
    ) -> Dict[str, Any]:
        """
        Generate today's puzzle using the scheduled AI model.
        
        Args:
            puzzle_date: Date for the puzzle (used for model rotation)
            category: Puzzle category ('math', 'word', 'art')
            difficulty: Current difficulty level (0.0-1.0)
            
        Returns:
            Complete puzzle data ready for database storage
        """
        
        # Determine which model should generate today's puzzle
        model_name = self._get_model_for_date(puzzle_date, category)
        
        if model_name not in self.generators:
            logger.warning(f"Model {model_name} not available, falling back to claude4")
            model_name = 'claude4'
        
        generator = self.generators[model_name]
        
        try:
            logger.info(f"Generating {category} puzzle for {puzzle_date} using {model_name}")
            
            # Generate the puzzle
            puzzle_data = await generator.generate_puzzle(category, difficulty)
            
            # Add metadata
            puzzle_data.update({
                'id': puzzle_date.strftime('%Y-%m-%d'),
                'category': category,
                'difficulty': difficulty,
                'generator_model': model_name,
                'created_at': datetime.now(),
                'is_active': True
            })
            
            # Validate the puzzle
            validation_result = await self._validate_puzzle_quality(
                puzzle_data, generator
            )
            
            if not validation_result['is_valid']:
                raise PuzzleGenerationError(
                    f"Generated puzzle failed validation: {validation_result['issues']}"
                )
            
            puzzle_data['validator_results'] = {
                model_name: validation_result
            }
            
            logger.info(f"Successfully generated validated puzzle for {puzzle_date}")
            return puzzle_data
            
        except Exception as e:
            logger.error(f"Failed to generate puzzle for {puzzle_date}: {str(e)}")
            raise PuzzleGenerationError(f"Puzzle generation failed: {str(e)}")
    
    async def validate_existing_puzzle(
        self, 
        puzzle_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Validate an existing puzzle with all available AI models.
        
        Args:
            puzzle_data: Existing puzzle to validate
            
        Returns:
            Dict of validation results keyed by model name
        """
        
        results = {}
        question = puzzle_data.get('question', puzzle_data.get('puzzle_content', {}).get('question', ''))
        solution = puzzle_data.get('solution', '')
        category = puzzle_data.get('category', '')
        
        for model_name, generator in self.generators.items():
            try:
                result = await generator.validate_puzzle(question, solution, category)
                results[model_name] = result
                logger.info(f"Validated puzzle with {model_name}: confidence {result.get('confidence', 0)}")
                
            except Exception as e:
                logger.error(f"Validation failed with {model_name}: {str(e)}")
                results[model_name] = {
                    'is_valid': False,
                    'confidence': 0.0,
                    'issues': [f"Validation error: {str(e)}"]
                }
        
        return results
    
    def get_available_models(self) -> List[str]:
        """Get list of currently available AI models"""
        return list(self.generators.keys())
    
    def _get_model_for_date(self, puzzle_date: date, category: str) -> str:
        """Determine which AI model should generate the puzzle for a given date"""
        
        # Use date and category to create a deterministic but varied rotation
        seed = puzzle_date.toordinal() + hash(category)
        random.seed(seed)
        
        available_models = [m for m in self.models if m in self.generators]
        if not available_models:
            return 'claude4'  # Fallback
        
        return random.choice(available_models)
    
    async def _validate_puzzle_quality(
        self, 
        puzzle_data: Dict[str, Any], 
        generator
    ) -> Dict[str, Any]:
        """Validate that the generated puzzle meets quality standards"""
        
        question = puzzle_data.get('question', '')
        solution = puzzle_data.get('solution', '')
        category = puzzle_data.get('category', '')
        
        # Basic validation checks
        if not question or not solution:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'issues': ['Missing question or solution']
            }
        
        if len(question) < 10:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'issues': ['Question too short']
            }
        
        # Use the generator to validate its own puzzle
        try:
            validation_result = await generator.validate_puzzle(question, solution, category)
            
            # Additional quality checks
            if validation_result.get('confidence', 0) < 0.6:
                validation_result['issues'] = validation_result.get('issues', []) + [
                    'Low confidence in solution'
                ]
                validation_result['is_valid'] = False
            
            return validation_result
            
        except Exception as e:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'issues': [f'Validation failed: {str(e)}']
            }


# Global service instance
puzzle_service = PuzzleGenerationService()