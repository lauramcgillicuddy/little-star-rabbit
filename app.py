"""
Little Star Rabbit 🌟🐇
A trauma-aware, kid-safe app for one very special star.
"""

import streamlit as st
import json
import os
import time as time_module
from datetime import datetime, time
from openai import OpenAI
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Little Star Rabbit",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
def inject_css():
    """Inject custom CSS for beautiful strawberry milkshake theme with starry magic"""
    st.markdown(
        """
        <style>
        /* --- IMPORT FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&family=Patrick+Hand&display=swap');

        /* --- GLOBAL FONT OVERRIDES --- */
        .stApp, .block-container, .stMarkdown, .stText, .stTextInput, .stNumberInput,
        .stRadio, .stSelectbox, .stTextarea, .stCheckbox, .stButton > button,
        .stTabs [data-baseweb="tab"], label, p, div {
            font-family: "Baloo 2", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        /* Use Patrick Hand for tiny helper text */
        .lsr-note {
            font-family: "Patrick Hand", "Baloo 2", system-ui, sans-serif;
            font-size: 1rem;
        }

        /* Background + layout - with magical stars! */
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.25) 0, transparent 55%),
                radial-gradient(circle at 80% 20%, rgba(255,255,255,0.17) 0, transparent 50%),
                radial-gradient(circle at 10% 80%, rgba(255,255,255,0.18) 0, transparent 55%),
                linear-gradient(180deg, #ffeef7 0%, #fff4ea 45%, #ffe9f2 100%);
            color: #2B102A;
        }
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 900px;
        }

        #MainMenu, footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Titles - bigger and bouncier! */
        h1, h2, h3, .lsr-hero-title {
            font-family: "Baloo 2", system-ui, sans-serif;
            letter-spacing: 0.03em;
        }
        h1 {
            font-size: 2.6rem;
            font-weight: 700;
        }
        h2 {
            font-size: 2.0rem;
            font-weight: 600;
        }
        h3 {
            font-size: 1.5rem;
            font-weight: 600;
        }
        .lsr-hero-title {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.3rem;
        }
        .lsr-hero-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #8a5574;
            margin-bottom: 2.2rem;
            font-family: "Patrick Hand", "Baloo 2", system-ui, sans-serif;
        }

        /* Big CTA buttons on landing */
        .lsr-cta-row {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        .lsr-cta-main {
            border-radius: 999px;
            padding: 0.9rem 2.6rem;
            border: none;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            box-shadow: 0 12px 26px rgba(242, 125, 144, 0.4);
            background: linear-gradient(90deg, #f9739a, #f27d90);
            color: #fffdf8;
        }
        .lsr-cta-secondary {
            border-radius: 999px;
            padding: 0.9rem 2.6rem;
            border: 1px solid #ffd0e1;
            background: #fffdfb;
            font-weight: 500;
            font-size: 0.95rem;
            cursor: pointer;
            color: #4a2037;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.04);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem;
            font-weight: 600;
            padding-top: 0.4rem;
            padding-bottom: 0.4rem;
        }

        /* Child hub card buttons - make entire card clickable */
        div[data-testid="stButton"] > button {
            font-family: "Baloo 2", system-ui, sans-serif;
            border-radius: 1.6rem;
            padding: 1.8rem 1.6rem;
            background: linear-gradient(145deg, #ffffff, #ffe9f4);
            box-shadow: 0 18px 40px rgba(242, 125, 144, 0.35);
            text-align: left;
            border: none;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            cursor: pointer;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            white-space: normal;
            height: auto;
            min-height: 180px;
            font-size: 1rem;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px);
            box-shadow: 0 22px 50px rgba(242, 125, 144, 0.45);
        }

        .lsr-card-icon {
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
            display: block;
        }
        .lsr-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            display: block;
            color: #2B102A;
        }
        .lsr-card-sub {
            font-size: 0.95rem;
            color: #8a5574;
            font-family: "Patrick Hand", "Baloo 2", system-ui, sans-serif;
            display: block;
            line-height: 1.4;
        }

        /* Story box */
        .lsr-story-box {
            border-radius: 1.4rem;
            padding: 1.4rem 1.6rem;
            background: #fffdfb;
            border: 1px solid #ffd9ea;
            box-shadow: 0 12px 30px rgba(242, 125, 144, 0.35);
            line-height: 1.7;
            font-size: 1.02rem;
        }

        /* Fact box */
        .lsr-fact-box {
            border-radius: 1.4rem;
            padding: 1.4rem 1.6rem;
            background: linear-gradient(135deg, #fffef9 0%, #fff8e1 100%);
            border: 2px solid #ffd700;
            box-shadow: 0 12px 30px rgba(255, 215, 0, 0.15);
            line-height: 1.7;
            font-size: 1.02rem;
        }

        /* Feeling boxes */
        .lsr-feeling-box {
            border-radius: 1.2rem;
            padding: 1.3rem 1.5rem;
            background: linear-gradient(135deg, #fff0f5 0%, #ffe6f0 100%);
            border-left: 5px solid #f27d90;
            box-shadow: 0 8px 20px rgba(242, 125, 144, 0.25);
            margin-bottom: 1.5rem;
            font-size: 1.05rem;
        }

        .lsr-info-box {
            border-radius: 1.2rem;
            padding: 1rem 1.3rem;
            background: linear-gradient(135deg, #fff4ea 0%, #ffe9f2 100%);
            border-left: 4px solid #f27d90;
            margin: 1rem 0;
            font-style: italic;
            color: #555;
            text-align: center;
        }

        /* Regular buttons (non-card) - bigger and friendlier */
        .stButton > button:not([data-testid]) {
            font-family: "Baloo 2", system-ui, sans-serif;
            border-radius: 999px;
            font-weight: 500;
            padding: 0.7rem 1.6rem;
            font-size: 0.98rem;
            border: 1px solid #ffd0e1;
            transition: all 0.2s ease;
        }

        .stButton > button:not([data-testid]):hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(242, 125, 144, 0.3);
        }

        /* Primary CTA-style buttons */
        .lsr-primary-btn {
            background: linear-gradient(90deg, #f9739a, #f27d90) !important;
            color: #fffdf8 !important;
            box-shadow: 0 10px 24px rgba(242, 125, 144, 0.4);
            border: none !important;
        }

        /* Soft secondary buttons */
        .lsr-secondary-btn {
            background: #fffdfb !important;
            border: 1px solid #ffd0e1 !important;
            color: #4a2037 !important;
        }

        /* Streamlit widgets */
        .stRadio > label, .stSelectbox > label, .stTextInput > label,
        .stNumberInput > label, .stTextarea > label {
            font-weight: 500;
            color: #4a2037;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Data directory setup
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# File paths
PROFILE_FILE = DATA_DIR / "profile.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
AFFIRMATIONS_FILE = DATA_DIR / "affirmations.json"
LESSONS_FILE = DATA_DIR / "lessons.json"
USAGE_FILE = DATA_DIR / "usage.json"

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "mode": "landing",
        "child_page": "home",
        "admin_page": "profile",
        "admin_authenticated": False,
        "current_story": None,
        "current_facts": None,
        "calm_timer_start": None,
        "calm_timer_duration": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Load/Save functions
def load_json(filepath, default):
    """Load JSON file or return default if not exists"""
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Default data structures
DEFAULT_PROFILE = {
    "child_name": "Little Star",
    "age": 7,
    "pronouns": "she/her",
    "interests": ["space", "animals", "stars"]
}

DEFAULT_SETTINGS = {
    "admin_pin": "1234",  # Default PIN - should be changed!
    "use_ai": True,
    "max_story_length": "medium",
    "banned_topics": {
        "death_illness": True,
        "violence": True,
        "scary_monsters": True
    },
    "reading_level": "simple",
    "custom_word_filters": [],
    "daily_limit_minutes": 20,
    "session_length_minutes": 10,
    "quiet_hours_start": "21:00",
    "quiet_hours_end": "07:00",
    "calm_timer_minutes": 5,  # Default calm timer duration
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 500
}

DEFAULT_AFFIRMATIONS = {
    "happy": [
        "I am allowed to feel joy! 🌟",
        "My happiness is important.",
        "It's wonderful to feel good!"
    ],
    "sad": [
        "It's okay to feel sad sometimes.",
        "My feelings are important.",
        "Sadness is a normal feeling that everyone has."
    ],
    "angry": [
        "It's okay to feel angry.",
        "My feelings matter, even angry ones.",
        "I can feel angry and still be a good person."
    ],
    "worried": [
        "It makes sense to feel worried sometimes.",
        "I am safe right now.",
        "Worries are just thoughts - they can't hurt me."
    ],
    "numb": [
        "Sometimes I don't know what I'm feeling, and that's okay.",
        "I don't have to understand all my feelings right now.",
        "It's okay to just be."
    ],
    "other": [
        "All my feelings are okay.",
        "I am enough, just as I am.",
        "I am loved."
    ]
}

DEFAULT_LESSONS = [
    {
        "id": 1,
        "category": "kindness",
        "title": "Being Kind to Myself",
        "emoji": "💛",
        "content": "Being kind to yourself means treating yourself like you would treat a good friend. If you make a mistake, instead of saying 'I'm so silly!', you can say 'Everyone makes mistakes, and that's okay.'\n\nExample: If you spill your juice, you can think 'Oops! That happens sometimes. I'll clean it up.'\n\nTry this: Next time something goes wrong, take a deep breath and say something nice to yourself.",
        "tags": ["kindness", "self-compassion"]
    },
    {
        "id": 2,
        "category": "brave_brain",
        "title": "Why My Heart Beats Fast",
        "emoji": "🧠",
        "content": "Sometimes when you feel scared or worried, your heart beats really fast. This is your body trying to help you! Your brain thinks there might be danger, so it gets your body ready to run or protect yourself.\n\nThis is totally normal! Even when there's no real danger, your brain might still do this sometimes.\n\nTry this: When your heart beats fast, put your hand on your chest and take 3 slow, deep breaths. This tells your brain 'We're okay, we're safe.'",
        "tags": ["anxiety", "body", "coping"]
    },
    {
        "id": 3,
        "category": "boundaries",
        "title": "Your Body Belongs to You",
        "emoji": "🛡",
        "content": "Your body is yours, and you get to decide who touches it. You can say 'no' to hugs, kisses, or tickles - even from people you love - if you don't want them right now.\n\nIt's okay to say:\n• 'No thank you'\n• 'I don't want a hug right now'\n• 'Please stop'\n\nGrown-ups who love you will understand. Your body, your choice!",
        "tags": ["boundaries", "body", "safety"]
    },
    {
        "id": 4,
        "category": "school",
        "title": "When Homework Feels Too Big",
        "emoji": "📚",
        "content": "Sometimes homework can feel like a huge mountain. Here's a secret: you don't have to climb the whole mountain at once!\n\nBreak it into tiny pieces:\n1. Start with just one problem or one sentence\n2. Take a little break (stretch, have a sip of water)\n3. Do another small piece\n\nTry this: Set a timer for just 5 minutes. Do what you can in those 5 minutes, then take a break. You can ask a grown-up for help too!",
        "tags": ["school", "focus", "coping"]
    }
]

# Load data on startup
profile = load_json(PROFILE_FILE, DEFAULT_PROFILE)
settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
affirmations = load_json(AFFIRMATIONS_FILE, DEFAULT_AFFIRMATIONS)
lessons = load_json(LESSONS_FILE, DEFAULT_LESSONS)

# Override with Streamlit secrets if available (for Streamlit Cloud deployment)
try:
    if hasattr(st, 'secrets'):
        # Override API key if set in secrets
        if 'openai' in st.secrets and 'api_key' in st.secrets['openai']:
            settings['api_key'] = st.secrets['openai']['api_key']

        # Override admin PIN if set in secrets
        if 'admin' in st.secrets and 'pin' in st.secrets['admin']:
            settings['admin_pin'] = st.secrets['admin']['pin']

        # Override profile if set in secrets
        if 'profile' in st.secrets:
            if 'child_name' in st.secrets['profile']:
                profile['child_name'] = st.secrets['profile']['child_name']
            if 'age' in st.secrets['profile']:
                profile['age'] = st.secrets['profile']['age']
            if 'pronouns' in st.secrets['profile']:
                profile['pronouns'] = st.secrets['profile']['pronouns']
            if 'interests' in st.secrets['profile']:
                # Convert comma-separated string to list
                interests_str = st.secrets['profile']['interests']
                profile['interests'] = [i.strip() for i in interests_str.split(',')]
except Exception:
    # Secrets not available (local development) - use JSON files only
    pass

def save_profile():
    save_json(PROFILE_FILE, profile)

def save_settings():
    save_json(SETTINGS_FILE, settings)

def save_affirmations():
    save_json(AFFIRMATIONS_FILE, affirmations)

def save_lessons():
    save_json(LESSONS_FILE, lessons)

# Usage tracking
def get_today_usage():
    """Get minutes used today"""
    usage = load_json(USAGE_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    return usage.get(today, 0)

def add_usage_minutes(minutes):
    """Add minutes to today's usage"""
    usage = load_json(USAGE_FILE, {})
    today = datetime.now().strftime("%Y-%m-%d")
    usage[today] = usage.get(today, 0) + minutes
    save_json(USAGE_FILE, usage)

def check_quiet_hours():
    """Check if current time is in quiet hours"""
    now = datetime.now().time()
    start = datetime.strptime(settings["quiet_hours_start"], "%H:%M").time()
    end = datetime.strptime(settings["quiet_hours_end"], "%H:%M").time()

    if start <= end:
        return start <= now <= end
    else:  # Overnight quiet hours
        return now >= start or now <= end

def check_usage_limit():
    """Check if daily usage limit is reached"""
    used = get_today_usage()
    limit = settings["daily_limit_minutes"]
    return used >= limit

# OpenAI helper
def get_openai_client():
    """Get OpenAI client using Streamlit secrets or environment variable"""
    try:
        # Check if API key is in settings (from Streamlit secrets or local JSON)
        api_key = settings.get('api_key')
        if api_key:
            return OpenAI(api_key=api_key)
        else:
            # Fall back to OPENAI_API_KEY environment variable (for local dev)
            return OpenAI()
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def synthesize_tts(text: str) -> bytes:
    """Convert text to speech using OpenAI TTS - cached for efficiency"""
    if not text:
        return b""
    try:
        client = get_openai_client()
        if not client:
            return b""

        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Warm, friendly female voice
            input=text
        )
        return response.content
    except Exception as e:
        st.error(f"Could not generate audio: {str(e)}")
        return b""

def tts_block(label: str, content: str, key: str):
    """Helper to add a TTS button with audio player"""
    if st.button(label, key=key, use_container_width=True):
        with st.spinner("🎤 Getting ready to read..."):
            audio_bytes = synthesize_tts(content)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

def generate_feelings_response(feeling: str, child_name: str) -> str:
    """Generate GPT response for feelings validation"""
    client = get_openai_client()
    if not client:
        return "⚠️ API key not set. Please ask a grown-up to set it up in the Grown-ups' Corner."

    system_prompt = """You are Little Star Rabbit, a gentle, kid-safe emotional support bunny talking to a child.
The child is between 7 and 10 years old. Use simple sentences, no heavy topics, no
mention of diagnoses or trauma. Always be validating and kind, never shaming.
Avoid talking about harm, death, abuse, or scary things. Focus on feelings,
self-kindness, and asking a trusted grown-up for help when needed.

Format your response in three parts:
1. VALIDATION: 1-2 sentences validating the feeling
2. SUGGESTION: 1 short, gentle idea for something they can try (like bunny breaths or talking to someone)
3. AFFIRMATIONS: 3 short affirmations as bullet points"""

    user_prompt = f"{child_name} is feeling {feeling}. Please respond with validation, a gentle suggestion, and 3 affirmations."

    try:
        response = client.chat.completions.create(
            model=settings.get("model", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble thinking right now. Maybe try again in a moment? 🌟"

def generate_lesson_text(topic: str, child_name: str) -> str:
    """Generate GPT response for Little Lessons"""
    client = get_openai_client()
    if not client:
        return "⚠️ API key not set. Please ask a grown-up to set it up in the Grown-ups' Corner."

    system_prompt = """You are Little Star Rabbit, a gentle, kid-safe teacher. Explain the selected topic
to a 7–10 year old child. Use simple language, short paragraphs, and examples.
Avoid all scary topics and heavy psychology words. Focus on kindness, self-compassion,
boundaries, and small practical ideas.

Structure:
- A short explanation (3–5 sentences)
- One simple example
- A tiny "Try this" suggestion at the end"""

    user_prompt = f"Please teach {child_name} about: {topic}"

    try:
        response = client.chat.completions.create(
            model=settings.get("model", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble thinking right now. Maybe try again in a moment? 🌟"

def generate_story(length, theme, tone):
    """Generate a kid-safe story"""
    client = get_openai_client()
    if not client:
        return "⚠️ API key not set. Please ask a grown-up to set it up in the Grown-ups' Corner."

    # Build system prompt with safety constraints
    banned = []
    if settings["banned_topics"]["death_illness"]:
        banned.append("death, illness, disease, or injury")
    if settings["banned_topics"]["violence"]:
        banned.append("violence, fighting, or hurting")
    if settings["banned_topics"]["scary_monsters"]:
        banned.append("scary monsters, ghosts, or frightening creatures")

    banned_text = ", ".join(banned) if banned else "anything frightening"

    length_guide = {
        "short": "3-4 short paragraphs",
        "medium": "5-7 paragraphs",
        "long": "8-10 paragraphs"
    }

    system_prompt = f"""You are a gentle storyteller for a {profile['age']}-year-old child named {profile['child_name']} who loves {', '.join(profile['interests'])}.

Create a {tone}, {theme}-themed story that is {length_guide.get(length, '5-7 paragraphs')} long.

CRITICAL SAFETY RULES:
- NO {banned_text}
- NO bullying, meanness, or cruelty
- NO abandonment or being lost/alone in scary ways
- NO bathroom humor or gross content
- Use simple, clear language at a {settings['reading_level']} reading level
- Make it cozy, safe, and age-appropriate
- Include gentle lessons about kindness, friendship, or wonder
- End on a happy, comforting note

The story should feel like a warm hug."""

    try:
        response = client.chat.completions.create(
            model=settings["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Tell me a {length} {tone} story about {theme}!"}
            ],
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"]
        )

        story = response.choices[0].message.content

        # Filter custom banned words
        for word in settings["custom_word_filters"]:
            if word.lower() in story.lower():
                return f"⚠️ The story contained something that's not allowed. Let's try a different story!"

        return story
    except Exception as e:
        return f"⚠️ Oops! Something went wrong: {str(e)}"

def generate_facts(category):
    """Generate kid-safe facts"""
    client = get_openai_client()
    if not client:
        return "⚠️ API key not set. Please ask a grown-up to set it up in the Grown-ups' Corner."

    system_prompt = f"""You are sharing interesting facts with a curious {profile['age']}-year-old named {profile['child_name']}.

RULES:
- Give 2-3 simple, amazing facts about {category}
- Use short sentences and simple words
- Make it exciting and wonder-filled!
- NO scary or sad facts
- NO death, danger, or anything frightening
- Keep it positive and fascinating
- Use emojis to make it fun

Think of facts that would make a child say "WOW!" or "COOL!" """

    try:
        response = client.chat.completions.create(
            model=settings["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Tell me some amazing facts about {category}!"}
            ],
            temperature=settings["temperature"],
            max_tokens=300
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Oops! Something went wrong: {str(e)}"

# ============================================================================
# LANDING PAGE
# ============================================================================

def show_landing():
    """Landing page with mode selection"""
    st.markdown("""
        <div class="lsr-hero-title">🌟 Little Star Rabbit 🐇</div>
        <div class="lsr-hero-subtitle">
            A tiny, safe cosmos for one very special star
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button("🎀 Play with Little Star Rabbit", use_container_width=True, type="primary"):
            # Check quiet hours and usage limits
            if check_quiet_hours():
                st.warning("🌙 Little Star Rabbit is sleeping right now. Come back during play time!")
            elif check_usage_limit():
                st.info("🐇 Little Star Rabbit is resting now. We can play again tomorrow! 💫")
            else:
                st.session_state["mode"] = "child"
                st.rerun()

    with col2:
        if st.button("🔒 Grown-ups' Corner", use_container_width=True):
            st.session_state["mode"] = "admin"
            st.rerun()

# ============================================================================
# CHILD MODE
# ============================================================================

def show_child_mode():
    """Main child mode controller"""
    # Always show a back to home button at the top if not on home page
    if st.session_state["child_page"] != "home":
        if st.button("⬅️ Back to Home", key="back_to_home"):
            st.session_state["child_page"] = "home"
            st.rerun()
        st.markdown("---")

    # Route to appropriate page
    if st.session_state["child_page"] == "home":
        show_child_home()
    elif st.session_state["child_page"] == "storytime":
        show_storytime()
    elif st.session_state["child_page"] == "facts":
        show_star_facts()
    elif st.session_state["child_page"] == "feelings":
        show_feelings()
    elif st.session_state["child_page"] == "lessons":
        show_lessons()
    elif st.session_state["child_page"] == "calm":
        show_calm_burrow()

def show_child_home():
    """Child mode home hub with activity cards"""
    st.markdown(f"<h1 style='text-align:center;'>Hello, {profile['child_name']}! 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<p class='lsr-note' style='text-align:center;'>What would you like to do today?</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Activity cards - each card is a clickable button with emoji text
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🌙\n\nStorytime\n\nSnuggle in for a cozy story", key="card_storytime", use_container_width=True):
            st.session_state["child_page"] = "storytime"
            st.rerun()

    with col2:
        if st.button("✨\n\nStar Facts\n\nLet's learn something cool together", key="card_facts", use_container_width=True):
            st.session_state["child_page"] = "facts"
            st.rerun()

    col3, col4 = st.columns(2, gap="large")
    with col3:
        if st.button("💖\n\nFeelings & Stars\n\nTap the card that feels closest to your heart", key="card_feelings", use_container_width=True):
            st.session_state["child_page"] = "feelings"
            st.rerun()

    with col4:
        if st.button("🧠\n\nLittle Lessons\n\nChoose a little lesson for your big, clever brain", key="card_lessons", use_container_width=True):
            st.session_state["child_page"] = "lessons"
            st.rerun()

    col5, col6 = st.columns(2, gap="large")
    with col5:
        if st.button("🐚\n\nCalm Burrow\n\nQuiet time in the bunny burrow", key="card_calm", use_container_width=True):
            st.session_state["child_page"] = "calm"
            st.rerun()

    # Exit button
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("👋 All done for now", key="exit_child", use_container_width=True):
        st.session_state["mode"] = "landing"
        st.session_state["child_page"] = "home"
        st.rerun()

def show_storytime():
    """Storytime section"""
    st.title("🌙 Storytime")
    st.markdown("### What kind of story do you want today?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**How long?**")
        length = st.radio("Length", ["Short", "Medium", "A bit longer"], label_visibility="collapsed", key="story_length")

    with col2:
        st.markdown("**What about?**")
        theme = st.radio("Theme", ["Animals", "Space", "Magic", "Friends", "Surprise me!"], label_visibility="collapsed", key="story_theme")

    with col3:
        st.markdown("**What kind?**")
        tone = st.radio("Tone", ["Silly", "Calm", "Adventurous"], label_visibility="collapsed", key="story_tone")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ Tell me a story!", use_container_width=True, type="primary"):
        with st.spinner("🌟 Little Star Rabbit is thinking of a story..."):
            story = generate_story(
                length.lower().replace("a bit longer", "long"),
                theme.lower().replace("surprise me!", "surprise"),
                tone.lower()
            )
            st.session_state["current_story"] = story

    if st.session_state.get("current_story"):
        st.markdown("---")
        st.markdown(f"""
            <div class='lsr-story-box'>
                {st.session_state["current_story"]}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Text-to-speech button
        tts_block("🔊 Read this story out loud", st.session_state["current_story"], "tts_story")

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Tell me another story", key="another_story", use_container_width=True):
                st.session_state["current_story"] = None
                st.rerun()
        with col2:
            if st.button("✅ That's enough for today", key="done_story", use_container_width=True):
                st.session_state["current_story"] = None
                st.session_state["child_page"] = "home"
                st.rerun()

def show_star_facts():
    """Star facts section"""
    st.title("✨ Today's Little Star Facts")
    st.markdown("### Tap a button to choose what kind of facts!")

    st.markdown("<br>", unsafe_allow_html=True)

    categories = [
        {"name": "Space", "emoji": "⭐"},
        {"name": "Animals", "emoji": "🐾"},
        {"name": "Nature", "emoji": "🌱"},
        {"name": "How Things Work", "emoji": "🧩"}
    ]

    cols = st.columns(2)
    for i, category in enumerate(categories):
        with cols[i % 2]:
            if st.button(
                f"{category['emoji']} {category['name']}",
                use_container_width=True,
                key=f"fact_{category['name']}"
            ):
                with st.spinner("🌟 Looking for amazing facts..."):
                    facts = generate_facts(category['name'])
                    st.session_state["current_facts"] = facts

    if st.session_state.get("current_facts"):
        st.markdown("---")
        st.markdown(f"""
            <div class='lsr-fact-box'>
                {st.session_state["current_facts"]}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Text-to-speech button
        tts_block("🔊 Read these facts out loud", st.session_state["current_facts"], "tts_facts")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ That's enough for today", use_container_width=True):
            st.session_state["current_facts"] = None
            st.session_state["child_page"] = "home"
            st.rerun()

def show_feelings():
    """Feelings & affirmations section"""
    st.title("💖 Feelings & Stars")
    st.markdown("### How are you feeling today?")

    st.markdown("<br>", unsafe_allow_html=True)

    feelings = [
        {"name": "Happy", "emoji": "😊", "key": "happy"},
        {"name": "Sad", "emoji": "😢", "key": "sad"},
        {"name": "Angry", "emoji": "😡", "key": "angry"},
        {"name": "Worried", "emoji": "😰", "key": "worried"},
        {"name": "Numb / I don't know", "emoji": "😶", "key": "numb"},
        {"name": "Something else", "emoji": "🎨", "key": "other"}
    ]

    # Display feeling buttons in a grid
    cols = st.columns(3)
    selected_feeling = None

    for i, feeling in enumerate(feelings):
        with cols[i % 3]:
            if st.button(
                f"{feeling['emoji']}\n\n{feeling['name']}",
                use_container_width=True,
                key=f"feeling_{feeling['key']}"
            ):
                selected_feeling = feeling['key']

    if selected_feeling:
        st.markdown("---")

        # Get feeling name for display
        feeling_name = next((f['name'] for f in feelings if f['key'] == selected_feeling), selected_feeling)

        # Generate GPT response with validation, suggestion, and affirmations
        with st.spinner("Little Star Rabbit is thinking about how you feel..."):
            response_text = generate_feelings_response(feeling_name, profile['child_name'])

        # Display the response in a soft card
        st.markdown(f"""
            <div class='lsr-feeling-box'>
                {response_text.replace('\n', '<br>')}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Add TTS button to listen to the response
        tts_block("🔊 Listen to this", response_text, f"tts_feeling_{selected_feeling}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
            <div class='lsr-info-box'>
                💫 Remember: You can always ask a grown-up for help. You don't have to do it all alone. 💫
            </div>
        """, unsafe_allow_html=True)

def show_lessons():
    """Little lessons section"""
    st.title("🧠 Little Lessons")
    st.markdown("### Choose a little lesson for your big, clever brain!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Display lessons as clickable cards
    lesson_topics = [
        {"title": "Being Kind to Myself", "emoji": "💛", "key": "kind_self"},
        {"title": "Trying Again When Things Are Hard", "emoji": "💪", "key": "try_again"},
        {"title": "My Body Belongs to Me", "emoji": "🛡", "key": "body_boundaries"},
        {"title": "What Makes a Good Friend", "emoji": "🤝", "key": "good_friend"},
        {"title": "When I Feel Big Feelings", "emoji": "🌊", "key": "big_feelings"},
        {"title": "Asking for Help is Brave", "emoji": "🌟", "key": "ask_help"},
    ]

    # Display lesson buttons in a grid
    cols = st.columns(2)
    for i, lesson in enumerate(lesson_topics):
        with cols[i % 2]:
            if st.button(
                f"{lesson['emoji']}\n\n{lesson['title']}",
                use_container_width=True,
                key=f"lesson_{lesson['key']}"
            ):
                st.session_state["selected_lesson"] = lesson

    # If a lesson is selected, show GPT-generated content
    if st.session_state.get("selected_lesson"):
        lesson = st.session_state["selected_lesson"]
        st.markdown("---")

        # Generate lesson content with GPT
        with st.spinner(f"Little Star Rabbit is preparing a lesson about {lesson['title'].lower()}..."):
            lesson_text = generate_lesson_text(lesson['title'], profile['child_name'])

        # Display in a soft card box
        st.markdown(f"""
            <div class='lsr-story-box'>
                {lesson_text.replace('\n', '<br>')}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Add TTS button
        tts_block("🔊 Listen to this lesson", lesson_text, f"tts_lesson_{lesson['key']}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Back button
        if st.button("← Choose a different lesson", key="back_from_lesson"):
            del st.session_state["selected_lesson"]
            st.rerun()

def show_calm_burrow():
    """Calm burrow section"""
    st.title("🐚 Calm Burrow")
    st.markdown("### Quiet time with the bunny")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌬\n\nBunny Breaths", use_container_width=True):
            st.session_state["calm_activity"] = "breaths"

    with col2:
        if st.button("🔢\n\nLittle Star\nCountdown", use_container_width=True):
            st.session_state["calm_activity"] = "countdown"

    with col3:
        if st.button("⏲\n\nCalm Timer", use_container_width=True):
            st.session_state["calm_activity"] = "timer"

    if st.session_state.get("calm_activity") == "breaths":
        st.markdown("---")
        st.markdown("""
            <div style='
                background: #e6f7ff;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                font-size: 1.2rem;
                line-height: 2;
            '>
                <h3>🌬 Bunny Breaths</h3>
                <p>Let's take 3 slow breaths together, just like a calm little bunny.</p>
                <br>
                <p><strong>Breath 1:</strong> Breathe in slowly through your nose... 🐇</p>
                <p>...and out through your mouth. 💨</p>
                <br>
                <p><strong>Breath 2:</strong> In through your nose... 🐇</p>
                <p>...and out through your mouth. 💨</p>
                <br>
                <p><strong>Breath 3:</strong> In through your nose... 🐇</p>
                <p>...and out through your mouth. 💨</p>
                <br>
                <p>✨ <em>Well done! How do you feel now?</em> ✨</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Back to Calm Burrow", key="back_from_breaths"):
            del st.session_state["calm_activity"]
            st.rerun()

    elif st.session_state.get("calm_activity") == "countdown":
        st.markdown("---")
        st.markdown("""
            <div style='
                background: #fff0f5;
                padding: 2rem;
                border-radius: 15px;
                font-size: 1.1rem;
                line-height: 2;
            '>
                <h3 style='text-align: center;'>🔢 Little Star Countdown (5-4-3-2-1)</h3>
                <p>This game helps you notice what's around you right now. Look around and find:</p>
                <br>
                <p><strong>5 things you can SEE 👀</strong></p>
                <p style='font-size: 0.9rem; color: #666; padding-left: 1rem;'>
                    (Maybe a book, a toy, a color on the wall...)
                </p>
                <br>
                <p><strong>4 things you can TOUCH 🤚</strong></p>
                <p style='font-size: 0.9rem; color: #666; padding-left: 1rem;'>
                    (Your shirt, the chair, your hair, the floor...)
                </p>
                <br>
                <p><strong>3 things you can HEAR 👂</strong></p>
                <p style='font-size: 0.9rem; color: #666; padding-left: 1rem;'>
                    (Birds? Voices? The hum of the computer?)
                </p>
                <br>
                <p><strong>2 things you can SMELL 👃</strong></p>
                <p style='font-size: 0.9rem; color: #666; padding-left: 1rem;'>
                    (Fresh air? A snack? Your clothes?)
                </p>
                <br>
                <p><strong>1 thing you can TASTE 👅</strong></p>
                <p style='font-size: 0.9rem; color: #666; padding-left: 1rem;'>
                    (Maybe your drink? Or just the inside of your mouth?)
                </p>
                <br>
                <p style='text-align: center;'>✨ <em>You did it! You're here, right now, and you're okay.</em> ✨</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Back to Calm Burrow", key="back_from_countdown"):
            del st.session_state["calm_activity"]
            st.rerun()

    elif st.session_state.get("calm_activity") == "timer":
        st.markdown("---")

        timer_minutes = settings.get("calm_timer_minutes", 5)

        # Check if timer is already running
        if not st.session_state.get("timer_running"):
            # Show start screen
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 3rem 2rem;
                    border-radius: 15px;
                    text-align: center;
                '>
                    <h2>⏲ Calm Timer</h2>
                    <p style='font-size: 1.3rem; margin: 2rem 0;'>
                        Ready for {timer_minutes} minutes of quiet time in the burrow?
                    </p>
                    <p style='font-size: 3rem; margin: 2rem 0;'>🐇✨</p>
                    <p>
                        Just rest, breathe, and be calm.<br>
                        Little Star Rabbit will rest with you.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🌟 Start Timer", key="start_timer", use_container_width=True):
                    st.session_state["timer_running"] = True
                    st.rerun()
            with col2:
                if st.button("← Back", key="back_from_timer_start", use_container_width=True):
                    del st.session_state["calm_activity"]
                    st.rerun()
        else:
            # Run the countdown timer
            total_seconds = timer_minutes * 60
            placeholder = st.empty()
            start_time = time_module.time()

            st.markdown("""
                <div style='text-align: center; margin-bottom: 2rem;'>
                    <h2>🐇 Calm Burrow Time 🐇</h2>
                    <p>Little Star Rabbit is resting with you...</p>
                </div>
            """, unsafe_allow_html=True)

            while True:
                elapsed = int(time_module.time() - start_time)
                remaining = total_seconds - elapsed

                if remaining <= 0:
                    break

                mins, secs = divmod(remaining, 60)
                placeholder.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 4rem 2rem;
                        border-radius: 15px;
                        text-align: center;
                        font-size: 3rem;
                        font-weight: 700;
                        margin: 2rem 0;
                    '>
                        {mins:02d}:{secs:02d}
                    </div>
                """, unsafe_allow_html=True)
                time_module.sleep(1)

            # Timer finished
            placeholder.markdown("""
                <div style='
                    background: linear-gradient(135deg, #f9739a 0%, #f27d90 100%);
                    color: white;
                    padding: 3rem 2rem;
                    border-radius: 15px;
                    text-align: center;
                '>
                    <h2>✨ Time is up! ✨</h2>
                    <p style='font-size: 1.5rem; margin: 2rem 0;'>🐇💖</p>
                    <p>Little Star Rabbit is done resting with you.</p>
                    <p>Well done taking quiet time!</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("All done!", key="done_resting", use_container_width=True):
                del st.session_state["calm_activity"]
                del st.session_state["timer_running"]
                st.session_state["child_page"] = "home"
                st.rerun()

# ============================================================================
# ADMIN MODE
# ============================================================================

def show_admin_mode():
    """Admin mode controller"""
    # Check authentication
    if not st.session_state.get("admin_authenticated"):
        show_admin_login()
        return

    # Show sidebar navigation
    st.sidebar.title("🔒 Grown-ups' Corner")

    admin_pages = {
        "profile": "👤 Child Profile",
        "content": "⚙️ Content Settings",
        "affirmations": "💝 Affirmations & Lessons",
        "time": "⏰ Time & Limits",
        "safety": "🔐 Safety & API"
    }

    selected_page = st.sidebar.radio(
        "Navigation",
        list(admin_pages.keys()),
        format_func=lambda x: admin_pages[x],
        key="admin_nav"
    )

    st.session_state["admin_page"] = selected_page

    if st.sidebar.button("🚪 Exit Admin Mode"):
        st.session_state["admin_authenticated"] = False
        st.session_state["mode"] = "landing"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Logged in • {datetime.now().strftime('%H:%M')}")

    # Route to appropriate admin page
    if st.session_state["admin_page"] == "profile":
        show_admin_profile()
    elif st.session_state["admin_page"] == "content":
        show_admin_content()
    elif st.session_state["admin_page"] == "affirmations":
        show_admin_affirmations()
    elif st.session_state["admin_page"] == "time":
        show_admin_time()
    elif st.session_state["admin_page"] == "safety":
        show_admin_safety()

def show_admin_login():
    """Admin PIN authentication"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>🔒 Grown-ups' Corner</h1>
            <p style='color: #666;'>Enter the PIN to continue</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        pin_input = st.text_input("PIN", type="password", label_visibility="collapsed", placeholder="Enter PIN")

        if st.button("Unlock", use_container_width=True, type="primary"):
            if pin_input == settings["admin_pin"]:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Wrong PIN. Please try again.")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("← Back", use_container_width=True):
            st.session_state["mode"] = "landing"
            st.rerun()

        st.caption("Default PIN is: 1234")

def show_admin_profile():
    """Admin: Child profile settings"""
    st.title("👤 Child Profile")
    st.markdown("Customize the app for your child")

    st.markdown("---")

    with st.form("profile_form"):
        name = st.text_input("Child's name / nickname", value=profile.get("child_name", "Little Star"))
        age = st.number_input("Age", min_value=3, max_value=12, value=profile.get("age", 7))
        pronouns = st.text_input("Pronouns", value=profile.get("pronouns", "she/her"))

        st.markdown("**Special interests** (comma-separated)")
        interests_str = ", ".join(profile.get("interests", []))
        interests = st.text_area("Interests", value=interests_str, help="These will be used to personalize stories and facts")

        if st.form_submit_button("💾 Save Profile", use_container_width=True):
            profile["child_name"] = name
            profile["age"] = age
            profile["pronouns"] = pronouns
            profile["interests"] = [i.strip() for i in interests.split(",") if i.strip()]
            save_profile()
            st.success("✅ Profile saved!")
            st.rerun()

def show_admin_content():
    """Admin: Content settings"""
    st.title("⚙️ Content Settings")
    st.markdown("Control what content is generated")

    st.markdown("---")

    with st.form("content_form"):
        st.subheader("AI Story Settings")

        use_ai = st.checkbox("Use AI to generate content", value=settings.get("use_ai", True))

        max_length = st.select_slider(
            "Max story length",
            options=["short", "medium", "long"],
            value=settings.get("max_story_length", "medium")
        )

        reading_level = st.select_slider(
            "Reading level",
            options=["very simple", "simple", "normal"],
            value=settings.get("reading_level", "simple")
        )

        st.markdown("---")
        st.subheader("Banned Topics")
        st.caption("Check to BLOCK these topics from stories")

        ban_death = st.checkbox(
            "Death, illness, disease, or injury",
            value=settings.get("banned_topics", {}).get("death_illness", True)
        )

        ban_violence = st.checkbox(
            "Violence, fighting, or hurting",
            value=settings.get("banned_topics", {}).get("violence", True)
        )

        ban_scary = st.checkbox(
            "Scary monsters or frightening creatures",
            value=settings.get("banned_topics", {}).get("scary_monsters", True)
        )

        st.markdown("---")
        st.subheader("Custom Word Filters")
        st.caption("Words that should NEVER appear (comma-separated)")

        filters_str = ", ".join(settings.get("custom_word_filters", []))
        custom_filters = st.text_area("Banned words", value=filters_str)

        if st.form_submit_button("💾 Save Content Settings", use_container_width=True):
            settings["use_ai"] = use_ai
            settings["max_story_length"] = max_length
            settings["reading_level"] = reading_level
            settings["banned_topics"] = {
                "death_illness": ban_death,
                "violence": ban_violence,
                "scary_monsters": ban_scary
            }
            settings["custom_word_filters"] = [f.strip() for f in custom_filters.split(",") if f.strip()]
            save_settings()
            st.success("✅ Content settings saved!")
            st.rerun()

def show_admin_affirmations():
    """Admin: Affirmations and lessons library"""
    st.title("💝 Affirmations & Lessons Library")

    tab1, tab2 = st.tabs(["✨ Affirmations", "📚 Lessons"])

    with tab1:
        st.markdown("### Affirmations by Feeling")

        for feeling_key, feeling_name in [
            ("happy", "😊 Happy"),
            ("sad", "😢 Sad"),
            ("angry", "😡 Angry"),
            ("worried", "😰 Worried"),
            ("numb", "😶 Numb / Don't know"),
            ("other", "🎨 Other")
        ]:
            with st.expander(feeling_name):
                current_affirmations = affirmations.get(feeling_key, [])

                # Display existing
                for i, aff in enumerate(current_affirmations):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(aff)
                    with col2:
                        if st.button("🗑", key=f"del_aff_{feeling_key}_{i}"):
                            affirmations[feeling_key].remove(aff)
                            save_affirmations()
                            st.rerun()

                # Add new
                new_aff = st.text_input(f"Add new affirmation for {feeling_name}", key=f"new_{feeling_key}")
                if st.button(f"➕ Add", key=f"add_{feeling_key}"):
                    if new_aff:
                        if feeling_key not in affirmations:
                            affirmations[feeling_key] = []
                        affirmations[feeling_key].append(new_aff)
                        save_affirmations()
                        st.success(f"Added!")
                        st.rerun()

    with tab2:
        st.markdown("### Little Lessons")

        # Display existing lessons
        for lesson in lessons:
            with st.expander(f"{lesson['emoji']} {lesson['title']}"):
                st.markdown(f"**Category:** {lesson.get('category', 'other')}")
                st.markdown(f"**Tags:** {', '.join(lesson.get('tags', []))}")
                st.markdown("---")
                st.markdown(lesson['content'])

                if st.button("🗑 Delete this lesson", key=f"del_lesson_{lesson['id']}"):
                    lessons.remove(lesson)
                    save_lessons()
                    st.rerun()

        st.markdown("---")
        st.markdown("### Add New Lesson")

        with st.form("new_lesson_form"):
            new_title = st.text_input("Title")
            new_emoji = st.text_input("Emoji", value="✨")
            new_category = st.selectbox("Category", ["kindness", "brave_brain", "boundaries", "school", "other"])
            new_content = st.text_area("Content", height=200)
            new_tags = st.text_input("Tags (comma-separated)")

            if st.form_submit_button("➕ Add Lesson"):
                if new_title and new_content:
                    new_id = max([l.get('id', 0) for l in lessons], default=0) + 1
                    new_lesson = {
                        "id": new_id,
                        "category": new_category,
                        "title": new_title,
                        "emoji": new_emoji,
                        "content": new_content,
                        "tags": [t.strip() for t in new_tags.split(",") if t.strip()]
                    }
                    lessons.append(new_lesson)
                    save_lessons()
                    st.success("✅ Lesson added!")
                    st.rerun()

def show_admin_time():
    """Admin: Time and usage limits"""
    st.title("⏰ Time & Limits")
    st.markdown("Set healthy boundaries for app usage")

    st.markdown("---")

    # Show today's usage
    today_usage = get_today_usage()
    st.metric("Today's Usage", f"{today_usage} minutes")

    st.markdown("---")

    with st.form("time_form"):
        st.subheader("Daily Limits")

        daily_limit = st.number_input(
            "Daily usage limit (minutes)",
            min_value=5,
            max_value=120,
            value=settings.get("daily_limit_minutes", 20),
            step=5
        )

        session_length = st.number_input(
            "Calm Burrow timer length (minutes)",
            min_value=5,
            max_value=30,
            value=settings.get("session_length_minutes", 10),
            step=5
        )

        st.markdown("---")
        st.subheader("Quiet Hours")
        st.caption("Times when the app cannot be used")

        col1, col2 = st.columns(2)

        with col1:
            quiet_start = st.time_input(
                "Quiet hours start",
                value=datetime.strptime(settings.get("quiet_hours_start", "21:00"), "%H:%M").time()
            )

        with col2:
            quiet_end = st.time_input(
                "Quiet hours end",
                value=datetime.strptime(settings.get("quiet_hours_end", "07:00"), "%H:%M").time()
            )

        if st.form_submit_button("💾 Save Time Settings", use_container_width=True):
            settings["daily_limit_minutes"] = daily_limit
            settings["session_length_minutes"] = session_length
            settings["quiet_hours_start"] = quiet_start.strftime("%H:%M")
            settings["quiet_hours_end"] = quiet_end.strftime("%H:%M")
            save_settings()
            st.success("✅ Time settings saved!")
            st.rerun()

    st.markdown("---")

    if st.button("🔄 Reset Today's Usage Counter", type="secondary"):
        usage = load_json(USAGE_FILE, {})
        today = datetime.now().strftime("%Y-%m-%d")
        if today in usage:
            del usage[today]
        save_json(USAGE_FILE, usage)
        st.success("✅ Usage counter reset!")
        st.rerun()

def show_admin_safety():
    """Admin: Safety and API settings"""
    st.title("🔐 Safety & API Settings")

    st.markdown("---")

    with st.form("safety_form"):
        st.subheader("Admin PIN")

        new_pin = st.text_input(
            "Change admin PIN",
            type="password",
            help="Leave blank to keep current PIN"
        )

        confirm_pin = st.text_input(
            "Confirm new PIN",
            type="password"
        )

        st.markdown("---")
        st.subheader("OpenAI API Settings")

        st.info("""
            **Note:** The OpenAI API key is read from the `OPENAI_API_KEY` environment variable.
            Set this on your server or in your Streamlit Cloud secrets.
        """)

        model = st.selectbox(
            "Model",
            options=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
            index=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"].index(settings.get("model", "gpt-4o-mini"))
        )

        temperature = st.slider(
            "Temperature (creativity)",
            min_value=0.0,
            max_value=1.0,
            value=settings.get("temperature", 0.7),
            step=0.1,
            help="Higher = more creative, Lower = more predictable"
        )

        max_tokens = st.number_input(
            "Max tokens per response",
            min_value=100,
            max_value=2000,
            value=settings.get("max_tokens", 500),
            step=100
        )

        if st.form_submit_button("💾 Save Settings", use_container_width=True):
            # Update PIN if provided
            if new_pin:
                if new_pin == confirm_pin:
                    settings["admin_pin"] = new_pin
                    st.success("✅ PIN updated!")
                else:
                    st.error("❌ PINs don't match!")
                    st.stop()

            # Update API settings (but not API key)
            settings["model"] = model
            settings["temperature"] = temperature
            settings["max_tokens"] = max_tokens

            save_settings()
            st.success("✅ Settings saved!")
            st.rerun()

    st.markdown("---")
    st.info("""
        **Security Note:** For security, API keys should be set as environment variables,
        not stored in config files. On Streamlit Cloud, use the Secrets management feature.
    """)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main app controller"""
    init_session_state()

    # Inject custom CSS for beautiful starry theme
    inject_css()

    # Route to appropriate mode
    if st.session_state["mode"] == "landing":
        show_landing()
    elif st.session_state["mode"] == "child":
        show_child_mode()
    elif st.session_state["mode"] == "admin":
        show_admin_mode()

if __name__ == "__main__":
    main()
