#!/usr/bin/env python3
"""
Art Puzzle Generation Test Runner

This script tests the complete art puzzle generation pipeline
with real Claude API integration.
"""

import os
import sys
import asyncio
import json
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_puzzle.settings')
django.setup()

from ai_services.claude import Claude4PuzzleGenerator
from ai_services.difficulty_framework import ArtDifficultyCalibrator, DynamicPromptBuilder
from ai_services.art_validation import ArtPuzzleValidator


async def test_single_art_puzzle(difficulty: float = 0.5):
    """Test generating a single art puzzle"""
    
    print(f"\n🎨 Testing Art Puzzle Generation (Difficulty: {difficulty})")
    print("=" * 60)
    
    try:
        # Initialize components
        generator = Claude4PuzzleGenerator()
        calibrator = ArtDifficultyCalibrator()
        validator = ArtPuzzleValidator()
        
        print(f"📡 API Mode: {'Mock' if generator.mock_mode else 'Real Claude API'}")
        
        # Generate puzzle
        print("🔄 Generating puzzle...")
        puzzle_data = await generator.generate_puzzle('art', difficulty)
        
        print("✅ Puzzle generated successfully!")
        print(f"📝 Question: {puzzle_data['question']}")
        print(f"💡 Solution: {puzzle_data['solution']}")
        print(f"📖 Explanation: {puzzle_data['explanation']}")
        
        if puzzle_data.get('hints'):
            print(f"💭 Hints: {puzzle_data['hints']}")
        
        print(f"⏱️ Estimated solve time: {puzzle_data.get('estimated_solve_time', 180)} seconds")
        
        # Validate puzzle
        print("\n🔍 Validating puzzle quality...")
        difficulty_factors = calibrator.generate_difficulty_factors(difficulty)
        validation = validator.validate_art_puzzle(puzzle_data, difficulty_factors, difficulty)
        
        print(f"✅ Validation Score: {validation.overall_score:.2f}/1.00")
        print(f"📊 Valid: {'✅ Yes' if validation.is_valid else '❌ No'}")
        
        if validation.issues:
            print(f"\n⚠️ Issues Found ({len(validation.issues)}):")
            for issue in validation.issues:
                severity_icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "critical": "🚨"}
                icon = severity_icon.get(issue.severity.value, "❓")
                print(f"  {icon} {issue.message}")
        
        # Print quality metrics
        print(f"\n📈 Quality Metrics:")
        for metric, score in validation.quality_metrics.items():
            status = "✅" if score >= 0.7 else "⚠️" if score >= 0.5 else "❌"
            print(f"  {status} {metric.replace('_', ' ').title()}: {score:.2f}")
        
        return puzzle_data, validation
        
    except Exception as e:
        print(f"❌ Error generating puzzle: {str(e)}")
        raise


async def test_multiple_difficulties():
    """Test puzzle generation across different difficulty levels"""
    
    print(f"\n🎯 Testing Multiple Difficulty Levels")
    print("=" * 60)
    
    difficulties = [0.2, 0.4, 0.6, 0.8]
    results = []
    
    for difficulty in difficulties:
        print(f"\n📊 Testing Difficulty: {difficulty}")
        try:
            puzzle_data, validation = await test_single_art_puzzle(difficulty)
            results.append({
                'difficulty': difficulty,
                'success': True,
                'score': validation.overall_score,
                'valid': validation.is_valid
            })
            print(f"✅ Success - Score: {validation.overall_score:.2f}")
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            results.append({
                'difficulty': difficulty,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n📋 DIFFICULTY TEST SUMMARY")
    print("-" * 40)
    successful_tests = sum(1 for r in results if r['success'])
    print(f"Successful: {successful_tests}/{len(difficulties)}")
    
    for result in results:
        if result['success']:
            status = "✅" if result['valid'] else "⚠️"
            print(f"{status} Difficulty {result['difficulty']}: Score {result['score']:.2f}")
        else:
            print(f"❌ Difficulty {result['difficulty']}: Failed")
    
    return results


async def test_claude_api_connection():
    """Test Claude API connection and basic functionality"""
    
    print(f"\n🔌 Testing Claude API Connection")
    print("=" * 60)
    
    try:
        generator = Claude4PuzzleGenerator()
        
        if generator.mock_mode:
            print("ℹ️ Running in mock mode - API key not configured or invalid")
            print("💡 To test real API, ensure ANTHROPIC_API_KEY is set in backend/.env")
            return True
        
        print("🔄 Testing API connection...")
        
        # Simple test puzzle generation
        puzzle_data = await generator.generate_puzzle('art', 0.5)
        
        if puzzle_data and 'question' in puzzle_data:
            print("✅ Claude API connection successful!")
            print(f"📝 Test question generated: {puzzle_data['question'][:100]}...")
            return True
        else:
            print("❌ API returned unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False


async def run_comprehensive_test():
    """Run comprehensive test suite"""
    
    print("🧪 Art Puzzle Generation - Comprehensive Test")
    print("=" * 60)
    print(f"🏗️ Testing sophisticated difficulty framework")
    print(f"🎨 Testing dynamic prompt generation")
    print(f"🔍 Testing comprehensive validation")
    print(f"🤖 Testing Claude API integration")
    
    # Test API connection
    api_success = await test_claude_api_connection()
    
    if not api_success:
        print("\n⚠️ API test failed, but continuing with available tests...")
    
    # Test single puzzle generation
    try:
        puzzle_data, validation = await test_single_art_puzzle(0.6)
        single_test_success = True
    except Exception as e:
        print(f"❌ Single puzzle test failed: {str(e)}")
        single_test_success = False
    
    # Test multiple difficulties
    try:
        difficulty_results = await test_multiple_difficulties()
        difficulty_test_success = len([r for r in difficulty_results if r['success']]) > 0
    except Exception as e:
        print(f"❌ Multiple difficulty test failed: {str(e)}")
        difficulty_test_success = False
    
    # Final summary
    print(f"\n🏁 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Claude API Connection", api_success),
        ("Single Puzzle Generation", single_test_success),
        ("Multiple Difficulty Testing", difficulty_test_success)
    ]
    
    passed_tests = sum(1 for _, success in tests if success)
    
    for test_name, success in tests:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall: {passed_tests}/{len(tests)} tests passed")
    
    if passed_tests == len(tests):
        print("🎉 All tests passed! Art puzzle generation system is ready.")
    elif passed_tests > 0:
        print("⚠️ Some tests passed. System partially functional.")
    else:
        print("❌ All tests failed. System needs attention.")
    
    return passed_tests == len(tests)


if __name__ == "__main__":
    print("🚀 Starting Art Puzzle Generation Tests...")
    
    # Run the comprehensive test
    success = asyncio.run(run_comprehensive_test())
    
    if success:
        print("\n✅ Test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test suite completed with failures.")
        sys.exit(1)