# The Daily Puzzle

A daily puzzle game where AI models compete to stump human players. The system automatically adjusts difficulty based on community performance, creating a dynamic challenge that evolves with player skill.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis

### Installation

1. Clone and setup:
```bash
git clone <repository-url>
cd the_daily_puzzle
npm run install:all
```

2. Environment setup:
```bash
cp .env.example .env
# Edit .env with your database and API keys
```

3. Database setup:
```bash
npm run backend:migrate
npm run backend:createsuperuser
```

4. Start development servers:
```bash
npm run dev
```

## Development Commands

- `npm run dev` - Start both frontend and backend
- `npm run backend:dev` - Django development server
- `npm run frontend:dev` - React development server
- `npm run backend:migrate` - Run database migrations
- `npm run celery:worker` - Start Celery worker
- `npm run celery:beat` - Start Celery beat scheduler

## Architecture

- **Frontend**: React (localhost:3000)
- **Backend**: Django REST API (localhost:8000)
- **Database**: PostgreSQL
- **Workers**: Celery with Redis
- **AI Models**: GPT-4o, Claude 3, Gemini

## Project Structure

```
├── backend/          # Django REST API
│   ├── daily_puzzle/     # Main Django project
│   ├── puzzles/          # Puzzle management
│   ├── users/            # User profiles
│   └── validators/       # AI model validation
├── frontend/         # React application
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
└── CLAUDE.md         # Detailed architecture docs
```