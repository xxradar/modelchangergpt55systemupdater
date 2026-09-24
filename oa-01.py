from openai import OpenAI

# Create an instance of the OpenAI class and assigning it to the variable client
client = OpenAI()

# Define MCP tools for the model to use
tools = [
  {
    "type": "mcp",
    "server_label": "filesystem",
    "server_url": "npx -y @modelcontextprotocol/server-filesystem /tmp",
    "require_approval": "never"
  }
]

# Call the create method of the responses object to get a model response with MCP tools
response = client.responses.create(
  model="gpt-4o",
  input="what is AI ?",
  tools=tools,
  store=False
)

# Print the response
print(response.output_text)
