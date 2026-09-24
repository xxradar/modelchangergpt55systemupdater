import os
from openai import OpenAI

# Create an instance of the OpenAI class and assigning it to the variable client
client = OpenAI()
memory_values = (
  f"enterprise={os.getenv('ENTERPRISE', 'unknown')}; "
  f"demo={os.getenv('DEMO', 'unknown')}; "
  f"DEMOKEYWORD={os.getenv('DEMOKEYWORD', 'unknown')}."
)

# Call the create method of the chat.completions object to get a model response
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": f"Known memory values: {memory_values}"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Display the known memory values you were given."
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

# Print the response
print(response.choices[0].message.content)
