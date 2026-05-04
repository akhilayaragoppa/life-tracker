#!/usr/bin/env python3
"""
Simple test script to verify the capture system works.
Run after setting up .env file.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_capture():
    """Test the capture endpoint with various inputs"""

    test_inputs = [
        "call the dentist sometime this week",
        "build self confidence",
        "grocery shopping tomorrow",
        "learn to play guitar - would love to play my favorite songs",
        "fix the leaky faucet by end of week"
    ]

    print("Testing capture endpoint...\n")

    for text in test_inputs:
        print(f"Input: {text}")

        response = requests.post(
            f"{BASE_URL}/capture",
            json={"text": text}
        )

        if response.status_code == 200:
            data = response.json()
            classification = data["classification"]

            print(f"  ✓ Type: {classification['item_type']}")
            print(f"  ✓ Title: {classification['title']}")
            print(f"  ✓ Category: {classification['category']}")
            print(f"  ✓ Timeline: {classification['timeline']}")

            if classification.get('loose_deadline'):
                print(f"  ✓ Deadline: {classification['loose_deadline']}")

            if classification.get('suggested_tasks'):
                print(f"  ✓ Suggested tasks: {', '.join(classification['suggested_tasks'])}")

            print()
        else:
            print(f"  ✗ Error: {response.status_code}")
            print(f"    {response.text}\n")


def test_inbox():
    """Test retrieving inbox items"""

    print("\nTesting inbox retrieval...\n")

    response = requests.get(f"{BASE_URL}/inbox?processed=false")

    if response.status_code == 200:
        items = response.json()
        print(f"✓ Found {len(items)} unprocessed items in inbox")

        for item in items[:3]:  # Show first 3
            print(f"  - {item['classification']['title']}")
    else:
        print(f"✗ Error: {response.status_code}")


if __name__ == "__main__":
    print("Life Tracker Backend Test\n" + "="*50 + "\n")

    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Server is running\n")
            test_capture()
            test_inbox()
        else:
            print("✗ Server returned unexpected status")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server at", BASE_URL)
        print("  Make sure the server is running: python main.py")
