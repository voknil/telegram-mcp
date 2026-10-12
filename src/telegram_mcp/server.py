from contextlib import asynccontextmanager

from mcp.server.mcpserver import MCPServer

from telegram_mcp.service import TelegramService
from telegram_mcp.tools import register_all


def create_server() -> MCPServer:
    service = TelegramService.from_settings()

    @asynccontextmanager
    async def lifespan(_server: MCPServer):
        await service.connect()
        try:
            yield None
        finally:
            await service.disconnect()

    mcp = MCPServer("telegram", lifespan=lifespan)
    register_all(mcp, service)
    return mcp


def main() -> None:
    create_server().run()


if __name__ == "__main__":
    main()
