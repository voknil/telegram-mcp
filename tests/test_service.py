from unittest.mock import AsyncMock, MagicMock

import pytest

from telegram_mcp.service import TelegramService


@pytest.fixture
def service() -> TelegramService:
    client = MagicMock()
    client.get_entity = AsyncMock(return_value="entity")
    return TelegramService(client)


@pytest.mark.parametrize(
    ("target", "expected_arg"),
    [
        ("@someuser", "someuser"),
        ("someuser", "someuser"),
        ("123456789", 123456789),
        ("-1001234567890", -1001234567890),
    ],
)
async def test_resolve_parses_target(service: TelegramService, target: str, expected_arg) -> None:
    result = await service.resolve(target)
    assert result == "entity"
    service.client.get_entity.assert_awaited_once_with(expected_arg)
