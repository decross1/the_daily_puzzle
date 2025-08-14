"""
Art Puzzle Validation Framework

Provides comprehensive validation metrics and quality assessment
specifically designed for art, culture, and creative puzzles.
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
import logging
from .difficulty_framework import ArtDifficultyFactors, KnowledgeDomain, CulturalScope

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    INFO = "info"
    WARNING = "warning" 
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ArtPuzzleValidation:
    """Comprehensive art puzzle validation results"""
    is_valid: bool
    overall_score: float  # 0.0-1.0
    issues: List[ValidationIssue]
    quality_metrics: Dict[str, float]
    difficulty_assessment: Dict[str, Any]
    cultural_accessibility: Dict[str, float]
    

class ArtPuzzleValidator:
    """Comprehensive validator for art puzzles"""
    
    def __init__(self):
        self.art_keywords = {
            'visual_arts': ['painting', 'sculpture', 'artist', 'canvas', 'brush', 'palette', 'style', 'technique'],
            'music': ['composer', 'symphony', 'opera', 'instrument', 'melody', 'harmony', 'tempo', 'genre'],
            'film': ['director', 'cinematography', 'screenplay', 'actor', 'genre', 'montage', 'scene'],
            'architecture': ['architect', 'building', 'style', 'structure', 'design', 'column', 'arch', 'blueprint'],
            'cultural': ['movement', 'period', 'influence', 'tradition', 'context', 'significance', 'impact']
        }
        
        # Known problematic terms that might be culturally specific or inappropriate
        self.cultural_flags = [
            'slang', 'colloquial', 'regional dialect', 'local custom', 'insider knowledge'
        ]
        
        # Quality indicators for art questions
        self.quality_indicators = {
            'descriptive_words': ['style', 'technique', 'period', 'movement', 'characteristics', 'known for'],
            'context_clues': ['famous for', 'characterized by', 'associated with', 'known to', 'typically'],
            'specificity_markers': ['specific', 'particular', 'exact', 'precise', 'exactly']
        }
    
    def validate_art_puzzle(
        self, 
        puzzle_data: Dict[str, Any], 
        difficulty_factors: ArtDifficultyFactors,
        target_difficulty: float
    ) -> ArtPuzzleValidation:
        """Comprehensive validation of an art puzzle"""
        
        issues = []
        quality_metrics = {}
        
        # Basic content validation
        content_issues, content_metrics = self._validate_content_quality(puzzle_data)
        issues.extend(content_issues)
        quality_metrics.update(content_metrics)
        
        # Difficulty alignment validation
        difficulty_issues, difficulty_assessment = self._validate_difficulty_alignment(
            puzzle_data, difficulty_factors, target_difficulty
        )
        issues.extend(difficulty_issues)
        
        # Cultural accessibility validation
        cultural_issues, cultural_metrics = self._validate_cultural_accessibility(puzzle_data)
        issues.extend(cultural_issues)
        
        # Art domain validation
        domain_issues, domain_metrics = self._validate_art_domain(puzzle_data)
        issues.extend(domain_issues)
        quality_metrics.update(domain_metrics)
        
        # Factual accuracy indicators
        accuracy_issues, accuracy_metrics = self._validate_factual_indicators(puzzle_data)
        issues.extend(accuracy_issues)
        quality_metrics.update(accuracy_metrics)
        
        # Calculate overall validation score
        overall_score = self._calculate_overall_score(issues, quality_metrics)
        is_valid = overall_score >= 0.7 and not any(issue.severity == ValidationSeverity.CRITICAL for issue in issues)
        
        return ArtPuzzleValidation(
            is_valid=is_valid,
            overall_score=overall_score,
            issues=issues,
            quality_metrics=quality_metrics,
            difficulty_assessment=difficulty_assessment,
            cultural_accessibility=cultural_metrics
        )
    
    def _validate_content_quality(self, puzzle_data: Dict[str, Any]) -> Tuple[List[ValidationIssue], Dict[str, float]]:
        """Validate basic content quality"""
        issues = []
        metrics = {}
        
        question = puzzle_data.get('question', '')
        solution = puzzle_data.get('solution', '')
        explanation = puzzle_data.get('explanation', '')
        
        # Question quality checks
        if len(question) < 20:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "content_length",
                "Question seems too short for art puzzle complexity",
                "Consider adding more context or descriptive details"
            ))
        
        if len(question) > 300:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "content_length", 
                "Question is very long and might be overwhelming",
                "Consider simplifying while maintaining necessary context"
            ))
        
        # Solution quality checks  
        if len(solution.strip()) == 0:
            issues.append(ValidationIssue(
                ValidationSeverity.CRITICAL,
                "solution_missing",
                "Solution cannot be empty"
            ))
        
        if len(solution.split()) > 10:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "solution_length",
                "Solution is quite long - art answers should typically be concise",
                "Consider if a shorter, more specific answer is possible"
            ))
        
        # Explanation quality
        if len(explanation) < 30:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "explanation_brief",
                "Explanation seems brief for an art puzzle",
                "Consider adding historical context or additional details"
            ))
        
        # Calculate quality metrics
        metrics['question_length_score'] = min(1.0, max(0.0, (len(question) - 20) / 200))
        metrics['explanation_depth_score'] = min(1.0, len(explanation) / 200)
        metrics['solution_specificity_score'] = 1.0 if 1 <= len(solution.split()) <= 5 else 0.5
        
        return issues, metrics
    
    def _validate_difficulty_alignment(
        self, 
        puzzle_data: Dict[str, Any], 
        difficulty_factors: ArtDifficultyFactors,
        target_difficulty: float
    ) -> Tuple[List[ValidationIssue], Dict[str, Any]]:
        """Validate that puzzle aligns with intended difficulty"""
        issues = []
        assessment = {
            'target_difficulty': target_difficulty,
            'calculated_difficulty': difficulty_factors.calculate_composite_difficulty(),
            'factors': {
                'knowledge_domain': difficulty_factors.knowledge_domain.value,
                'cultural_scope': difficulty_factors.cultural_scope.value,
                'cognitive_load': difficulty_factors.cognitive_load.value
            }
        }
        
        question = puzzle_data.get('question', '').lower()
        calculated_difficulty = difficulty_factors.calculate_composite_difficulty()
        
        # Check difficulty calibration
        difficulty_delta = abs(calculated_difficulty - target_difficulty)
        if difficulty_delta > 0.2:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "difficulty_mismatch",
                f"Calculated difficulty ({calculated_difficulty:.2f}) differs significantly from target ({target_difficulty:.2f})",
                "Review difficulty factors or adjust question complexity"
            ))
        
        # Domain-specific difficulty indicators
        if difficulty_factors.knowledge_domain == KnowledgeDomain.UNIVERSAL:
            if not any(famous in question for famous in ['famous', 'well-known', 'renowned', 'celebrated']):
                issues.append(ValidationIssue(
                    ValidationSeverity.INFO,
                    "universal_domain",
                    "Universal difficulty should reference well-known subjects",
                    "Consider adding context about fame/recognition"
                ))
        
        elif difficulty_factors.knowledge_domain == KnowledgeDomain.EXPERT:
            if any(basic in question for basic in ['famous', 'popular', 'well-known']):
                issues.append(ValidationIssue(
                    ValidationSeverity.WARNING,
                    "expert_domain",
                    "Expert difficulty shouldn't rely on popular knowledge",
                    "Focus on specialized techniques, theories, or lesser-known aspects"
                ))
        
        return issues, assessment
    
    def _validate_cultural_accessibility(self, puzzle_data: Dict[str, Any]) -> Tuple[List[ValidationIssue], Dict[str, float]]:
        """Validate cultural accessibility and inclusivity"""
        issues = []
        metrics = {}
        
        question = puzzle_data.get('question', '').lower()
        explanation = puzzle_data.get('explanation', '').lower()
        full_text = f"{question} {explanation}".lower()
        
        # Check for cultural flags
        cultural_flag_count = sum(1 for flag in self.cultural_flags if flag in full_text)
        if cultural_flag_count > 0:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "cultural_specificity",
                f"Found {cultural_flag_count} potentially culture-specific references",
                "Ensure international accessibility or provide context"
            ))
        
        # Check for region-specific references
        regional_indicators = ['american', 'european', 'asian', 'local', 'regional', 'native']
        regional_count = sum(1 for indicator in regional_indicators if indicator in full_text)
        
        # Assess accessibility score
        accessibility_score = 1.0 - (cultural_flag_count * 0.2) - (regional_count * 0.1)
        metrics['cultural_accessibility'] = max(0.0, accessibility_score)
        
        # Language complexity check
        complex_words = ['subsequently', 'consequently', 'furthermore', 'nevertheless', 'contemporaneous']
        complexity_count = sum(1 for word in complex_words if word in full_text)
        metrics['language_accessibility'] = max(0.0, 1.0 - complexity_count * 0.15)
        
        return issues, metrics
    
    def _validate_art_domain(self, puzzle_data: Dict[str, Any]) -> Tuple[List[ValidationIssue], Dict[str, float]]:
        """Validate that puzzle is appropriately art-focused"""
        issues = []
        metrics = {}
        
        question = puzzle_data.get('question', '').lower()
        explanation = puzzle_data.get('explanation', '').lower()
        full_text = f"{question} {explanation}".lower()
        
        # Check for art domain keywords
        domain_scores = {}
        for domain, keywords in self.art_keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword in full_text)
            domain_scores[domain] = keyword_count
        
        total_art_keywords = sum(domain_scores.values())
        if total_art_keywords == 0:
            issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "art_domain_missing",
                "Puzzle doesn't contain clear art domain keywords",
                "Ensure question clearly relates to art, music, film, or culture"
            ))
        
        # Identify primary domain
        primary_domain = max(domain_scores, key=domain_scores.get) if domain_scores else None
        metrics['art_domain_strength'] = min(1.0, total_art_keywords / 3)
        metrics['domain_focus'] = domain_scores.get(primary_domain, 0) / max(1, total_art_keywords)
        
        # Check for context clues
        context_clue_count = sum(1 for clue_set in self.quality_indicators.values() 
                                for clue in clue_set if clue in full_text)
        metrics['context_richness'] = min(1.0, context_clue_count / 3)
        
        return issues, metrics
    
    def _validate_factual_indicators(self, puzzle_data: Dict[str, Any]) -> Tuple[List[ValidationIssue], Dict[str, float]]:
        """Validate indicators of factual accuracy and verifiability"""
        issues = []
        metrics = {}
        
        question = puzzle_data.get('question', '')
        solution = puzzle_data.get('solution', '')
        explanation = puzzle_data.get('explanation', '')
        
        # Check for vague or subjective language
        subjective_words = ['probably', 'might be', 'could be', 'seems like', 'appears to']
        subjective_count = sum(1 for word in subjective_words 
                             if word in f"{question} {solution} {explanation}".lower())
        
        if subjective_count > 0:
            issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                "subjective_language",
                f"Found {subjective_count} instances of uncertain language",
                "Art puzzles should have definitive, verifiable answers"
            ))
        
        # Check for specific dates, names, or concrete facts
        has_proper_nouns = bool(re.search(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', solution))
        has_dates = bool(re.search(r'\b\d{4}\b|\b\d{1,2}th\s+century\b', f"{question} {explanation}"))
        has_specific_terms = any(term in explanation.lower() for term in 
                               ['technique', 'style', 'movement', 'period', 'school', 'method'])
        
        factual_indicators = sum([has_proper_nouns, has_dates, has_specific_terms])
        metrics['factual_specificity'] = factual_indicators / 3
        
        # Verifiability indicators
        verification_terms = ['encyclopedia', 'documented', 'recorded', 'established', 'recognized']
        verification_score = sum(1 for term in verification_terms 
                               if term in explanation.lower()) / len(verification_terms)
        metrics['verifiability_indicators'] = verification_score
        
        return issues, metrics
    
    def _calculate_overall_score(self, issues: List[ValidationIssue], quality_metrics: Dict[str, float]) -> float:
        """Calculate overall validation score"""
        
        # Start with base score from quality metrics
        base_score = sum(quality_metrics.values()) / max(1, len(quality_metrics))
        
        # Apply penalties for issues
        penalties = {
            ValidationSeverity.INFO: 0.05,
            ValidationSeverity.WARNING: 0.15,
            ValidationSeverity.ERROR: 0.3,
            ValidationSeverity.CRITICAL: 0.5
        }
        
        total_penalty = sum(penalties.get(issue.severity, 0) for issue in issues)
        final_score = max(0.0, base_score - total_penalty)
        
        return round(final_score, 3)
    
    def generate_validation_report(self, validation: ArtPuzzleValidation) -> str:
        """Generate human-readable validation report"""
        
        report = f"""
Art Puzzle Validation Report
===========================

Overall Score: {validation.overall_score:.2f}/1.00
Status: {'✅ VALID' if validation.is_valid else '❌ NEEDS IMPROVEMENT'}

Quality Metrics:
{'-' * 40}
"""
        
        for metric, score in validation.quality_metrics.items():
            status = "✅" if score >= 0.7 else "⚠️" if score >= 0.5 else "❌"
            report += f"{status} {metric.replace('_', ' ').title()}: {score:.2f}\n"
        
        if validation.issues:
            report += f"\nIssues Found ({len(validation.issues)}):\n{'-' * 40}\n"
            for issue in validation.issues:
                severity_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "critical": "🚨"}
                icon = severity_icon.get(issue.severity.value, "❓")
                report += f"{icon} {issue.severity.value.upper()}: {issue.message}\n"
                if issue.suggestion:
                    report += f"   💡 Suggestion: {issue.suggestion}\n"
                report += "\n"
        
        report += f"""
Difficulty Assessment:
{'-' * 40}
Target: {validation.difficulty_assessment['target_difficulty']:.2f}
Calculated: {validation.difficulty_assessment['calculated_difficulty']:.2f}
Domain: {validation.difficulty_assessment['factors']['knowledge_domain']}
Scope: {validation.difficulty_assessment['factors']['cultural_scope']}

Cultural Accessibility:
{'-' * 40}
Accessibility Score: {validation.cultural_accessibility.get('cultural_accessibility', 0):.2f}
Language Score: {validation.cultural_accessibility.get('language_accessibility', 0):.2f}
"""
        
        return report