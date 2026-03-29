from dotenv import load_dotenv
from mem0 import MemoryClient
import logging
import json


load_dotenv()
user_name = 'Moanish'
mem0 = MemoryClient()

def add_memory():
    messages_formatted = [
        {
            "role": "user",
            "content": "I really like Linkin Park."
        },
        {
            "role": "assistant",
            "content": "That is a good choice."
        },
        {
            "role": "user",
            "content": "I think so too."
        },
        {
            "role": "assistant",
            "content": "What is your favorite song by them?"
        },
    ]
    mem0.add(messages_formatted, user_id="Moanish")
    print("Memory added.")

def get_all_memories():
    mem0 = MemoryClient()
    response = mem0.get_all(user_id=user_name, filters={"user_id": user_name})
    print(f"Raw get_all response: {response}")

    results = response if isinstance(response, list) else response.get("results", [])

    memories = [
        {
            "memory": result["memory"],
            "updated_at": result.get("updated_at", "")
        }
        for result in results
    ]

    memories_str = json.dumps(memories)
    print(f"Memories: {memories_str}")
    return memories_str


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    get_all_memories()