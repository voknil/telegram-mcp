import re

from mcp.server.mcpserver import MCPServer
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from telegram_mcp.errors import as_error_result
from telegram_mcp.service import TelegramService

INVITE_RE = re.compile(r"(?:t\.me/|telegram\.me/)?(?:\+|joinchat/)([\w-]+)")


def register(mcp: MCPServer, service: TelegramService) -> None:
    @mcp.tool()
    async def telegram_join_chat(target: str) -> dict:
        """Join a channel or group by @username or invite link (t.me/... or t.me/+...).

        Args:
            target: @username, bare username, or an invite link (public or private).
        """
        m = INVITE_RE.search(target)
        try:
            if m:
                result = await service.client(ImportChatInviteRequest(m.group(1)))
                chat = result.chats[0]
            else:
                entity = await service.resolve(target)
                await service.client(JoinChannelRequest(entity))
                chat = entity
            return {"ok": True, "id": chat.id, "title": getattr(chat, "title", None)}
        except Exception as e:  # noqa: BLE001 — surfaced to the caller as a structured result
            return as_error_result(e)

    @mcp.tool()
    async def telegram_leave_chat(target: str) -> dict:
        """Leave a group or channel, or delete a private dialog, by id or @username.

        Args:
            target: @username, bare username, or numeric chat id.
        """
        try:
            entity = await service.resolve(target)
            await service.client.delete_dialog(entity)
            return {"ok": True}
        except Exception as e:  # noqa: BLE001
            return as_error_result(e)
