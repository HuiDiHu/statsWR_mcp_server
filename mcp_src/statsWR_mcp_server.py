import os
import json
import httpx
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv, find_dotenv

from .api_requests.champion import *
from .web_scraping import *
from .prompt_library import plib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

try:
    mcp = FastMCP(
            "statsWR",
            stateless_http=True
        )
    logger.info(f"MCP server initialized on port {os.getenv('PORT', 8127)}")
except Exception as e:
    logger.error(f"Failed to initialize MCP server: {e}")
    raise

def create_error_response(error_msg: str, context: str = "") -> str:
    """Create a standardized error response"""
    full_msg = f"Error in {context}: {error_msg}" if context else f"Error: {error_msg}"
    logger.error(full_msg)
    return json.dumps({
        "error": True,
        "message": error_msg,
        "context": context,
        "data": None
    })

# ---------- start of endpoints ----------

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

        Otherwise return an error logger string. Please output the exact logger object if you recieve it.
    """
    try:
        if not champion_label or not isinstance(champion_label, str):
            return create_error_response("Champion label must be a non-empty string", "get_champion_data_from_label")
        
        champion_label = champion_label.strip().upper()
        if not champion_label:
            return create_error_response("Champion label cannot be empty or whitespace only", "get_champion_data_from_label")
        
        logger.info(f"Fetching champion data for: {champion_label}")
        
        data = await get_all_data_for_single_champ_all_roles(champion_label)
        
        if not data:
            logger.warning(f"No data found for champion: {champion_label}")
            return json.dumps({
                "error": False,
                "message": f"No data available for champion '{champion_label}'. Please check the spelling or try a different champion name.",
                "suggested_action": "Verify champion name spelling and try again",
                "data": None
            })
        
        res = ""
        res += plib.PROACTIVE_CHAMPION_SUGGESTIONS
        res += plib.COMPARATIVE_CHAMPION_ANALYSIS
        res += plib.CHAMPION_TREND_IDENTIFICATION
        res += str(data)
        
        logger.info(f"Successfully retrieved data for champion: {champion_label}")
        return res
        
    except httpx.TimeoutException:
        return create_error_response("Request timed out while fetching champion data", "get_champion_data_from_label")
    except httpx.HTTPStatusError as e:
        return create_error_response(f"HTTP error occurred: {e.response.status_code}", "get_champion_data_from_label")
    except ConnectionError:
        return create_error_response("Connection error - unable to reach data source", "get_champion_data_from_label")
    except json.JSONDecodeError:
        return create_error_response("Invalid JSON response from data source", "get_champion_data_from_label")
    except Exception as e:
        logger.error(f"Unexpected error in get_champion_data_from_label: {traceback.format_exc()}")
        return create_error_response(f"Unexpected error occurred: {str(e)}", "get_champion_data_from_label")

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

        Otherwise return an error logger string. Please output the exact logger object if you recieve it.
    """
    try:
        if not isinstance(role, int):
            try:
                role = int(role)
            except (ValueError, TypeError):
                return create_error_response("Role must be an integer between 0 and 5", "get_most_recent_champ_data_for_all_champs_in_certain_role")
        
        if role < 0 or role > 5:
            return create_error_response("Role must be between 0 and 5 inclusive. 0=All roles, 1=Baron, 2=Jungle, 3=Mid, 4=Dragon, 5=Support", "get_most_recent_champ_data_for_all_champs_in_certain_role")
        
        logger.info(f"Fetching champion data for role: {role}")
        
        data = await get_most_recent_data_for_all_champs_by_role(role)
        
        if not data:
            role_names = {0: 'All roles', 1: 'Baron', 2: 'Jungle', 3: 'Mid', 4: 'Dragon', 5: 'Support'}
            logger.warning(f"No data found for role: {role}")
            return json.dumps({
                "error": False,
                "message": f"No recent data available for role '{role_names.get(role, role)}'",
                "data": None
            })
        
        logger.info(f"Successfully retrieved data for role: {role}")
        return str(data)
        
    except httpx.TimeoutException:
        return create_error_response("Request timed out while fetching role data", "get_most_recent_champ_data_for_all_champs_in_certain_role")
    except httpx.HTTPStatusError as e:
        return create_error_response(f"HTTP error occurred: {e.response.status_code}", "get_most_recent_champ_data_for_all_champs_in_certain_role")
    except ConnectionError:
        return create_error_response("Connection error - unable to reach data source", "get_most_recent_champ_data_for_all_champs_in_certain_role")
    except Exception as e:
        logger.error(f"Unexpected error in get_most_recent_champ_data_for_all_champs_in_certain_role: {traceback.format_exc()}")
        return create_error_response(f"Unexpected error occurred: {str(e)}", "get_most_recent_champ_data_for_all_champs_in_certain_role")

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

        Otherwise return an error logger string. Please output the exact logger object if you recieve it.
    """
    try:
        if not champion_name or not isinstance(champion_name, str):
            return create_error_response("Champion name must be a non-empty string", "get_matchups_for_champion_for_all_viable_roles")
        
        champion_name = champion_name.strip().lower()
        if not champion_name:
            return create_error_response("Champion name cannot be empty or whitespace only", "get_matchups_for_champion_for_all_viable_roles")
        
        logger.info(f"Fetching matchup data for champion: {champion_name}")
        
        data = await scrape_matchups(champion_name)
        
        if not data:
            logger.warning(f"No matchup data found for champion: {champion_name}")
            return json.dumps({
                "error": False,
                "message": f"No matchup data available for champion '{champion_name}'. Please check the spelling or try a different champion name.",
                "suggested_action": "Verify champion name spelling and format (lowercase, spaces->hyphens, remove apostrophes)",
                "data": None
            })
        
        logger.info(f"Successfully retrieved matchup data for champion: {champion_name}")
        return str(data)
        
    except httpx.TimeoutException:
        return create_error_response("Request timed out while fetching matchup data", "get_matchups_for_champion_for_all_viable_roles")
    except httpx.HTTPStatusError as e:
        return create_error_response(f"HTTP error occurred: {e.response.status_code}", "get_matchups_for_champion_for_all_viable_roles")
    except ConnectionError:
        return create_error_response("Connection error - unable to reach data source", "get_matchups_for_champion_for_all_viable_roles")
    except Exception as e:
        logger.error(f"Unexpected error in get_matchups_for_champion_for_all_viable_roles: {traceback.format_exc()}")
        return create_error_response(f"Unexpected error occurred: {str(e)}", "get_matchups_for_champion_for_all_viable_roles")

@mcp.tool()
async def health_check() -> str:
    """
    Health check endpoint to verify server status
    
    Return:
        Status information about the server
    """
    try:
        return json.dumps({
            "status": "healthy",
            "message": "MCP server is running normally",
            "server_name": "statsWR",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return create_error_response(f"Health check failed: {str(e)}", "health_check")

if __name__ == "__main__":
    try:
        logger.info("Starting MCP server...")
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error starting server: {e}")
        logger.error(traceback.format_exc())
        raise