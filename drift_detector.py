import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("FEATHERLESS_API_KEY"),
    base_url="https://api.featherless.ai/v1"
)

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
        response = await client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("DRIFT_DETECTED:"):
            return result.replace("DRIFT_DETECTED:", "").strip()
        return None

    except Exception as e:
        print(f"Drift detection skipped: {e}")
        return None