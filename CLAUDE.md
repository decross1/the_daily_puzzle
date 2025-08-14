# AI Puzzle Game - Implementation Guide

## Current Status: Phase 2 - AI Integration
**Platform Status**: ✅ Core infrastructure complete | 🚧 AI service integration in progress

## Quick Status Summary
- ✅ **Backend**: Django REST API with all endpoints operational
- ✅ **Database**: PostgreSQL with models migrated and ready
- ✅ **Frontend**: Mobile-first React app (Wordle-inspired)
- ✅ **Scheduling**: Celery + Redis for automated daily cycles
- ✅ **Game Logic**: Difficulty adjustment, scoring, and leaderboards
- 🚧 **AI Integration**: Claude Sonnet 4 API implementation needed
- ⏳ **Authentication**: User system ready to implement

## Next Focus: Claude Sonnet 4 API Integration

### Immediate Tasks
1. **Create `services/puzzle_generation.py`**
   - Implement `ClaudeSonnetClient` class
   - Add puzzle generation methods for each category
   - Include validation logic

2. **Update Environment Variables**
   ```bash
   ANTHROPIC_API_KEY=your_actual_claude_api_key
   ```

3. **Implement Puzzle Generation Flow**
   - Connect `generate_daily_puzzle` task to AI service
   - Add cross-model validation
   - Test with manual generation endpoint

### Claude Sonnet 4 Integration Plan
```python
class ClaudeSonnetClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_puzzle(self, category: str, difficulty: float) -> dict:
        # Map difficulty to puzzle complexity
        # Generate puzzle based on category
        # Return structured puzzle data
```

## Puzzle Categories Documentation

### **Math Puzzles**
**Examples:**
* Algebraic equations: "Solve for x: 3x² + 7x - 20 = 0"
* Physics problems: "A ball is thrown upward at 20 m/s. When does it hit the ground?"
* Number theory: "Find the next prime number after 1,009"
* Geometry: "What's the area of a triangle with sides 5, 12, 13?"
* Statistics: "What's the probability of rolling three 6s in a row?"
* Calculus: "Find the derivative of f(x) = 3x³ - 2x² + 5"
* Logic: "If all Bloops are Razzies and all Razzies are Lazzies..."

### **Word Puzzles**
**Examples:**
* Riddles: "I have cities, but no houses. I have water, but no fish. What am I?"
* Word searches: "Find 7 animals hidden in this 10x10 grid"
* Anagrams: "Unscramble: TNERALC EGNIEN" (CENTRAL ENGINE)
* Wordplay: "What 5-letter word becomes shorter when you add two letters?"
* Cryptic clues: "Capital gains from Paris adventure (6)"
* Palindromes: "Find the longest palindrome using these letters: A,C,E,R,R"
* Etymology: "What language does 'algebra' originally come from?"

### **Art Puzzles**
**Examples:**
* Music identification: "Name this song from a 3-second audio clip"
* Visual recognition: "Identify the movie from this blurred poster"
* Artist identification: "Who painted this detail from a famous work?"
* Style matching: "Which art movement does this piece represent?"
* Color theory: "What color do you get mixing cyan and yellow?"
* Film trivia: "Name the director known for single-take sequences"
* Architecture: "Identify this building from its silhouette"

## Implementation Architecture

### System Flow
```
User Request → API Endpoint → Puzzle Service → Claude Sonnet 4
                                     ↓
                              Generate Puzzle
                                     ↓
                              Validate Solution
                                     ↓
                            Store in Database ← Return to User
```

### Daily Cycle (Automated)
1. **00:00 UTC**: Celery triggers `generate_daily_puzzle`
2. **Generation**: Claude Sonnet 4 creates puzzle at current difficulty
3. **Validation**: AI verifies it can solve its own puzzle
4. **Publishing**: Puzzle becomes available to players
5. **23:59 UTC**: `evaluate_daily_results` adjusts difficulty
6. **Repeat**: Next AI model in rotation generates tomorrow's puzzle

## Code Structure

### Backend Services Structure
```
backend/
├── services/
│   ├── __init__.py
│   ├── puzzle_generation.py    # Main generation service
│   ├── ai_clients/
│   │   ├── __init__.py
│   │   ├── claude_client.py    # Claude Sonnet 4 integration
│   │   ├── openai_client.py    # GPT-4o integration (future)
│   │   └── gemini_client.py    # Gemini integration (future)
│   └── validators/
│       ├── __init__.py
│       └── puzzle_validator.py # Cross-model validation
```

## API Endpoints Reference

### Puzzle Endpoints
- `GET /api/puzzle/daily/` - Get today's puzzle
- `POST /api/puzzle/submit/` - Submit answer
- `GET /api/puzzle/history/` - View past puzzles
- `POST /api/puzzle/generate/` - Manual generation (admin)

### Stats & Leaderboards
- `GET /api/leaderboard/` - Top players
- `GET /api/stump-tally/` - AI model performance
- `GET /api/stats/` - Personal statistics

## Development Priorities

### Week 1-2: AI Integration ← **CURRENT FOCUS**
- [ ] Implement Claude Sonnet 4 client
- [ ] Create puzzle generation templates
- [ ] Add solution validation
- [ ] Test with all puzzle categories
- [ ] Connect to scheduled tasks

### Week 3: User System
- [ ] JWT authentication
- [ ] User registration/login
- [ ] Profile management
- [ ] Persistent progress tracking

### Week 4: Enhanced Features
- [ ] Real-time countdown timer
- [ ] Share functionality
- [ ] Achievement system
- [ ] Advanced analytics

### Week 5: Polish & Deploy
- [ ] Performance optimization
- [ ] Production deployment
- [ ] Load testing
- [ ] User feedback integration

## Quick Commands

```bash
# Start all services
docker-compose up -d

# Test AI integration manually
curl -X POST http://localhost:8000/api/puzzle/generate/ \
  -H "Content-Type: application/json" \
  -d '{"category": "math", "difficulty": 0.5}'

# Monitor Celery tasks
docker logs -f daily_puzzle-celery-1

# Access Django shell for testing
docker exec -it daily_puzzle-backend-1 python manage.py shell
```

## Environment Setup

### Required API Keys
```env
# AI Services (Required for Phase 2)
ANTHROPIC_API_KEY=sk-ant-xxx  # Claude Sonnet 4
OPENAI_API_KEY=sk-xxx         # GPT-4o (future)
GOOGLE_API_KEY=xxx            # Gemini (future)

# Database (Already configured)
DB_NAME=daily_puzzle
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis (Already configured)
REDIS_URL=redis://redis:6379/0
```

## Success Metrics

### Technical KPIs
- API response time < 200ms
- Puzzle generation time < 5s
- Validation accuracy > 95%
- System uptime > 99.9%

### Game Balance Metrics
- Community solve rate: 40-60%
- Difficulty distribution: 30% Mini, 50% Mid, 20% Beast
- Daily active users growth
- Average session duration > 5 minutes

## Testing Strategy

### Unit Tests
- Puzzle generation logic
- Difficulty adjustment algorithm
- Answer validation
- API endpoints

### Integration Tests
- AI service connectivity
- Database transactions
- Celery task execution
- End-to-end user flow

### Manual Testing Checklist
- [ ] Generate puzzle for each category
- [ ] Verify difficulty scaling
- [ ] Test answer submission
- [ ] Check leaderboard updates
- [ ] Validate scheduled tasks

---

**Next Action**: Implement `ClaudeSonnetClient` in `backend/services/puzzle_generation.py`
**Priority**: Connect Claude Sonnet 4 API for puzzle generation
**Blocking**: All automated features waiting on AI integration