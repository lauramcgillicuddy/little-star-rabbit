"""
GPT utility functions for Little Star Rabbit
Centralizes all OpenAI API calls with trauma-aware, child-safe prompts
"""

from openai import OpenAI
import streamlit as st
from typing import Optional
from dataclasses import dataclass

@dataclass
class StoryOptions:
    length: str  # "short", "medium", "long"
    topic: str
    mood: str
    child_name: str

def get_openai_client() -> Optional[OpenAI]:
    """Get OpenAI client from settings or environment"""
    try:
        # Try to get from Streamlit secrets first
        if hasattr(st, 'secrets') and 'openai' in st.secrets:
            api_key = st.secrets['openai']['api_key']
            return OpenAI(api_key=api_key)
        # Fall back to settings or environment
        import json
        from pathlib import Path
        settings_file = Path("data/settings.json")
        if settings_file.exists():
            with open(settings_file) as f:
                settings = json.load(f)
                api_key = settings.get('api_key')
                if api_key:
                    return OpenAI(api_key=api_key)
        # Last resort: environment variable
        return OpenAI()
    except Exception:
        return None

def generate_story(options: StoryOptions) -> str:
    """Generate a trauma-aware bedtime story"""
    client = get_openai_client()
    if not client:
        return "I'm having trouble thinking of a story right now. Try again in a moment!"

    word_limits = {"short": 300, "medium": 500, "long": 700}
    word_limit = word_limits.get(options.length, 400)

    prompt = f"""Write a gentle, cozy story for a 7-year-old girl named {options.child_name}.

Topic: {options.topic}
Mood: {options.mood}
Length: approximately {word_limit} words

RULES:
- Keep it warm, safe, and non-scary
- No family conflict, no loss, no danger
- Focus on wonder, kindness, nature, animals, or gentle adventure
- End on a calm, happy note
- Use simple, age-7 vocabulary
- No mention of parents, trauma, or anything heavy
- Make the main character curious and capable

Write the story now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=word_limit + 100,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"I'm having trouble making up a story right now. Maybe try again in a moment?"

def generate_star_facts(topic: str) -> list[str]:
    """Generate 3-5 kid-friendly facts about a topic"""
    client = get_openai_client()
    if not client:
        return ["I'm having trouble thinking of facts right now!"]

    prompt = f"""Generate exactly 4 fascinating, positive facts about {topic} for a 7-year-old.

RULES:
- Each fact should be 1-2 short sentences
- Use simple, age-7 vocabulary
- Make them wonder-inducing and positive
- NO sad facts (extinctions, natural disasters, death, etc.)
- NO scary facts
- Focus on amazing, beautiful, or funny things

Format as a simple numbered list (1. 2. 3. 4.)"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        facts_text = response.choices[0].message.content.strip()
        # Parse into list
        facts = []
        for line in facts_text.split('\n'):
            line = line.strip()
            # Remove numbering
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                fact = line.lstrip('0123456789.-•) ').strip()
                if fact:
                    facts.append(fact)
        return facts if facts else [facts_text]
    except Exception:
        return ["I'm having trouble thinking of facts right now!"]

def generate_feelings_response(feeling: str, character_name: str) -> dict:
    """Generate validating response for a feeling with character"""
    client = get_openai_client()
    if not client:
        return {
            "validation": "Your feelings make sense, whatever they are.",
            "suggestion": "Maybe try taking a deep breath?",
            "reminder": "You're doing okay."
        }

    prompt = f"""A 7-year-old girl has selected the feeling: {feeling}
The emotion character is named: {character_name}

Generate a response with THREE parts:

1. VALIDATION (2-3 sentences): Validate the feeling warmly. Mention {character_name} is visiting. Explain what this feeling might feel like in the body (tummy, chest, etc.). Say it's okay to feel this way.

2. SUGGESTION (1 sentence): Offer ONE tiny, gentle suggestion like "Would you like to try a bunny breath?" or "Maybe draw what {character_name} looks like?" - NOT a command.

3. REMINDER (1 sentence): A short reminder that feelings come and go, or that she's doing okay.

RULES:
- Never say "I love you" or "I'm your friend"
- Don't mention parents, family, trauma, or anything heavy
- Keep it warm but not saccharine
- Age-7 vocabulary
- No shame, only validation

Format:
VALIDATION: [text]
SUGGESTION: [text]
REMINDER: [text]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()

        # Parse the response
        result = {"validation": "", "suggestion": "", "reminder": ""}
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('VALIDATION:'):
                result['validation'] = line.replace('VALIDATION:', '').strip()
            elif line.startswith('SUGGESTION:'):
                result['suggestion'] = line.replace('SUGGESTION:', '').strip()
            elif line.startswith('REMINDER:'):
                result['reminder'] = line.replace('REMINDER:', '').strip()

        return result
    except Exception:
        return {
            "validation": f"It sounds like {character_name} is with you today. Your feelings make sense.",
            "suggestion": "Would you like to try a bunny breath together?",
            "reminder": "Feelings come and go, like clouds in the sky."
        }

def generate_little_lesson(topic: str, child_name: str) -> str:
    """Generate psycho-education content for kids"""
    client = get_openai_client()
    if not client:
        return "I'm having trouble explaining this right now. Try again soon!"

    prompt = f"""Write a very short lesson about {topic} for a 7-year-old named {child_name}.

RULES:
- 3-4 short paragraphs maximum
- Age-7 vocabulary
- Focus on self-kindness, feelings, bodies, basic coping
- Warm and encouraging tone
- No mention of parents, trauma, abuse, or anything heavy
- Make it about "lots of kids" not "you specifically"
- Include 1-2 tiny examples

Write the lesson now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "I'm having trouble explaining this right now!"

def generate_daily_affirmation(child_name: str) -> str:
    """Generate a gentle daily affirmation"""
    client = get_openai_client()
    if not client:
        return f"{child_name}, I'm really glad you're here today."

    prompt = f"""Write one short, gentle message for a 7-year-old girl named {child_name}.

RULES:
- 1-2 sentences maximum
- Tell her she matters and is welcome
- Do NOT use "love", "friend", or mention parents
- Focus on: worth, curiosity, feelings being okay, ideas mattering
- Warm but not saccharine
- Age-7 vocabulary

Write the message now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip().strip('"')
    except Exception:
        return f"{child_name}, I'm really glad you're here today."

def answer_wonder_question(question: str, child_name: str) -> str:
    """Answer a wonder question safely"""
    client = get_openai_client()
    if not client:
        return "That's such a good question! I'm having trouble thinking right now, but keep wondering!"

    prompt = f"""A 7-year-old named {child_name} asked: "{question}"

Answer this in 2-4 simple sentences.

RULES:
- Be warm, curious, and non-judgmental
- Age-7 vocabulary
- Don't mention parents, religion, politics, or anything heavy
- Focus on feelings, bodies, animals, science, nature, or everyday life
- Validate that wondering is good
- If the question is inappropriate or too heavy, gently redirect

Answer now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "That's such a good question! Keep wondering about the world."

def generate_wonder_question_prompt() -> str:
    """Generate a fun wonder question suggestion"""
    client = get_openai_client()
    if not client:
        return "What color do you think the wind would be if we could see it?"

    prompt = """Generate ONE fun, imaginative question for a 7-year-old.

RULES:
- NOT personal, NOT about family, NOT about trauma, NOT scary
- About: animals, nature, space, colors, gentle feelings, imagination
- 1 sentence
- Should spark wonder and curiosity
- Age-appropriate

Examples:
- "If you could invent an animal, what would it be like?"
- "What's a sound you really like?"
- "What color do you think happiness would be?"

Generate one question now:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip().strip('"?') + '?'
    except Exception:
        return "If animals could talk, what do you think a bunny would say?"

def generate_routine_content(routine_type: str, child_name: str) -> dict:
    """Generate content for morning/afterschool/bedtime routines"""
    client = get_openai_client()

    templates = {
        "morning": {
            "stretch": "Reach up high like you're touching a star, then gently float your arms down.",
            "thought": f"Good morning, {child_name}. Your ideas make the world more interesting."
        },
        "afterschool": {
            "breath": "Let's take three slow bunny breaths together. In through your nose... out through your mouth.",
            "question": "How does your body feel right now? Calm? Fizzy? Tired? All of those are okay."
        },
        "bedtime": {
            "script": f"Close your eyes if you want to, {child_name}. Imagine a tiny star floating gently in the sky. It's peaceful and safe. You can rest now.",
            "reminder": "Time to put the screen down and get cosy. Sleep well, little star."
        }
    }

    return templates.get(routine_type, templates["morning"])
