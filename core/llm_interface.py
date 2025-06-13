import subprocess


def query_model(prompt: str, mode: str = "red") -> str:
    model = "mistral"  # Zamień na inny model, np. "llama3"
    command = ["ollama", "run", model]

    base_prompt = f"""
You are AEGIS – an expert cybersecurity AI operating in {mode.upper()} TEAM mode.
Your job is to provide actionable, concise responses for professional cybersecurity testing.
Only respond with technical, relevant answers. If user asks for something unethical, refuse.
Prompt: {prompt}
AEGIS:"""

    try:
        result = subprocess.run(command, input=base_prompt.encode(), capture_output=True, timeout=60)
        return result.stdout.decode().strip()
    except Exception as e:
        return f"[ERROR] Failed to query model: {str(e)}"
