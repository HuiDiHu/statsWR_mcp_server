# make request to statsWR champion gameplay data api

import httpx
from typing import Any

async def get_all_data_for_single_champ_all_roles(champion_label:str) -> list[dict[str, Any]] | None:
    print("calling get_all_data_for_single_champ_all_roles\n")
    url = f"https://statswr-api.onrender.com/api/v1/champions/{champion_label}" # first part of path is from vercel deployment, everything afer /v1 is for statsWR route
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=60)
            response.raise_for_status()
            res = response.json()

            if 'champion' in res.keys():
                print("- champion retrieved successfully")
                return res['champion']

            print("- champion field not found within response")
            return None
        except Exception as e:
            print(e)
            return None


async def get_most_recent_data_for_all_champs_by_role(role:int = 0) -> list[dict[str, Any]] | None:
    url = f"https://statswr-api.onrender.com/api/v1/champions/lanes/latest/{role}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=60)
            response.raise_for_status()
            res = response.json()

            if 'champions' in res.keys():
                print("- champions retrieved successfully")
                return res['champions']

            print("- champions field not found within response")
            return None
        except Exception as e:
            print(e)
            return None

__all__ = [
    "get_all_data_for_single_champ_all_roles",
    "get_most_recent_data_for_all_champs_by_role"
]
