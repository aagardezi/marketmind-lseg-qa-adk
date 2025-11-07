# MarketMind - Investment Research Agent

## Project Overview

MarketMind is a sophisticated investment research agent designed to assist asset managers and financial analysts in making informed decisions. It leverages a multi-agent system built with the Google Agent Development Kit (ADK) to gather, analyze, and synthesize financial data from various sources, including LSEG (London Stock Exchange Group) and Finnhub.

The agent is capable of providing a comprehensive analysis of a company, including its financial performance, market sentiment, ESG (Environmental, Social, and Governance) indicators, and significant events. The final output is a detailed report that can be used for investment evaluation.

## Architecture

The MarketMind agent is built on a hierarchical and parallel agent architecture, enabling efficient and specialized data processing.

### Agent/Sub-agent Design

The core of the system is a `root_agent` that orchestrates the entire workflow. The architecture is as follows:

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
*   **Finnhub API**: The `finhubtools` provide access to the Finnhub API for a wide range of financial data, including:
    *   Company News
    *   Company Profile
    *   Basic Financials
    *   Insider Sentiment
*   **Google Search**: Used by the `symbol_to_ric_agent` and `companynews_agent` to find RICs and news articles.
*   **BigQuery**: The `lsegtools` use the BigQuery API to query the LSEG datasets.

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
