"""
Enhanced Difficulty Measurement Framework for AI Puzzle Generation

This module provides sophisticated difficulty measurement and calibration
specifically designed for art, culture, and creative puzzles.
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class KnowledgeDomain(Enum):
    """Art knowledge domains by accessibility"""
    UNIVERSAL = "universal"  # Leonardo da Vinci, Mona Lisa
    MAINSTREAM = "mainstream"  # Van Gogh, Picasso, Beatles
    EDUCATED = "educated"  # Art movements, classical composers
    SPECIALIZED = "specialized"  # Specific techniques, regional artists
    EXPERT = "expert"  # Art theory, obscure periods


class CulturalScope(Enum):
    """Cultural specificity of knowledge required"""
    GLOBAL = "global"  # Universally known
    WESTERN = "western"  # Western art tradition
    REGIONAL = "regional"  # Specific cultural region
    NICHE = "niche"  # Subculture or specialized knowledge


class CognitiveLoad(Enum):
    """Mental processing complexity"""
    RECOGNITION = "recognition"  # "Who painted this?"
    ANALYSIS = "analysis"  # "What technique is used?"
    SYNTHESIS = "synthesis"  # "How do these styles relate?"
    EVALUATION = "evaluation"  # "Why is this historically significant?"


@dataclass
class ArtDifficultyFactors:
    """Comprehensive difficulty factors for art puzzles"""
    knowledge_domain: KnowledgeDomain
    cultural_scope: CulturalScope
    cognitive_load: CognitiveLoad
    time_period_obscurity: float  # 0.0 (Renaissance) to 1.0 (obscure periods)
    technical_specificity: float  # 0.0 (general) to 1.0 (highly technical)
    interdisciplinary_complexity: float  # 0.0 (pure art) to 1.0 (multiple domains)
    
    def calculate_composite_difficulty(self) -> float:
        """Calculate weighted composite difficulty score (0.0-1.0)"""
        
        # Domain difficulty mapping
        domain_weights = {
            KnowledgeDomain.UNIVERSAL: 0.1,
            KnowledgeDomain.MAINSTREAM: 0.3,
            KnowledgeDomain.EDUCATED: 0.5,
            KnowledgeDomain.SPECIALIZED: 0.7,
            KnowledgeDomain.EXPERT: 0.9
        }
        
        # Cultural scope difficulty
        scope_weights = {
            CulturalScope.GLOBAL: 0.0,
            CulturalScope.WESTERN: 0.2,
            CulturalScope.REGIONAL: 0.4,
            CulturalScope.NICHE: 0.6
        }
        
        # Cognitive load difficulty
        cognitive_weights = {
            CognitiveLoad.RECOGNITION: 0.2,
            CognitiveLoad.ANALYSIS: 0.4,
            CognitiveLoad.SYNTHESIS: 0.6,
            CognitiveLoad.EVALUATION: 0.8
        }
        
        # Weighted combination
        base_difficulty = (
            domain_weights[self.knowledge_domain] * 0.4 +
            scope_weights[self.cultural_scope] * 0.2 +
            cognitive_weights[self.cognitive_load] * 0.3 +
            self.time_period_obscurity * 0.1
        )
        
        # Apply technical and interdisciplinary modifiers
        technical_modifier = 1.0 + (self.technical_specificity * 0.3)
        interdisciplinary_modifier = 1.0 + (self.interdisciplinary_complexity * 0.2)
        
        final_difficulty = min(1.0, base_difficulty * technical_modifier * interdisciplinary_modifier)
        
        return round(final_difficulty, 3)


class ArtDifficultyCalibrator:
    """Calibrates difficulty based on target difficulty and historical performance"""
    
    def __init__(self):
        self.performance_data = {}  # Could be loaded from database
        
    def generate_difficulty_factors(self, target_difficulty: float, constraints: Dict[str, Any] = None) -> ArtDifficultyFactors:
        """Generate appropriate difficulty factors for target difficulty level"""
        
        constraints = constraints or {}
        
        # Define difficulty thresholds
        if target_difficulty < 0.25:  # Mini Easy
            return ArtDifficultyFactors(
                knowledge_domain=KnowledgeDomain.UNIVERSAL,
                cultural_scope=CulturalScope.GLOBAL,
                cognitive_load=CognitiveLoad.RECOGNITION,
                time_period_obscurity=0.0,
                technical_specificity=0.1,
                interdisciplinary_complexity=0.0
            )
        elif target_difficulty < 0.45:  # Mini Hard
            return ArtDifficultyFactors(
                knowledge_domain=KnowledgeDomain.MAINSTREAM,
                cultural_scope=CulturalScope.GLOBAL,
                cognitive_load=CognitiveLoad.RECOGNITION,
                time_period_obscurity=0.2,
                technical_specificity=0.2,
                interdisciplinary_complexity=0.1
            )
        elif target_difficulty < 0.65:  # Mid Easy
            return ArtDifficultyFactors(
                knowledge_domain=KnowledgeDomain.EDUCATED,
                cultural_scope=CulturalScope.WESTERN,
                cognitive_load=CognitiveLoad.ANALYSIS,
                time_period_obscurity=0.4,
                technical_specificity=0.4,
                interdisciplinary_complexity=0.3
            )
        elif target_difficulty < 0.8:  # Mid Hard
            return ArtDifficultyFactors(
                knowledge_domain=KnowledgeDomain.SPECIALIZED,
                cultural_scope=CulturalScope.REGIONAL,
                cognitive_load=CognitiveLoad.SYNTHESIS,
                time_period_obscurity=0.6,
                technical_specificity=0.6,
                interdisciplinary_complexity=0.5
            )
        else:  # Beast
            return ArtDifficultyFactors(
                knowledge_domain=KnowledgeDomain.EXPERT,
                cultural_scope=CulturalScope.NICHE,
                cognitive_load=CognitiveLoad.EVALUATION,
                time_period_obscurity=0.8,
                technical_specificity=0.8,
                interdisciplinary_complexity=0.7
            )
    
    def validate_difficulty_match(self, factors: ArtDifficultyFactors, target_difficulty: float, tolerance: float = 0.15) -> bool:
        """Validate that generated factors produce difficulty within tolerance of target"""
        calculated_difficulty = factors.calculate_composite_difficulty()
        return abs(calculated_difficulty - target_difficulty) <= tolerance
    
    def adjust_for_performance(self, factors: ArtDifficultyFactors, solve_rate: float) -> ArtDifficultyFactors:
        """Adjust difficulty factors based on community solve rate feedback"""
        
        # Target solve rate: 45-55% for optimal engagement
        if solve_rate > 0.7:  # Too easy, increase difficulty
            adjustment_factor = 1.2
        elif solve_rate < 0.3:  # Too hard, decrease difficulty
            adjustment_factor = 0.8
        else:
            return factors  # Within acceptable range
        
        # Apply adjustments while maintaining enum constraints
        new_factors = ArtDifficultyFactors(
            knowledge_domain=factors.knowledge_domain,
            cultural_scope=factors.cultural_scope,
            cognitive_load=factors.cognitive_load,
            time_period_obscurity=min(1.0, factors.time_period_obscurity * adjustment_factor),
            technical_specificity=min(1.0, factors.technical_specificity * adjustment_factor),
            interdisciplinary_complexity=min(1.0, factors.interdisciplinary_complexity * adjustment_factor)
        )
        
        logger.info(f"Adjusted difficulty factors based on solve rate {solve_rate:.2f}")
        return new_factors


class DynamicPromptBuilder:
    """Builds dynamic prompts based on difficulty factors and context"""
    
    def __init__(self):
        self.art_domains = {
            "visual_arts": ["painting", "sculpture", "photography", "printmaking"],
            "music": ["classical", "popular", "jazz", "world_music", "composition"],
            "film": ["directors", "cinematography", "film_movements", "genre_theory"],
            "architecture": ["styles", "architects", "structural_elements", "periods"],
            "cultural": ["art_movements", "cultural_context", "patronage", "influence"]
        }
        
        self.difficulty_templates = {
            "recognition": {
                "easy": "Who {action} this famous {item}?",
                "medium": "Which {creator_type} is known for {specific_trait}?",
                "hard": "Identify the {creator_type} of this {description}"
            },
            "analysis": {
                "easy": "What {technique} is primarily used in {context}?",
                "medium": "Which {movement} emphasized {characteristics}?",
                "hard": "Analyze the {aspect} that distinguishes {comparison}"
            },
            "synthesis": {
                "easy": "How do {element1} and {element2} relate in {context}?",
                "medium": "What connection exists between {concept1} and {concept2}?",
                "hard": "Synthesize the relationship between {complex_concept1} and {complex_concept2}"
            }
        }
    
    def build_art_prompt(self, factors: ArtDifficultyFactors, category_constraints: Dict[str, Any] = None) -> str:
        """Build sophisticated prompt for art puzzle generation"""
        
        category_constraints = category_constraints or {}
        target_difficulty = factors.calculate_composite_difficulty()
        
        # Knowledge domain context
        domain_context = self._get_domain_context(factors.knowledge_domain)
        
        # Cultural scope guidelines
        scope_guidelines = self._get_scope_guidelines(factors.cultural_scope)
        
        # Cognitive load instructions
        cognitive_instructions = self._get_cognitive_instructions(factors.cognitive_load)
        
        # Time period context
        period_context = self._get_period_context(factors.time_period_obscurity)
        
        # Technical specificity requirements
        technical_reqs = self._get_technical_requirements(factors.technical_specificity)
        
        # Build comprehensive prompt
        prompt = f"""
        You are an expert art puzzle creator for "The Daily Puzzle" game. Generate a sophisticated art puzzle with precise difficulty calibration.

        DIFFICULTY SPECIFICATION:
        - Target Difficulty: {target_difficulty:.3f} (on 0.0-1.0 scale)
        - Knowledge Domain: {factors.knowledge_domain.value} 
        - Cultural Scope: {factors.cultural_scope.value}
        - Cognitive Load: {factors.cognitive_load.value}
        - Time Period Obscurity: {factors.time_period_obscurity:.2f}
        - Technical Specificity: {factors.technical_specificity:.2f}
        - Interdisciplinary Complexity: {factors.interdisciplinary_complexity:.2f}

        CONTENT GUIDELINES:
        {domain_context}
        
        {scope_guidelines}
        
        {cognitive_instructions}
        
        {period_context}
        
        {technical_reqs}

        QUALITY REQUIREMENTS:
        - Ensure factual accuracy and verifiable answers
        - Avoid visual recognition requiring specific images
        - Focus on describable characteristics, historical facts, or well-known associations
        - Include sufficient context clues for fair solving
        - Balance challenge with solvability for the target difficulty

        DIFFICULTY VALIDATION:
        The puzzle should be solvable by approximately {self._estimate_solve_percentage(target_difficulty):.0f}% of players familiar with art.
        Estimated solve time: {self._estimate_solve_time(target_difficulty)} minutes.

        Respond in this exact JSON format:
        {{
            "question": "The sophisticated art puzzle question",
            "solution": "The precise correct answer",
            "explanation": "Detailed explanation including artistic/cultural context",
            "hints": ["strategic hint 1", "strategic hint 2"],
            "media_url": null,
            "estimated_solve_time": {self._estimate_solve_time(target_difficulty) * 60},
            "difficulty_justification": "Detailed analysis of why this matches the difficulty factors",
            "knowledge_verification": "How to verify this answer (sources, references)",
            "cultural_considerations": "Any cultural context important for understanding"
        }}

        Generate the art puzzle now:
        """
        
        return prompt.strip()
    
    def _get_domain_context(self, domain: KnowledgeDomain) -> str:
        """Get context based on knowledge domain"""
        contexts = {
            KnowledgeDomain.UNIVERSAL: "Focus on globally recognized masterpieces and artists known worldwide (Da Vinci, Picasso, etc.)",
            KnowledgeDomain.MAINSTREAM: "Include well-known artists and works familiar to educated audiences (Van Gogh, Impressionism, etc.)",
            KnowledgeDomain.EDUCATED: "Draw from art history knowledge expected of college-educated individuals (specific movements, techniques)",
            KnowledgeDomain.SPECIALIZED: "Require specialized knowledge of specific periods, regional traditions, or technical aspects",
            KnowledgeDomain.EXPERT: "Demand expert-level knowledge of art theory, obscure periods, or highly specialized techniques"
        }
        return f"Knowledge Domain: {contexts[domain]}"
    
    def _get_scope_guidelines(self, scope: CulturalScope) -> str:
        """Get cultural scope guidelines"""
        guidelines = {
            CulturalScope.GLOBAL: "Use universally recognized cultural references accessible to international audiences",
            CulturalScope.WESTERN: "Focus on Western art traditions but ensure broad accessibility within that tradition",
            CulturalScope.REGIONAL: "May include region-specific knowledge (European, Asian, etc.) with context provided",
            CulturalScope.NICHE: "Can reference specialized cultural knowledge with appropriate background context"
        }
        return f"Cultural Scope: {guidelines[scope]}"
    
    def _get_cognitive_instructions(self, load: CognitiveLoad) -> str:
        """Get cognitive load instructions"""
        instructions = {
            CognitiveLoad.RECOGNITION: "Create identification/recognition questions requiring factual recall",
            CognitiveLoad.ANALYSIS: "Require analysis of techniques, styles, or characteristics",
            CognitiveLoad.SYNTHESIS: "Demand synthesis of multiple concepts or comparison of elements",
            CognitiveLoad.EVALUATION: "Require evaluation of significance, influence, or artistic merit"
        }
        return f"Cognitive Requirement: {instructions[load]}"
    
    def _get_period_context(self, obscurity: float) -> str:
        """Get time period context based on obscurity level"""
        if obscurity < 0.3:
            return "Time Period: Focus on well-known periods (Renaissance, Impressionism, Classical, etc.)"
        elif obscurity < 0.6:
            return "Time Period: Include moderately known periods with some context provided"
        else:
            return "Time Period: May reference lesser-known periods but provide sufficient historical context"
    
    def _get_technical_requirements(self, specificity: float) -> str:
        """Get technical specificity requirements"""
        if specificity < 0.3:
            return "Technical Level: Use general art terminology accessible to educated audiences"
        elif specificity < 0.6:
            return "Technical Level: Include specific techniques or terminology with context provided"
        else:
            return "Technical Level: May use specialized terminology but ensure clarity and context"
    
    def _estimate_solve_percentage(self, difficulty: float) -> float:
        """Estimate percentage of target audience that should solve this"""
        # Exponential decay: easier puzzles solved by more people
        return 75 * (1 - difficulty) + 25
    
    def _estimate_solve_time(self, difficulty: float) -> int:
        """Estimate solve time in minutes"""
        return max(2, int(2 + difficulty * 6))  # 2-8 minutes based on difficulty