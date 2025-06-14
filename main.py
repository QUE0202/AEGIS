# main.py

import sys
from agents import worm, red_team, blue_team

def show_help():
    print("""
AEGIS – Local Offensive & Defensive AI Assistant
------------------------------------------------
Usage:
  python main.py [mode]

Available modes:
  blue    - Run Blue Team AI assistant (defensive mode)
  red     - Run Red Team AI assistant (standard offensive mode with filters)
  worm    - Run WORM AI (jailbroken offensive mode for test labs only)
  help    - Show this help menu

Example:
  python main.py red
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    mode = sys.argv[1].lower()

    if mode == "blue":
        blue_team.blue_mode()

    elif mode == "red":
        red_team.red_mode()

    elif mode == "worm":
        worm.worm_mode()

    elif mode == "help":
        show_help()

    else:
        print(f"[!] Unknown mode: {mode}")
        show_help()

if __name__ == "__main__":
    main()
