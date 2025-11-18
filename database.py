"""
Database utilities for Little Star Rabbit app using Neon PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from datetime import datetime
import json

def get_db_connection():
    """Get database connection from Streamlit secrets"""
    try:
        conn = psycopg2.connect(
            st.secrets["database"]["url"],
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

def init_database():
    """Initialize database tables if they don't exist"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        # Profiles table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id SERIAL PRIMARY KEY,
                child_name VARCHAR(100) NOT NULL,
                age INTEGER,
                pronouns VARCHAR(50),
                interests TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Journal entries table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                entry_text TEXT NOT NULL,
                mood VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Wins/achievements table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS wins (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                win_text TEXT NOT NULL,
                win_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Unlocked strengths table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS unlocked_strengths (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                strength_id VARCHAR(100) NOT NULL,
                strength_name VARCHAR(200),
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(profile_id, strength_id)
            )
        """)

        # Story history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS story_history (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                story_text TEXT NOT NULL,
                story_length VARCHAR(20),
                story_topic VARCHAR(100),
                story_mood VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Settings table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS app_settings (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                setting_key VARCHAR(100) NOT NULL,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(profile_id, setting_key)
            )
        """)

        # Usage tracking table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usage_tracking (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                activity_type VARCHAR(100),
                activity_count INTEGER DEFAULT 1,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        if conn:
            conn.close()
        return False

# ============================================================================
# PROFILE FUNCTIONS
# ============================================================================

def create_or_get_profile(child_name, age=None, pronouns=None, interests=None):
    """Create a new profile or get existing one by name"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor()

        # Check if profile exists
        cur.execute("SELECT * FROM profiles WHERE child_name = %s", (child_name,))
        profile = cur.fetchone()

        if profile:
            profile_id = profile['id']
        else:
            # Create new profile
            cur.execute("""
                INSERT INTO profiles (child_name, age, pronouns, interests)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (child_name, age, pronouns, interests or []))
            profile_id = cur.fetchone()['id']
            conn.commit()

        cur.close()
        conn.close()
        return profile_id
    except Exception as e:
        st.error(f"Profile error: {str(e)}")
        if conn:
            conn.close()
        return None

def update_profile(profile_id, child_name=None, age=None, pronouns=None, interests=None):
    """Update profile information"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        updates = []
        params = []

        if child_name is not None:
            updates.append("child_name = %s")
            params.append(child_name)
        if age is not None:
            updates.append("age = %s")
            params.append(age)
        if pronouns is not None:
            updates.append("pronouns = %s")
            params.append(pronouns)
        if interests is not None:
            updates.append("interests = %s")
            params.append(interests)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(profile_id)
            query = f"UPDATE profiles SET {', '.join(updates)} WHERE id = %s"
            cur.execute(query, params)
            conn.commit()

        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Profile update error: {str(e)}")
        if conn:
            conn.close()
        return False

# ============================================================================
# JOURNAL FUNCTIONS
# ============================================================================

def save_journal_entry(profile_id, entry_text, mood=None):
    """Save a journal entry"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO journal_entries (profile_id, entry_text, mood)
            VALUES (%s, %s, %s)
        """, (profile_id, entry_text, mood))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Journal save error: {str(e)}")
        if conn:
            conn.close()
        return False

def get_journal_entries(profile_id, limit=10):
    """Get recent journal entries"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM journal_entries
            WHERE profile_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (profile_id, limit))
        entries = cur.fetchall()
        cur.close()
        conn.close()
        return entries
    except Exception as e:
        st.error(f"Journal fetch error: {str(e)}")
        if conn:
            conn.close()
        return []

# ============================================================================
# WINS/ACHIEVEMENTS FUNCTIONS
# ============================================================================

def save_win(profile_id, win_text, win_type=None):
    """Save a win/achievement"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO wins (profile_id, win_text, win_type)
            VALUES (%s, %s, %s)
        """, (profile_id, win_text, win_type))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Win save error: {str(e)}")
        if conn:
            conn.close()
        return False

def get_wins(profile_id, limit=50):
    """Get recent wins"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM wins
            WHERE profile_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (profile_id, limit))
        wins = cur.fetchall()
        cur.close()
        conn.close()
        return wins
    except Exception as e:
        st.error(f"Wins fetch error: {str(e)}")
        if conn:
            conn.close()
        return []

# ============================================================================
# STRENGTHS FUNCTIONS
# ============================================================================

def unlock_strength(profile_id, strength_id, strength_name):
    """Unlock a strength for a profile"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO unlocked_strengths (profile_id, strength_id, strength_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (profile_id, strength_id) DO NOTHING
        """, (profile_id, strength_id, strength_name))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Strength unlock error: {str(e)}")
        if conn:
            conn.close()
        return False

def get_unlocked_strengths(profile_id):
    """Get all unlocked strengths for a profile"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM unlocked_strengths
            WHERE profile_id = %s
            ORDER BY unlocked_at DESC
        """, (profile_id,))
        strengths = cur.fetchall()
        cur.close()
        conn.close()
        return strengths
    except Exception as e:
        st.error(f"Strengths fetch error: {str(e)}")
        if conn:
            conn.close()
        return []

# ============================================================================
# STORY HISTORY FUNCTIONS
# ============================================================================

def save_story(profile_id, story_text, length=None, topic=None, mood=None):
    """Save a generated story"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO story_history (profile_id, story_text, story_length, story_topic, story_mood)
            VALUES (%s, %s, %s, %s, %s)
        """, (profile_id, story_text, length, topic, mood))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Story save error: {str(e)}")
        if conn:
            conn.close()
        return False

def get_story_history(profile_id, limit=20):
    """Get story history"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM story_history
            WHERE profile_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (profile_id, limit))
        stories = cur.fetchall()
        cur.close()
        conn.close()
        return stories
    except Exception as e:
        st.error(f"Story history fetch error: {str(e)}")
        if conn:
            conn.close()
        return []

# ============================================================================
# USAGE TRACKING FUNCTIONS
# ============================================================================

def track_activity(profile_id, activity_type):
    """Track usage activity"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usage_tracking (profile_id, activity_type, activity_count, last_activity)
            VALUES (%s, %s, 1, CURRENT_TIMESTAMP)
            ON CONFLICT (profile_id, activity_type)
            DO UPDATE SET
                activity_count = usage_tracking.activity_count + 1,
                last_activity = CURRENT_TIMESTAMP
        """, (profile_id, activity_type))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        # Silently fail for tracking to not disrupt user experience
        if conn:
            conn.close()
        return False
