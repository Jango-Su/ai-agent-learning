import json
import os

from openai import OpenAI


def get_weather(city: str) -> str:
    if city == "Singapore":
        raise RuntimeError("Weather service unavailable")

    return f"The weather in {city} is sunny."


tool_registry = {
    "get_weather":get_weather
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

messages = [
        {
            "role": "user",
            "content": "What's the weather in Singapore?"
        }
]


while True:
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message
    messages.append(message)
    print(message)

    if not message.tool_calls:
        break

    for tool_call in message.tool_calls:
        name = tool_call.function.name
        arguments = tool_call.function.arguments

        func = tool_registry.get(name)
        if not func:
            result = f"Error: tool '{name}' not found."
        else:
            try:
                arg = json.loads(arguments)
                result = func(**arg)
            except Exception as e:
                result = f"Tool execution failed: {type(e).__name__}: {e}"

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )
