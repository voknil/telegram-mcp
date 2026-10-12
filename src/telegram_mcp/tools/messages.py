from mcp.server.mcpserver import MCPServer

from telegram_mcp.errors import as_error_result
from telegram_mcp.service import TelegramService


def register(mcp: MCPServer, service: TelegramService) -> None:
    @mcp.tool()
    async def telegram_send_message(target: str, text: str) -> dict:
        """Send a text message to a user, group or channel.

        Args:
            target: @username, bare username, phone number, or numeric chat id.
            text: message text (Telegram markdown supported).
        """
        try:
            entity = await service.resolve(target)
            msg = await service.client.send_message(entity, text)
            return {"ok": True, "message_id": msg.id}
        except Exception as e:  # noqa: BLE001
            return as_error_result(e)

    @mcp.tool()
    async def telegram_get_messages(target: str, limit: int = 20) -> list[dict]:
        """Read recent messages from a chat, newest first.

        Args:
            target: @username, bare username, phone number, or numeric chat id.
            limit: max number of messages to return.
        """
        entity = await service.resolve(target)
        out = []
        async for msg in service.client.iter_messages(entity, limit=limit):
            sender = await msg.get_sender()
            sender_name = None
            if sender:
                sender_name = getattr(sender, "username", None) or getattr(sender, "first_name", None)
            out.append(
                {
                    "id": msg.id,
                    "date": msg.date.isoformat() if msg.date else None,
                    "sender": sender_name,
                    "text": msg.message,
                }
            )
        return out
