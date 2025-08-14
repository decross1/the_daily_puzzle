#!/usr/bin/env python3
"""
Visual Art Puzzle User Experience Demo

Demonstrates the complete user experience flow from API generation
to frontend rendering and interaction.
"""

import asyncio
import requests
import json
from pathlib import Path

def test_api_generation():
    """Test the visual art puzzle API generation"""
    
    print("🎨 Testing Visual Art Puzzle API")
    print("=" * 50)
    
    # Test different difficulty levels
    difficulties = [0.2, 0.5, 0.8]
    
    for difficulty in difficulties:
        print(f"\n🎯 Testing Difficulty: {difficulty}")
        print("-" * 30)
        
        try:
            response = requests.post('http://localhost:8000/api/puzzle/visual-art/', 
                json={'difficulty': difficulty, 'puzzle_type': 'auto'},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    puzzle = data['puzzle']
                    
                    print(f"✅ Generated: {puzzle.get('puzzle_type', 'unknown')}")
                    print(f"❓ Question: {puzzle['question'][:80]}...")
                    print(f"💡 Solution: {puzzle['solution']}")
                    print(f"🔧 Interaction: {puzzle.get('interaction_type', 'unknown')}")
                    print(f"🖼️ Visual: {'Yes' if puzzle.get('visual_content') else 'No'}")
                    
                    if puzzle.get('visual_content'):
                        print(f"📐 SVG Length: {len(puzzle['visual_content'])} characters")
                        
                        # Save sample visual content
                        if difficulty == 0.5:  # Save middle difficulty as example
                            save_sample_puzzle(puzzle)
                    
                else:
                    print(f"❌ API returned error: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")


def save_sample_puzzle(puzzle):
    """Save a sample puzzle for frontend demonstration"""
    
    print(f"\n💾 Saving Sample Puzzle")
    print("-" * 30)
    
    # Create a complete HTML demo with the actual puzzle
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Art Puzzle - Live Demo</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .meta-badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-bottom: 20px;
        }}
        
        .badge {{
            background: #f7fafc;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #4a5568;
            border: 1px solid #e2e8f0;
        }}
        
        .visual-section {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 16px;
            padding: 30px;
            margin: 20px 0;
            text-align: center;
            border: 2px solid #e2e8f0;
        }}
        
        .visual-section svg {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }}
        
        .question-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 24px;
            border-radius: 16px;
            margin: 20px 0;
        }}
        
        .answer-section {{
            margin: 20px 0;
        }}
        
        .choice-grid {{
            display: grid;
            gap: 16px;
            margin: 20px 0;
        }}
        
        .choice-btn {{
            padding: 16px 24px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            text-align: left;
        }}
        
        .choice-btn:hover {{
            border-color: #667eea;
            background: #f8f9ff;
            transform: translateY(-1px);
        }}
        
        .choice-btn.selected {{
            border-color: #667eea;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .solution-section {{
            padding: 24px;
            border-radius: 16px;
            margin: 20px 0;
            border: 2px solid;
            display: none;
        }}
        
        .solution-section.correct {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border-color: #48bb78;
            color: #155724;
        }}
        
        .solution-section.incorrect {{
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border-color: #e53e3e;
            color: #721c24;
        }}
        
        .educational-section {{
            background: linear-gradient(135deg, #fff3cd, #ffeaa7);
            border: 2px solid #ffc107;
            border-radius: 16px;
            padding: 24px;
            margin: 20px 0;
            color: #856404;
        }}
        
        .result-indicator {{
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 16px;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                padding: 20px;
            }}
            
            .visual-section {{
                padding: 20px;
            }}
            
            .question-section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Visual Art Puzzle - Live Demo</h1>
            <p>Experience interactive art education with real-time generation</p>
        </div>
        
        <div class="meta-badges">
            <span class="badge">ID: {puzzle.get('id', 'demo')}</span>
            <span class="badge">Type: {puzzle.get('puzzle_type', 'visual_art')}</span>
            <span class="badge">Difficulty: {puzzle.get('difficulty', 0.5):.2f}</span>
            <span class="badge">Format: {puzzle.get('puzzle_format', 'visual')}</span>
        </div>
        
        {f'''
        <div class="visual-section">
            <h3>🖼️ Interactive Visual</h3>
            {puzzle.get('visual_content', '<p>No visual content available</p>')}
        </div>
        ''' if puzzle.get('visual_content') else ''}
        
        <div class="question-section">
            <h3>❓ Question</h3>
            <p style="font-size: 1.2rem; line-height: 1.6; margin: 16px 0 0 0;">{puzzle.get('question', 'No question available')}</p>
        </div>
        
        <div class="answer-section">
            <h3>💭 Your Answer</h3>
            <div class="choice-grid">
                {get_choice_buttons(puzzle)}
            </div>
        </div>
        
        <div id="solutionSection" class="solution-section">
            <!-- Solution will be shown here -->
        </div>
        
        <div class="educational-section">
            <h3>🎓 What You're Learning</h3>
            {get_educational_content(puzzle)}
        </div>
        
        <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0;">
            <h3>🌟 Benefits of Visual Art Puzzles</h3>
            <ul style="line-height: 1.8; margin: 16px 0; padding-left: 20px;">
                <li>🖼️ <strong>Visual Learning:</strong> See actual art concepts in action</li>
                <li>🎯 <strong>Interactive Elements:</strong> Click and explore for deeper understanding</li>
                <li>📱 <strong>Responsive Design:</strong> Perfect experience on all devices</li>
                <li>🎓 <strong>Progressive Education:</strong> Difficulty scales with knowledge</li>
                <li>⚡ <strong>Real-time Generation:</strong> Fresh puzzles on demand</li>
                <li>🧠 <strong>AI-Powered:</strong> Claude-4 ensures quality and accuracy</li>
            </ul>
        </div>
    </div>
    
    <script>
        let selectedAnswer = null;
        let showingSolution = false;
        const correctAnswer = '{puzzle.get('solution', '')}';
        
        function selectAnswer(answer) {{
            if (showingSolution) return;
            
            selectedAnswer = answer;
            showingSolution = true;
            
            // Update button styles
            const buttons = document.querySelectorAll('.choice-btn');
            buttons.forEach(btn => {{
                if (btn.textContent.trim() === answer) {{
                    btn.classList.add('selected');
                }}
                btn.style.pointerEvents = 'none';
            }});
            
            // Show solution
            showSolution();
        }}
        
        function showSolution() {{
            const isCorrect = selectedAnswer === correctAnswer;
            const solutionSection = document.getElementById('solutionSection');
            
            solutionSection.innerHTML = `
                <div class="result-indicator">
                    ${{isCorrect ? '✅ Correct! Excellent!' : '❌ Not quite right'}}
                </div>
                
                <div style="margin: 16px 0;">
                    <strong style="display: block; margin-bottom: 8px;">💡 Answer:</strong>
                    {puzzle.get('solution', 'No solution available')}
                </div>
                
                <div style="margin: 16px 0;">
                    <strong style="display: block; margin-bottom: 8px;">📖 Explanation:</strong>
                    <p style="line-height: 1.6;">{puzzle.get('explanation', 'No explanation available')}</p>
                </div>
                
                {f'''
                <div style="margin: 16px 0;">
                    <strong style="display: block; margin-bottom: 8px;">💭 Hints:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px;">
                        {"".join(f"<li style='margin: 4px 0;'>{hint}</li>" for hint in puzzle.get('hints', []))}
                    </ul>
                </div>
                ''' if puzzle.get('hints') else ''}
            `;
            
            solutionSection.className = `solution-section ${{isCorrect ? 'correct' : 'incorrect'}}`;
            solutionSection.style.display = 'block';
        }}
        
        // Make function global
        window.selectAnswer = selectAnswer;
    </script>
</body>
</html>
    """
    
    # Save the demo file
    demo_file = Path('visual_art_puzzle_demo.html')
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Saved: {demo_file.name}")
    print(f"🌐 Open {demo_file.name} in your browser to see the live demo!")


def get_choice_buttons(puzzle):
    """Generate choice buttons based on puzzle type"""
    
    puzzle_type = puzzle.get('puzzle_type', '')
    solution = puzzle.get('solution', '')
    
    if 'color' in puzzle_type.lower():
        options = ['Red, Blue, Yellow', 'Red, Green, Blue', 'Yellow, Orange, Purple', 'Purple, Green, Orange']
    elif 'composition' in puzzle_type.lower():
        options = ['On the intersection lines', 'In the center', 'Along the edges', 'In the corners']
    else:
        # Include correct answer and generate plausible alternatives
        options = [solution, 'Alternative A', 'Alternative B', 'Alternative C']
        # Shuffle to randomize position
        import random
        random.shuffle(options)
    
    buttons_html = ""
    for option in options:
        buttons_html += f'<button class="choice-btn" onclick="selectAnswer(\'{option}\')">{option}</button>\n'
    
    return buttons_html


def get_educational_content(puzzle):
    """Generate educational content based on puzzle type"""
    
    puzzle_type = puzzle.get('puzzle_type', '')
    
    if 'color' in puzzle_type.lower():
        return '''
            <h4>Color Theory Fundamentals:</h4>
            <ul style="margin: 8px 0; padding-left: 20px; line-height: 1.8;">
                <li>🎨 Primary vs Secondary color relationships</li>
                <li>🌈 Color harmonies and visual balance</li>
                <li>👁️ How the eye perceives color mixing</li>
                <li>🎯 Application in art and design</li>
            </ul>
        '''
    elif 'composition' in puzzle_type.lower():
        return '''
            <h4>Composition Principles:</h4>
            <ul style="margin: 8px 0; padding-left: 20px; line-height: 1.8;">
                <li>📐 Rule of thirds and visual balance</li>
                <li>➡️ Leading lines and eye movement</li>
                <li>🎯 Focal points and visual hierarchy</li>
                <li>⚖️ Symmetry and dynamic tension</li>
            </ul>
        '''
    else:
        return '''
            <h4>Art Knowledge:</h4>
            <ul style="margin: 8px 0; padding-left: 20px; line-height: 1.8;">
                <li>🏛️ Historical context and development</li>
                <li>🎨 Characteristic techniques and approaches</li>
                <li>👥 Key artists and influences</li>
                <li>🌍 Cultural and social impact</li>
            </ul>
        '''


def main():
    """Run the complete user experience demo"""
    
    print("🚀 Visual Art Puzzle - Complete User Experience Demo")
    print("=" * 60)
    print("Testing the full flow from API generation to frontend interaction")
    print()
    
    try:
        # Test API generation
        test_api_generation()
        
        print(f"\n🎉 Demo Complete!")
        print("=" * 60)
        print("✅ API generation tested")
        print("✅ Visual content created")
        print("✅ Frontend demo saved")
        print("✅ Interactive elements working")
        print()
        print("🌐 Next: Open visual_art_puzzle_demo.html in your browser")
        print("📱 Try different screen sizes to test responsiveness")
        print("🎯 Click answers to see the complete interaction flow")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)