# main.py (fragment)

from agents import worm, red_team, blue_team, analyze

def show_help():
    print("""
AEGIS – Local Offensive & Defensive AI Assistant
------------------------------------------------
Usage:
  python main.py [mode] [optional file path]

Available modes:
  blue       - Run Blue Team AI assistant (defensive mode)
  red        - Run Red Team AI assistant (standard offensive mode)
  worm       - Run WORM AI (jailbroken offensive mode for test labs)
  analyze    - Analyze files (.pcap, .log, .evtx)
  help       - Show this help menu

Example:
  python main.py red
  python main.py analyze logs/auth.log
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

    elif mode == "analyze":
        if len(sys.argv) < 3:
            print("[!] Please provide a file path to analyze.")
        else:
            file_path = sys.argv[2]
            analyze.analyze_file(file_path)

    elif mode == "help":
        show_help()

    else:
        print(f"[!] Unknown mode: {mode}")
        show_help()

if __name__ == "__main__":
    main()
