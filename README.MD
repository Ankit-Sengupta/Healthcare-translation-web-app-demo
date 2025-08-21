# Healthcare Translation App 🌐

A prototype web app that:
- Converts voice/text input to text
- Translates between multiple languages
- Provides audio playback of translated text

## Tech
- **Backend:** FastAPI, gTTS, OpenAI (for generative translation)
- **Frontend:** HTML + JS (mobile-first design)
- **Deployment:** Render (backend) + Vercel (frontend)

## Deploy Steps
### Backend
1. Go to Render.com → New Web Service.
2. Connect GitHub repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend
1. Go to Vercel.com → New Project.
2. Import `frontend/` folder.
3. Deploy 🚀


