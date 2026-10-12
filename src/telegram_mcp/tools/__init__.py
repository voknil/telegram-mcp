"""Tool registry. Each module here owns one category of Telegram capability
and exposes `register(mcp, service)`, which wires its tools onto the server.

To add a new category: create `tools/<name>.py` with a `register()` function
matching the others, then add the module to MODULES below. Nothing else
(server.py, config, tests) needs to change.
"""

from mcp.server.mcpserver import MCPServer

from telegram_mcp.service import TelegramService

from . import account, chats, dialogs, messages

MODULES = [account, dialogs, chats, messages]


def register_all(mcp: MCPServer, service: TelegramService) -> None:
    for module in MODULES:
        module.register(mcp, service)
