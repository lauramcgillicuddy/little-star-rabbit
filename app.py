"""
Little Star Rabbit 🌟🐇
A trauma-aware, kid-safe app for one very special star.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import os
import time as time_module
from datetime import datetime, time, date
from openai import OpenAI
from pathlib import Path

# Import our new utilities
from gpt_utils import (
    generate_story, generate_star_facts, generate_feelings_response,
    generate_little_lesson, generate_daily_affirmation, answer_wonder_question,
    generate_wonder_question_prompt, generate_routine_content, StoryOptions
)
from tts_utils import render_read_aloud, render_read_aloud_simple, text_to_speech

# Page config
st.set_page_config(
    page_title="Little Star Rabbit",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
def inject_css():
    """Inject custom CSS for adorable pink handwritten theme"""
    st.markdown(
        """
        <style>
        /* --- IMPORT CUTE HANDWRITTEN FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Covered+By+Your+Grace&family=Indie+Flower&family=Caveat:wght@400;700&display=swap');

        /* --- GLOBAL FONT OVERRIDES - Super Cute Handwritten! --- */
        .stApp, .block-container, .stMarkdown, .stText, .stTextInput, .stNumberInput,
        .stRadio, .stSelectbox, .stTextarea, .stCheckbox, .stButton > button,
        .stTabs [data-baseweb="tab"], label, p, div {
            font-family: "Patrick Hand", "Indie Flower", cursive, sans-serif;
            font-size: 1.45rem;
        }

        /* Ensure all text is visible and bigger */
        p, span, div, label, .stMarkdown {
            color: #4a1942;
            font-size: 1.45rem;
        }

        /* Use extra cute handwritten for helper text */
        .lsr-note {
            font-family: "Covered By Your Grace", "Patrick Hand", cursive;
            font-size: 1.35rem;
        }

        /* Background + layout - Super Pink and Magical! */
        .stApp {
            background:
                radial-gradient(circle at 20% 30%, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255, 192, 203, 0.3) 0%, transparent 50%),
                linear-gradient(180deg, #ffb6d9 0%, #ffd4e5 30%, #ffe5f0 60%, #fff0f5 100%);
            color: #4a1942;
        }

        /* Cute floating doodles */
        .cute-doodle {
            position: fixed;
            font-size: 2rem;
            opacity: 0.15;
            pointer-events: none;
            z-index: 0;
            animation: gentle-float 8s ease-in-out infinite;
        }

        @keyframes gentle-float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(5deg); }
        }

        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 900px;
        }

        #MainMenu, footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Titles - Big and Playful! */
        h1, h2, h3, .lsr-hero-title {
            font-family: "Caveat", "Patrick Hand", cursive;
            letter-spacing: 0.02em;
            color: #d5006d !important;
            text-shadow: 2px 2px 4px rgba(255, 182, 193, 0.4);
        }
        h1 {
            font-size: 3.05rem;
            font-weight: 700;
        }
        h2 {
            font-size: 2.45rem;
            font-weight: 700;
        }
        h3 {
            font-size: 2.05rem;
            font-weight: 600;
        }
        .lsr-hero-title {
            font-size: 3.75rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
            color: #d5006d !important;
        }
        .lsr-hero-subtitle {
            text-align: center;
            font-size: 1.55rem;
            color: #c2185b !important;
            margin-bottom: 2.2rem;
            font-family: "Covered By Your Grace", "Patrick Hand", cursive;
        }

        /* Landing page buttons - Cute but not too big! */
        .lsr-cta-row {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        .lsr-cta-main {
            border-radius: 1.5rem;
            padding: 0.7rem 1.8rem;
            border: 2px solid #ff69b4;
            font-weight: 600;
            font-size: 1.3rem;
            cursor: pointer;
            box-shadow: 0 6px 16px rgba(255, 105, 180, 0.3);
            background: linear-gradient(135deg, #ff85c0, #ffb6d9);
            color: #fff;
            transition: transform 0.2s ease;
        }
        .lsr-cta-main:hover {
            transform: scale(1.03) rotate(-1deg);
        }
        .lsr-cta-secondary {
            border-radius: 1.5rem;
            padding: 0.7rem 1.8rem;
            border: 2px solid #ffb6d9;
            background: #fff;
            font-weight: 500;
            font-size: 1.3rem;
            cursor: pointer;
            color: #c2185b;
            box-shadow: 0 5px 12px rgba(255, 182, 193, 0.25);
            transition: transform 0.2s ease;
        }
        .lsr-cta-secondary:hover {
            transform: scale(1.03) rotate(1deg);
        }

        /* Tabs - Cute and Pink! */
        .stTabs [data-baseweb="tab"] {
            font-size: 1.35rem;
            font-weight: 600;
            padding: 0.8rem 1.2rem;
            border-radius: 1rem 1rem 0 0;
            font-family: "Patrick Hand", cursive;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        /* Child hub card buttons - Super Cute Cards! */
        div[data-testid="stButton"] > button {
            border-radius: 2rem;
            padding: 2rem 1.8rem;
            background: linear-gradient(145deg, #fff, #ffe5f0);
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.3);
            border: 3px solid #ffb6d9;
            text-align: left;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: normal;
            height: auto;
            min-height: 180px;
            color: #4a1942 !important;
            font-size: 1.35rem;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-6px) rotate(-1deg);
            box-shadow: 0 15px 40px rgba(255, 105, 180, 0.5);
            border-color: #ff85c0;
        }

        .lsr-card-icon {
            font-size: 3.25rem;
            margin-bottom: 1rem;
            display: block;
        }
        .lsr-card-title {
            font-size: 1.65rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: block;
            color: #d5006d;
        }
        .lsr-card-sub {
            font-size: 1.3rem;
            color: #c2185b;
            font-family: "Covered By Your Grace", "Patrick Hand", cursive;
            display: block;
            line-height: 1.5;
        }

        /* Story box - Super Cute! */
        .lsr-story-box {
            border-radius: 2rem;
            padding: 2rem 2.2rem;
            background: linear-gradient(135deg, #fff 0%, #ffe5f0 100%);
            border: 3px solid #ffb6d9;
            box-shadow: 0 10px 25px rgba(255, 105, 180, 0.3);
            line-height: 1.8;
            font-size: 1.4rem;
        }

        /* Fact box - Sparkly! */
        .lsr-fact-box {
            border-radius: 2rem;
            padding: 2rem 2.2rem;
            background: linear-gradient(135deg, #ffffed 0%, #fff8dc 100%);
            border: 3px solid #ffd700;
            box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);
            line-height: 1.8;
            font-size: 1.4rem;
        }

        /* Feeling boxes - Extra Pink! */
        .lsr-feeling-box {
            border-radius: 1.8rem;
            padding: 1.8rem 2rem;
            background: linear-gradient(135deg, #ffe5f0 0%, #ffd4e5 100%);
            border: 3px solid #ff85c0;
            box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);
            margin-bottom: 1.5rem;
            font-size: 1.4rem;
        }

        .lsr-info-box {
            border-radius: 1.8rem;
            padding: 1.5rem 1.8rem;
            background: linear-gradient(135deg, #fff0f5 0%, #ffe5f0 100%);
            border: 3px solid #ffb6d9;
            margin: 1rem 0;
            color: #c2185b;
            text-align: center;
            font-size: 1.35rem;
        }

        /* Regular buttons (non-card) - Cute and not too big! */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #ff85c0, #ffb6d9);
            color: white;
            border: none;
            border-radius: 1.5rem;
            font-size: 1.25rem;
            padding: 0.6rem 1.4rem;
        }

        .stButton > button:not([data-testid]) {
            border-radius: 1.5rem;
            font-weight: 500;
            padding: 0.6rem 1.4rem;
            border: 2px solid #ffb6d9;
            transition: all 0.2s ease;
            color: #4a1942 !important;
            background-color: #ffffff;
            font-size: 1.25rem;
        }

        .stButton > button:not([data-testid]):hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 20px rgba(255, 105, 180, 0.35);
            border-color: #ff85c0;
        }

        /* Streamlit widgets - Cute! */
        .stRadio > label, .stSelectbox > label, .stTextInput > label,
        .stNumberInput > label, .stTextarea > label {
            font-weight: 600;
            color: #c2185b;
            font-size: 1.1rem;
        }

        /* Input fields - Pink borders! */
        input, textarea, select {
            border-radius: 1rem !important;
            border: 2px solid #ffb6d9 !important;
            font-family: "Patrick Hand", cursive !important;
        }

        /* Radio and checkboxes - Pink! */
        .stRadio > div {
            gap: 0.8rem;
        }

        /* Ensure sidebar is visible */
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }

        /* Add cute hover effects everywhere! */
        .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
            transform: scale(1.01);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Scroll helper function
def scroll_to_top():
    """Scroll the page to top using JavaScript component"""
    components.html(
        """
        <script>
            setTimeout(function() {
                const mainSection = window.parent.document.querySelector('section.main');
                if (mainSection) {
                    mainSection.scrollTo({top: 0, behavior: 'smooth'});
                }
                // Also try scrolling the whole window
                window.parent.scrollTo({top: 0, behavior: 'smooth'});
            }, 100);
        </script>
        """,
        height=0,
    )

# Add cute doodles to the page
def add_cute_doodles():
    """Add cute floating doodles to the background"""
    st.markdown("""
        <div class="cute-doodle" style="top: 10%; right: 8%;">💕</div>
        <div class="cute-doodle" style="top: 25%; left: 5%; animation-delay: 1s;">⭐</div>
        <div class="cute-doodle" style="top: 60%; right: 12%; animation-delay: 2s;">✨</div>
        <div class="cute-doodle" style="top: 80%; left: 15%; animation-delay: 3s;">🌸</div>
        <div class="cute-doodle" style="top: 45%; left: 90%; animation-delay: 1.5s;">🦋</div>
        <div class="cute-doodle" style="top: 70%; right: 85%; animation-delay: 2.5s;">🌈</div>
    """, unsafe_allow_html=True)

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
        # NEW: Daily affirmation
        "daily_affirmation": None,
        "affirmation_date": None,
        # NEW: Little Wins tracking
        "completed_storytime_today": False,
        "selected_feeling_today": False,
        "did_bunny_breaths_today": False,
        "asked_wonder_question_today": False,
        "used_journal_today": False,
        "used_routines_today": False,
        # NEW: Secret Strengths
        "feelings_count": 0,
        "storytime_count": 0,
        "questions_asked_count": 0,
        "unlocked_strengths": set(),
        # NEW: Wonder question suggestion
        "wonder_suggestion": None,
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

def synthesize_story_audio(text):
    """Convert story text to speech using OpenAI TTS"""
    if not text:
        return None
    try:
        client = get_openai_client()
        if not client:
            return None

        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Warm, friendly female voice
            input=text
        )
        return response.content
    except Exception as e:
        st.error(f"Could not generate audio: {str(e)}")
        return None

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
# NEW FEATURE HELPERS
# ============================================================================

def get_daily_affirmation():
    """Get or generate daily affirmation"""
    today = date.today()
    child_name = profile.get("child_name", "Little Star")

    # Check if we need a new affirmation
    if (st.session_state.get("affirmation_date") != today or
        not st.session_state.get("daily_affirmation")):
        affirmation = generate_daily_affirmation(child_name)
        st.session_state["daily_affirmation"] = affirmation
        st.session_state["affirmation_date"] = today

    return st.session_state["daily_affirmation"]

def unlock_strength(strength_id: str):
    """Unlock a secret strength"""
    if "unlocked_strengths" not in st.session_state:
        st.session_state["unlocked_strengths"] = set()
    st.session_state["unlocked_strengths"].add(strength_id)

def check_strength_unlocks():
    """Check if any new strengths should be unlocked"""
    # Notice feelings
    if st.session_state.get("feelings_count", 0) >= 3:
        unlock_strength("feelings_noticer")

    # Curious learner
    if st.session_state.get("storytime_count", 0) >= 5:
        unlock_strength("curious_learner")

    # Wonder seeker
    if st.session_state.get("questions_asked_count", 0) >= 3:
        unlock_strength("wonder_seeker")

# Emotion character mapping
EMOTION_CHARACTERS = {
    "happy": {"name": "Sunny", "emoji": "🌞"},
    "sad": {"name": "Drippy", "emoji": "💧"},
    "angry": {"name": "Blaze", "emoji": "🔥"},
    "worried": {"name": "Zoomer", "emoji": "💨"},
    "scared": {"name": "Shiver", "emoji": "❄️"},
    "numb": {"name": "Floaty", "emoji": "☁️"},
    "something else": {"name": "Mystery Star", "emoji": "✨"},
}

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
    # NEW PAGES
    elif st.session_state["child_page"] == "wonder":
        show_ask_a_little_star()
    elif st.session_state["child_page"] == "journal":
        show_bunny_journal()
    elif st.session_state["child_page"] == "routines":
        show_star_routines()
    elif st.session_state["child_page"] == "wins":
        show_little_wins()
    elif st.session_state["child_page"] == "strengths":
        show_secret_strengths()

def show_child_home():
    """Enhanced home page with daily affirmation and new features"""
    child_name = profile.get("child_name", "Little Star")

    # Header
    st.markdown(f"""
        <div class="lsr-hero-title">🌟 Hello, {child_name}! 🐇</div>
        <div class="lsr-hero-subtitle">
            Welcome to your safe little cosmos
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FEATURE 1: Daily Affirmation
    st.markdown("### 🌟 Little Star Message")
    affirmation = get_daily_affirmation()

    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #ffe5f0 0%, #fff0f5 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border: 3px solid #ffb6d9;
            text-align: center;
            margin: 1rem 0 2rem 0;
            font-size: 1.3rem;
            color: #c2185b;
            box-shadow: 0 8px 20px rgba(255, 182, 217, 0.3);
        '>
            {affirmation}
        </div>
    """, unsafe_allow_html=True)

    # Read aloud button for affirmation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_read_aloud_simple(affirmation, "daily_affirmation")

    st.markdown("---")

    # Navigation cards
    st.markdown("### Choose an adventure:")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button("📖\n\nStorytime", use_container_width=True, type="primary"):
            st.session_state["child_page"] = "storytime"
            st.rerun()

        if st.button("🌟\n\nStar Facts", use_container_width=True):
            st.session_state["child_page"] = "facts"
            st.rerun()

        if st.button("💖\n\nFeelings & Stars", use_container_width=True):
            st.session_state["child_page"] = "feelings"
            st.rerun()

        if st.button("🌈\n\nLittle Lessons", use_container_width=True):
            st.session_state["child_page"] = "lessons"
            st.rerun()

    with col2:
        if st.button("🐇\n\nCalm Burrow", use_container_width=True):
            st.session_state["child_page"] = "calm"
            st.rerun()

        # FEATURE 2: Ask a Little Star
        if st.button("✨\n\nAsk a Little Star", use_container_width=True):
            st.session_state["child_page"] = "wonder"
            st.rerun()

        # FEATURE 5: Bunny Journal
        if st.button("📓\n\nBunny Journal", use_container_width=True):
            st.session_state["child_page"] = "journal"
            st.rerun()

        # FEATURE 6: Star Routines
        if st.button("🌅\n\nLittle Star Routines", use_container_width=True):
            st.session_state["child_page"] = "routines"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Links to achievements
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏅 Little Wins", use_container_width=True):
            st.session_state["child_page"] = "wins"
            st.rerun()
    with col2:
        if st.button("⭐ Secret Strengths", use_container_width=True):
            st.session_state["child_page"] = "strengths"
            st.rerun()
    with col3:
        if st.button("🚪 Exit", use_container_width=True):
            st.session_state["mode"] = "landing"
            st.rerun()

def show_storytime():
    """Updated storytime with GPT integration and TTS"""
    child_name = profile.get("child_name", "Little Star")

    st.markdown("### 📖 Storytime")

    # Story options
    col1, col2, col3 = st.columns(3)

    with col1:
        length = st.selectbox("Length", ["short", "medium", "long"])
    with col2:
        topic = st.selectbox("Topic", [
            "animals", "nature", "space", "magic",
            "friendship", "adventure", "cozy day"
        ])
    with col3:
        mood = st.selectbox("Mood", [
            "calm", "gentle", "cozy", "happy", "curious"
        ])

    if st.button("🌟 Tell me a story!", type="primary", use_container_width=True):
        with st.spinner("Creating your story..."):
            story = generate_story(length, topic, mood)
            st.session_state["current_story"] = story
            st.session_state["completed_storytime_today"] = True
            st.session_state["storytime_count"] = st.session_state.get("storytime_count", 0) + 1
            check_strength_unlocks()
            st.rerun()

    # Display story with TTS
    if st.session_state.get("current_story"):
        st.markdown("---")
        render_read_aloud(
            st.session_state["current_story"],
            "Read the story aloud",
            "current_story"
        )

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
    """Updated star facts with GPT and TTS"""
    st.markdown("### 🌟 Star Facts")

    topic = st.selectbox("What do you want to learn about?", [
        "ocean animals", "space", "butterflies", "weather",
        "trees", "birds", "dinosaurs", "rainbows", "stars"
    ])

    if st.button("✨ Show me facts!", type="primary", use_container_width=True):
        with st.spinner("Finding amazing facts..."):
            facts = generate_star_facts(topic)
            st.session_state["current_facts"] = {"topic": topic, "facts": facts}
            st.rerun()

    # Display facts with TTS
    if st.session_state.get("current_facts"):
        st.markdown("---")
        st.markdown(f"**Amazing facts about {st.session_state['current_facts']['topic']}:**")

        facts_text = ""
        for i, fact in enumerate(st.session_state["current_facts"]["facts"], 1):
            st.markdown(f"{i}. {fact}")
            facts_text += f"{fact} "

        st.markdown("<br>", unsafe_allow_html=True)
        render_read_aloud_simple(facts_text, "star_facts")

def show_feelings():
    """FEATURE 7: Updated feelings with emotion characters"""
    child_name = profile.get("child_name", "Little Star")

    st.markdown("### 💖 Feelings & Stars")

    st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            <p style='font-size: 1.2rem;'>How are you feeling right now?</p>
        </div>
    """, unsafe_allow_html=True)

    # Emotion buttons with characters
    col1, col2, col3 = st.columns(3)

    feelings = ["happy", "sad", "angry", "worried", "scared", "numb", "something else"]

    selected_feeling = None

    for idx, feeling in enumerate(feelings):
        col = [col1, col2, col3][idx % 3]
        with col:
            character = EMOTION_CHARACTERS[feeling]
            if st.button(
                f"{character['emoji']}\n\n{feeling.title()}\n({character['name']})",
                use_container_width=True,
                key=f"feeling_{feeling}"
            ):
                selected_feeling = feeling

    if selected_feeling:
        character = EMOTION_CHARACTERS[selected_feeling]

        with st.spinner(f"{character['name']} is here..."):
            response = generate_feelings_response(selected_feeling, character["name"])

            st.markdown("---")

            # Character intro
            st.markdown(f"""
                <div style='text-align: center; margin: 1rem 0;'>
                    <p style='font-size: 2rem;'>{character['emoji']}</p>
                    <p style='font-size: 1.3rem; color: #c2185b;'>
                        {character['name']} is here
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Validation
            render_read_aloud(response["validation"], "Read this", "feelings_validation")

            # Suggestion
            st.markdown(f"""
                <div style='
                    background: #ffe5f0;
                    padding: 1rem;
                    border-radius: 10px;
                    border-left: 4px solid #ff85c0;
                    margin: 1rem 0;
                '>
                    💡 {response['suggestion']}
                </div>
            """, unsafe_allow_html=True)

            # Reminder
            st.info(f"✨ {response['reminder']}")

            # Track
            st.session_state["selected_feeling_today"] = True
            st.session_state["feelings_count"] = st.session_state.get("feelings_count", 0) + 1
            check_strength_unlocks()

def show_lessons():
    """Little lessons section"""
    st.title("🧠 Little Lessons")
    st.markdown("### Choose a lesson to learn something helpful!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Group lessons by category
    categories = {
        "kindness": {"name": "Kindness & Friends", "emoji": "💛", "color": "#fff9e6"},
        "brave_brain": {"name": "Brave Brain", "emoji": "🧠", "color": "#e6f3ff"},
        "boundaries": {"name": "Body & Boundaries", "emoji": "🛡", "color": "#ffe6f0"},
        "school": {"name": "School & Focus", "emoji": "📚", "color": "#f0ffe6"}
    }

    # Display lessons
    for lesson in lessons:
        cat = lesson.get("category", "other")
        if cat in categories:
            cat_info = categories[cat]

            with st.expander(f"{lesson['emoji']} {lesson['title']}"):
                st.markdown(f"""
                    <div style='
                        background: {cat_info['color']};
                        padding: 1.5rem;
                        border-radius: 10px;
                        font-size: 1.05rem;
                        line-height: 1.7;
                    '>
                        {lesson['content'].replace(chr(10), '<br><br>')}
                    </div>
                """, unsafe_allow_html=True)

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
        # Scroll to activity content
        scroll_to_top()
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

        # Track achievement
        st.session_state["did_bunny_breaths_today"] = True

        if st.button("Back to Calm Burrow", key="back_from_breaths"):
            del st.session_state["calm_activity"]
            st.rerun()

    elif st.session_state.get("calm_activity") == "countdown":
        # Scroll to activity content
        scroll_to_top()
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
        # Scroll to activity content
        scroll_to_top()
        st.markdown("---")

        timer_minutes = settings.get("session_length_minutes", 5)
        total_seconds = timer_minutes * 60

        # Initialize timer state if needed
        if "timer_start_time" not in st.session_state:
            st.session_state["timer_start_time"] = None
        if "timer_paused_at" not in st.session_state:
            st.session_state["timer_paused_at"] = None

        # Check if timer is running
        if st.session_state["timer_start_time"] is None:
            # Show start screen
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ff85c0 0%, #ffb6d9 100%);
                    color: white;
                    padding: 3rem 2rem;
                    border-radius: 2rem;
                    text-align: center;
                    border: 3px solid #ff69b4;
                    box-shadow: 0 10px 30px rgba(255, 105, 180, 0.3);
                '>
                    <h2>⏲ Calm Timer</h2>
                    <p style='font-size: 1.5rem; margin: 2rem 0;'>
                        Ready for {timer_minutes} minutes of quiet time?
                    </p>
                    <p style='font-size: 3rem; margin: 2rem 0;'>🐇✨</p>
                    <p style='font-size: 1.2rem;'>
                        Just rest, breathe, and be calm.<br>
                        Little Star Rabbit will rest with you.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🌟 Start Timer", key="start_timer", use_container_width=True, type="primary"):
                    st.session_state["timer_start_time"] = time_module.time()
                    st.session_state["timer_running"] = True
                    st.rerun()
            with col2:
                if st.button("← Back", key="back_from_timer_start", use_container_width=True):
                    del st.session_state["calm_activity"]
                    st.session_state["timer_start_time"] = None
                    st.session_state["timer_paused_at"] = None
                    st.rerun()
        else:
            # Calculate elapsed and remaining time
            if st.session_state.get("timer_paused_at"):
                elapsed = st.session_state["timer_paused_at"]
            else:
                elapsed = int(time_module.time() - st.session_state["timer_start_time"])

            remaining = max(0, total_seconds - elapsed)

            if remaining > 0 and not st.session_state.get("timer_paused_at"):
                # Timer is active - show countdown
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 2rem;'>
                        <h2 style='color: #d5006d;'>🐇 Calm Burrow Time 🐇</h2>
                        <p style='font-size: 1.4rem; color: #c2185b;'>Little Star Rabbit is resting with you...</p>
                    </div>
                """, unsafe_allow_html=True)

                mins, secs = divmod(remaining, 60)
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #ff85c0 0%, #ffb6d9 100%);
                        color: white;
                        padding: 4rem 2rem;
                        border-radius: 2rem;
                        text-align: center;
                        font-size: 4rem;
                        font-weight: 700;
                        margin: 2rem 0;
                        border: 3px solid #ff69b4;
                        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.4);
                    '>
                        {mins:02d}:{secs:02d}
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⏸ Stop Timer", key="stop_timer", use_container_width=True):
                        st.session_state["timer_paused_at"] = elapsed
                        st.rerun()
                with col2:
                    if st.button("🏠 Go Home", key="cancel_timer", use_container_width=True):
                        del st.session_state["calm_activity"]
                        st.session_state["timer_start_time"] = None
                        st.session_state["timer_paused_at"] = None
                        st.session_state["child_page"] = "home"
                        st.rerun()

                # Auto-refresh every second
                time_module.sleep(1)
                st.rerun()

            elif st.session_state.get("timer_paused_at"):
                # Timer is paused
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 2rem;'>
                        <h2 style='color: #d5006d;'>⏸ Timer Stopped</h2>
                        <p style='font-size: 1.4rem; color: #c2185b;'>Take your time!</p>
                    </div>
                """, unsafe_allow_html=True)

                mins, secs = divmod(remaining, 60)
                st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #ffd4e5 0%, #ffe5f0 100%);
                        color: #d5006d;
                        padding: 4rem 2rem;
                        border-radius: 2rem;
                        text-align: center;
                        font-size: 4rem;
                        font-weight: 700;
                        margin: 2rem 0;
                        border: 3px solid #ffb6d9;
                        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.3);
                    '>
                        {mins:02d}:{secs:02d}
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Resume Timer", key="resume_timer", use_container_width=True, type="primary"):
                        # Resume by adjusting start time
                        st.session_state["timer_start_time"] = time_module.time() - st.session_state["timer_paused_at"]
                        st.session_state["timer_paused_at"] = None
                        st.rerun()
                with col2:
                    if st.button("🏠 Go Home", key="cancel_paused_timer", use_container_width=True):
                        del st.session_state["calm_activity"]
                        st.session_state["timer_start_time"] = None
                        st.session_state["timer_paused_at"] = None
                        st.session_state["child_page"] = "home"
                        st.rerun()

            else:
                # Timer finished!
                st.markdown("""
                    <div style='
                        background: linear-gradient(135deg, #ff85c0 0%, #ffb6d9 100%);
                        color: white;
                        padding: 3rem 2rem;
                        border-radius: 2rem;
                        text-align: center;
                        border: 3px solid #ff69b4;
                        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.4);
                    '>
                        <h2>✨ Time is up! ✨</h2>
                        <p style='font-size: 2rem; margin: 2rem 0;'>🐇💖</p>
                        <p style='font-size: 1.3rem;'>
                            Little Star Rabbit is done resting with you.<br>
                            Well done taking quiet time!
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("All done! 🌟", key="done_resting", use_container_width=True, type="primary"):
                    del st.session_state["calm_activity"]
                    st.session_state["timer_start_time"] = None
                    st.session_state["timer_paused_at"] = None
                    st.session_state["child_page"] = "home"
                    st.rerun()

# ============================================================================
# NEW FEATURE PAGES
# ============================================================================

def show_ask_a_little_star():
    """FEATURE 2: Wonder questions Q&A page"""
    child_name = profile.get("child_name", "Little Star")

    st.markdown("### ✨ Ask a Little Star")

    st.markdown("""
        <div style='
            background: #fff0f5;
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid #ffb6d9;
            margin: 1rem 0;
        '>
            <p style='margin: 0;'>You can ask a wonder-question, like:</p>
            <ul>
                <li>"Why do people cry?"</li>
                <li>"Do dogs have dreams?"</li>
                <li>"Why is the sky blue?"</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Wonder question suggestion
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input("What do you wonder about?", placeholder="Type your question here...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ I need an idea"):
            suggestion = generate_wonder_question_prompt()
            st.session_state["wonder_suggestion"] = suggestion
            st.rerun()

    # Show suggestion if available
    if st.session_state.get("wonder_suggestion"):
        st.info(f"💡 Try asking: {st.session_state['wonder_suggestion']}")
        if st.button("Use this question"):
            question = st.session_state["wonder_suggestion"]
            st.session_state["wonder_suggestion"] = None

    if st.button("🌟 Answer my wonder!", type="primary", use_container_width=True):
        if not question or len(question.strip()) < 3:
            st.warning("🐇 Type a question first, then press the button!")
        else:
            with st.spinner("Thinking about your question..."):
                answer = answer_wonder_question(question, child_name)

                st.markdown("---")
                st.markdown(f"**You asked:** {question}")

                render_read_aloud(answer, "Read the answer", f"wonder_{hash(question)}")

                # Track achievement
                st.session_state["asked_wonder_question_today"] = True
                st.session_state["questions_asked_count"] = st.session_state.get("questions_asked_count", 0) + 1
                check_strength_unlocks()

def show_little_wins():
    """FEATURE 4: Little Wins tracker"""
    st.markdown("### 🏅 Little Wins")

    st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            <p style='font-size: 1.2rem; color: #c2185b;'>
                These are things you've done today. No scores, no streaks - just gentle celebrations!
            </p>
        </div>
    """, unsafe_allow_html=True)

    wins = []

    if st.session_state.get("completed_storytime_today"):
        wins.append("⭐ You enjoyed a story today")

    if st.session_state.get("selected_feeling_today"):
        wins.append("⭐ You noticed your feelings today")

    if st.session_state.get("did_bunny_breaths_today"):
        wins.append("⭐ You took some bunny breaths")

    if st.session_state.get("asked_wonder_question_today"):
        wins.append("⭐ You asked a wonder question")

    if st.session_state.get("used_journal_today"):
        wins.append("⭐ You shared your thoughts in the journal")

    if st.session_state.get("used_routines_today"):
        wins.append("⭐ You tried a Little Star Routine")

    if wins:
        for win in wins:
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ffe5f0 0%, #fff0f5 100%);
                    padding: 1rem;
                    border-radius: 10px;
                    border: 2px solid #ffb6d9;
                    margin: 0.5rem 0;
                    font-size: 1.3rem;
                    text-align: center;
                '>
                    {win}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <p style='font-size: 1.2rem; color: #c2185b;'>
                    You haven't collected any wins yet today.<br>
                    That's okay! Every moment is a fresh start. 💖
                </p>
            </div>
        """, unsafe_allow_html=True)

def show_secret_strengths():
    """FEATURE 8: Secret Strengths constellation"""
    st.markdown("### ⭐ Secret Strengths")

    st.markdown("""
        <div style='text-align: center; margin: 1rem 0 2rem 0;'>
            <p style='font-size: 1.2rem; color: #c2185b;'>
                These are special strengths you're discovering, one star at a time.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Define all strengths
    strengths = {
        "feelings_noticer": {
            "title": "⭐ Feelings Noticer",
            "description": "You pay attention to your feelings. That takes courage and care.",
            "condition": "Use Feelings & Stars 3 times"
        },
        "curious_learner": {
            "title": "⭐ Curious Learner",
            "description": "You're curious about how things work. Your questions make the world more interesting.",
            "condition": "Read 5 stories"
        },
        "wonder_seeker": {
            "title": "⭐ Wonder Seeker",
            "description": "You ask beautiful questions about the world. Keep wondering!",
            "condition": "Ask 3 wonder questions"
        },
        "calm_finder": {
            "title": "⭐ Calm Finder",
            "description": "You know how to help your body feel calm. That's a powerful skill.",
            "condition": "Use Calm Burrow 5 times"
        },
    }

    unlocked = st.session_state.get("unlocked_strengths", set())

    for strength_id, strength_info in strengths.items():
        if strength_id in unlocked:
            # Unlocked - show fully
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ff85c0 0%, #ffb6d9 100%);
                    color: white;
                    padding: 1.5rem;
                    border-radius: 15px;
                    border: 3px solid #ff69b4;
                    margin: 1rem 0;
                    box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);
                '>
                    <h3 style='color: white; margin: 0 0 0.5rem 0;'>{strength_info['title']}</h3>
                    <p style='color: white; margin: 0; font-size: 1.1rem;'>{strength_info['description']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Locked - show hint
            st.markdown(f"""
                <div style='
                    background: rgba(255, 182, 217, 0.2);
                    padding: 1.5rem;
                    border-radius: 15px;
                    border: 2px dashed #ffb6d9;
                    margin: 1rem 0;
                    opacity: 0.6;
                '>
                    <h3 style='margin: 0 0 0.5rem 0;'>🔒 ???</h3>
                    <p style='margin: 0; font-size: 0.9rem; color: #999;'>{strength_info['condition']}</p>
                </div>
            """, unsafe_allow_html=True)

def show_bunny_journal():
    """FEATURE 5: Bunny Journal"""
    child_name = profile.get("child_name", "Little Star")

    st.markdown("### 📓 Bunny Journal")

    st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            <p style='font-size: 1.2rem; color: #c2185b;'>
                This is a safe place to share your thoughts, feelings, or drawings.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Simple text journal
    st.markdown("**Write or tell something about your day:**")
    journal_text = st.text_area(
        "Your thoughts...",
        placeholder="You can write anything you want here. It's just for you.",
        height=150,
        label_visibility="collapsed"
    )

    # Drawing simulation (since we can't easily embed canvas)
    st.markdown("**Or imagine drawing something:**")
    st.info("🎨 Close your eyes and imagine drawing what you're feeling. What colors would you use? What shapes?")

    if st.button("🐇 Share with the bunny", use_container_width=True, type="primary"):
        if journal_text and len(journal_text.strip()) > 0:
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ffe5f0 0%, #fff0f5 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    border: 3px solid #ffb6d9;
                    text-align: center;
                    margin: 1rem 0;
                '>
                    <p style='font-size: 1.3rem; color: #c2185b; margin: 0;'>
                        Thank you for sharing your thoughts today, {child_name}.<br>
                        It takes care to put things on the page. 💖
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.session_state["used_journal_today"] = True
        else:
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #ffe5f0 0%, #fff0f5 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    border: 3px solid #ffb6d9;
                    text-align: center;
                    margin: 1rem 0;
                '>
                    <p style='font-size: 1.3rem; color: #c2185b; margin: 0;'>
                        That's okay! Sometimes we just want to be quiet.<br>
                        The bunny is here whenever you're ready. 🐇
                    </p>
                </div>
            """, unsafe_allow_html=True)

def show_star_routines():
    """FEATURE 6: Little Star Routines"""
    child_name = profile.get("child_name", "Little Star")

    st.markdown("### 🌅 Little Star Routines")

    st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            <p style='font-size: 1.2rem; color: #c2185b;'>
                Tiny rituals for different parts of your day
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Three tabs for different times
    tab1, tab2, tab3 = st.tabs(["🌅 Morning Sparkle", "🏫 After-School Pause", "🌙 Bedtime Glow"])

    with tab1:
        st.markdown("#### Morning Sparkle")
        morning = generate_routine_content("morning", child_name)

        st.markdown("**Tiny Stretch:**")
        render_read_aloud(morning["stretch"], "Read stretch", "morning_stretch")

        st.markdown("**Morning Thought:**")
        render_read_aloud(morning["thought"], "Read thought", "morning_thought")

    with tab2:
        st.markdown("#### After-School Pause")
        afterschool = generate_routine_content("afterschool", child_name)

        st.markdown("**Three Bunny Breaths:**")
        render_read_aloud(afterschool["breath"], "Read breaths", "afterschool_breath")

        st.markdown("**Body Check:**")
        render_read_aloud(afterschool["question"], "Read question", "afterschool_question")

    with tab3:
        st.markdown("#### Bedtime Glow")
        bedtime = generate_routine_content("bedtime", child_name)

        st.markdown("**Calm Script:**")
        render_read_aloud(bedtime["script"], "Read script", "bedtime_script")

        st.markdown("**Goodnight Reminder:**")
        render_read_aloud(bedtime["reminder"], "Read reminder", "bedtime_reminder")

    st.session_state["used_routines_today"] = True

# ============================================================================
# ADMIN MODE
# ============================================================================

def show_admin_mode():
    """Admin mode controller"""
    # Check authentication
    if not st.session_state.get("admin_authenticated"):
        show_admin_login()
        return

    # Header with exit button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔒 Grown-ups' Corner")
    with col2:
        if st.button("🚪 Exit", use_container_width=True):
            st.session_state["admin_authenticated"] = False
            st.session_state["mode"] = "landing"
            st.rerun()

    st.markdown("---")

    # Main navigation using tabs - all sections visible at once!
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Child Profile",
        "⚙️ Content Settings",
        "💝 Affirmations & Lessons",
        "⏰ Time & Limits",
        "🔐 Safety & API"
    ])

    with tab1:
        show_admin_profile()

    with tab2:
        show_admin_content()

    with tab3:
        show_admin_affirmations()

    with tab4:
        show_admin_time()

    with tab5:
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
    st.markdown("### Customize the app for your child")
    st.markdown("")

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

    # Add cute floating doodles
    add_cute_doodles()

    # Route to appropriate mode
    if st.session_state["mode"] == "landing":
        show_landing()
    elif st.session_state["mode"] == "child":
        show_child_mode()
    elif st.session_state["mode"] == "admin":
        show_admin_mode()

if __name__ == "__main__":
    main()
