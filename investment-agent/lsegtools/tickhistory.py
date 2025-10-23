from . import helpercode
import pandas as pd
import google.cloud.bigquery.client as bigquery

PROJECT_ID = helpercode.get_project_id()

def getVWAP(rics: list, start_date: str, end_date: str) -> dict:
    """Uses The tick history product to get the VWAP for a RIC code

    Args:
        rics (lsit): The stock RICs of the companies whoes VWAP is being retreived.
        start_date (str): The date from which to start VWAP calculation.
        end_date (str): The date from whcih to end VWAP calculation.

    Returns:
        dict: status and result or error msg.
    """
    placeholders = ', '.join(map(str, rics))
    query = ("""### Obtain VWAP for RIC
        WITH AllTrades AS(
            SELECT Date_Time,RIC,Price,Volume, Ask_Price,Ask_Size,Bid_Price,Bid_Size,Qualifiers
            FROM `dbd-sdlc-prod.LSE_NORMALISED.LSE_NORMALISED`
            WHERE Price IS NOT NULL
            -- Specific Date/Time range:
            AND (Date_Time BETWEEN "{1} 00:00:00.000000" AND "{2} 23:59:59.999999")
            AND Type = "Trade"
            AND VOLUME > 0
            AND PRICE > 0
            )
        SELECT CAST (extract(DATE FROM Date_Time) AS STRING) AS date_time, RIC, ROUND(SAFE_DIVIDE(SUM(Volume*Price),SUM(Volume)),3) AS VWAP,SUM(Volume) AS TotalVolume,AVG(Price) AS AvgPrice,
        COUNT(RIC) AS NumTrades, MAX(Ask_Price) AS MaxAskPrice,MAX(Ask_Size) as MaxAskSize,
         MAX(Bid_Price) AS MaxBidPrice, MAx(Bid_Size) AS MaxBidSize
        FROM AllTrades
        WHERE RIC IN ('{0}')
        GROUP BY RIC, date_time
        ORDER BY 1,2""").format(placeholders, start_date, end_date)
    
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(query)
    rows = query_job.result()
    pd = rows.to_dataframe()
    return {
        "status": "success",
        "function": "getVWAP",
        "report": (
            pd.to_json()
        ),
    }


def getMarketPsycSentiment(rics: list, start_date: str, end_date: str) -> dict:
    """Uses LSEG QA MarketPsyc data to get Sentiment data for  RIC codes

    Args:
        rics (list): The stock RIC of the companys whoes sentiment is being retreived.
        start_date (str): The date from which to start sentiment retreival.
        end_date (str): The date from whcih to end sentiment retreival.

    Returns:
        dict: status and result or error msg.
    """
    placeholders = ', '.join(map(str, rics))
    query = ("""### Obtain Sentiment for RICs
        SELECT a.ric, b.date_, avg(b.sentiment) sentiment,avg(b.uncertainty) uncertainty, avg(b.anger) anger, 
        avg(b.stress) stress, avg(b.optimism) optimism, avg(b.joy) joy, avg(b.fear) fear, avg(b.surprise) surprise, 
        avg(b.trust) trust, avg(b.violence) violence, avg(b.volatility) volatility, avg(b.gloom) gloom, avg(b.buzz) buzz, 
        avg(b.conflict) conflict, avg(b.cybercrime) cybercrime,
        avg(b.emotionvsfact) emotionvsfact, avg(b.innovation) innovation, avg(b.labordispute) labordispute, avg(b.longshort) longshort, avg(b.longshortforecast) longshortforecast, avg(b.lovehate) lovehate, avg(b.marketrisk) marketrisk, avg(b.mergers) mergers FROM `genaillentsearch.LSEGQA202510.company_info_mpicmpinfo` a
        inner join `genaillentsearch.LSEGQA202510.company_emotion_MPICmpEmeaData` b
        on a.orgpermid = b.orgpermid
        inner join `genaillentsearch.LSEGQA202510.MPICode` c
        on b.datatype = c.type_
        where ric in ('{0}')
        and date_ between "{1} 00:00:00.000000" AND "{2} 23:59:59.999999"
        and c.desc_ not in ('AMER','APAC')
        and datatype=2
        group by a.ric, b.date_
        order by a.ric, b.date_
        """).format(placeholders, start_date, end_date)
    
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(query)
    rows = query_job.result()
    pd = rows.to_dataframe()
    return {
        "status": "success",
        "function": "getMarketPsycSentiment",
        "report": (
            pd.to_json()
        ),
    }

def getCompanyDetails(rics: list) -> dict:
    """Uses LSEG QA Data to get Company Details  RIC codes

    Args:
        rics (list): The stock RIC of the companies whoes details is being retreived.
    Returns:
        dict: status and result or error msg.
    """
    placeholders = ', '.join(map(str, rics))
    query = ("""### Obtain Company Details for RICs
        SELECT a.ric, b.* FROM `genaillentsearch.LSEGQA202510.CompanyInfo_RKDFndInfo` a
        inner join `genaillentsearch.LSEGQA202510.company_info_RKDFndCmpDet` b
        on a.code=b.code
        where ric in ('{0}')
        """).format(placeholders)
    
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(query)
    rows = query_job.result()
    pd = rows.to_dataframe()
    return {
        "status": "success",
        "function": "getCompanyDetails",
        "report": (
            pd.to_json()
        ),
    }

def getSignificantEvents(rics: list, start_date: str, end_date: str) -> dict:
    """Uses LSEG QA MarketPsyc data to get Sentiment data for  RIC codes

    Args:
        rics (list): The stock RIC of the companies whoes significant events are being retreived.
        start_date (str): The date from which to start significant events retreival.
        end_date (str): The date from whcih to end significant events retreival.
    Returns:
        dict: status and result or error msg.
    """
    placeholders = ', '.join(map(str, rics))
    query = ("""### Obtain Company Details for RICs
        SELECT * from  `genaillentsearch.LSEGQA202510.rkdcmpsigdev` b
        where b.ric in ('{0}')
        and b.srcdt between "{1} 00:00:00.000000" AND "{2} 23:59:59.999999"
        """).format(placeholders, start_date, end_date)
    
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(query)
    rows = query_job.result()
    pd = rows.to_dataframe()
    return {
        "status": "success",
        "function": "getCompanyDetails",
        "report": (
            pd.to_json()
        ),
    }