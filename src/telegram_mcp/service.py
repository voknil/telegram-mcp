from typing import Any

from telethon import TelegramClient

from telegram_mcp.config import get_settings


class TelegramService:
    """Thin wrapper around one Telethon client: connection lifecycle and
    entity resolution shared by every tool module, so individual tools
    don't each reimplement username/phone/id parsing.
    """

    def __init__(self, client: TelegramClient) -> None:
        self.client = client

    @classmethod
    def from_settings(cls) -> "TelegramService":
        settings = get_settings()
        client = TelegramClient(
            str(settings.telegram_session_path),
            settings.telegram_api_id,
            settings.telegram_api_hash,
        )
        return cls(client)

    async def connect(self) -> None:
        await self.client.connect()
        if not await self.client.is_user_authorized():
            raise RuntimeError("Not logged in — run `telegram-mcp login` first")

    async def disconnect(self) -> None:
        await self.client.disconnect()

    async def resolve(self, target: str) -> Any:
        """Resolve @username / bare username / phone number / numeric id to a Telethon entity."""
        stripped = target.lstrip("@")
        if stripped.lstrip("-").isdigit():
            return await self.client.get_entity(int(stripped))
        return await self.client.get_entity(stripped)
