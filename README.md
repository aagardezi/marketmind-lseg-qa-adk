# MarketMind - Investment Research Agent

## Project Overview

MarketMind is a sophisticated investment research agent designed to assist asset managers and financial analysts in making informed decisions. It leverages a multi-agent system built with the Google Agent Development Kit (ADK) to gather, analyze, and synthesize financial data from various sources, including LSEG (London Stock Exchange Group) and Finnhub.

The agent is capable of providing a comprehensive analysis of a company, including its financial performance, market sentiment, ESG (Environmental, Social, and Governance) indicators, and significant events. The final output is a detailed report that can be used for investment evaluation.

## Architecture

The MarketMind agent is built on a hierarchical and parallel agent architecture, enabling efficient and specialized data processing.

### Agent/Sub-agent Design

The core of the system is a `root_agent` (named `investment_agent` in the code) that orchestrates the entire workflow. The architecture is as follows:

1.  **`root_agent`**: The main entry point that receives the user's query. It uses a `sequential_agent` to manage the analysis process.

2.  **`sequential_agent`**: This agent ensures a two-step process:
    *   **`data_retrieval_agent`**: A parallel agent that simultaneously dispatches requests to multiple specialized sub-agents to gather data.
    *   **`report_creation_agent`**: An LLM agent that takes the data gathered by the `data_retrieval_agent` and synthesizes it into a coherent and well-formatted report.

3.  **`data_retrieval_agent` (ParallelAgent)**: This agent runs the following sub-agents in parallel to maximize efficiency:
    *   **`companyinfo_agent`**: Fetches company details.
    *   **`vwap_agent`**: Calculates the Volume-Weighted Average Price (VWAP).
    *   **`marketpsycsentiment_agent`**: Gathers market sentiment data.
    *   **`significantevent_agent`**: Retrieves information about significant corporate events.
    *   **`esgenvindicator_agent`**: Collects ESG Environmental indicators.
    *   **`esggovindicator_agent`**: Collects ESG Governance indicators.
    *   **`esgsocindicator_agent`**: Collects ESG Social indicators.
    *   **`companynews_agent`**: Fetches the latest company news.

4.  **`symbol_to_ric_agent`**: A utility agent used by other agents to convert company names into their corresponding RIC (Reuters Instrument Code), which is necessary for querying LSEG data.

This modular design allows for easy extension and maintenance. New data sources or analysis types can be added by creating new sub-agents and integrating them into the `data_retrieval_agent`.

### Tools

The MarketMind agent utilizes a variety of tools to perform its functions:

*   **LSEG Tick History**: Queries LSEG's tick history data stored in Google BigQuery to calculate VWAP and retrieve other market data.
*   **LSEG QA MarketPsyc**: Uses LSEG's MarketPsyc data in BigQuery to get market sentiment scores.
*   **LSEG QA ESG**: Retrieves ESG indicators from LSEG's ESG data in BigQuery.
*   **Google Search**: Used by the `symbol_to_ric_agent` and `companynews_agent` to find RICs and news articles.
*   **BigQuery**: The `lsegtools` use the BigQuery API to query the LSEG datasets.
*   **Finnhub API (Available)**: The project includes `finhubtools` (`investment_agent/generaltools/finhubtools.py`) that provide access to the Finnhub API for a wide range of financial data (Company News, Profile, Financials, etc.). However, the default agent configuration in `investment_agent/agent.py` primarily relies on LSEG tools and Google Search. The Finnhub tools are available for use but are not fully integrated into the main workflow.

### Data Sources

The agent relies on the following primary data sources:

*   **LSEG Data on Google Cloud**:
    *   Tick History
    *   QA MarketPsyc
    *   QA ESG
    *   Company Information
*   **Finnhub API**: A real-time API for financial market data.
*   **Google Search**: For general information and news.

### SQL

The agent dynamically generates and executes SQL queries against Google BigQuery to retrieve data from the LSEG datasets. The queries are constructed within the `lsegtools/tickhistory.py` file and are parameterized to fetch data for specific RICs and date ranges. The agent has read-only access to the BigQuery tables to ensure data integrity.

## Customer Use Cases

A typical user of the MarketMind agent would be a financial analyst or an asset manager who needs to quickly gather and analyze a large amount of information about a company. Here are some potential use cases:

*   **Due Diligence**: An analyst can use the agent to perform due diligence on a company before making an investment decision. The agent can provide a comprehensive report covering all key aspects of the company's performance and market perception.
*   **Competitor Analysis**: The agent can be used to compare multiple companies in the same sector, providing a side-by-side analysis of their financials, market sentiment, and ESG performance.
*   **Monitoring Existing Investments**: An asset manager can use the agent to monitor their existing investments by regularly generating reports and staying up-to-date with the latest news and events.
*   **Idea Generation**: The agent can be used to screen for potential investment opportunities based on specific criteria, such as positive market sentiment or strong ESG scores.

## Gemini Enterprise Ecosystem

The MarketMind agent is designed to be a valuable component of the Gemini Enterprise ecosystem. It can be deployed as a custom agent, allowing employees within an organization to leverage its powerful financial analysis capabilities.

By integrating with Gemini Enterprise, the MarketMind agent can:

*   **Be easily discovered and used by employees**: The agent can be published to the organization's private agent catalog, making it accessible to anyone with the necessary permissions.
*   **Leverage enterprise data**: The agent can be configured to access and analyze proprietary enterprise data, in addition to public financial data.
*   **Be managed and governed centrally**: Gemini Enterprise provides a centralized platform for managing, monitoring, and securing custom agents.
*   **Be integrated into other workflows**: The agent can be called by other agents or applications within the Gemini ecosystem, enabling the creation of more complex and powerful workflows.

## Setup and Usage

To set up and run the MarketMind agent, you will need to:

1.  **Install the required libraries**:
    ```bash
    pip install -r investment_agent/requirements.txt
    ```
2.  **Configure your Google Cloud project**:
    *   Make sure you have a Google Cloud project with the BigQuery API enabled.
    *   You will need to have access to the LSEG datasets in BigQuery.
    *   Set up authentication by running `gcloud auth application-default login`.
    *   (Optional) Create a `.env` file in the root directory (or `investment_agent` directory) to specify environment variables like `GOOGLE_CLOUD_PROJECT`.
3.  **Set up your Finnhub API key**:
    *   Get a free API key from [https://finnhub.io/](https://finnhub.io/).
    *   Store the API key in Google Secret Manager with the name `FinHubAccessKey`.
4.  **Run the agent**:
    The agent is designed to be run within the Google ADK environment. You can interact with it through the ADK CLI or by deploying it as a custom agent.

    Example interaction:
    ```
    > analyze Vodafone
    ```
    This command will trigger the agent to perform a full analysis of Vodafone, resulting in a detailed report.

## Evaluations

The project includes a comprehensive evaluation suite using the Google Agent Development Kit (ADK) `adk eval` framework to test the investment analyst agent's performance.

### How Evaluations are Created

Evaluations are designed using the V2 ADK evaluation format. They consist of:
1.  **Test Cases (`investment_agent/eval/investment_agent.test.json`)**: Contains defining inputs (e.g., prompt to analyze Vodafone and BT) and the expected outputs. Crucially, this file includes a recorded "gold standard" agent trace, specifying the exact sequence of sub-agent tool calls (`expected_tool_use`) that the `root_agent` should make to successfully retrieve the required data.
2.  **Configuration (`investment_agent/eval/test_config.json`)**: Defines the evaluation strictness.
    -   `tool_trajectory_avg_score`: Set to `ANY_ORDER` with a threshold of `1.0`. This ensures that the agent makes all the necessary API calls/tool usages to gather complete data, but allows the LLM some non-deterministic flexibility in the *order* those parallel requests are dispatched.
    -   `response_match_score`: Configured with a floating threshold (e.g., `0.30`) to accommodate the natural variance in how an LLM synthesizes and phrases long financial reports while still ensuring the core facts are present.

### How to Enhance Evaluations

To build upon the testing framework:
*   **Add New Test Cases:** Capture the full execution trace of the agent handling a new edge case or a different sector analysis using the ADK logging format. Insert this new input/output mapping into the `investment_agent.test.json` array.
*   **Extend Tool Checks:** As new tools (like Finnhub endpoints) are integrated into the main workflow, their expected invocations should be added to the `expected_tool_use` array within new or existing eval cases.

### Value of the Evaluation Suite

*   **Regression Testing:** Ensures that modifying the agent's prompts, adding new sub-agents, or switching underlying LLM models (e.g., migrating from Gemini 2.5 flash to Gemini 3.1 Pro) does not break existing data retrieval trajectories.
*   **Reliability:** By enforcing that all required tools (VWAP, ESG, Sentiment, etc.) are actually called during analysis, we guarantee the final report is grounded in complete data rather than LLM hallucinations.
*   **Performance Tuning:** The `response_match_score` provides a benchmark to iterate on system prompts to yield better, more consistent report formatting.

### How to Run

You can execute the evaluation suite locally using the ADK CLI. Ensure you are in the root of the project directory.

```bash
adk eval investment_agent investment_agent/eval/investment_agent.test.json --config_file_path investment_agent/eval/test_config.json --print_detailed_results
```
The output will display the `tool_trajectory_avg_score` and `response_match_score` for all test cases, indicating whether the agent's logic remains intact.

## Deployment

The project includes scripts to help you deploy the agent to Google Cloud (Agent Engine).

*   `agentenginedeploy.sh`: Deploys the MarketMind agent using a default configuration.
*   `agentenginedeploygemini3.sh`: Deploys the agent using the Gemini 3 model configuration.

These scripts use `curl` to interact with the Discovery Engine API. You may need to customize them with your specific project and location details before running.
