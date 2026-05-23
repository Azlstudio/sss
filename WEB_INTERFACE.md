# 🌐 LocalAI Assistant - Web Interface

Modern, minimalist ChatGPT-style web interface for the LocalAI Assistant.

## Features

✨ **Modern Design**
- Dark gray color scheme (#0f0f0f, #1a1a1a, #2a2a2a)
- Rounded corners and smooth animations
- Responsive design (desktop and mobile)
- Light theme option

🎨 **User Experience**
- Clean, intuitive chat interface
- Real-time message streaming
- Domain switcher (FiveM, MTA, Design, Programming)
- Memory statistics viewer
- Settings panel

⚡ **Performance**
- Fast, responsive interface
- No heavy frameworks (vanilla JavaScript)
- Instant domain switching
- Efficient REST API

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama (if not already running)

```bash
ollama serve
```

### 3. Start the Web Server

```bash
python web_server.py
```

The web interface will be available at:
```
http://localhost:5000
```

## File Structure

```
web/
├── public/
│   ├── index.html              # Main interface
│   └── static/
│       ├── styles.css          # Modern styling (1000+ lines)
│       └── script.js           # Client logic
└── ...

web_server.py                   # Flask backend
```

## Components

### Sidebar
- **Logo** - LocalAI branding
- **Domain Selector** - Switch between specializations
  - General
  - FiveM (with icon)
  - MTA (with icon)
  - Design (with icon)
  - Programming (with icon)
- **Actions**
  - Memory Stats
  - Clear Memory

### Chat Area
- **Welcome Message** - On first load
- **Messages** - User and assistant messages
  - Smooth animations
  - Timestamps
  - Markdown-like formatting
  - Responsive layout

### Input Area
- **Textarea** - Auto-expanding input
- **Send Button** - Round, accessible
- **Status Info** - Privacy reminders

### Header
- **Title** - "LocalAI Assistant"
- **Settings** - Configure parameters

## Design Details

### Color Palette

```css
/* Dark Gray Theme */
--bg-primary: #0f0f0f       /* Main background */
--bg-secondary: #1a1a1a     /* Sidebar, modals */
--bg-tertiary: #2a2a2a      /* Buttons, cards */
--bg-hover: #353535         /* Hover states */

--text-primary: #ffffff     /* Main text */
--text-secondary: #d1d5db   /* Secondary text */
--text-tertiary: #9ca3af    /* Tertiary text */

--accent-color: #6366f1     /* Interactive elements */
--accent-hover: #4f46e5
```

### Rounded Corners

- **Small**: 6px (form elements)
- **Medium**: 12px (buttons, inputs)
- **Large**: 16px (messages, modals)

### Spacing

- Consistent 8px/12px/16px/24px/32px grid
- Proper breathing room around elements
- Responsive padding on mobile

## API Endpoints

### Chat

**POST** `/api/chat`

```json
{
  "query": "How do I create a job system?",
  "domain": "fivem"
}
```

Response:

```json
{
  "response": "To create a job...",
  "domain": "fivem",
  "facts_learned": ["QBCore uses Lua"],
  "thinking": "Optional reasoning steps"
}
```

### Domain Management

**GET** `/api/domain`
- Get current domain

**POST** `/api/domain`
- Set current domain

**GET** `/api/domains`
- List available domains

### Memory

**GET** `/api/memory`
- Get memory statistics
- Returns vector store, fact store, and conversation stats

### Learning

**POST** `/api/learn`
- Learn from a file

**POST** `/api/project`
- Learn from a project directory

### Preferences

**GET** `/api/preferences?key=framework`
- Get a preference

**POST** `/api/preferences`
- Set a preference

### Export

**POST** `/api/export`
- Export memories to file

## Usage Examples

### Basic Chat

1. Open http://localhost:5000
2. Type: "How do I use loops in Lua?"
3. Press Enter or click Send
4. Get instant response with memory context

### Switch Domain

1. Click domain button (FiveM, MTA, Design, etc.)
2. Ask domain-specific questions
3. Assistant uses specialized knowledge

### Learn from Code

API request:
```bash
curl -X POST http://localhost:5000/api/learn \
  -H "Content-Type: application/json" \
  -d '{"filepath": "./my_script.lua"}'
```

### Check Memory

1. Click "Memory Stats" in sidebar
2. See:
   - Total semantic memories
   - Stored facts
   - Known projects
   - Interaction logs

## Styling

### Light Theme

Toggle in Settings to enable light theme:
- Light gray backgrounds
- Dark text
- Same rounded corners and spacing

### Dark Theme (Default)

Optimized for:
- Eye comfort in low light
- Reduced eye strain
- Modern appearance

## Responsive Design

### Desktop (>1024px)
- Full sidebar visible
- Chat area takes full width
- Multi-column layouts

### Tablet (768px - 1024px)
- Sidebar auto-collapses
- Responsive grid for tips
- Touch-friendly buttons

### Mobile (<768px)
- Bottom sidebar
- Single column layout
- Full-width messages
- Touch optimizations

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance

### Page Load
- ~200ms initial render
- Lazy load embeddings
- No external CDN (fonts/icons local)

### Chat Response
- ~100ms for API call
- ~2-10s for LLM inference
- Real-time message display

### Memory
- Instant domain switching
- Fast memory retrieval
- Smooth animations (60fps)

## Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line
- **Escape** - Close modal
- **Tab** - Navigate buttons

## Accessibility

- Semantic HTML
- ARIA labels where needed
- High contrast colors
- Readable font sizes
- Keyboard navigation support

## Development

### Add Custom Component

```html
<!-- In index.html -->
<div class="your-component">
  <button class="btn-primary">Click me</button>
</div>
```

```css
/* In styles.css */
.your-component {
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
}
```

### Add API Route

```python
# In web_server.py
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    data = request.json
    # Do something
    return jsonify({'result': 'success'})
```

```javascript
// In script.js
const response = await fetch('/api/your-endpoint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({/* data */})
});
```

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure `ollama serve` is running
- Check http://localhost:11434

### Slow responses
- Check `/api/memory` for memory size
- Reduce max_tokens in settings
- Use smaller model

### White screen on load
- Check browser console (F12)
- Verify http://localhost:5000 is accessible
- Check Flask server logs

### Domain switch not working
- Refresh the page
- Check API endpoint in network tab
- Verify domain is in available list

## Future Enhancements

- [ ] Dark/Light mode toggle (implemented, needs testing)
- [ ] Voice input (Whisper integration)
- [ ] Code syntax highlighting
- [ ] Image upload support
- [ ] File sharing
- [ ] Conversation export
- [ ] Multi-turn reasoning display
- [ ] Real-time memory indexing display
- [ ] Collaborative memory (multi-user)

## License

Same as LocalAI Assistant

## Support

- Check WEB_INTERFACE.md for this documentation
- Check README.md for general help
- Check logs at `logs/assistant.log`

---

**Modern. Minimalist. Local. Private.**

Everything stays on your machine. No external APIs. No tracking.

Start the web server and explore: `python web_server.py`
