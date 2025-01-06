# Repast 🍽️

An AI-powered restaurant discovery tool that helps you find and evaluate local restaurants through detailed analysis of reviews and ratings. ✨

## Features

- 🔍 Search for restaurants by location (zip code or address)
- 🌮 Filter by cuisine type or keywords
- 🤖 AI-powered analysis of customer reviews
- ⭐️ Detailed restaurant information including ratings, hours, and contact details
- 🎯 Smart recommendations based on review sentiment and patterns

## Project Structure 🏗️

```bash
repast/
├── api/        # Flask backend
├── www/        # SvelteKit frontend
└── shared/     # Shared types/configs
```

## Getting Started 🚀

### Prerequisites 📋

- Python 3.12+ 🐍
- Node.js 18+ ⚡️
- Poetry (Python dependency management) 📦
- pnpm (Node.js package management) 📦

### Backend Setup 🛠️

1. Navigate to the API directory:
```bash
cd api
```

2. Install dependencies:
```bash
poetry install
```

3. Create a `.env` file with required API keys:
```bash
GOOGLE_PLACES_API_KEY=your_key_here
GOOGLE_AI_API_KEY=your_key_here
JWT_SECRET_KEY=your_key_here
```

4. Start the Flask server:
```bash
poetry run python -m repast.main
```

### Frontend Setup 💻

1. Navigate to the frontend directory:
```bash
cd www
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm dev
```

## API Documentation 📚

The backend provides the following endpoints:

- 🔍 `POST /api/search` - Search for restaurants by location and keyword
- ℹ️ `GET /api/place-details/<place_id>` - Get detailed information about a specific place
- 🔑 `POST /api/auth` - Authenticate and receive JWT token

## Contributing 🤝

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- 🗺️ Powered by Google Places API
- 🧠 AI analysis provided by Google Gemini
- ⚡️ Built with Flask and SvelteKit

I've added emojis to:
1. Section headers to make them stand out
2. Technical requirements to make them more visually interesting
3. API endpoints to make them easier to scan
4. Acknowledgments to make them more visually appealing

I also fixed the Python module name in the backend setup from `miette.main` to `repast.main`. Would you like me to adjust any of the emojis or add more visual elements?