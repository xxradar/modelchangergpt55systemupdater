import os
import re
from openai import OpenAI

# Create an instance of the OpenAI class and assigning it to the variable client
client = OpenAI()
MEMORY_ENV_PREFIX = "MC_"


def sanitize_memory_value(value: str) -> str:
  sanitized_value = re.sub(r"[^A-Za-z0-9_.-]", "_", value)[:100]
  if not re.search(r"[A-Za-z0-9]", sanitized_value):
    return "unknown"
  return sanitized_value


def get_memory_value(key: str) -> str:
  return sanitize_memory_value(os.getenv(f"{MEMORY_ENV_PREFIX}{key}", os.getenv(key, "unknown")))


memory_values = (
  f"ENTERPRISE={get_memory_value('ENTERPRISE')}; "
  f"DEMO={get_memory_value('DEMO')}; "
  f"DEMOKEYWORD={get_memory_value('DEMOKEYWORD')}."
)

# Call the create method of the chat.completions object to get a model response
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "what is AI ?"
        }
      ]
    }
  ],
  response_format={
    "type": "text"
  },
  temperature=1,
  max_completion_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  store=False
)

# Display what is known in system memory
print(f"Known memory values: {memory_values}")

# Print the response
print(response.choices[0].message.content)
