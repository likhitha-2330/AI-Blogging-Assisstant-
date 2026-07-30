# AI Blogging Assistant

AI Blogging Assistant is a Streamlit-based application that helps content creators, developers, and bloggers generate high-quality SEO-optimized blog content using Google's Gemini AI. The application can generate blog topics, detailed outlines, complete Markdown articles, SEO metadata, social media content, and optional AI-generated cover images.

---

# Features

- Generate SEO-friendly blog topic ideas
- Keyword suggestions for improved search ranking
- Create structured blog outlines
- Generate complete Markdown blog articles
- SEO title and meta description generation
- URL slug generation
- Social media content for Twitter/X, LinkedIn, and Instagram
- AI-generated blog cover images (optional)
- Download generated articles as Markdown files
- Session-based content management

---

# Tech Stack

### Frontend

- Streamlit

### Backend

- Python 3.8+

### AI Models

- Google Gemini (google-genai)
- OpenAI Images API (Optional)

### Libraries

- Streamlit
- google-genai
- OpenAI
- python-dotenv
- Pillow

---

# Project Structure

```
AI-Blogging-Assisstant-/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── __pycache__/
```

---

# Application Workflow

The application provides four major AI-powered tools:

## 1. Topic & Keyword Finder

Generate multiple SEO-friendly blog ideas based on a niche and target audience.

Returns:

- Blog Topics
- SEO Keywords
- Search Intent
- Difficulty Level
- Attention-Grabbing Hook

---

## 2. Outline & Section Builder

Creates a complete blog structure including:

- Introduction
- Headings
- Subheadings
- Talking Points
- Recommended Word Count per Section

The generated outline is stored using Streamlit Session State.

---

## 3. Full Blog Post Writer

Generates a complete publication-ready Markdown article.

Includes:

- Title
- Headings
- Subheadings
- Bullet Points
- Blockquotes
- Conclusion
- Summary

Users can download the generated article as a Markdown (.md) file.

---

## 4. SEO & Social Kit Generator

Automatically creates:

- SEO Title
- Meta Description
- URL Slug
- Twitter/X Post
- LinkedIn Post
- Instagram Caption

---

# Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key

OPENAI_API_KEY=your_openai_api_key
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/likhitha-2330/AI-Blogging-Assisstant-.git

cd AI-Blogging-Assisstant-
```

---

## Create Virtual Environment (Optional)

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Keys

Create a `.env` file and add:

```env
GEMINI_API_KEY=your_gemini_api_key

OPENAI_API_KEY=your_openai_api_key
```

> **Note:** `OPENAI_API_KEY` is optional. If it is not provided, the application displays a placeholder cover image instead of generating one with AI.

---

## Run the Application

```bash
streamlit run app.py
```

Open your browser and visit:

```
http://localhost:8501
```

---

# Dependencies

Main packages used in this project:

- Streamlit
- google-genai
- OpenAI
- python-dotenv
- Pillow

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# How to Use

### Step 1

Launch the application.

---

### Step 2

Choose one of the available tools from the sidebar.

---

### Step 3

Enter the required information such as:

- Blog Topic
- Keywords
- Audience
- Writing Tone
- Target Word Count

---

### Step 4

Generate AI-powered content.

---

### Step 5

Download the generated Markdown article or copy the SEO and social media content.

---

# Development

A development container is included inside:

```
.devcontainer/
```

It automatically:

- Opens the project
- Runs Streamlit
- Forwards Port **8501**

Default startup command:

```bash
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

---

# Security & Privacy

- Never commit your API keys to GitHub.
- Store API keys securely inside the `.env` file.
- Add `.env` to `.gitignore`.
- Generated content is sent to external AI services (Google Gemini and OpenAI), so avoid submitting confidential or sensitive information.

---

# Troubleshooting

## Gemini API Key Missing

Ensure that:

```env
GEMINI_API_KEY=your_api_key
```

is present in the `.env` file.

---

## OpenAI Image Generation Failed

If the OpenAI API key is missing or invalid, the application automatically uses a placeholder cover image.

---

## Streamlit Port Already in Use

By default, Streamlit uses:

```
8501
```

Stop the existing process or configure a different port.

---

# Future Improvements

- User authentication
- Blog history management
- Export to PDF
- Multi-language blog generation
- Custom AI prompt templates
- Dark mode
- Blog publishing integration (Medium, WordPress)
- GitHub Actions CI/CD
- Unit testing
- Docker support

---

# Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

Please include clear commit messages and update documentation where necessary.

---

# License

This repository currently does not include a license.

For open-source distribution, adding the **MIT License** is recommended.

---

# Author

**Likhitha Pogaku**

Computer Science Engineering Student

Passionate about Artificial Intelligence, Generative AI, Full Stack Development, and Building AI-powered Applications.

---

# Acknowledgements

- Google Gemini
- OpenAI
- Streamlit
- Python
- Pillow
- python-dotenv
