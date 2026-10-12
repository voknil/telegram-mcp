from unittest.mock import MagicMock

from mcp.server.mcpserver import MCPServer

from telegram_mcp.service import TelegramService
from telegram_mcp.tools import register_all

EXPECTED_TOOLS = {
    "telegram_whoami",
    "telegram_list_dialogs",
    "telegram_join_chat",
    "telegram_leave_chat",
    "telegram_send_message",
    "telegram_get_messages",
}


async def test_register_all_wires_every_module_without_network() -> None:
    mcp = MCPServer("telegram-test")
    service = TelegramService(MagicMock())

    register_all(mcp, service)

    names = {t.name for t in await mcp.list_tools()}
    assert EXPECTED_TOOLS <= names
