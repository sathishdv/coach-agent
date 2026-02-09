#!/usr/bin/env python3
"""Smoke test: onboard a student and run 3 interactions.

Usage:
    python scripts/smoke_test.py [--base-url http://localhost:8001/api]
"""

import argparse
import sys
import time

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="JEE Coach Agent Smoke Test")
    parser.add_argument(
        "--base-url", default="http://localhost:8001/api", help="API base URL"
    )
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    print("=" * 60)
    print("JEE Coach Agent — Smoke Test")
    print("=" * 60)

    student_id = f"smoke_{int(time.time())}"

    # --- 1. Health check ---
    print("\n[1/5] Health check...")
    try:
        r = httpx.get(f"{base}/health", timeout=10)
        r.raise_for_status()
        print(f"  OK: {r.json()}")
    except Exception as e:
        print(f"  FAIL: {e}")
        print("  Is the server running? Start with: python run.py")
        sys.exit(1)

    # --- 2. Onboard student ---
    print(f"\n[2/5] Onboarding student '{student_id}'...")
    try:
        r = httpx.post(
            f"{base}/student/{student_id}/onboard",
            json={
                "name": "Test Student",
                "grade": "12",
                "target_year": 2026,
                "daily_hours": 4,
                "strengths": ["Mathematics"],
                "weaknesses": ["Organic Chemistry"],
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        print(f"  OK: {data['message']}")
        print(f"  Coach says: {data['coach_response'][:200]}...")
    except Exception as e:
        print(f"  FAIL: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"  Detail: {e.response.text[:500]}")
        sys.exit(1)

    # --- 3. Chat interaction 1 ---
    print("\n[3/5] Chat: asking about kinematics...")
    try:
        r = httpx.post(
            f"{base}/chat",
            json={
                "student_id": student_id,
                "message": "Can you help me understand projectile motion? What are the key concepts I need to know for JEE?",
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        print(f"  OK: reply length = {len(data['reply'])} chars")
        print(f"  Preview: {data['reply'][:200]}...")
    except Exception as e:
        print(f"  FAIL: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"  Detail: {e.response.text[:500]}")

    # --- 4. Chat interaction 2 ---
    print("\n[4/5] Chat: asking to solve a problem (should get hints first)...")
    try:
        r = httpx.post(
            f"{base}/chat",
            json={
                "student_id": student_id,
                "message": "Solve this: A ball is thrown at 60 degrees with velocity 20 m/s. Find the maximum height.",
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        print(f"  OK: reply length = {len(data['reply'])} chars")
        print(f"  Preview: {data['reply'][:200]}...")
    except Exception as e:
        print(f"  FAIL: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"  Detail: {e.response.text[:500]}")

    # --- 5. Chat interaction 3 ---
    print("\n[5/5] Chat: attempting the problem...")
    try:
        r = httpx.post(
            f"{base}/chat",
            json={
                "student_id": student_id,
                "message": "I think the max height is H = u^2 sin^2(theta) / (2g) = 20^2 * sin^2(60) / (2*10) = 400 * 0.75 / 20 = 15 meters. Is that correct?",
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        print(f"  OK: reply length = {len(data['reply'])} chars")
        print(f"  Preview: {data['reply'][:200]}...")
    except Exception as e:
        print(f"  FAIL: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"  Detail: {e.response.text[:500]}")

    # --- 6. Get student profile ---
    print(f"\n[Bonus] Fetching student profile for '{student_id}'...")
    try:
        r = httpx.get(f"{base}/student/{student_id}", timeout=30)
        r.raise_for_status()
        profile = r.json()
        print(f"  Name: {profile['name']}")
        print(f"  Grade: {profile['grade']}, Target: JEE {profile['target_year']}")
        print(f"  Mastery entries: {len(profile.get('mastery', []))}")
        print(f"  Has plan: {profile.get('current_plan') is not None}")
    except Exception as e:
        print(f"  FAIL: {e}")

    print("\n" + "=" * 60)
    print("Smoke test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
