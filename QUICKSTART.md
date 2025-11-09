# 🏛️ AI-stotle Backend - Quick Start Guide

## ❌ Issue: API Connection Failed

The frontend can't connect because the backend isn't running yet. Follow these steps:

## 🚀 Quick Start (5 minutes)

### Step 1: Create .env File

```bash
cd backend
cp .env.example .env
```

### Step 2: Add Your API Key

Edit `backend/.env` and add your DeepSeek API key:

```bash
# Get a FREE API key from: https://platform.deepseek.com/
DEEPSEEK_API_KEY=your-actual-api-key-here
```

**Don't have a DeepSeek key?**
- Visit: https://platform.deepseek.com/
- Sign up (free)
- Get your API key
- Paste it in `.env`

### Step 3: Install Dependencies

```bash
# From the backend directory
pip install -r requirements.txt
```

**Key packages:**
- `fastapi` - Web framework
- `chromadb` - Vector database
- `sentence-transformers` - Embeddings
- `openai` - DeepSeek client

### Step 4: Start the Server

```bash
# From the backend directory
python -m api.main
```

Or using uvicorn directly:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
🏛️ AI-STOTLE API SERVER
🚀 Starting server...
📍 http://localhost:8000
📚 Docs: http://localhost:8000/docs
```

### Step 5: Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:8000/

# Should return:
# {"status":"online","service":"AI-stotle","version":"1.0.0",...}
```

Or visit in browser:
- API Root: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- Metadata: http://localhost:8000/meta.json

### Step 6: Refresh Your Frontend

Now go back to http://localhost:5173 and refresh!

The "API Connection Failed" should change to "✅ API Connected"

---

## 🐛 Troubleshooting

### "DEEPSEEK_API_KEY not found in environment"

You forgot to create `.env` or didn't add your API key.

**Fix:**
```bash
cd backend
cp .env.example .env
# Edit .env and add your API key
```

### "Module not found" errors

Dependencies not installed.

**Fix:**
```bash
pip install -r requirements.txt
```

### Port 8000 already in use

Another process is using port 8000.

**Fix:**
```bash
# Option 1: Kill the process
lsof -ti:8000 | xargs kill -9

# Option 2: Use different port
uvicorn api.main:app --port 8001
# Then update frontend apiUrl to http://localhost:8001
```

### CORS errors in browser console

The frontend origin isn't allowed.

**Fix:**
Check `backend/.env` includes:
```bash
CORS_ORIGINS=http://localhost:5173,...
```

### "chromadb" not installed

**Fix:**
```bash
pip install chromadb>=0.4.0
```

---

## 📁 Project Structure

```
backend/
├── .env.example        ← Copy to .env
├── .env               ← Your actual config (create this!)
├── requirements.txt   ← Python dependencies
├── api/
│   └── main.py       ← FastAPI app (run this)
├── core/
│   └── aristotle_brain.py
└── knowledge/
    └── embedding_engine.py
```

---

## 🎯 Full Development Setup

### Terminal 1: Backend
```bash
cd backend
python -m api.main
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Browser
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📊 Populating the Knowledge Base

Once the backend is running, you can add experiments:

```python
from knowledge.embedding_engine import LocalEmbeddingEngine

engine = LocalEmbeddingEngine()

# Add experiments from JSON
engine.embed_experiments("../data/experiments.json")

# Add Q&A pairs
engine.embed_qa_pairs("../data/experiments.json")
```

The knowledge base will persist in `data/embeddings/chroma/`

---

## ✅ Success Checklist

- [ ] Created `.env` file
- [ ] Added DeepSeek API key
- [ ] Installed Python dependencies
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] API connection shows "✅ Connected"
- [ ] Chat widget appears in bottom-right

---

## 💰 Costs

**Backend:**
- ChromaDB: $0 (local, free)
- Embeddings: $0 (local, free)
- DeepSeek API: ~$0.14 per 1M tokens (ultra-cheap!)

**Frontend:**
- Development: $0 (local)
- Deployment: ~$0 (static hosting on Netlify/Vercel)

---

## 🆘 Still Having Issues?

1. Check backend logs for errors
2. Check browser console for errors
3. Verify `.env` file exists and has API key
4. Make sure both servers are running
5. Try restarting both servers

Need help? Check:
- Backend logs in the terminal
- Browser DevTools → Console tab
- Browser DevTools → Network tab
