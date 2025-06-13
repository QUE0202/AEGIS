from core.llm_interface import query_model

def blue_team_interface():
    print("\n🔵 BLUE TEAM MODE | Type 'exit' to quit\n")
    while True:
        prompt = input("[AEGIS:Blue] >>> ")
        if prompt.lower() in ["exit", "quit"]:
            break
        result = query_model(prompt, mode="blue")
        print(result)
