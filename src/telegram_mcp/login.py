"""One-time interactive login: scan a QR code with the Telegram app
(Settings -> Devices -> Link Desktop Device). Saves the session file that
the MCP server then loads read-only on every subsequent run.
"""

import asyncio
import getpass
import sys

import qrcode
from telethon import errors

from telegram_mcp.config import get_settings
from telegram_mcp.service import TelegramService, harden_session_file


def print_qr(url: str) -> None:
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make()
    qr.print_ascii(invert=True)


async def run_login() -> None:
    service = TelegramService.from_settings()
    client = service.client
    await client.connect()
    harden_session_file(service.session_path)

    if await client.is_user_authorized():
        me = await client.get_me()
        session_path = get_settings().telegram_session_path
        print(f"Already logged in as @{me.username or me.id}. Session: {session_path}")
        await client.disconnect()
        return

    qr_login = await client.qr_login()
    print_qr(qr_login.url)
    print("\nScan this QR in Telegram: Settings -> Devices -> Link Desktop Device")
    print("Waiting for scan (QR refreshes automatically)...")

    while True:
        try:
            await qr_login.wait(timeout=20)
            break
        except TimeoutError:
            await qr_login.recreate()
            print_qr(qr_login.url)
            print("QR expired, refreshed — scan again.")
        except errors.SessionPasswordNeededError:
            pw = getpass.getpass("Two-step verification password: ")
            await client.sign_in(password=pw)
            break

    harden_session_file(service.session_path)
    me = await client.get_me()
    print(f"\nLogged in as @{me.username or me.id}. Session saved to {get_settings().telegram_session_path}")
    await client.disconnect()


def main() -> None:
    try:
        asyncio.run(run_login())
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
