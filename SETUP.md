# 🔧 LocalAI Assistant - Detailed Setup Guide

Complete step-by-step instructions for setting up the LocalAI Assistant.

## Prerequisites

- **OS**: Windows, macOS, or Linux
- **Python**: 3.10 or higher
- **RAM**: 16GB minimum (32GB recommended)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (for speed), CPU-only mode available
- **Disk**: 50GB+ free space (for models and memory storage)

## Step 1: Install Python

### Windows
Download from https://www.python.org/downloads/
- Select "Add Python to PATH" during installation
- Verify: `python --version`

### macOS / Linux
```bash
# macOS (using Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3-pip
```

Verify installation:
```bash
python3 --version
pip3 --version
```

## Step 2: Install Ollama

Download from https://ollama.ai

### Quick Setup
```bash
# Windows / macOS: Download and run installer
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh
```

### Start Ollama
```bash
# This will start the server on localhost:11434
ollama serve

# In another terminal, pull a model:
ollama pull mistral
```

**Recommended Models**:
- `mistral` - Fast, good quality (7B parameters)
- `llama2` - Slower but more capable (7B/13B)
- `neural-chat` - Fast, optimized (7B)

Check installed models:
```bash
ollama list
```

## Step 3: Clone/Setup Repository

```bash
cd /path/to/sss
# Already in a git repo, so just ensure we're on the right branch
git checkout claude/local-ai-persistent-memory-A4fNA
```

## Step 4: Install Python Dependencies

```bash
# Navigate to project root
cd /path/to/sss

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: First-time setup takes time because sentence-transformers downloads the embedding model (~130MB).

## Step 5: Configure Settings

Edit `config.yaml` to match your setup:

```yaml
llm:
  base_url: "http://localhost:11434"  # Ollama URL
  model: "mistral"                     # Change if needed
  parameters:
    temperature: 0.7                   # 0=factual, 1=creative
    max_tokens: 2048                   # Reduce if out of memory

embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  device: "cuda"  # Change to "cpu" if no GPU
```

**GPU/CPU Selection**:
- `cuda`: NVIDIA GPU (fast, uses VRAM)
- `cpu`: CPU only (slower, uses RAM)
- Check: `python -c "import torch; print(torch.cuda.is_available())"`

## Step 6: Verify Installation

```bash
# Test Python environment
python -c "import assistant; print('✅ Assistant imports OK')"

# Test Ollama connection
python -c "from assistant.core import LLMClient; c = LLMClient(); print('✅ Ollama OK' if c.is_available() else '❌ Ollama not running')"

# Test embeddings
python -c "from assistant.core import EmbeddingEngine; e = EmbeddingEngine(); print('✅ Embeddings OK')"

# Run quick test
python example_usage.py
```

## Step 7: Initial Setup & First Run

### Create Directory Structure
```bash
# Already created by code, but verify
ls -la brain/
# Should show: vectors/, facts/, conversations/, training_data/
```

### Warmup (Optional but Recommended)
First runs download models and build indices. This takes time:
- First Ollama inference: 30-60 seconds (model loading)
- First embedding: 10-30 seconds (model download)
- First vector DB query: 5-10 seconds (index building)

This is one-time only.

```bash
# Run example to warmup
python example_usage.py
```

## Step 8: Start Using

### Interactive CLI (Recommended)
```bash
python cli.py
```

Then:
```
You> /help
You> /domain fivem
You> How do I create a job system?
You> /learn ./my_script.lua
You> /memory
You> /exit
```

### Python Script
```python
from assistant import LocalAIAssistant

assistant = LocalAIAssistant()
result = assistant.chat("Your question here", domain="fivem")
print(result['response'])
```

## Troubleshooting Setup

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### "Ollama not available"
```bash
# Check if running
ollama serve

# In new terminal:
ollama pull mistral
ollama list

# Then test
python -c "from assistant.core import LLMClient; print(LLMClient().is_available())"
```

### "Cannot import sentence_transformers"
```bash
# Reinstall with extras
pip install --upgrade sentence-transformers torch

# If still failing (GPU issues)
pip install sentence-transformers --no-deps
pip install torch
```

### "CUDA not available"
```bash
# Use CPU instead (slower but works)
# Edit config.yaml:
# embeddings:
#   device: "cpu"
```

### "Out of memory"
```bash
# Option 1: Use smaller model
ollama pull neural-chat
# Edit config.yaml: model: "neural-chat"

# Option 2: Reduce token limit
# Edit config.yaml: max_tokens: 1024

# Option 3: Use CPU
# Edit config.yaml: device: "cpu"
```

### "Slow responses"
Check what's running:
```bash
# Monitor GPU/CPU
nvidia-smi        # GPU usage
htop              # CPU/RAM usage (Linux)
```

Solutions:
- Close other applications
- Reduce max_tokens in config
- Increase temperature slightly (0.8)
- Check vector store size with `/memory`

## Performance Tuning

### Fast Mode (Use CPU Inference)
```yaml
llm:
  model: "neural-chat"
  parameters:
    temperature: 0.5
    max_tokens: 1024
embeddings:
  device: "cpu"
```

### Quality Mode (Use GPU)
```yaml
llm:
  model: "mistral"
  parameters:
    temperature: 0.7
    max_tokens: 2048
embeddings:
  device: "cuda"
```

### Balanced Mode
```yaml
llm:
  model: "llama2"
  parameters:
    temperature: 0.6
    max_tokens: 1500
embeddings:
  device: "cuda"
```

## Verify Everything Works

Run complete test:
```bash
python << 'PYEOF'
from assistant import LocalAIAssistant

print("Testing LocalAI Assistant Setup...\n")

assistant = LocalAIAssistant()
print("✅ Assistant initialized")

# Test chat
result = assistant.chat(
    "What is 2+2?",
    domain="general"
)
print(f"✅ Chat working: {result['response'][:50]}...")

# Test memory
stats = assistant.memory_status()
print(f"✅ Memory system: {stats['vector_store']}")

print("\n✅ All systems operational!")
print("Ready to use: python cli.py")
PYEOF
```

## Optional: GPU Optimization

### NVIDIA CUDA Setup
```bash
# Check GPU
nvidia-smi

# Install CUDA toolkit (if needed)
# Download from https://developer.nvidia.com/cuda-toolkit

# Verify PyTorch sees GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Model Size Selection
- `neural-chat`: 7B params, fast on 8GB VRAM
- `mistral`: 7B params, good quality, 8GB+ VRAM
- `llama2`: 7B/13B params, slower, needs more VRAM

## Updating

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update local models
ollama pull mistral
```

## Troubleshooting Checklist

- [ ] Python 3.10+ installed
- [ ] pip working (`pip --version`)
- [ ] Virtual environment active
- [ ] requirements.txt installed
- [ ] Ollama running on 11434
- [ ] Model downloaded (`ollama list`)
- [ ] config.yaml correct (URLs, paths)
- [ ] First test passed (cli.py works)

## Next Steps

1. **Quick Start**: `python cli.py`
2. **Learn Patterns**: `python example_usage.py`
3. **Read**: Check `README.md` for features
4. **Train**: Add custom data to `brain/training_data/`
5. **Extend**: Add new specializations or tools

## Support

If you run into issues:

1. Check logs: `cat logs/assistant.log`
2. Verify Ollama: `ollama serve` (in one terminal)
3. Test Python: Run the verification script above
4. Check config: `cat config.yaml`

---

You're all set! Start with: `python cli.py`
