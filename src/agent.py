
def get_weather(city: str) -> str:
    return f"the weather in {city} is sunny."


def run_agent(user_intput: str):
    print("User:", user_intput)

    # 暂时假装这是LLM做出的决定
    if "weather" in user_intput.lower():
        result = get_weather("ShenZhen")
        print("Tool Result: ", result)

    print("Agent finish")


run_agent("What's the weather today")

