# make request to statsWR champion gameplay data api

import httpx
from typing import Any
from mcp_configs import api_config

async def get_all_data_for_single_champ_all_roles(champion_label:str) -> list[dict[str, Any]] | None:
    url = f"{api_config.BASE_URL}/champions/{champion_label}" # first part of path is from vercel deployment, everything afer /v1 is for statsWR route
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=api_config.DEFAULT_TIMEOUT, headers=api_config.DEFAULT_HEADERS)
            response.raise_for_status()
            res = response.json()

            if 'champion' in res.keys():
                return res['champion']

            return None
        except Exception as e:
            print(e)
            return None


async def get_most_recent_data_for_all_champs_by_role(role:int = 0) -> list[dict[str, Any]] | None:
    url = f"{api_config.BASE_URL}/champions/lanes/latest/{role}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=api_config.DEFAULT_TIMEOUT, headers=api_config.DEFAULT_HEADERS)
            response.raise_for_status()
            res = response.json()

            if 'champions' in res.keys():
                return res['champions']

            return None
        except Exception as e:
            print(e)
            return None

__all__ = [
    "get_all_data_for_single_champ_all_roles",
    "get_most_recent_data_for_all_champs_by_role"
]
