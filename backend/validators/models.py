from django.db import models


class ValidationResult(models.Model):
    puzzle_id = models.CharField(max_length=20)
    ai_model = models.CharField(max_length=20)
    success = models.BooleanField()
    response = models.TextField()
    processing_time = models.FloatField()  # seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('puzzle_id', 'ai_model')
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.ai_model} - {self.puzzle_id} ({status})"