"""
Check what prompt is being sent to the agent
"""
import datetime
import pytz
from agi_agents.prompts import QWEN_AGENT

# Format with current date like the agent does
pacific_tz = pytz.timezone("US/Pacific")
current_date = datetime.datetime.now(pacific_tz).strftime("%Y-%m-%d")
current_date = f"Current date (YYYY-MM-DD): {current_date}"

# Format the prompt
formatted_prompt = QWEN_AGENT.format(date=current_date)

print("="*80)
print("SYSTEM PROMPT SENT TO AGENT")
print("="*80)
print(formatted_prompt)
print("="*80)

# Also check the goal message with navigation hint
goal = 'Look through Newsletters and under Discover section, subscribe to "Remote Work Chronicles" and "Leadership Insights".'
navigation_keywords = ["Look through", "Go to", "Navigate to", "Access", "Visit", "Open"]
navigation_hint = ""
if any(keyword in goal for keyword in navigation_keywords):
    navigation_hint = "\n\n**IMPORTANT**: This task requires navigating to a specific section. Look for navigation links in sidebars (usually on the left) or top navigation bars. Click the appropriate link to navigate before attempting other actions."

goal_message = f"## Task Goal\n{goal}{navigation_hint}"

print("\n" + "="*80)
print("GOAL MESSAGE FOR networkin-13 TASK")
print("="*80)
print(goal_message)
print("="*80)
