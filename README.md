# telegram-mcp

MCP server for a **personal** Telegram account (MTProto via
[Telethon](https://docs.telethon.dev/), not the Bot API) — join/leave chats,
read and send messages, list dialogs, exposed as MCP tools for any MCP
client (Claude Code, openclaw, etc).

Telethon was chosen over GramJS/`telegram` (npm) because the latter is
archived upstream; Telethon is the actively maintained MTProto library for
Python.

## Architecture

```
src/telegram_mcp/
  config.py     Settings — reads TELEGRAM_API_ID / TELEGRAM_API_HASH / session path from .env
  service.py    TelegramService — owns the Telethon client, connect/disconnect, entity resolution
  errors.py     Shared Telethon-exception -> structured-result conversion (flood-wait, etc.)
  login.py      One-time interactive QR login, writes the session file
  server.py     Builds the MCPServer, wires its lifespan to TelegramService, calls tools.register_all
  cli.py        `telegram-mcp` / `telegram-mcp login` entry points
  tools/
    __init__.py   MODULES list + register_all(mcp, service) — the only file every new
                   category needs to touch
    account.py    telegram_whoami
    dialogs.py    telegram_list_dialogs
    chats.py      telegram_join_chat, telegram_leave_chat
    messages.py   telegram_send_message, telegram_get_messages
tests/
  test_service.py             entity-resolution parsing, no network
  test_tools_registration.py  every tools/*.py module registers cleanly
```

Each `tools/*.py` module owns one capability area and exposes a single
`register(mcp, service) -> None` that adds its tools via `@mcp.tool()`
closures over the shared `TelegramService`. No tool talks to Telethon
directly for connection setup or entity parsing — that goes through
`service.resolve()` / `service.client`, so adding a tool never means
re-deriving "is this a username, a phone, or a numeric id".

### Adding a new tool

1. Pick the right `tools/<category>.py` (or create a new one for a new
   category — e.g. `tools/media.py` for sending/downloading files).
2. Add a function inside its `register()`, decorated with `@mcp.tool()`,
   using `service.client` (raw Telethon) or `service.resolve(target)` for
   user-supplied chat/user references.
3. Return a plain `dict`/`list[dict]`. For anything that mutates state
   (send, join, leave, delete...), wrap the body in `try/except Exception
   as e: return as_error_result(e)` from `telegram_mcp.errors` so flood-waits
   and API errors come back structured instead of as a stack trace.
4. New category module → add it to `MODULES` in `tools/__init__.py`.
5. Add a case to `tests/test_tools_registration.py`'s `EXPECTED_TOOLS` (and,
   if the tool has non-trivial parsing logic, a focused unit test like
   `test_service.py`).

## Setup

```bash
uv venv && uv pip install -e . --group dev
cp .env.example .env   # fill TELEGRAM_API_ID / TELEGRAM_API_HASH from https://my.telegram.org

uv run telegram-mcp login   # scan the QR code in Telegram -> Settings -> Devices -> Link Desktop Device
uv run telegram-mcp         # or just `telegram-mcp` — starts the MCP server on stdio
```

The session is a local file (`state/session` by default, override with
`TELEGRAM_SESSION_PATH`), never leaves the machine.

## Dev

```bash
uv run ruff check src tests
uv run pytest
uv run mypy src
```
