import os
from pathlib import Path
from typing import Any

from telethon import TelegramClient

from telegram_mcp.config import get_settings


def harden_session_file(session_path: Path) -> None:
    """Telethon's SQLite session holds the account auth key (equivalent to a
    password) but doesn't restrict file permissions itself — do it ourselves
    so other local users/processes can't read it.
    """
    sqlite_path = session_path if session_path.suffix == ".session" else session_path.with_suffix(".session")
    if sqlite_path.exists():
        os.chmod(sqlite_path, 0o600)


class TelegramService:
    """Thin wrapper around one Telethon client: connection lifecycle and
    entity resolution shared by every tool module, so individual tools
    don't each reimplement username/phone/id parsing.
    """

    def __init__(self, client: TelegramClient, session_path: Path) -> None:
        self.client = client
        self.session_path = session_path

    @classmethod
    def from_settings(cls) -> "TelegramService":
        settings = get_settings()
        client = TelegramClient(
            str(settings.telegram_session_path),
            settings.telegram_api_id,
            settings.telegram_api_hash,
        )
        return cls(client, settings.telegram_session_path)

    async def connect(self) -> None:
        await self.client.connect()
        harden_session_file(self.session_path)
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
