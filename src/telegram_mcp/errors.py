from telethon.errors import FloodWaitError


def as_error_result(exc: Exception) -> dict:
    """Convert a Telethon exception into the structured error dict every
    mutating tool returns instead of raising, so the MCP client gets a
    machine-readable reason (e.g. flood-wait seconds) instead of a stack trace.
    """
    if isinstance(exc, FloodWaitError):
        return {"ok": False, "error": f"rate limited by Telegram, wait {exc.seconds}s before retrying"}
    return {"ok": False, "error": str(exc)}
