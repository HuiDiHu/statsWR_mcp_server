import json
import httpx
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

from requests.champion import *

# Initialize FastMCP server
mcp = FastMCP("statsWR")

# start of MCP endpoints
@mcp.tool()
async def get_champion_data_from_label(champion_label: str) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        champion_label: Capitalized champion full name. 
                        If a champion's name consists of multiple words, connect them using "_".
                        For example: "Aatrox" -> "AATROX", "Master Yi" -> "MASTER_YI".
    
    Return:
        A stringified list of dictionaries will be returned. Each dictionary represent a champion's
        gameplay data history for a specific role (indicated by the "role" field). Each number corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
    """

    data = await get_all_data_for_single_champ_all_roles(champion_label)

    if data:
        return str(data)
    return ""

@mcp.tool()
async def get_most_recent_champ_data_for_all_champs_in_certain_role(role: int) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        role: A champion's role when they are played in the game. You will need to convert the role parameter into an integer
        according to the following dictionary. Keep in mind 'Baron' can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        If the user is asking for all roles or does not specify a role, the role parameter should be set to 0.
        {'Baron': 1, 'Jungle':2, 'Mid':3, 'Dragon':4, 'Support':5}

    Return:
        A stringified list of dictionaries will be returned. Each dictionary represent a champion's
        gameplay data history for a specific role (indicated by the "role" field). Each number corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
        If the champion/role combination specified by the user is not mentioned in the returned data, Simply state 
        that there is not enough data for the champion in that role.
        Anything that is surrounded by <System></System> are system messages
    """
    
    if role > 5 or role < 0:
        return '</System>the role is incorrect. It must be between 0 and 5 inclusive</System>'
    
    data = await get_most_recent_data_for_all_champs_by_role(role)

    if data:
        return str(data)
    return "<System>The date may have been incorrect</System>"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
