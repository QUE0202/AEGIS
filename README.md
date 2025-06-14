## ⚠️ Disclaimer

AEGIS is an educational and testing tool. Using it to attack systems without explicit permission is illegal and punishable by law.
Use responsibly, only within controlled lab or test environments.

---

# 🛡️ AEGIS – Local AI Assistant for Red and Blue Teams

AEGIS is a lightweight, local AI assistant designed specifically for cybersecurity professionals — Red Teams and Blue Teams alike.  
It operates fully offline using a local Large Language Model (LLM) powered via [Ollama](https://ollama.com), ensuring full control over your environment and data security.

---

## 🎯 Project Purpose

AEGIS aims to support offensive and defensive cybersecurity operations during security assessments, attack simulations, and incident analyses by providing intelligent suggestions and actionable recommendations.

---

## ⚙️ Features

### Red Team Mode:
- Generates phishing emails and payloads  
- Creates attack scenarios aligned with the MITRE ATT&CK framework  
- Analyzes scanning results (e.g., Nmap, Nessus)  
- Suggests exploits and social engineering techniques

### Blue Team Mode:
- Analyzes system and application logs  
- Proposes SIEM alert rules (Splunk, ELK, Wazuh)  
- Provides incident response recommendations  
- Assists in threat hunting and IOC detection

---

## 🚀 Requirements

- Python 3.11 or higher  
- [Ollama](https://ollama.com) (tool to run LLMs locally)  
- A local LLM model (e.g., `mistral`, `llama3`) available in Ollama  
- Python package `typer` for CLI support

---

## 📦 Installation

1. **Install Ollama** following instructions on the official site:  
   https://ollama.com  

2. **Download an LLM model:**  
   ```bash
   ollama run mistral

---

3. **Install Python dependencies:**
   ```bash
    pip install typer

---

## Clone the repository and run AEGIS:
```
git clone <https://github.com/QUE0202/AEGIS>
cd aegis
python main.py red   # to run in Red Team mode
python main.py blue  # to run in Blue Team mode
```
---

## 🖥️ Usage

After launching AEGIS in your selected mode, type queries and commands related to red or blue team tasks.

Example queries:


*🟥 Red Team:*

Create a phishing email campaign targeting LinkedIn users

Which exploits correspond to CVE-2023-12345?


*🟦 Blue Team:*

Analyze this system log and suggest an alert rule

What steps should I take after detecting suspicious network traffic?


*🧪 WORM:*

Generate a reverse shell payload for Windows

Show a post-exploitation chain for Linux privilege escalation

---

## 📂 Project Structure

main.py – application entry point

agents/red_team.py – Red Team mode interface

agents/blue_team.py – Blue Team mode interface

core/llm_interface.py – integration with the local LLM (Ollama)

config.yaml – basic configuration file

README.md – project documentation

---

## 🤝 Contact

For questions, feature requests, or bug reports, please open an issue on GitHub or contact the maintainer directly.