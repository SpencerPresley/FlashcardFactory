![Flash-Factory](./public/FlashFactory.png)

## Table of Contents

- [FlashcardFactory](#flashcardfactory)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [How It Works](#how-it-works)
  - [Tech Stack](#tech-stack)
  - [Technologies Used](#technologies-used)
  - [Usage](#usage)
    - [Using our Hosted Site](#using-our-hosted-site)
    - [Running Locally](#running-locally)
      - [Prerequisites](#prerequisites)
      - [Installation](#installation)
      - [Using Docker (Recommended)](#using-docker-recommended)
    - [How to Use](#how-to-use)
  - [Exporting to Quizlet](#exporting-to-quizlet)
  - [Project Structure](#project-structure)
  - [Acknowledgments](#acknowledgments)

## Overview

FlashcardFactory is an intelligent study tool that automatically generates customized flashcards from educational materials. The application uses AI to analyze uploaded documents and create study cards tailored to your preferences and educational level.

## Features

- **Document Processing**: Upload various document formats (.pdf, .ppt, .docx, .txt)
- **Customization Options**: Set course name, subject, difficulty level, and educational level
- **Content Control**: Specify rules or special instructions for flashcard generation
- **Quantity Control**: Choose how many flashcards to generate
- **AI-Powered**: Utilizes Gemini AI models to extract and organize key information

## How It Works

1. **Upload Documents**: Provide lecture notes, textbooks, or study materials
2. **Set Preferences**: Customize the flashcards to your specific needs
3. **Generate**: The AI processes your materials and creates tailored flashcards
4. **Study**: View and use the generated flashcards in an easy-to-use interface

## Tech Stack

- **Backend**: Python with FastAPI
- **AI Processing**: Google's Gemini AI models
- **Document Parsing**: Multiple document format support (PDF, DOCX, PPT, TXT)
- **Frontend**: HTML/CSS with Jinja2 templates
- **Development & Deployment**: Docker and Docker Compose for containerization

## Technologies Used

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white" alt="Jinja2" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini" />
</div>

## Usage

You can use FlashcardFactory either through our hosted web application or by running it locally on your machine.

### Using our Hosted Site

For the quickest experience with no setup required, visit our hosted application at:

[HOSTED_SITE_URL_PLACEHOLDER]

### Running Locally

You can run FlashcardFactory locally either with Docker (recommended) or by setting up Python directly.

#### Prerequisites

- Python 3.8+ (if not using Docker)
- Docker and Docker Compose (for Docker method)
- Google API key (for Gemini AI)

#### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/HenHacks2025.git
   cd HenHacks2025
   ```

2. Set up your environment variables

   ```bash
   # Create a .env file with your Google API key
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. Choose one of the following methods to run the application:

#### Using Docker (Recommended)

The easiest way to run FlashcardFactory locally is with Docker:

1. Make sure Docker and Docker Compose are installed on your system

2. Run the application:

   ```bash
   chmod +x run_docker.sh
   ```

   ```bash
   ./run_docker.sh
   ```

   Alternatively, you can use Docker Compose directly:

   ```bash
   docker compose up -d
   ```

3. Open your browser and navigate to `http://localhost:8000`

4. To view logs:

   ```bash
   docker compose logs -f
   ```

5. To stop the application:

   ```bash
   docker compose down
   ```

**If you prefer not to use Docker**, you can run directly with Python:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

2. Run the application:

   ```bash
   sh run.sh
   # or
   uvicorn server:app --reload
   ```

3. Open your browser and navigate to `http://localhost:8000`

### How to Use

Once you have the application running (either hosted or locally):

1. Upload your study materials through the web interface
2. Fill in the form with your preferences:
   - Course name
   - Subject
   - Difficulty level (easy, medium, hard)
   - School level
   - Any specific rules for flashcard creation
   - Number of flashcards to generate
3. Click "Create Flashcards!"
4. View and use your AI-generated flashcards directly on our website

## Exporting to Quizlet

While our application provides a built-in flashcard interface, you can also export your flashcards to Quizlet:

1. After generating your flashcards, download the text file containing your flashcards
2. Go to [Quizlet](https://quizlet.com) and create an account or sign in
3. Click "Create" to start a new study set
4. Select "Import" from the available options
5. In the import settings, choose:
   - "Between term and definition" → Comma (,)
   - "Between cards" → Semicolon (;)
6. Paste the contents of your downloaded flashcards text file
7. Click "Import" to create your Quizlet study set
8. Review and make any final adjustments to your flashcards

## Project Structure

```
.
├── public/               # Public assets
├── src/
│   ├── backend/
│   │   ├── ai/           # AI processing modules
│   │   ├── models/       # Data models
│   │   ├── parsers/      # Document parsing logic
│   │   └── prompts/      # AI prompt templates
│   └── frontend/
│       ├── static/       # CSS, JavaScript
│       └── templates/    # HTML templates
├── server.py             # FastAPI server
├── requirements.txt      # Python dependencies
└── run.sh                # Startup script
```

## Acknowledgments

- Created during HenHacks 2025
- Powered by Google's Gemini AI models
