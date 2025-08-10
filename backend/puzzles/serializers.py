from rest_framework import serializers
from .models import Puzzle, PlayerProgress, StumpTally, DifficultyHistory

class PuzzleSerializer(serializers.ModelSerializer):
    """Serializer for Puzzle model"""
    difficulty_band = serializers.SerializerMethodField()
    solve_rate = serializers.ReadOnlyField()
    question = serializers.SerializerMethodField()
    hints = serializers.SerializerMethodField()
    media_url = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = Puzzle
        fields = [
            'id', 'date', 'category', 'difficulty', 'difficulty_band',
            'question', 'hints', 'media_url', 'total_attempts', 'successful_solves', 
            'solve_rate', 'generator_model', 'created_at'
        ]
        # Don't expose the solution or validator_results in the API!
    
    def get_difficulty_band(self, obj):
        """Calculate difficulty band from difficulty value"""
        if obj.difficulty < 0.4:
            return 'Mini'
        elif obj.difficulty < 0.7:
            return 'Mid'
        else:
            return 'Beast'
    
    def get_question(self, obj):
        """Extract question from puzzle_content JSON"""
        return obj.puzzle_content.get('question', '') if obj.puzzle_content else ''
    
    def get_hints(self, obj):
        """Extract hints from puzzle_content JSON"""
        return obj.puzzle_content.get('hints', []) if obj.puzzle_content else []
    
    def get_media_url(self, obj):
        """Extract media URL from puzzle_content JSON"""
        return obj.puzzle_content.get('media_url') if obj.puzzle_content else None
        
    def get_date(self, obj):
        """Extract date from puzzle ID (format: YYYY-MM-DD)"""
        return obj.id  # The ID is the date string


class PlayerProgressSerializer(serializers.ModelSerializer):
    """Serializer for PlayerProgress model (adapted from PuzzleAttemptSerializer)"""
    username = serializers.CharField(source='user.username', read_only=True)
    puzzle_id = serializers.CharField(source='puzzle.id', read_only=True)
    
    class Meta:
        model = PlayerProgress
        fields = [
            'id', 'username', 'puzzle_id', 'solved', 
            'solve_time', 'attempts', 'solved_at'
        ]


class PlayerStatsSerializer(serializers.ModelSerializer):
    """Serializer for aggregated player statistics"""
    username = serializers.CharField(read_only=True)
    solve_rate = serializers.SerializerMethodField()
    
    # Since we don't have a PlayerStats model yet, this will be used for computed stats
    total_solved = serializers.IntegerField(read_only=True)
    total_attempts = serializers.IntegerField(read_only=True)
    fastest_solve = serializers.IntegerField(read_only=True, allow_null=True)
    avg_solve_time = serializers.FloatField(read_only=True, allow_null=True)
    math_solved = serializers.IntegerField(read_only=True)
    word_solved = serializers.IntegerField(read_only=True)
    art_solved = serializers.IntegerField(read_only=True)
    current_streak = serializers.IntegerField(read_only=True)
    longest_streak = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = None  # This is for computed data, not a specific model
        fields = [
            'username', 'current_streak', 'longest_streak', 
            'total_solved', 'total_attempts', 'solve_rate',
            'fastest_solve', 'avg_solve_time', 'math_solved', 'word_solved', 'art_solved'
        ]
    
    def get_solve_rate(self, obj):
        """Calculate solve rate from total stats"""
        if hasattr(obj, 'total_attempts') and obj.get('total_attempts', 0) > 0:
            return obj.get('total_solved', 0) / obj.get('total_attempts', 1)
        return 0


class StumpTallySerializer(serializers.ModelSerializer):
    """Serializer for StumpTally model"""
    stump_rate = serializers.ReadOnlyField()
    model_name = serializers.CharField(source='ai_model', read_only=True)
    puzzles_generated = serializers.IntegerField(source='total_generated', read_only=True)
    times_stumped_community = serializers.IntegerField(source='successful_stumps', read_only=True)
    
    class Meta:
        model = StumpTally
        fields = [
            'model_name', 'category', 'puzzles_generated', 'times_stumped_community',
            'stump_rate', 'last_updated'
        ]


class DifficultyHistorySerializer(serializers.ModelSerializer):
    """Serializer for DifficultyHistory model (adapted from DifficultySettingsSerializer)"""
    current_difficulty = serializers.FloatField(source='difficulty', read_only=True)
    last_updated = serializers.DateTimeField(source='date', read_only=True)
    
    class Meta:
        model = DifficultyHistory
        fields = [
            'category', 'current_difficulty', 'previous_difficulty', 
            'adjustment_reason', 'last_updated'
        ]


# Additional serializers for API responses

class LeaderboardEntrySerializer(serializers.Serializer):
    """Serializer for leaderboard entries"""
    username = serializers.CharField()
    rank = serializers.IntegerField()
    solve_time = serializers.IntegerField(allow_null=True)
    attempts = serializers.IntegerField(required=False)
    total_solved = serializers.IntegerField(required=False)
    avg_solve_time = serializers.FloatField(allow_null=True, required=False)


class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard response"""
    daily_leaderboard = LeaderboardEntrySerializer(many=True)
    all_time_leaderboard = LeaderboardEntrySerializer(many=True)


class PuzzleStatsSerializer(serializers.Serializer):
    """Serializer for overall puzzle statistics"""
    total_puzzles = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    total_solves = serializers.IntegerField()
    overall_solve_rate = serializers.FloatField()
    category_stats = serializers.DictField()


class PuzzleSubmissionSerializer(serializers.Serializer):
    """Serializer for puzzle answer submissions"""
    answer = serializers.CharField(max_length=1000, required=True)
    solve_time = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    
    def validate_answer(self, value):
        """Validate answer is not empty after stripping"""
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty")
        return value.strip()


class PuzzleSubmissionResponseSerializer(serializers.Serializer):
    """Serializer for puzzle submission responses"""
    is_correct = serializers.BooleanField()
    attempts = serializers.IntegerField()
    solved = serializers.BooleanField()
    solve_time = serializers.IntegerField(allow_null=True)
    message = serializers.CharField()


class PuzzleGenerationRequestSerializer(serializers.Serializer):
    """Serializer for manual puzzle generation requests"""
    category = serializers.ChoiceField(
        choices=['math', 'word', 'art'],
        default='math'
    )
    difficulty = serializers.FloatField(
        min_value=0.0, 
        max_value=1.0, 
        default=0.5
    )