
class Prompts:

    # champion data
    NO_CHAMPION_DATA = "Since there are no data found, explain that this could mean: 1) The champion isn't viable in that role, 2) Insufficient sample size, 3) The champion is new/reworked. Suggest alternative roles for that champion.\n"

    # user experience
    PROACTIVE_CHAMPION_SUGGESTIONS = "<System>After providing requested data, offer related insights like: 'Would you like to see this champion's performance in other roles?' or 'Should I compare this to similar champions in the same role?'</System>\n"

    COMPARATIVE_CHAMPION_ANALYSIS = "<System>When appropriate, provide context by comparing the champion's performance to role averages or mentioning if they're above/below the median for their role.</System>\n"

    CHAMPION_TREND_IDENTIFICATION = "<System>Look for patterns in the data such as consistently high ban rates, role flexibility (performing well in multiple roles), or significant performance differences between roles.</System>\n"

plib = Prompts()

    