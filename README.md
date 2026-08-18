# AI Career Guidance System

A complete Flask + SQLite hackathon project that recommends careers using an explainable scoring engine, identifies skill gaps, creates career-specific roadmaps and optionally adds a natural-language AI explanation.

## Problem statement

Students often see career advice as a list of job titles without understanding why a path fits them or what to learn next. This project combines academic performance, interests, skills, work preferences and assessment answers to produce a transparent career profile.

## Solution

> We don't just recommend a career. We explain why it fits the student, identify the student's skill gaps, and generate a personalized roadmap to reach that career.

## Features

- Multi-step responsive assessment
- Stream-aware academic subjects
- Interest and skill selection
- 1–5 career preference ratings
- 10 non-clinical aptitude/personality-style questions
- Explainable weighted recommendation engine
- Top 3 career matches with percentages
- Rule-based explanation when no AI API is configured
- Optional external AI explanation through environment variables
- Skill-gap analysis
- Career-specific roadmap
- Career snapshot, roles and project ideas
- Career comparison
- “What if I choose another career?” exploration
- SQLite persistence
- Input validation and friendly error pages
- Unit tests for common hackathon demo profiles

## Tech stack

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python + Flask
- Database: SQLite
- Recommendation engine: Python weighted scoring
- Optional AI: OpenAI-compatible Responses API endpoint configured through environment variables

## Architecture

```text
Browser
  |
  v
Flask routes (app.py)
  |---------------------> SQLite (database.py)
  |
  v
Assessment data
  |
  v
recommendation.py
  |       \
  |        \--> top 3 + reasons + skill gap
  |
  +--> ai_service.py --> optional external AI
  |
  v
Jinja result dashboard
```

The core recommendation path does not require an API key.

## Folder structure

```text
AI-Career-Guidance/
├── app.py
├── database.py
├── init_db.py
├── recommendation.py
├── ai_service.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
│   └── careers.json
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── assessment.html
│   ├── result.html
│   ├── compare.html
│   └── error.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
└── tests/
    └── test_recommendation.py
```

`career.db` is generated automatically by `python init_db.py`, so it is intentionally not required in the source archive.

## Installation

Python 3.10+ is recommended.

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

## Optional AI configuration

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

The key stays on the server and is never placed in frontend JavaScript. If the key is missing, invalid, unavailable, or the request fails, the app automatically uses its local rule-based explanation.

Do not commit `.env` or any real API key to Git.

## Database schema

### careers
Stores career descriptions, skills, education, roles, roadmap, demand and project ideas.

### assessment_questions
Stores the ten assessment questions and their five answer options.

### results
Stores a student's name, JSON assessment/result payload and timestamp for demo persistence.

The app uses parameterized SQLite queries for database writes/lookups.

## Recommendation algorithm

Default weights:

| Factor | Weight |
|---|---:|
| Academic performance | 20% |
| Interests | 25% |
| Skills | 20% |
| Career preferences | 20% |
| Aptitude answers | 15% |

Every career receives a score. Scores are clamped to 0–100, sorted, and the top three are returned.

The reasons are generated from actual overlaps such as:
- relevant subjects with strong marks
- selected interests
- existing skills required by the career
- preference alignment
- aptitude answer patterns

This makes the demo explainable instead of random.

## Testing

Run:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:
1. Science + AI interest
2. Commerce + finance interest
3. Programming interest
4. Data interest
5. Cyber security interest
6. Design interest

## 3–5 minute hackathon demo

1. Open the home page.
2. Click **Start Career Assessment**.
3. Use a sample student profile.
4. Complete the six steps.
5. Submit and show the top match.
6. Point out the percentage and “Why this career?” explanation.
7. Show current vs missing skills.
8. Scroll through the personalized roadmap.
9. Click **Compare careers**.
10. Return to the result and demonstrate **What if I choose another career?**

## Five-member team split

### Member 1 — AI/Recommendation
- `recommendation.py`
- `ai_service.py`
- weights and scoring experiments

### Member 2 — Frontend/UI
- `templates/`
- `static/css/style.css`
- `static/js/script.js`

### Member 3 — Backend/Database
- `app.py`
- `database.py`
- `init_db.py`
- Flask routes

### Member 4 — Career research/data
- `data/careers.json`
- question design
- roadmaps, skills and project ideas

### Member 5 — Testing/docs/demo
- `tests/`
- README
- demo script
- presentation and judge Q&A

## Future scope

- User accounts and saved profiles
- More validated career datasets
- Course recommendations from trusted education providers
- Labor-market data APIs
- Multilingual guidance
- Admin dashboard
- Explainability charts
- Model-based recommendation trained on anonymized outcomes

## Important note

This system provides educational guidance, not a guarantee that a student will succeed in a career or receive a particular salary. Career decisions should consider personal goals, access to education, current market conditions and advice from qualified educators/counsellors.
