# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data & Models
data/embeddings/*.index
data/embeddings/*.pkl
data/raw/
data/processed/
*.h5
*.pkl
*.pth
*.bin

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# FastAPI
.pytest_cache/

# Hugging Face cache
.cache/
models/

# Node modules (for frontend)
node_modules/
frontend/node_modules/
frontend/.next/
frontend/out/
frontend/build/
frontend/dist/

# Testing
.coverage
htmlcov/
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
Step 3: Create README.md
powershell@"
# 🏛️ AI-Stotle: The Wise AI Science Tutor

AI-powered science tutor for Carls Newton shows in Dubai, combining the wisdom of Aristotle with cutting-edge AI technology.

## 🌟 Features

- **🤖 Hybrid AI Backend**: DeepSeek (ultra-low-cost) or Claude (premium quality)
- **📚 FAISS Vector Database**: Free, fast semantic search for scientific knowledge
- **🧠 RAG System**: Retrieval-Augmented Generation for accurate, grounded answers
- **💰 Ultra-Low Cost**: ~\`$\`0.000002 per answer with DeepSeek (97% cheaper than GPT-4)
- **🎯 Age-Appropriate**: Tailored responses for students aged 6-14
- **🔬 Experiment Knowledge**: Pre-loaded with Carls Newton show experiments

## 💡 How It Works

1. **Student asks question** → 
2. **FAISS searches** knowledge base (local, instant, free) → 
3. **AI generates answer** using relevant context (DeepSeek/Claude) → 
4. **Wise, engaging response** delivered!

## 📊 Cost Comparison (per 1M tokens)

| Provider | Cost | Use Case |
|----------|------|----------|
| DeepSeek | \`$\`0.21 | Production (ultra-cheap) |
| Claude Sonnet 4 | \`$\`9.00 | Premium quality |
| GPT-4 | \`$\`20.00 | Expensive alternative |

**Savings**: 97.5% cost reduction with DeepSeek!

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- DeepSeek API key (from https://platform.deepseek.com/)

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/Gamtec1000/AI-stotle_brain.git
cd AI-stotle_brain

# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Configuration

1. Copy \`.env.example\` to \`.env\`:
\`\`\`bash
cp .env.example .env
\`\`\`

2. Add your API keys to \`.env\`:
\`\`\`env
ARISTOTLE_AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
\`\`\`

### Test the System

\`\`\`bash
# Test knowledge base
python knowledge/faiss_knowledge.py

# Test AI-Stotle brain
python core/aristotle_brain.py
\`\`\`

## 📁 Project Structure

\`\`\`
ai-stotle/
├── backend/
│   ├── api/              # FastAPI endpoints
│   ├── core/             # AI-Stotle brain
│   │   └── aristotle_brain.py
│   ├── knowledge/        # FAISS knowledge base
│   │   └── faiss_knowledge.py
│   ├── generation/       # Content generation
│   ├── utils/            # Utilities
│   ├── scripts/          # Helper scripts
│   ├── main.py           # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/             # React/Next.js (coming soon)
├── data/
│   ├── embeddings/       # FAISS index files
│   ├── raw/              # Source documents
│   └── processed/        # Processed data
└── README.md
\`\`\`

## 🧪 Available Experiments (Pre-loaded Knowledge)

- Elephant Toothpaste (Chemistry)
- Catalysts & Reactions (Chemistry)
- Dry Ice Fog (Physics)
- Static Electricity (Physics)
- Slime (Chemistry)
- Mentos & Coke (Physics)
- Volcano (Chemistry)
- Invisible Ink (Chemistry)
- Oobleck (Physics)
- And more!

## 🔧 Adding More Knowledge

\`\`\`python
# Use the add_knowledge script
python scripts/add_knowledge.py

# Or import from files
python scripts/import_from_file.py
\`\`\`

## 🎭 AI-Stotle's Personality

- Wise but never condescending
- Patient and encouraging
- Excited about discovery
- Makes complex ideas simple
- Uses analogies and metaphors
- Occasional philosophical wisdom

## 📈 Roadmap

- [x] FAISS vector database
- [x] DeepSeek integration
- [x] Claude integration (optional)
- [x] Knowledge base with experiments
- [ ] FastAPI REST API
- [ ] WebSocket for streaming responses
- [ ] React frontend
- [ ] Image generation (Stable Diffusion)
- [ ] Video generation (Runway)
- [ ] Voice interaction
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 🙏 Acknowledgments

- Inspired by Aristotle's wisdom and teaching philosophy
- Built for Carls Newton science shows in Dubai
- Powered by DeepSeek, FAISS, and Sentence Transformers

---

**Made with 🧠 and ❤️ for curious young minds**