from collections.abc import Iterable
import httpx

from models import AccountTokens, Unit, AccountTokensAndUnitUUIDs
from parsers.units import group_by_dodo_is_api_account_name, to_uuids

__all__ = ("parse_account_tokens_response", "merge_account_tokens_and_units")


def parse_account_tokens_response(response: httpx.Response) -> AccountTokens:
    response_json = response.text
    return AccountTokens.model_validate_json(response_json)


def merge_account_tokens_and_units(
    accounts_tokens: Iterable[AccountTokens],
    units: Iterable[Unit],
) -> list[AccountTokensAndUnitUUIDs]:
    account_name_to_units = group_by_dodo_is_api_account_name(units)
    return [
        AccountTokensAndUnitUUIDs(
            access_token=account_tokens.access_token,
            unit_uuids=to_uuids(
                account_name_to_units.get(account_tokens.account_name, [])
            ),
        )
        for account_tokens in accounts_tokens
    ]
