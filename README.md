# koreanbangla — Python Flask Korean-to-Bangla learning website

## Included
- 36 structured beginner lessons (Hangul, pronunciation, grammar, daily speech, work, transport, food, health and revision)
- Searchable Korean-to-Bangla vocabulary and phrase dictionary
- JSON content files so you can add or correct lessons and words
- Interactive quiz with score and answer explanations
- Mobile-responsive Bangla UI
- JSON endpoints: `/api/lessons`, `/api/vocabulary`, `/api/quiz`

## Run locally
Needs Python 3.10+.

```bash
python -m venv .venv
```

Activate:
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

Install packages:
```bash
pip install -r requirements.txt
```

Run:
```bash
python app.py
```
Open `http://127.0.0.1:5000`.

## Publish online (example: Render)
1. Create a GitHub account and a new repository named `koreanbangla`.
2. Unzip this project and upload all files/folders to the repository.
3. Create/sign in to a Render account and choose **New + → Web Service**.
4. Connect your GitHub repository.
5. Set **Build Command** to `pip install -r requirements.txt`.
6. Set **Start Command** to `gunicorn app:app`.
7. Choose a plan, then click deploy. Render will provide a public `onrender.com` URL. If the provider's UI changes, follow its current Flask deployment instructions.
8. For your own domain, buy a domain from a registrar and configure it in the hosting dashboard.

`gunicorn` is listed in requirements. Do not use Flask's `debug=True` development server in production.

## Add content
- Lessons: edit `data/lessons.json`.
- Dictionary: edit `data/vocabulary.json`. Each item has `ko`, `bn`, `pron`, `category`.
- Quiz: edit `data/quiz.json`. Each item has `q`, `opts`, `answer` (0-based index), and `explain`.

## Important editorial note
This is a sizeable starter learning site, not a professionally proofread complete textbook. Bengali pronunciation is approximate and many grammar points depend on context. Before public launch or monetization, ask a qualified Korean-language teacher to review Korean spelling, grammar, Bengali meanings and examples. It currently does not include user accounts, progress tracking, audio recordings, payment, ads, or an exhaustive dictionary.
