# Cebu Weather Mood API (FastAPI)

A simple API that returns **mood suggestions** based on the **current weather** in **Cebu City, Philippines**.

## How to run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set your OpenWeatherMap API key.

3. Run the server:
```bash
uvicorn app.main:app --reload
```

4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test.
