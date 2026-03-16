import vertexai
import asyncio

async def main():
    client = vertexai.Client(  # For service interactions via client.agent_engines
        project="genaillentsearch",
        location="us-central1",
    )

    adk_app = client.agent_engines.get(name="projects/884152252139/locations/us-central1/reasoningEngines/8422729659740848128")

    # print(adk_app)

    session = await adk_app.async_create_session(user_id="sgardezi")
    # session = await adk_app.async_get_session(user_id="sgardezi", session_id="7554017892140843008")

    # print(session)
    session_id = session['id']
    final_output={}
    async for event in adk_app.async_stream_query(
        user_id="sgardezi",
        session_id=session_id,  # Optional
        message="Create a report on Vodafone for October 2025",
    ):
        # print(event)
        final_output = event
    
    await adk_app.async_delete_session(user_id="sgardezi", session_id=session_id)
    print(final_output['content']['parts'][0]['text'])

asyncio.run(main())