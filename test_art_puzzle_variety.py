#!/usr/bin/env python3
"""
Art Puzzle Variety Testing Script

Generates multiple art puzzles across difficulty spectrum to test
user experience and engagement for NYT-quality puzzle game feel.

Usage:
    python test_art_puzzle_variety.py
"""

import requests
import json
import time
from datetime import datetime

def test_art_puzzle_variety():
    """Generate variety of art puzzles for UX testing"""
    
    base_url = "http://localhost:8000/api/puzzle/visual-art/"
    
    # Test configurations for different difficulty levels and types
    test_configs = [
        # Mini Puzzles (Easy, 30 seconds, 80%+ solve rate)
        {"difficulty": 0.15, "name": "Mini - Color Theory Basic", "expected_time": "30 seconds"},
        {"difficulty": 0.2, "name": "Mini - Famous Artist", "expected_time": "30 seconds"},
        {"difficulty": 0.25, "name": "Mini - Basic Composition", "expected_time": "45 seconds"},
        {"difficulty": 0.3, "name": "Mini - Art Styles", "expected_time": "45 seconds"},
        
        # Mid Puzzles (Moderate, 2-3 minutes, 50-60% solve rate)
        {"difficulty": 0.4, "name": "Mid - Art Movement", "expected_time": "2 minutes"},
        {"difficulty": 0.45, "name": "Mid - Style Analysis", "expected_time": "2.5 minutes"},
        {"difficulty": 0.5, "name": "Mid - Historical Context", "expected_time": "3 minutes"},
        {"difficulty": 0.55, "name": "Mid - Technique Recognition", "expected_time": "3 minutes"},
        {"difficulty": 0.6, "name": "Mid - Cultural Art", "expected_time": "3.5 minutes"},
        
        # Beast Puzzles (Expert, 5+ minutes, 20-30% solve rate)
        {"difficulty": 0.7, "name": "Beast - Advanced Theory", "expected_time": "5 minutes"},
        {"difficulty": 0.75, "name": "Beast - Art History Deep", "expected_time": "6 minutes"},
        {"difficulty": 0.8, "name": "Beast - Obscure Artists", "expected_time": "7 minutes"},
        {"difficulty": 0.85, "name": "Beast - Cross-Cultural", "expected_time": "8 minutes"},
        {"difficulty": 0.9, "name": "Beast - Expert Analysis", "expected_time": "10+ minutes"},
    ]
    
    print("🎨 Art Puzzle Variety Testing")
    print("=" * 50)
    print(f"Testing {len(test_configs)} puzzle configurations")
    print(f"Target: NYT Puzzle Game quality and engagement")
    print()
    
    results = []
    
    for i, config in enumerate(test_configs, 1):
        print(f"📝 Test {i}/{len(test_configs)}: {config['name']}")
        print(f"   Difficulty: {config['difficulty']:.2f}")
        print(f"   Expected Time: {config['expected_time']}")
        
        try:
            # Generate puzzle
            response = requests.post(
                base_url,
                json={"difficulty": config["difficulty"], "puzzle_type": "auto"},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                puzzle = data.get('puzzle', {})
                
                # Extract key information for evaluation
                result = {
                    "test_name": config['name'],
                    "difficulty": config['difficulty'],
                    "expected_time": config['expected_time'],
                    "question": puzzle.get('question', '')[:100] + "...",
                    "solution": puzzle.get('solution', ''),
                    "puzzle_type": puzzle.get('puzzle_type', 'unknown'),
                    "interaction_type": puzzle.get('interaction_type', 'unknown'),
                    "has_visual": bool(puzzle.get('visual_content')),
                    "estimated_solve_time": puzzle.get('estimated_solve_time', 0),
                    "explanation": puzzle.get('explanation', '')[:100] + "...",
                    "timestamp": datetime.now().isoformat()
                }
                
                results.append(result)
                
                print(f"   ✅ Generated: {puzzle.get('puzzle_type', 'unknown')}")
                print(f"   ❓ Question: {result['question']}")
                print(f"   💡 Answer: {result['solution']}")
                print(f"   🖼️ Visual: {'Yes' if result['has_visual'] else 'No'}")
                print(f"   ⏱️ Est. Solve: {result['estimated_solve_time']}s")
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                print(f"   Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   💥 Exception: {str(e)}")
        
        print()
        time.sleep(1)  # Brief pause between requests
    
    # Save results for analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"art_puzzle_variety_test_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("📊 Testing Complete!")
    print("=" * 50)
    print(f"Generated: {len(results)} successful puzzles")
    print(f"Results saved: {filename}")
    print()
    
    # Summary analysis
    difficulty_groups = {
        "Mini (0.1-0.3)": [r for r in results if 0.1 <= r['difficulty'] <= 0.3],
        "Mid (0.4-0.6)": [r for r in results if 0.4 <= r['difficulty'] <= 0.6], 
        "Beast (0.7-0.9)": [r for r in results if 0.7 <= r['difficulty'] <= 0.9]
    }
    
    for group_name, group_results in difficulty_groups.items():
        if group_results:
            avg_solve_time = sum(r['estimated_solve_time'] for r in group_results) / len(group_results)
            visual_count = sum(1 for r in group_results if r['has_visual'])
            
            print(f"📈 {group_name}: {len(group_results)} puzzles")
            print(f"   Average solve time: {avg_solve_time:.0f} seconds")
            print(f"   Visual puzzles: {visual_count}/{len(group_results)}")
            print()
    
    print("🎯 Next Steps for UX Evaluation:")
    print("1. Test each puzzle in browser: http://localhost:3000")
    print("2. Time yourself solving each difficulty level")
    print("3. Rate engagement and 'aha moment' satisfaction")
    print("4. Check mobile experience on phone/tablet")
    print("5. Evaluate educational value and visual clarity")
    print()
    print("Target Success Rates:")
    print("• Mini: 80%+ solve rate (quick satisfaction)")
    print("• Mid: 50-60% solve rate (moderate challenge)")  
    print("• Beast: 20-30% solve rate (expert difficulty)")

if __name__ == "__main__":
    test_art_puzzle_variety()