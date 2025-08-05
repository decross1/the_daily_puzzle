from django.contrib import admin
from .models import Puzzle, DifficultyHistory, PlayerProgress, StumpTally


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'generator_model', 'difficulty', 'solve_rate', 'is_active')
    list_filter = ('category', 'generator_model', 'is_active', 'created_at')
    search_fields = ('id', 'puzzle_content')
    readonly_fields = ('created_at', 'solve_rate')
    
    def solve_rate(self, obj):
        return f"{obj.solve_rate:.2%}"
    solve_rate.short_description = 'Solve Rate'


@admin.register(DifficultyHistory)
class DifficultyHistoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'date', 'difficulty', 'previous_difficulty', 'adjustment_reason')
    list_filter = ('category', 'date')
    ordering = ('-date',)


@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'puzzle', 'solved', 'attempts', 'solve_time', 'solved_at')
    list_filter = ('solved', 'puzzle__category', 'solved_at')
    search_fields = ('user__username', 'puzzle__id')


@admin.register(StumpTally)
class StumpTallyAdmin(admin.ModelAdmin):
    list_display = ('ai_model', 'category', 'successful_stumps', 'total_generated', 'stump_rate')
    list_filter = ('ai_model', 'category')
    
    def stump_rate(self, obj):
        return f"{obj.stump_rate:.2%}"
    stump_rate.short_description = 'Stump Rate'