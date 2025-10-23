import datetime
def get_current_date() -> dict:
    """Returns the current date.

    

    Returns:
        dict: status and result or error msg.
    """

    report = (
        f'The current date is {datetime.date.today()}'
    )
    return {"status": "success", "report": report}