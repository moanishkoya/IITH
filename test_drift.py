import asyncio
from drift_detector import detect_drift

memories = [
    {"memory": "User likes Linkin Park", "updated_at": "2026-01-01T10:00:00"},
    {"memory": "User has been listening to lo-fi and jazz lately", "updated_at": "2026-03-01T10:00:00"},
    {"memory": "User prefers calm and relaxing music now", "updated_at": "2026-03-29T10:00:00"},
]

async def main():
    result = await detect_drift(memories)
    if result:
        print(f"Drift detected:\n{result}")
    else:
        print("No drift detected.")

asyncio.run(main())