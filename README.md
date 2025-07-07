# Chaldean Numerology Calculator

A comprehensive web application for Chaldean numerology calculations and interpretations, built with FastAPI and modern web technologies.

## Features

- **Personal Numerology Reports**: Calculate Name Number, Birth Number, and Destiny Number
- **Compatibility Analysis**: Compare numerological compatibility between two people
- **Interactive Web Interface**: Beautiful, responsive design with real-time calculations
- **Historical Context**: Learn about the ancient Babylonian system of numerology
- **API Endpoints**: RESTful API for integration with other applications

## Quick Start

### Using UV (Recommended)

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies and run:

```bash
uv run main.py
```

The application will start on `http://localhost:8000`

### Manual Installation

1. Install dependencies:
```bash
uv sync
```

2. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. Run the application:
```bash
python main.py
```

## About Chaldean Numerology

Chaldean numerology is one of the oldest known systems of numerology, originating over 4,000 years ago in ancient Babylon. Unlike other numerological systems:

- Uses vibrational-based letter assignments (not sequential)
- Considers number 9 as sacred (excluded from letter chart)
- Emphasizes compound numbers with deeper meanings
- Focuses on the name you're commonly known by

### The Chaldean Chart

| Number | Letters | Key Energies |
|--------|---------|-------------|
| 1 | A, I, J, Q, Y | Leadership, independence |
| 2 | B, K, R | Sensitivity, cooperation |
| 3 | C, G, L, S | Creativity, expression |
| 4 | D, M, T | Stability, practicality |
| 5 | E, H, N | Freedom, adaptability |
| 6 | U, V, W, X | Harmony, responsibility |
| 7 | O, Z | Intuition, spirituality |
| 8 | F, P | Power, material success |
| 9 | *Sacred* | Universal love, completion |

## API Endpoints

- `GET /` - Home page with calculator
- `POST /calculate` - Generate numerology report (JSON)
- `POST /calculate-form` - Generate report from form submission
- `GET /compatibility` - Compatibility calculator page
- `POST /compatibility` - Calculate compatibility (JSON)
- `POST /quick-calculate` - Quick text calculation
- `GET /about` - Information about Chaldean numerology
- `GET /api/chart` - Get the Chaldean chart data
- `GET /health` - Health check endpoint

## Technology Stack

- **Backend**: FastAPI, Python 3.12+
- **Frontend**: Bootstrap 5, Jinja2 templates, Vanilla JavaScript
- **Package Management**: UV
- **Validation**: Pydantic
- **Styling**: Custom CSS with modern gradients and animations

## Project Structure

```
numerology/
├── main.py                 # FastAPI application
├── chaldean_calculator.py  # Core numerology logic
├── models.py              # Pydantic data models
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── report.html
│   ├── compatibility.html
│   └── about.html
├── static/               # CSS and JavaScript
│   ├── style.css
│   └── script.js
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

Numerology is a tool for self-reflection and personal insight. While it can provide valuable guidance, it should be used as a complement to, not a replacement for, critical thinking and personal responsibility in making life decisions.
