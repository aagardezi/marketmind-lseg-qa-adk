import asyncio
import sys
import os
import json
from google.adk.runners import InMemoryRunner
from google.genai import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from investment_agent.agent import root_agent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(app_name="test", user_id="user1")
    
    prompt = "Compare the investment potential of Vodafone and BT."
    user_message = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    
    final_text = ""
    tool_uses = []
    
    async for event in runner.run_async(user_id="user1", session_id=session.id, new_message=user_message):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call:
                    tool_uses.append({
                        "name": part.function_call.name,
                        "args": part.function_call.args
                    })
        if event.is_final_response() and event.content:
            final_text += event.content.parts[0].text
            
    with open('/tmp/vodafone_bt_trace.json', 'w') as f:
        json.dump({"final_text": final_text, "tool_uses": tool_uses}, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
