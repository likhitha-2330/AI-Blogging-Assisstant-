import streamlit as st
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

from openai import OpenAI

openai_client = None
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
else:
    st.sidebar.warning("⚠️ OPENAI_API_KEY not found. Blog cover images will use a generated placeholder.")

# Page configuration
st.set_page_config(
    page_title="AI Blogging Assistant | Streamlit & Gemini",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)
def create_placeholder_blog_image(title):
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGB", (1024, 1024), color=(18, 24, 40))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except Exception:
        font = ImageFont.load_default()

    draw.text((80, 320), "AI Blog Cover", fill=(255, 255, 255), font=font)
    draw.text((80, 390), title[:70], fill=(255, 120, 60), font=font)
    draw.rectangle((80, 470, 944, 520), fill=(255, 120, 60))
    return image


def generate_blog_image(prompt, title="Blog Cover"):
    if not openai_client:
        return create_placeholder_blog_image(title)

    try:
        response = openai_client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
        )

        if getattr(response, "data", None):
            first_item = response.data[0]
            image_base64 = getattr(first_item, "b64_json", None)

            if image_base64:
                import base64
                from io import BytesIO
                from PIL import Image

                return Image.open(BytesIO(base64.b64decode(image_base64)))
    except Exception as exc:
        st.warning(f"OpenAI image generation failed; using a placeholder image instead. ({exc})")

    return create_placeholder_blog_image(title)

# Custom Styling for Streamlit
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fbff 0%, #eef6ff 45%, #e6f0ff 100%);
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f4c81;
        margin-bottom: 0.2rem;
        text-shadow: none;
    }

    .sub-header {
        font-size: 1.0rem;
        color: #35536b;
        margin-bottom: 1.5rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #1f7a8c 0%, #3db6c6 100%);
        color: #ffffff;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        box-shadow: 0 6px 16px rgba(31, 122, 140, 0.18);
        padding: 0.5rem 1rem;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #3db6c6 0%, #1f7a8c 100%);
        color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stSlider>div>div>div {
        background-color: #ffffff;
        color: #112233;
        border: 1px solid #c8d8e8;
        border-radius: 8px;
    }

    .stSidebar {
        background: linear-gradient(180deg, #f4f9ff 0%, #e9f3ff 100%);
        border-right: 1px solid rgba(15, 76, 129, 0.12);
    }

    .stSidebar .st-bd,
    .stSidebar p,
    .stSidebar label,
    .stSidebar h1,
    .stSidebar h2,
    .stSidebar h3 {
        color: #123148;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Gemini API Client Setup
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.sidebar.error("⚠️ GEMINI_API_KEY not found in environment variables.")
    api_key_input = st.sidebar.text_input("Enter Gemini API Key:", type="password")
    if api_key_input:
        api_key = api_key_input

@st.cache_resource
def get_gemini_client(key):
    if not key:
        return None
    return genai.Client(api_key=key)

client = get_gemini_client(api_key)

# Sidebar Navigation
st.sidebar.title("📝 AI Blogging Assistant")
st.sidebar.caption("Powered by Google Gemini 3.6 Flash & Streamlit")

mode = st.sidebar.radio(
    "Choose Assistant Tool:",
    [
        "🎯 Topic & Keyword Finder",
        "📑 Outline & Section Builder",
        "✍️ Full Blog Post Writer",
        "🚀 SEO & Social Kit Generator"
    ]
)

# Tone and Style options in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Content Parameters")
selected_tone = st.sidebar.selectbox(
    "Writing Tone:",
    ["Professional & Authoritative", "Conversational & Engaging", "Tech & Brutalist", "Storytelling & Educational", "Persuasive & Marketing"]
)
target_word_count = st.sidebar.slider("Target Word Count:", 500, 2500, 1000, 250)

# -------------------------------------------------------------
# MODE 1: Topic & Keyword Finder
# -------------------------------------------------------------
if mode == "🎯 Topic & Keyword Finder":
    st.markdown('<div class="main-header">🎯 SEO Topic & Keyword Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover trending, high-ranking blog ideas tailored to your audience.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Blog Niche / Industry:", "Generative AI & Software Engineering")
    with col2:
        audience = st.text_input("Target Audience:", "Developers, Tech Leads, AI Enthusiasts")

    if st.button("✨ Generate Blog Topics"):
        if not client:
            st.error("Please provide a valid Gemini API Key to proceed.")
        else:
            with st.spinner("Analyzing search intent & generating topics with Gemini..."):
                prompt = f"""
You are an expert SEO Content Strategist.
Niche: {niche}
Audience: {audience}
Tone: {selected_tone}

Generate 5 high-converting, SEO-optimized blog topic ideas.
Return JSON format with structure:
{{
  "topics": [
    {{
      "title": "Catchy SEO Title",
      "hook": "1-2 sentence compelling tagline",
      "targetKeywords": ["keyword1", "keyword2", "keyword3"],
      "searchIntent": "Informational | Commercial",
      "difficulty": "Easy | Medium | Hard"
    }}
  ]
}}
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                    data = json.loads(response.text)
                    st.success("Generated Topic Ideas:")
                    for i, topic in enumerate(data.get("topics", [])):
                        with st.expander(f"📌 {i+1}. {topic.get('title')}", expanded=True):
                            st.write(f"**Hook:** {topic.get('hook')}")
                            st.write(f"**Keywords:** {', '.join(topic.get('targetKeywords', []))}")
                            c1, c2 = st.columns(2)
                            c1.metric("Search Intent", topic.get("searchIntent"))
                            c2.metric("SEO Difficulty", topic.get("difficulty"))
                except Exception as e:
                    st.error(f"Error generating topics: {e}")

# -------------------------------------------------------------
# MODE 2: Outline & Section Builder
# -------------------------------------------------------------
elif mode == "📑 Outline & Section Builder":
    st.markdown('<div class="main-header">📑 Outline & Section Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Structure headlines, subheadings, and key talking points before writing.</div>', unsafe_allow_html=True)

    topic = st.text_input("Blog Topic / Headline:", "The Future of AI Code Generation & Developer Productivity")
    keywords = st.text_input("Target Keywords (comma-separated):", "AI code generator, Gemini 3.6, software engineering")

    if st.button("📑 Generate Detailed Outline"):
        if not client:
            st.error("Please provide a valid Gemini API Key.")
        else:
            with st.spinner("Structuring blog hierarchy with Gemini..."):
                prompt = f"""
Create a detailed blog post outline for:
Topic: {topic}
Keywords: {keywords}
Tone: {selected_tone}
Target Length: {target_word_count} words

Return JSON format:
{{
  "title": "{topic}",
  "sections": [
    {{
      "heading": "H2 Heading",
      "talkingPoints": ["Point 1", "Point 2"],
      "wordCount": 200
    }}
  ],
  "keyTakeaways": ["Takeaway 1", "Takeaway 2"],
  "callToAction": "Suggested CTA"
}}
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                    outline = json.loads(response.text)
                    st.session_state["blog_outline"] = outline
                    st.subheader(outline.get("title"))
                    for sec in outline.get("sections", []):
                        st.markdown(f"### {sec.get('heading')} ({sec.get('wordCount', 200)} words)")
                        for point in sec.get("talkingPoints", []):
                            st.markdown(f"- {point}")
                    st.success("Outline saved to session state!")
                except Exception as e:
                    st.error(f"Error generating outline: {e}")

# -------------------------------------------------------------
# MODE 3: Full Blog Post Writer
# -------------------------------------------------------------
elif mode == "✍️ Full Blog Post Writer":
    st.markdown('<div class="main-header">✍️ Full Blog Post Writer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate publication-ready Markdown articles complete with code & examples.</div>', unsafe_allow_html=True)

    blog_title = st.text_input("Blog Article Title:", "Navigating the New Frontier of Generative AI")
    keywords_list = st.text_input("Focus Keywords:", "Generative AI, Machine Learning, Future of Work, Ethics")

    if st.button("🚀 Write Full Article"):
        if not client:
            st.warning("Gemini API key is not available. Showing a fallback article draft and blog cover image.")
            article_markdown = f"""# {blog_title}

## Overview
This is a fallback article draft created because Gemini is currently unavailable.

## Why This Topic Matters
- It helps readers understand the subject quickly.
- It offers a practical starting point for further research.
- It can be expanded into a full publication-ready article later.

## Key Takeaways
- Start with a clear headline.
- Keep the structure easy to scan.
- Add actionable insights and examples.
"""
        else:
            with st.spinner("Drafting full blog post with Gemini 3.6 Flash..."):
                prompt = f"""
You are an expert senior tech blogger writing a complete publication-ready article in Markdown.
Topic: {blog_title}
Keywords: {keywords_list}
Tone: {selected_tone}
Target Word Count: {target_word_count} words

Requirements:
- Add a compelling H1 title.
- Introduction with a strong hook.
- Well-structured H2 and H3 subheadings with actionable insights.
- Bullet points, bold key phrases, and blockquotes.
- Summary block with Key Takeaways at the end.
- Avoid robotic fluff words.
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    article_markdown = response.text
                except Exception as e:
                    st.error(f"Error drafting blog post: {e}")
                    article_markdown = f"""# {blog_title}

## Overview
A fallback article draft is being shown because the AI generation step failed.
"""

        image_prompt = f"""
Create a modern, high-quality blog cover image for:

Title: {blog_title}

Style:
- Professional
- Minimal
- Clean
- High quality
- No text
- Digital illustration
"""

        with st.spinner("Generating blog cover image..."):
            blog_image = generate_blog_image(image_prompt, blog_title)

        st.image(
            blog_image,
            caption="AI Generated Blog Cover",
            use_container_width=True
        )
        st.session_state["latest_article"] = article_markdown

        st.markdown("---")
        st.markdown(article_markdown)

        st.download_button(
            label="📥 Download Article (.md)",
            data=article_markdown,
            file_name=f"{blog_title.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )

# -------------------------------------------------------------
# MODE 4: SEO & Social Kit Generator
# -------------------------------------------------------------
elif mode == "🚀 SEO & Social Kit Generator":
    st.markdown('<div class="main-header">🚀 SEO & Social Media Kit Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Auto-generate Meta Descriptions, URL Slugs, Tweets, and LinkedIn posts.</div>', unsafe_allow_html=True)

    sample_article = st.text_area("Paste Article or Enter Title:", st.session_state.get("latest_article", "Generative AI is transforming creative workflows across art, coding, and writing."))

    if st.button("⚡ Generate Marketing & SEO Kit"):
        if not client:
            st.error("Please provide a valid Gemini API Key.")
        else:
            with st.spinner("Optimizing SEO & social teasers with Gemini..."):
                prompt = f"""
Analyze this blog content and generate an SEO + Social Media Kit:
Article:
{sample_article[:1500]}

Return JSON format:
{{
  "seoTitle": "Optimized Page Title (50-60 chars)",
  "metaDescription": "Compelling Meta Description (140-155 chars)",
  "urlSlug": "kebab-case-slug",
  "twitterX": "Engaging Twitter thread starter with hashtags",
  "linkedIn": "Professional LinkedIn post summary with bullet points",
  "instagram": "Instagram caption with hashtags"
}}
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                    kit = json.loads(response.text)

                    colA, colB = st.columns(2)
                    with colA:
                        st.subheader("🔍 Search Engine Optimization")
                        st.text_input("SEO Page Title:", kit.get("seoTitle", ""))
                        st.text_area("Meta Description:", kit.get("metaDescription", ""))
                        st.text_input("URL Slug:", kit.get("urlSlug", ""))

                    with colB:
                        st.subheader("📱 Social Media Distribution")
                        st.text_area("Twitter / X Thread:", kit.get("twitterX", ""))
                        st.text_area("LinkedIn Post:", kit.get("linkedIn", ""))
                        st.text_area("Instagram Caption:", kit.get("instagram", ""))
                except Exception as e:
                    st.error(f"Error generating SEO kit: {e}")
