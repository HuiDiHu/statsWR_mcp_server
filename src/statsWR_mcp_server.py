import os
import json
import httpx
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv, find_dotenv


from api_requests.champion import *
from web_scraping import *
from prompt_library import plib

load_dotenv(find_dotenv())

# Initialize FastMCP server
mcp = FastMCP("statsWR", host="0.0.0.0", port=int(os.getenv('PORT', 8127)), streamable_http_path="/")

# start of MCP endpoints
@mcp.tool()
async def get_champion_data_from_label(champion_label: str) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        champion_label: Capitalized champion full name. 
                        If a champion's name consists of multiple words, connect them using "_".
                        For example: "Aatrox" -> "AATROX", "Master Yi" -> "MASTER_YI".
                        If the user provides a champion name that doesn't exist or is misspelled, 
                        suggest the closest matching champion names and ask for clarification. 
                        Common misspellings include: 'Yi' for 'Master Yi', 'Kai Sa' for 'Kai'Sa', etc.
    
    Return:
        A stringified list of dictionaries will be returned. Each dictionary represent a champion's
        gameplay data history for a specific role (indicated by the "role" field). Each number corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
    """
    try:
        data = await get_all_data_for_single_champ_all_roles(champion_label)
    except Exception as e:
        return f"{plib.NO_CHAMPION_DATA}"

    res = ""
    if data:
        res += plib.PROACTIVE_CHAMPION_SUGGESTIONS
        res += plib.COMPARATIVE_CHAMPION_ANALYSIS
        res += plib.CHAMPION_TREND_IDENTIFICATION
        res += str(data)
    return res

@mcp.tool()
async def get_most_recent_champ_data_for_all_champs_in_certain_role(role: int) -> str:
    """
    Get gameplay data for a specific WildRift champion

    Args:
        role: A champion's role when they are played in the game. 
        When users mention roles, automatically convert common variations: 'Top'/'Baron Lane'→'Baron', 'ADC'/'Bot'/'Marksman'→'Dragon', 'Mid Lane'→'Mid', 'Supp'→'Support'. 
        If role is unclear, ask for clarification.
        If the user is asking for all roles or does not specify a role, the role parameter should be set to 0.
        You will need to convert the role parameter into an integer according to the following dictionary.
        {'Baron': 1, 'Jungle':2, 'Mid':3, 'Dragon':4, 'Support':5}

    Return:
        A stringified list of dictionaries will be returned. Each dictionary represent a champion's
        gameplay data history for a specific role (indicated by the "role" field). Each number corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
        If the champion/role combination specified by the user is not mentioned in the returned data, Simply state 
        that there is not enough data for the champion in that role.
    """
    
    if role > 5 or role < 0:
        return '</System>the role is incorrect. It must be between 0 and 5 inclusive. Please ask the user to pick a valid role</System>'
    
    data = await get_most_recent_data_for_all_champs_by_role(role)

    res = ""
    if data:
        res += str(data)
    return res

@mcp.tool()
async def get_matchups_for_champion_for_all_viable_roles(champion_name: str) -> str:
    """
    Get matchup data for a specific WildRift champion to see who they are weak/strong against for all their viable roles

    Args:
        champion_name: A champion's name in the game. This parameter should be set to the champions name in all lowercase. 
        if the champion has a space in their name, replace it with a '-' character. Also remove all ' characters.
        Example: Dr. Mundo -> dr-mundo
        Example: Ms Fortune -> ms-fortune
        Example: Kai'Sa -> kaisa
        If the user provides a champion name that doesn't exist or is misspelled, 
        suggest the closest matching champion names and ask for clarification. 
        Common misspellings include: 'Yi' for 'Master Yi', 'Kai Sa' for 'Kai'Sa', etc.

    Return:
        A list of dictionaries will be returned. Each dictionary has a _role_id key where each value corresponds
        to a different lane assignment for the champion as specified by the dictionary below. Keep in mind 'Baron'
        can also be 'Top' and 'Dragon can be 'ADC' or 'AD Carry'.
        {1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
        example return object: 
        result = [
                    {
                        '_role_id': an integer from 1-5,
                        'counters': [champions who counter {champion_name}],
                        'good_matchups': [champions who are countered by {champion_name}],
                        'counter_strategy': a string with info on how to counter the champion
                    },
                    ...
                 ]
        If the user is asking how to play the champion, then use the 'counter_strategy' value as a reference and
        say the opposite
    """
    
    data = await scrape_matchups(champion_name)

    res = ""
    if data:
        res += str(data)
    return res

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='streamable-http')
