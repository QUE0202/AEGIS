from core.llm_interface import query_model

def red_team_interface():
    print("\n🔴 RED TEAM MODE | Type 'exit' to quit\n")
    while True:
        prompt = input("[AEGIS:Red] >>> ")
        if prompt.lower() in ["exit", "quit"]:
            break
        result = query_model(prompt, mode="red")
        print(result)
