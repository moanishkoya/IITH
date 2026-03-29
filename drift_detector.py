import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

async def detect_drift(memories: list) -> str | None:
    if len(memories) < 2:
        return None  # Not enough history to detect drift

    memories_str = json.dumps(memories, indent=2)

    prompt = f"""You are analyzing a user's memory history to detect behavioral or preference drift.

Here are the user's memories sorted by date:
{memories_str}

Your job:
1. Compare older memories vs newer ones.
2. Detect if the user's preferences, habits, mood, or context have noticeably shifted.
3. If drift is detected, respond in this exact format:
   DRIFT_DETECTED: Your preferences have shifted because <reason>. Previously you <old behavior>, but now you seem to <new behavior>. Updated recommendation: <recommendation>.
4. If no significant drift is detected, respond with:
   NO_DRIFT

Only respond with one of the two formats above, nothing else."""

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )

        result = response.text.strip()

        if result.startswith("DRIFT_DETECTED:"):
            return result.replace("DRIFT_DETECTED:", "").strip()
        return None

    except Exception as e:
        # Don't crash the agent if drift detection fails
        print(f"Drift detection skipped: {e}")
        return None