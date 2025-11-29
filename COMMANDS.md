# 🔧 Common Commands

Quick reference for running your Price Tracker

## Installation

```bash
# Install dependencies (one-time)
pip install -r requirements.txt
```

## Version 1: Simple Script

```bash
# Run the tracker
python src/tracker.py

# Run in background (Linux/Mac)
nohup python src/tracker.py > tracker.log 2>&1 &

# View logs
tail -f tracker.log

# Stop background process
pkill -f "python src/tracker.py"
```

## Version 2: FastAPI API

```bash
# Run with auto-reload (development)
uvicorn src.main:app --reload

# Run on specific port (development)
uvicorn src.main:app --reload --port 8001

# Run without auto-reload (production)
uvicorn src.main:app

# Run on all interfaces (for external access)
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Run with workers (production)
uvicorn src.main:app --workers 4

# Run in background (Linux/Mac)
nohup uvicorn src.main:app > server.log 2>&1 &

# View logs
tail -f server.log

# Stop background server
pkill -f uvicorn
```

## FastAPI Endpoints (with curl)

```bash
# Health check
curl http://localhost:8000/

# List all products
curl http://localhost:8000/products

# Add a product
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 13",
    "url": "https://www.amazon.in/dp/B09V4B6K53/",
    "target_price": 50000
  }'

# Get single product
curl http://localhost:8000/products/1

# Delete a product
curl -X DELETE http://localhost:8000/products/1

# Get price history
curl http://localhost:8000/products/1/history

# Force price check
curl -X POST http://localhost:8000/trigger-scan

# Get system stats
curl http://localhost:8000/stats
```

## Database

```bash
# View price history (V1)
cat data/price_history.csv

# Query SQLite database (V2)
sqlite3 data/tracker.db

# SQLite commands (inside sqlite3)
.tables                    # List tables
SELECT * FROM products;    # View products
SELECT * FROM price_history; # View price logs
.quit                      # Exit
```

## Configuration

```bash
# Edit environment variables
nano .env

# Test if .env is being read
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('EMAIL_USER'))"
```

## Troubleshooting

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify imports work
python -c "import requests, bs4, fastapi; print('All imports OK')"

# Test price scraper directly
python src/scraper.py

# Check if port is in use
lsof -i :8000

# Kill process on specific port
kill -9 $(lsof -t -i:8000)

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Development

```bash
# Start interactive Python shell
python

# Import and test scraper
from src.scraper import fetch_amazon_price
fetch_amazon_price("https://www.amazon.in/dp/...")

# Import and test models
from src.models import Product, PriceLog
```

## Deployment

```bash
# Check if requirements.txt is up to date
pip freeze > requirements_new.txt
diff requirements.txt requirements_new.txt

# Create fresh virtual environment
python -m venv venv_new
source venv_new/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest

# Format code (optional)
black src/

# Lint code (optional)
pylint src/
```

## Monitoring

```bash
# Monitor process (Linux)
watch -n 1 'ps aux | grep -E "python|uvicorn" | grep -v grep'

# Monitor system resources
top

# Check logs for errors
grep -i error *.log

# Monitor specific process
ps aux | grep uvicorn
```

## Git

```bash
# Check git status
git status

# Commit changes
git add .
git commit -m "your message"

# Push to remote
git push origin main

# View git log
git log --oneline
```

## Docker (Optional)

```bash
# Build Docker image
docker build -t price-tracker .

# Run Docker container
docker run -p 8000:8000 price-tracker

# Run with environment file
docker run -p 8000:8000 --env-file .env price-tracker
```

## Useful One-Liners

```bash
# Kill all Python processes
pkill -f python

# Clean all cache and start fresh
find . -type d -name __pycache__ -exec rm -rf {} + && python -m py_compile src/*.py

# Test API is running
curl -s http://localhost:8000/ && echo "✓ API is running"

# Watch file for changes
watch -n 0.5 'cat data/price_history.csv | tail -5'

# Count lines of code
find src -name "*.py" -exec wc -l {} + | tail -1
```

## Quick Testing Checklist

```bash
# 1. Check dependencies
pip install -r requirements.txt

# 2. Test scraper directly
python -c "from src.scraper import fetch_amazon_price; print(fetch_amazon_price('https://www.amazon.in/dp/B09V4B6K53/'))"

# 3. Test database models
python -c "from src.models import Product, PriceLog; print('✓ Models OK')"

# 4. Start API
uvicorn src.main:app --reload

# 5. Test API in another terminal
curl http://localhost:8000/

# 6. Test script version
python src/tracker.py
```
