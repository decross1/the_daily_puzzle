from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Puzzle(models.Model):
    CATEGORY_CHOICES = [
        ('math', 'Math'),
        ('word', 'Word'),
        ('art', 'Art'),
    ]
    
    AI_MODEL_CHOICES = [
        ('gpt4o', 'GPT-4o'),
        ('claude3', 'Claude 3'),
        ('gemini', 'Gemini'),
    ]

    id = models.CharField(max_length=20, primary_key=True)  # Format: 2025-08-03
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    difficulty = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    generator_model = models.CharField(max_length=20, choices=AI_MODEL_CHOICES)
    
    # Puzzle content stored as JSON
    puzzle_content = models.JSONField()
    solution = models.TextField()
    generator_solution = models.TextField()
    
    # Validation results from all AI models
    validator_results = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Community solve statistics
    total_attempts = models.IntegerField(default=0)
    successful_solves = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Puzzle {self.id} - {self.category} by {self.generator_model}"
    
    @property
    def solve_rate(self):
        if self.total_attempts == 0:
            return 0
        return self.successful_solves / self.total_attempts
    
    @property
    def puzzle_question(self):
        return self.puzzle_content.get('question', '')
    
    @property
    def media_url(self):
        return self.puzzle_content.get('media_url')


class DifficultyHistory(models.Model):
    category = models.CharField(max_length=10, choices=Puzzle.CATEGORY_CHOICES)
    date = models.DateField()
    difficulty = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    previous_difficulty = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    adjustment_reason = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('category', 'date')
        ordering = ['-date']


class PlayerProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    solve_time = models.IntegerField(null=True, blank=True)  # seconds
    attempts = models.IntegerField(default=0)
    solved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'puzzle')
    
    def __str__(self):
        status = "Solved" if self.solved else "Attempted"
        return f"{self.user.username} - {self.puzzle.id} ({status})"


class StumpTally(models.Model):
    ai_model = models.CharField(max_length=20, choices=Puzzle.AI_MODEL_CHOICES)
    category = models.CharField(max_length=10, choices=Puzzle.CATEGORY_CHOICES)
    successful_stumps = models.IntegerField(default=0)
    total_generated = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('ai_model', 'category')
    
    def __str__(self):
        return f"{self.ai_model} - {self.category}: {self.successful_stumps}/{self.total_generated}"
    
    @property
    def stump_rate(self):
        if self.total_generated == 0:
            return 0
        return self.successful_stumps / self.total_generated