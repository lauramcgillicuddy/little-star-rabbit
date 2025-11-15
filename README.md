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

- **Streamlit** — UI / frontend
- **Python** — app logic
- **OpenAI API** (optional) — safe content generation
- **Session State** — navigation + time tracking
- **JSON** — persistent storage for settings, affirmations, and lessons

📁 Project Structure

```
little-star-rabbit/
│
├── app.py                 # Main Streamlit app (all-in-one)
├── requirements.txt       # Python dependencies
│
├── data/                  # Auto-created on first run
│   ├── profile.json       # Child profile settings
│   ├── settings.json      # Admin settings & API keys
│   ├── affirmations.json  # Affirmations by feeling
│   ├── lessons.json       # Mini-lessons library
│   └── usage.json         # Daily usage tracking
│
└── README.md
```

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

**1. Clone the repository:**

```bash
git clone https://github.com/lauramcgillicuddy/little-star-rabbit.git
cd little-star-rabbit
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Run the app:**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**4. First-time setup:**

- Click "Grown-ups' Corner" on the landing page
- Enter the default PIN: `1234`
- Go to "Safety & API" settings
- **IMPORTANT:** Change the default PIN to something secure!
- Enter your OpenAI API key (get one at https://platform.openai.com/api-keys)
- Configure other settings as desired

**5. Customize for your child:**

- Go to "Child Profile" and enter your child's name, age, and interests
- Adjust content settings, time limits, and quiet hours
- Review and customize affirmations and lessons

**Note:** Your API key and all settings are stored locally in the `data/` folder. This folder is gitignored for security.

---

## ☁️ Deploying to Streamlit Cloud (Recommended)

Want to access the app from anywhere? Deploy it for free to Streamlit Community Cloud!

**1. Push your code to GitHub:**

Your code is already in this GitHub repository. Make sure all changes are committed and pushed.

**2. Go to Streamlit Community Cloud:**

- Visit [share.streamlit.io](https://share.streamlit.io)
- Sign in with your GitHub account
- Click "New app"

**3. Configure your app:**

- **Repository:** `lauramcgillicuddy/little-star-rabbit`
- **Branch:** `main` (or your preferred branch)
- **Main file path:** `app.py`

**4. Set up secrets:**

Before deploying, you MUST configure your secrets:

- Click "Advanced settings"
- In the "Secrets" section, paste the following (with your actual values):

```toml
# OpenAI API Configuration
[openai]
api_key = "sk-your-actual-openai-api-key-here"

# Admin Settings
[admin]
pin = "your-secure-pin-here"  # CHANGE THIS!

# Child Profile (optional - can also configure in the app)
[profile]
child_name = "Aoibheann"
age = 7
pronouns = "she/her"
interests = "space,animals,stars,ducks"
```

**5. Deploy!**

- Click "Deploy"
- Wait a few minutes for your app to build
- You'll get a URL like `https://your-app-name.streamlit.app`
- Bookmark it and share with family!

**Important Notes for Cloud Deployment:**

- Secrets are REQUIRED on Streamlit Cloud (API key and PIN)
- Any settings you change in the Grown-ups' Corner will be saved to the cloud instance
- The `data/` folder persists between sessions on the same cloud instance
- If you redeploy the app, your `data/` folder may be reset, so keep backups of important customizations
- You can update secrets anytime from the Streamlit Cloud dashboard

**Privacy Note:** When deployed to Streamlit Cloud, your data is stored on Streamlit's servers. For maximum privacy, consider running locally instead.

---

🌸 Customisation

All affirmations, lessons, themes, word filters, and story settings can be customized via:

**Option 1: Through the UI (Recommended)**
- Use the Grown-ups' Corner admin interface
- All changes are saved automatically to JSON files
- No coding required!

**Option 2: Edit JSON files directly**
- Navigate to the `data/` folder
- Edit `affirmations.json`, `lessons.json`, etc.
- Restart the app to see changes

**Option 3: Modify the code**
- Edit default values in `app.py`
- Customize system prompts for GPT
- Adjust styling and layout

This makes the app adaptable for different ages, family values, or educational needs.

⚙️ Configuration Options

**In Grown-ups' Corner, you can:**

- ✏️ Set child's name, age, pronouns, and interests
- 🚫 Block specific topics (death, violence, scary content)
- 📖 Set reading level (very simple / simple / normal)
- ⏰ Set daily time limits and quiet hours
- 💬 Add custom affirmations and lessons
- 🔐 Change the admin PIN
- 🤖 Configure OpenAI API settings (model, temperature, etc.)

🤍 Credits

Designed & developed by:
🌸 Laura McGillicuddy
For sweet Aoibheann, who deserves a safe little universe of her own.
