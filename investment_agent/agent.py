import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, ParallelAgent, SequentialAgent, LlmAgent
from google.adk.tools import agent_tool, AgentTool
from google.adk.tools import google_search
from .generaltools.generaltools import get_current_date
from .lsegtools.tickhistory import getVWAP, getMarketPsycSentiment, getCompanyDetails, getSignificantEvents, getESGEnvIndicator, getESGGovIndicator, getESGSocIndicator
from .generaltools.finhubtools import symbol_lookup
from .config import config
import google.auth

from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode

# Define a tool configuration to block any write operations
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

application_default_credentials, _ = google.auth.default()
print(application_default_credentials)

credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

# Instantiate a BigQuery toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

symbol_to_ric_agent = LlmAgent(
    name="symbol_to_ric_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to convert Company to RIC"
    ),
    instruction=(
        "convert the Company name to the RIC code and return the ric code in the response"
        "Get the RIC code for common stock traded on the London Stock Exchange (LSE)"
        "if the the company is Vodafone then the RIC is VOD.L"
        "if the the company is BT then the RIC is BT.L"
    ),
    tools=[google_search],
)

companynews_agent = LlmAgent(
    name="companynews_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the company info for a list of company RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the company news for a company or set of companies."
        "Make sure the news is for the time period requested by the user"
        "Only look for verified news and not roumers"
        "use news from reputable sites and providers"
    ),
    tools=[google_search],
    output_key="companynews_result"
)

companyinfo_agent = LlmAgent(
    name="companyinfo_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the company info for a list of company RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the company info for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getCompanyDetails tool"
        "You can send multiple RICs to the getCompanyDetails tool as well"
        "Return the company info with a formatted table in the repsonse that can be used in a report"
        "ignore any time duration when doing this analysis"
        "do not prompt the user, just return the company info in the repsonse"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), getCompanyDetails],
    output_key="companyinfo_result"
)


vwap_agent = LlmAgent(
    name="vwap_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the VWAP for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the VWAP for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getVWAP tool"
        "You can sent multiple RICs to the getVWAP tool as well"
        "Return the VWAP table in the repsonse and an analysis of the results"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getVWAP],
    output_key="vwap_result"
)

marketpsycsentiment_agent = LlmAgent(
    name="marketpsycsentiment_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the market sentiment for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the sentiment for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getMarketPsycSentiment tool"
        "You can sent multiple RICs to the getMarketPsycSentiment tool as well"
        "Return the sentiment table in the repsonse and an analysis of the results"
        "The values for these fields are typically float type and represent a metric derived from content analysis." 
        "Fields marked with (Range: -1 to 1) are bipolar, representing a net balance of positive vs. negative references." 
        "Fields marked with (Range: 0 to 1) are unipolar, meaning they track the frequency of a certain emotion/topic (they can range below 0, though not below -1)"
        "Analyze Anomalies (Unipolar): For Unipolar indices (Joy, Anger, Fear, Gloom, Stress, Surprise, Uncertainty, Violence), flag any values significantly above the 0.5 threshold as indicating high attention or concern regarding that specific topic/emotion."
        "Analyze Direction (Bipolar): For Bipolar indices (Sentiment, Optimism, LoveHate, Trust, Conflict, TimeUrgency, EmotionVsFact, MarketRisk), flag values close to 1 as highly positive/favorable and values close to -1 as highly negative/unfavorable."
        "Contextualize: For any company showing low Trust or high Anger/Fear, cross-reference these findings with other risk-related fields in the same table, such as DebtDefault, Litigation, or MgmtTrust to identify potential drivers of the negative sentiment."
        "Do not generate code, just analyse the data directly"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getMarketPsycSentiment],
    output_key="marketpsycsentiment_result"
)

significantevent_agent = LlmAgent(
    name="significantevent_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the significant events for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the significant events for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getSignificantEvents tool"
        "You can sent multiple RICs to the getSignificantEvents tool as well"
        "Return the details of significant events in the repsonse and an analysis of the results"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getSignificantEvents],
    output_key="significantevent_result"
)

esgenvindicator_agent = LlmAgent(
    name="esgenvindicator_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the ESG Environmental Indicators for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the ESG Environmental Indicators for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getESGEnvIndicator tool"
        "You can sent multiple RICs to the getESGEnvIndicator tool as well"
        "Return the details of ESG Environmental Indicator in the repsonse and an analysis of the results"
        "getESGEnvIndicator tool requires the fyscal year (as a interger) as input."
        "Do not generate code, just analyse the data directly"
        "ignore any time duration from the pompt when doing this analysis, just use the current fiscal year based on the users input and get_current_date"
        "If you are unsure about the year, use 2025"
        "Make sure your run the getESGGovIndicator tool with the year 2025 regard if you are unable to do anything"
        "Regardless of the request duration use the current year 2025 and call the tool: getESGGovIndicator"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getESGEnvIndicator],
    output_key="esgenvindicator_result"
)

esggovindicator_agent = LlmAgent(
    name="esggovindicator_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the ESG Gov Indicators for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the ESG Gov Indicators for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getESGGovIndicator tool"
        "You can sent multiple RICs to the getESGGovIndicator tool as well"
        "Return the details of ESG Gov Indicator in the repsonse and an analysis of the results"
        "getESGGovIndicator tool requires the fyscal year (as a interger) as input. "
        "Do not generate code, just analyse the data directly"
        "ignore any time duration from the pompt when doing this analysis, just use the current fiscal year based on the users input and get_current_date"
        "If you are unsure about the year, use 2025"
        "Make sure your run the getESGGovIndicator tool with the current year if you are unable to do anything"
        "Regardless of the request duration use the current year 2025 and call the tool: getESGGovIndicator"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getESGGovIndicator],
    output_key="esggovindicator_result"
)

esgsocindicator_agent = LlmAgent(
    name="esgsocindicator_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the ESG Soc Indicators for a list of stock RICs"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the ESG Soc Indicators for a stock or stocks via the RIC code."
        "Use the symbol_to_ric_agent tool to first get the ric code and use it as input to the getESGSocIndicator tool"
        "You can sent multiple RICs to the getESGSocIndicator tool as well"
        "Return the details of ESG Soc Indicator in the repsonse and an analysis of the results"
        "getESGSocIndicator tool requires the fyscal year (as a interger) as input. "
        "Do not generate code, just analyse the data directly"
        "ignore any time duration from the pompt when doing this analysis, just use the current fiscal year based on the users input date and get_current_date"
        "If you are unsure about the year, use 2025"
        "Make sure your run the getESGGovIndicator tool with the current year if you are unable to do anything"
        "Regardless of the request duration use the current year 2025 and call the tool: getESGGovIndicator"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getESGSocIndicator],
    output_key="esgsocindicator_result"
)

data_retrieval_agent = ParallelAgent(
    name="data_retrieval_agent",
    # model="gemini-2.5-flash",
    description=(
        "You are an agent that helps a financial analyst to retreive info about a company or stock"
    ),
    # instruction=(
    #     "You are a financal assistant agent that uses all the sub agents to retreive info about a company or a stock"
    #     "Use the company_news_agent to get company news"
    #     "Use the company_profile_agent to get company profile"
    #     "Use the company_basic_financials_agent to get company basic financials"
    #     "Use the insider_sentiment_agent to get insider sentiment"
    #     "Use the financials_reported_agent to get financials reported"
    #     "Use the sec_filings_agent to get sec filings"
    # ),
    sub_agents=[companyinfo_agent, vwap_agent, marketpsycsentiment_agent, significantevent_agent, esgenvindicator_agent, esggovindicator_agent, esgsocindicator_agent, companynews_agent]
)


report_creation_agent = LlmAgent(
    name="report_creation_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst create a report on an asset or stock"
    ),
    instruction=(
        """
        Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.
        **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**
         **Input Summaries:**
            {companyinfo_result}
            {vwap_result}
            {marketpsycsentiment_result}
            {significantevent_result}
            {esgenvindicator_result}
            {esggovindicator_result}
            {esgsocindicator_result}
            {companynews_result}

    In the analysis always add a section at the end to correlate the VAWP Result {vwap_result} with the news data {marketpsycsentiment_result} and explain how the news impacts the vwap
    Also include details from {significantevent_result}, {esgenvindicator_result}, {esgsocindicator_result}, {companynews_result},and {esggovindicator_result} in the correlations as well.
    Make sure the entire report output is professionally formated in markdown. 
        **Comprehensive Report:** Your report should be comprehensive, detailes
        Start with a seciton detailing the company info as stated in {companyinfo_result}. Format it nicely as a table with all the detail and some infrered metrics.


                        **4. Data Handling and Error Management:**

                        *   **Data Completeness:** If a function requires date that is not present or unavailable, use the current year as the default period. Report missing data but don't let it stop you.
                        *   **Function Execution:** Execute functions carefully, ensuring you have the necessary data, especially dates and symbols, before invoking any function.
                        *   **Clear Output:** Present results in a clear and concise manner, suitable for an asset management investor.

                        **5. Analytical Perspective:**

                        *   **Asset Management Lens:** Conduct all analysis with an asset manager's perspective in mind. Evaluate the company as a potential investment, focusing on risk, return, and long-term prospects."""
    )
)

sequential_agent = SequentialAgent(
    name="sequential_agent",
    description=(
        "you are the agent that runs the process for collecting the data and creating the report"
    ),
    sub_agents=[data_retrieval_agent, report_creation_agent]
)

root_agent = LlmAgent(
    name="investment_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst at an asset manager"
    ),
    instruction=(
        # "You are an investment analyst agent that creates an analysis of assets and stock"
        # "You use the tools and subagents at your disposal to get the data and summarise the data"
        # "Include a detailed summary in the response"
        # "use the get_current_date tool to get the current data in order to use with any of the subagents"
        # "use the symbol_lookup_agent to get a stock symbol from a company name"
        # "use the news subagent to get company news"
        # "In the response include a detailed section on the news"
        # "If the user does not specify a start date or end date, use the current date as the start date using the get_current_date tool"
        # "use the date from 6 months ago as the end date"
        # "If the user specifies the date as a duration, use get_current_date to get the start date and calculate it"
        # "make sure to always use the get_current_date tool to do the date calculation"
        # "use all the sub agnets to create a report on the investment"
        """You are a highly skilled financial analyst specializing in asset management. Your task is to conduct thorough financial analysis and generate detailed reports from an investor's perspective. Follow these guidelines meticulously:

                        **1. RIC Identification and Lookup:**

                        *   **Primary RIC Focus:** When multiple RICs exist for a company, prioritize the *primary* RIC on the LSE market.
                        *   **Mandatory symbol_to_ric_agent tool Lookup:** Before executing any other functions, always use the `symbol_to_ric_agent` function to identify and confirm the correct primary RIC for the company or companies under analysis. Do not proceed without a successful lookup.
                        *   **Handle Lookup Failures:** If `symbol_to_ric_agent` fails to identify a symbol, inform the user and gracefully end the analysis.

                        **2. Date Handling:**

                        *   **Current Date Determination:** Use the `get_current_date` function to obtain the current date at the beginning of each analysis. This date is critical for subsequent time-sensitive operations.
                        *   **Default Year Range:** If a function call requires a date range and the user has not supplied one, calculate the start and end dates for the *current year* using the date obtained from `current_date`. Use these as the default start and end dates in the relevant function calls.
                        *   Make sure you get the date and calculate the start and end date based on the current date if the prompt asks.
                        If the prompt already mentions a start and end date then use it.
                        Do not generate code to handle date, use the the get_current_date tool to do the date calculation.

                        **3. Analysis Components:**

                        Use the data_retrieval_agent to collect data for the following sections

                        

                        **4. Data Handling and Error Management:**

                        *   **Data Completeness:** If a function requires date that is not present or unavailable, use the current year as the default period. Report missing data but don't let it stop you.
                        *   **Function Execution:** Execute functions carefully, ensuring you have the necessary data, especially dates and symbols, before invoking any function.
                        *   **Clear Output:** Present results in a clear and concise manner, suitable for an asset management investor.

                        **5. Analytical Perspective:**

                        *   **Asset Management Lens:** Conduct all analysis with an asset manager's perspective in mind. Evaluate the company as a potential investment, focusing on risk, return, and long-term prospects.

                        **Example Workflow (Implicit):**

                        1.  Get the current date using `get_current_date`.
                        2.  Use `symbol_to_ric_agent` to identify the primary RICs for the company provided by the user.
                        3.  If no RIC is found, end the process and report back.
                        4.  Calculate the start and end date by using the result of the get_current_date tool.
                        5.  Call the data_retrieval_agent retrieve the company_profile_agent, company_news_agent, company_basic_financials_agent, insider_sentiment_agent, financials_reported_agent, and sec_filings_agent, news, financials, insider sentiment, and SEC filings. Use the current year start and end date when required, or the date specified by the user.
                        6.  Assemble a detailed and insightful report that addresses each of the sections mentioned above using report_creation_agent.
                        
                        "Make sure you run all the sub agents" 
                        "Use the report_creation_agent to create a report on the investment and return it"
                        "in order to analyse a company use the data_retrieval_agent"
                        "report_creation_agent should be called right at the end of the analysis to create the final report."
                        Always call report_creation_agent at the end of the analysis.

                        Make sure you get convert the company name to RIC using the symbol_to_ric_agent. Do this first always.

                        """

    ),
    tools=[get_current_date],
    # sub_agents=[symbol_lookup_agent, data_retrieval_agent, report_creation_agent]
    sub_agents=[sequential_agent]
)