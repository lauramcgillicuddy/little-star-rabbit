🌟 Little Star Rabbit

A gentle, kid-safe companion app built with Streamlit.

Little Star Rabbit is a small, cosy digital space designed for young children to explore stories, learn simple facts, practice emotional literacy, and enjoy calm time — all within a safe, curated environment.
The app runs on Streamlit and optionally integrates with GPT APIs to generate child-appropriate content under strict safety controls.

Created with care by Laura McGillicuddy for Aoibheann, and built to be easily extended by parents or guardians.

✨ Features
🐇 Child Mode

A simple, accessible interface with large buttons, gentle colours, and no sidebar navigation.
Child Mode contains:

1. Storytime

Generate kid-safe stories using GPT

Choose themes (Animals, Space, Magic, Friends, Surprise)

Select story length

Strict safety filters and language constraints

2. Star Facts

Bite-sized facts in simple language

Categories: Space, Animals, Nature, How Things Work

Designed to spark curiosity without overwhelm

3. Feelings & Stars

A gentle emotional-awareness space with:

Feeling buttons (Happy, Sad, Angry, Worried, “I Don’t Know,” etc.)

Validating text (“It’s okay to feel this way.”)

Small grounding ideas (“Let’s take 3 bunny breaths together.”)

Soft affirmations that emphasise safety and worth

4. Little Lessons

Tiny, child-friendly explanations of:

Kindness

Friendship

Boundaries

Worries

School & focus

Simple “try this” prompts
Lessons can be prewritten or generated with safe prompting.

5. Calm Burrow

A quiet, grounding section including:

“Bunny Breaths” (guided breathing)

The Star Countdown (5–4–3–2–1 senses)

A Calm Timer / Timebox

A gentle end-of-session message

🧑‍🏫 Grown-Ups’ Corner (Admin Mode)

PIN-protected area for parents/guardians.

1. Child Profile

Name / nickname

Age

Interests (space, animals, sharks, ducks etc.)
Used to personalise stories & facts.

2. Content Controls

Toggle AI-generated content on/off

Story length controls

Reading level slider

Allowed & banned themes

Optional custom banned-word list

3. Affirmations & Lessons Library

Add, edit, delete affirmations

Add custom mini-lessons

Tag content by feeling or theme

4. Time & Usage Limits

Daily time limit

Session length limit

Quiet hours

Automatic lock after time limit reached

5. Safety + API Settings

GPT API keys (hidden after entry)

Model selection

Temperature / token controls

Preview of system prompts used for child content

🧩 Tech Stack

Streamlit — UI / frontend

Python — app logic

GPT API (optional) — safe content generation

Session State — navigation + time tracking

YAML / JSON — storing admin content (affirmations, lessons)

📁 Project Structure (suggested)
little-star-rabbit/
│
├── app.py                 # Main Streamlit app
├── pages/                 # Optional subpages (if not using state routing)
│
├── config/
│   ├── settings.yaml      # Admin settings (time limits, reading level, etc.)
│   ├── affirmations.json  # Bank of affirmations
│   ├── lessons.json       # Mini-lessons library
│   └── filters.json       # Banned words / safe themes
│
├── utils/
│   ├── prompts.py         # System prompts for safe GPT usage
│   ├── generation.py      # GPT wrappers
│   ├── state.py           # Session state helpers
│   └── safety.py          # Output filtering
│
├── assets/
│   ├── logo.png
│   ├── bunny.svg
│   └── icons/
│
└── README.md

🛡 Safety Principles

Little Star Rabbit is built around:

Kid-safe language filters

No violence, fear, illness, or harmful topics

Positive, validating emotional support

Simple, gentle explanations

Predictable navigation

Clear time boundaries

The aim is not diagnosis, but providing a warm, safe digital space where a child can rest, learn, and feel understood.

🚀 Installation & Running

Clone the repo:

git clone https://github.com/yourname/little-star-rabbit.git
cd little-star-rabbit


Install dependencies:

pip install -r requirements.txt


Set your GPT API key:

export OPENAI_API_KEY="your-key-here"


Run the app:

streamlit run app.py

🌸 Customisation

All affirmations, lessons, themes, word filters, and story settings can be customised via:

The Grown-Ups’ Corner (UI)

Editing the JSON files

Modifying the system prompts in utils/prompts.py

This makes the app adaptable for different ages, family values, or educational needs.

🤍 Credits

Designed & developed by:
🌸 Laura McGillicuddy
For sweet Aoibheann, who deserves a safe little universe of her own.
