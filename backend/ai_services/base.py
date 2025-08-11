from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PuzzleGenerationError(Exception):
    """Custom exception for puzzle generation failures"""
    pass


class BasePuzzleGenerator(ABC):
    """Abstract base class for all AI puzzle generators"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.logger = logging.getLogger(f"{__name__}.{model_name}")
    
    @abstractmethod
    async def generate_puzzle(
        self, 
        category: str, 
        difficulty: float,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a puzzle for the given category and difficulty.
        
        Args:
            category: One of 'math', 'word', 'art'
            difficulty: Float between 0.0 and 1.0
            constraints: Optional constraints for puzzle generation
            
        Returns:
            Dict containing:
            - question: The puzzle question/prompt
            - solution: The correct answer
            - explanation: Optional explanation of the solution
            - media_url: Optional URL for media content (images, audio)
            - hints: Optional list of hints
        """
        pass
    
    @abstractmethod
    async def validate_puzzle(
        self, 
        question: str, 
        solution: str, 
        category: str
    ) -> Dict[str, Any]:
        """
        Validate that a puzzle can be solved correctly.
        
        Args:
            question: The puzzle question
            solution: The expected solution
            category: Puzzle category
            
        Returns:
            Dict containing:
            - is_valid: Boolean indicating if puzzle is valid
            - generated_solution: AI's attempt at solving
            - confidence: Float between 0.0 and 1.0
            - issues: List of any problems found
        """
        pass
    
    def get_difficulty_prompt(self, difficulty: float) -> str:
        """Convert difficulty float to descriptive text"""
        if difficulty < 0.4:
            return "beginner-friendly (Mini difficulty)"
        elif difficulty < 0.7:
            return "moderate challenge (Mid difficulty)" 
        else:
            return "expert-level challenge (Beast difficulty)"
    
    def get_category_context(self, category: str) -> str:
        """Get context-specific information for each category"""
        contexts = {
            'math': "Focus on algebra, geometry, number theory, or applied mathematics. Ensure solutions are precise and verifiable.",
            'word': "Create wordplay, riddles, anagrams, or language puzzles. Solutions should be clever but unambiguous.", 
            'art': "Create puzzles about visual arts, music, film, architecture, or cultural knowledge. Examples: artist identification, art movement recognition, color theory, famous works, film/music trivia, architectural styles. Ensure answers are factual and verifiable."
        }
        return contexts.get(category, "General puzzle")