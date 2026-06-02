def format_response(success: bool, message: str, data: dict = None) -> dict:
    """
    Standard Response Format:
    {
      "success": true,
      "message": "Action completed successfully",
      "data": {}
    }
    """
    if data is None:
        data = {}
    return {
        "success": success,
        "message": message,
        "data": data
    }
