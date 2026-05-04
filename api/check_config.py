#!/usr/bin/env python3
"""
Configuration checker - verifies all keys and connections are working.
"""

from config import get_settings
import sys


def check_llm_provider():
    """Check if LLM provider is configured correctly"""
    settings = get_settings()

    print(f"LLM Provider: {settings.llm_provider}")

    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key or settings.anthropic_api_key == "your_anthropic_key_here":
            print("  ✗ ANTHROPIC_API_KEY not configured")
            return False
        print(f"  ✓ Anthropic API key configured ({settings.anthropic_api_key[:10]}...)")

        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=settings.anthropic_api_key)
            # Test with a simple call
            response = client.messages.create(
                model="claude-haiku-4.0-20250604",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            print("  ✓ Anthropic API working")
            return True
        except Exception as e:
            print(f"  ✗ Anthropic API error: {e}")
            return False

    elif settings.llm_provider == "google":
        if not settings.google_api_key or settings.google_api_key == "your_google_key_here":
            print("  ✗ GOOGLE_API_KEY not configured")
            return False
        print(f"  ✓ Google API key configured ({settings.google_api_key[:10]}...)")

        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.google_api_key)
            model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
            response = model.generate_content("test")
            print("  ✓ Google Gemini API working")
            return True
        except Exception as e:
            print(f"  ✗ Google API error: {e}")
            return False

    return False


def check_supabase():
    """Check if Supabase is configured correctly"""
    settings = get_settings()

    print(f"\nSupabase URL: {settings.supabase_url}")

    if not settings.supabase_url or settings.supabase_url == "your_supabase_url":
        print("  ✗ SUPABASE_URL not configured")
        return False

    if not settings.supabase_key or settings.supabase_key == "your_supabase_anon_key":
        print("  ✗ SUPABASE_KEY not configured")
        return False

    # Check if URL is correct format (should be REST API URL, not postgres URL)
    if "postgres." in settings.supabase_url:
        print("  ✗ Error: SUPABASE_URL appears to be a postgres connection URL")
        print("     It should be the REST API URL (starts with https://)")
        print("     Find it in: Supabase Dashboard → Settings → API → Project URL")
        return False

    print(f"  ✓ Supabase key configured ({settings.supabase_key[:20]}...)")

    try:
        from supabase import create_client
        client = create_client(settings.supabase_url, settings.supabase_key)

        # Test connection by listing tables
        result = client.table("inbox").select("id").limit(1).execute()
        print("  ✓ Supabase connection working")
        return True
    except Exception as e:
        print(f"  ✗ Supabase connection error: {e}")
        print("\nPossible issues:")
        print("  1. Make sure you've run supabase_schema.sql in your Supabase SQL Editor")
        print("  2. Verify the URL is the Project URL (not Database URL)")
        print("  3. Check that the anon key is correct")
        return False


if __name__ == "__main__":
    print("Life Tracker Configuration Check\n" + "="*50 + "\n")

    llm_ok = check_llm_provider()
    supabase_ok = check_supabase()

    print("\n" + "="*50)
    if llm_ok and supabase_ok:
        print("✓ All checks passed! Ready to run.")
        sys.exit(0)
    else:
        print("✗ Configuration issues found. Please fix them before running.")
        sys.exit(1)
