from mcp.server.mcpserver import MCPServer

from telegram_mcp.service import TelegramService


def register(mcp: MCPServer, service: TelegramService) -> None:
    @mcp.tool()
    async def telegram_list_dialogs(limit: int = 50) -> list[dict]:
        """List recent chats: users, groups and channels, with unread counts.

        Args:
            limit: max number of dialogs to return (most recent first).
        """
        out = []
        async for d in service.client.iter_dialogs(limit=limit):
            entity = d.entity
            kind = "user" if d.is_user else "channel" if d.is_channel else "group"
            out.append(
                {
                    "id": d.id,
                    "title": d.name,
                    "type": kind,
                    "username": getattr(entity, "username", None),
                    "unread_count": d.unread_count,
                }
            )
        return out
