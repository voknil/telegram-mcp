from mcp.server.mcpserver import MCPServer

from telegram_mcp.service import TelegramService


def register(mcp: MCPServer, service: TelegramService) -> None:
    @mcp.tool()
    async def telegram_whoami() -> dict:
        """Current logged-in account: id, username, name, phone."""
        me = await service.client.get_me()
        return {
            "id": me.id,
            "username": me.username,
            "first_name": me.first_name,
            "last_name": me.last_name,
            "phone": me.phone,
        }
