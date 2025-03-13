import os
from openai import OpenAI
from time import sleep


open_ai_key = "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"
system = """ You are an expert football/soccer coach who creates detailed training drills. Always output in JSON format exactly as requested.

CRITICAL RULES:
1. For a NxM drill format (like 3x3, 4x2), ALWAYS use exactly N players of one color and M players of another distinct color.
2. For rondos, the first number (N) represents players on the outside (possession team) and should have one color, while the second number (M) represents defenders in the middle with a different color.
3. When neutral players are mentioned, give them a third distinct color.
4. Ensure each drill's description explains the exact player setup, roles, and color coding.
5. Position players according to their functional roles in the drill (e.g., defenders in defensive positions).

"""

# Initialize OpenAI client
client = OpenAI(api_key = open_ai_key)


def test_model(model_id, test_input):
    """Test the fine-tuned model"""
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {"role": "user", "content": test_input}
        ]
    )
    return completion.choices[0].message

test_input = """Rondo 3x3 with two neutral players in the center."""

result = test_model('ft:gpt-4o-mini-2024-07-18:isvisoft::B6z0LmHd', test_input)
print(result)