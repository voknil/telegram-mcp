import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="telegram-mcp")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("run", help="Start the MCP server on stdio (default)")
    sub.add_parser("login", help="Interactive QR login, saves the session file")
    args = parser.parse_args()

    if args.command == "login":
        from telegram_mcp.login import main as login_main

        login_main()
    else:
        from telegram_mcp.server import main as server_main

        server_main()


if __name__ == "__main__":
    main()
