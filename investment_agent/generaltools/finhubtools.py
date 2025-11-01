import finnhub
from . import helpercode
import logging

PROJECT_ID = helpercode.get_project_id()

finnhub_client = finnhub.Client(api_key=helpercode.access_secret_version(PROJECT_ID, "FinHubAccessKey"))

def symbol_lookup(company_name: str) -> dict:
    """Does a lookup on a compay name to get its trading symbol

    Args:
        company_name (str): The name of the company whoes symbol is being looked up.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.symbol_lookup(company_name)
        ),
    }

def company_news(symbol: str, start_date: str, end_date: str) -> dict:
    """Does a search of company news between the start date and the end date supplied

    Args:
        symbol (str): The stock symbol of the company being looked up for financial news.
        start_date (str): The date from which to start search for news.
        end_date (str): The date from whcih to end searching for news.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.company_news(symbol, _from=start_date, to=end_date)
        ),
    }

def company_profile(symbol: str) -> dict:
    """Retrieves the company profile for the symbol specified

    Args:
        symbol (str): The stock symbol of the company being looked up for Company Profile.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.company_profile2(symbol=symbol)
        ),
    }

def company_basic_financials(symbol: str) -> dict:
    """Retrieves the company financials for the symbol specified

    Args:
        symbol (str): The stock symbol of the company being looked up for company basic financials.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.company_basic_financials(symbol, 'all')
        ),
    }

def insider_sentiment(symbol: str, start_date: str, end_date: str) -> dict:
    """Retrieves the insider sentiment for the symbol specified

    Args:
        symbol (str): The stock symbol of the company being looked up for Insider Sentiment.
        start_date (str): The date from which to start search for news.
        end_date (str): The date from whcih to end searching for news.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.stock_insider_sentiment(symbol, start_date, end_date)
        ),
    }

def financials_reported(symbol: str) -> dict:
    """Retrieves the financials reported for the symbol specified

    Args:
        symbol (str): The stock symbol of the company being looked up for financials reported.

    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": (
            finnhub_client.financials_reported(symbol)
        )
    }

def sec_filings(symbol: str, start_date: str, end_date: str) -> dict:
    """Retrieves the sec filings for the symbol specified

    Args:
        symbol (str): The stock symbol of the company being looked up for Sec Filings.
        start_date (str): The date from which to start search for news.
        end_date (str): The date from whcih to end searching for news.

    Returns:
        dict: status and result or error msg.
    """
    print("sec_filings called")
    secfilings = finnhub_client.filings(symbol, start_date, end_date)
    parsed_filings = []
    for filing in secfilings:
        if filing['form'] in ['10-Q', '8-K']:
            parsed_filings.append({"accessNumber":filing['accessNumber'], 
                                   "symbol": symbol, 
                                   "filedDate": filing['filedDate'],
                                   "report": helpercode.get_text_from_url(filing['reportUrl'])})
            print(filing['reportUrl'])


    return {
        "status": "success",
        "report": (
            parsed_filings
        ),
    }

