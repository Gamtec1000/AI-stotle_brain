# 🏛️ AI-stotle Frontend Widget

Beautiful, embeddable chat widget for the AI-stotle science tutor.

## Features

- ✅ **React + TypeScript** - Type-safe development
- ✅ **ChromaDB Integration** - RAG-powered answers
- ✅ **Dark/Light Themes** - Customizable appearance
- ✅ **Responsive Design** - Works on all devices
- ✅ **Zero-Cost Embeddings** - Local, free vector search
- ✅ **DeepSeek AI** - Ultra-low-cost responses

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The widget will be available at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

Build output will be in `dist/` directory.

## Usage

### Basic Integration

```tsx
import AristotleWidget from './components/AristotleWidget';

function App() {
  return (
    <AristotleWidget
      apiUrl="https://api.carlsnewton.com"
      studentAge={10}
      theme="dark"
      position="bottom-right"
    />
  );
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `apiUrl` | string | `http://localhost:8000` | Backend API URL |
| `studentAge` | number | `10` | Student age for appropriate responses |
| `theme` | `'light' \| 'dark'` | `'dark'` | Widget color theme |
| `position` | `'bottom-right' \| 'bottom-left'` | `'bottom-right'` | Widget position |

## API Client

The frontend includes a typed API client for all backend endpoints:

```typescript
import { aristotleApi } from './services/aristotleApi';

// Ask a question
const response = await aristotleApi.askQuestion({
  question: "What makes slime stretchy?",
  student_age: 8,
  use_knowledge_base: true
});

// Search experiments
const experiments = await aristotleApi.searchExperiments({
  query: "chemistry",
  limit: 5
});

// Get API metadata
const meta = await aristotleApi.getMeta();
console.log(meta.capabilities.knowledge_base.total_experiments);
```

## TypeScript Types

All API types are defined in `src/types/api.ts`:

- `AskQuestionRequest` - Question request payload
- `QuestionResponse` - AI response with answer and sources
- `ExperimentSearchResponse` - Search results
- `MetaResponse` - API capabilities and configuration
- And more...

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Demo page
├── src/
│   ├── components/
│   │   ├── AristotleWidget.tsx   # Main widget component
│   │   └── AristotleWidget.css   # Widget styles
│   ├── services/
│   │   └── aristotleApi.ts       # API client
│   └── types/
│       └── api.ts                # TypeScript types
├── package.json
└── README.md
```

## Customization

### Changing Colors

Edit `AristotleWidget.css`:

```css
.aristotle-fab {
  background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
}
```

### Adding Custom Greetings

Edit the initial message in `AristotleWidget.tsx`:

```tsx
const [messages, setMessages] = useState<Message[]>([
  {
    role: 'assistant',
    content: 'Your custom greeting here!',
    timestamp: new Date()
  }
]);
```

## Backend Requirements

The widget requires the AI-stotle backend running with these endpoints:

- `POST /ask` - Main question endpoint
- `GET /health` - Health check
- `GET /meta.json` - API metadata
- `GET /experiments/search` - Search experiments

Ensure CORS is configured to allow your frontend domain.

## Deployment

### Option 1: Static Hosting (Netlify, Vercel)

```bash
npm run build
# Deploy dist/ folder
```

### Option 2: Embed in Existing Site

1. Build the widget: `npm run build`
2. Include the generated JS/CSS in your HTML:

```html
<link rel="stylesheet" href="/path/to/widget.css">
<script src="/path/to/widget.js"></script>
<div id="aristotle-widget-root"></div>
```

### Option 3: npm Package

Package for distribution:

```bash
npm pack
# Install in other projects: npm install ./aristotle-widget-1.0.0.tgz
```

## Environment Variables

Create `.env` file:

```bash
VITE_API_URL=http://localhost:8000
VITE_DEFAULT_AGE=10
```

Use in code:

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

## Browser Support

- Chrome/Edge: ✅ Latest 2 versions
- Firefox: ✅ Latest 2 versions
- Safari: ✅ Latest 2 versions
- Mobile: ✅ iOS Safari, Chrome Android

## Performance

- Initial load: ~50KB gzipped
- API response: ~1-2s average
- Embeddings: Local (zero latency)
- Smooth 60fps animations

## Troubleshooting

### Widget not appearing?

1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in backend `main.py`
3. Open browser console for errors

### API requests failing?

1. Verify `apiUrl` prop matches backend
2. Check CORS configuration
3. Test endpoint directly: `curl http://localhost:8000/ask -X POST -H "Content-Type: application/json" -d '{"question":"test"}'`

### TypeScript errors?

```bash
npm install
npm run build
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-org/AI-stotle_brain/issues
- Email: support@carlsnewton.com

---

Built with ❤️ for Carls Newton Science Shows • Dubai, UAE
