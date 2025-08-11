import asyncio
import json
import httpx
from typing import Dict, Any, Optional
from django.conf import settings
from .base import BasePuzzleGenerator, PuzzleGenerationError


class Claude4PuzzleGenerator(BasePuzzleGenerator):
    """Claude-4 puzzle generator implementation"""
    
    def __init__(self):
        super().__init__("claude4")
        self.api_key = settings.ANTHROPIC_API_KEY
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"  # Using latest available Claude model
        
        # Security: Never log the actual API key
        self.mock_mode = not self.api_key or not self.api_key.startswith('sk-ant-')
        if self.mock_mode:
            if not self.api_key:
                self.logger.warning("ANTHROPIC_API_KEY not configured - running in mock mode")
            else:
                self.logger.warning("Invalid ANTHROPIC_API_KEY format - running in mock mode")
        else:
            # Only log that key is configured, never the actual key
            self.logger.info(f"Claude-4 initialized with API key (ends with ...{self.api_key[-8:]})")
    
    async def generate_puzzle(
        self, 
        category: str, 
        difficulty: float,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a puzzle using Claude-4"""
        
        if self.mock_mode:
            return self._generate_mock_puzzle(category, difficulty)
        
        prompt = self._build_generation_prompt(category, difficulty, constraints)
        
        try:
            response = await self._call_claude_api(prompt)
            puzzle_data = self._parse_puzzle_response(response)
            
            self.logger.info(f"Generated {category} puzzle at difficulty {difficulty}")
            return puzzle_data
            
        except Exception as e:
            self.logger.error(f"Puzzle generation failed: {str(e)}")
            raise PuzzleGenerationError(f"Failed to generate puzzle: {str(e)}")
    
    async def validate_puzzle(
        self, 
        question: str, 
        solution: str, 
        category: str
    ) -> Dict[str, Any]:
        """Validate a puzzle by attempting to solve it"""
        
        if self.mock_mode:
            return self._generate_mock_validation(question, solution, category)
        
        validation_prompt = f"""
        You are validating a {category} puzzle. Attempt to solve it independently and check if your solution matches the expected answer.
        
        Puzzle Question: {question}
        Expected Solution: {solution}
        
        Respond in this JSON format:
        {{
            "is_valid": true/false,
            "generated_solution": "your solution attempt",
            "confidence": 0.0-1.0,
            "issues": ["any problems found"],
            "reasoning": "your step-by-step solution process"
        }}
        """
        
        try:
            response = await self._call_claude_api(validation_prompt)
            validation_data = json.loads(response)
            
            self.logger.info(f"Validated puzzle with confidence {validation_data.get('confidence', 0)}")
            return validation_data
            
        except Exception as e:
            self.logger.error(f"Puzzle validation failed: {str(e)}")
            return {
                "is_valid": False,
                "generated_solution": "",
                "confidence": 0.0,
                "issues": [f"Validation failed: {str(e)}"],
                "reasoning": "Could not complete validation"
            }
    
    def _build_generation_prompt(
        self, 
        category: str, 
        difficulty: float, 
        constraints: Optional[Dict[str, Any]]
    ) -> str:
        """Build the prompt for puzzle generation"""
        
        difficulty_desc = self.get_difficulty_prompt(difficulty)
        category_context = self.get_category_context(category)
        
        if category == 'art':
            prompt = f"""
            You are an expert puzzle creator for "The Daily Puzzle" game specializing in art, culture, and creative puzzles. Generate an {category} puzzle with {difficulty_desc}.
            
            Art Puzzle Guidelines:
            - Focus on visual arts, music, film, architecture, or cultural knowledge
            - Examples: "Which artist painted 'Starry Night'?", "What art movement emphasized geometric shapes and multiple perspectives?", "This architectural style features flying buttresses and pointed arches - what is it?"
            - Use universally recognized works, artists, and concepts
            - Ensure the answer is a specific, verifiable fact
            - For {difficulty_desc}: {"Choose well-known classics" if difficulty < 0.4 else "Include more specific art knowledge" if difficulty < 0.7 else "Require deeper expertise in art history/theory"}
            
            Specific Requirements for Art Puzzles:
            - Question should test knowledge, not guessing
            - Answer must be factually correct and unambiguous  
            - Include context clues in the question when needed
            - Avoid questions requiring visual recognition of specific images (since no media is provided)
            - Focus on describable characteristics, historical facts, or well-known associations
            
            Respond in this exact JSON format:
            {{
                "question": "The puzzle question/prompt about art, music, film, or culture",
                "solution": "The exact correct answer (artist name, movement, technique, etc.)", 
                "explanation": "Clear explanation with context about why this is the answer",
                "hints": ["helpful clue 1", "helpful clue 2"],
                "media_url": null,
                "estimated_solve_time": {int(120 + (difficulty * 120))},
                "difficulty_justification": "Why this matches {difficulty_desc} - explain the knowledge level required"
            }}
            
            Generate a high-quality art puzzle now:
            """
        else:
            prompt = f"""
            You are an expert puzzle creator for "The Daily Puzzle" game. Generate a {category} puzzle with {difficulty_desc}.
            
            Context: {category_context}
            
            Requirements:
            - Create an engaging, fair puzzle appropriate for the difficulty level
            - Ensure there is exactly one correct answer
            - Make the puzzle solvable within 5 minutes for someone with appropriate skill level
            - Avoid culturally specific references that might confuse international users
            - For math: Show clear problem setup, avoid trick questions
            - For word: Ensure wordplay is clever but not obscure
            
            Respond in this exact JSON format:
            {{
                "question": "The puzzle question/prompt",
                "solution": "The exact correct answer", 
                "explanation": "Clear explanation of how to solve it",
                "hints": ["optional hint 1", "optional hint 2"],
                "media_url": null,
                "estimated_solve_time": 180,
                "difficulty_justification": "Why this matches the requested difficulty"
            }}
            
            Generate a high-quality puzzle now:
            """
        
        if constraints:
            prompt += f"\n\nAdditional Constraints: {json.dumps(constraints)}"
        
        return prompt
    
    async def _call_claude_api(self, prompt: str) -> str:
        """Make API call to Claude"""
        
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise PuzzleGenerationError(
                    f"Claude API error {response.status_code}: {response.text}"
                )
            
            response_data = response.json()
            return response_data["content"][0]["text"]
    
    def _parse_puzzle_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's response into puzzle data"""
        
        try:
            # Extract JSON from response (Claude sometimes adds extra text)
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            puzzle_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["question", "solution", "explanation"]
            for field in required_fields:
                if field not in puzzle_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set defaults for optional fields
            puzzle_data.setdefault("hints", [])
            puzzle_data.setdefault("media_url", None)
            puzzle_data.setdefault("estimated_solve_time", 180)
            
            return puzzle_data
            
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Failed to parse puzzle response: {response}")
            raise PuzzleGenerationError(f"Invalid response format: {str(e)}")
    
    def _generate_mock_puzzle(self, category: str, difficulty: float) -> Dict[str, Any]:
        """Generate a mock puzzle for development/testing"""
        
        mock_puzzles = {
            'math': {
                'question': 'If a train travels 60 miles in 45 minutes, what is its speed in miles per hour?',
                'solution': '80 mph',
                'explanation': 'Speed = Distance / Time. Convert 45 minutes to 0.75 hours: 60 miles / 0.75 hours = 80 mph'
            },
            'word': {
                'question': 'What 7-letter word becomes longer when the third letter is removed?',
                'solution': 'lounger',
                'explanation': 'Remove the "u" from "lounger" to get "longer"'
            },
            'art': {
                'question': 'Which famous painting technique creates the illusion of depth by making distant objects appear bluer and less distinct?',
                'solution': 'atmospheric perspective',
                'explanation': 'Atmospheric perspective mimics how the atmosphere affects our perception of distant objects'
            }
        }
        
        puzzle_template = mock_puzzles.get(category, mock_puzzles['math'])
        
        return {
            'question': puzzle_template['question'],
            'solution': puzzle_template['solution'],
            'explanation': puzzle_template['explanation'],
            'hints': ['Think step by step', 'Consider the key concepts'],
            'media_url': None,
            'estimated_solve_time': int(120 + (difficulty * 180)),  # 2-5 minutes based on difficulty
            'difficulty_justification': f'Mock puzzle at {difficulty} difficulty level'
        }
    
    def _generate_mock_validation(self, question: str, solution: str, category: str) -> Dict[str, Any]:
        """Generate mock validation results for development/testing"""
        
        return {
            'is_valid': True,
            'generated_solution': solution,
            'confidence': 0.85,
            'issues': [],
            'reasoning': f'Mock validation successful for {category} puzzle'
        }


# Synchronous wrapper for backwards compatibility
def generate_claude_puzzle(category: str, difficulty: float) -> Dict[str, Any]:
    """Synchronous wrapper for Claude puzzle generation"""
    
    generator = Claude4PuzzleGenerator()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(
            generator.generate_puzzle(category, difficulty)
        )
    finally:
        loop.close()


def validate_claude_puzzle(question: str, solution: str, category: str) -> Dict[str, Any]:
    """Synchronous wrapper for Claude puzzle validation"""
    
    generator = Claude4PuzzleGenerator()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(
            generator.validate_puzzle(question, solution, category)
        )
    finally:
        loop.close()