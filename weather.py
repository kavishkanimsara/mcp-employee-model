from typing import Any, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
LOCAL_API_BASE = "http://localhost:3000/api"

# Make a request to the NWS API with proper error handling.- helper function
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# Make a request to the local API with proper error handling
async def make_local_request(url: str) -> dict[str, Any] | None:
    """Make a request to the local API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request to local API: {e}")
            return None

# Format an alert feature into a readable string.- helper function
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_all_employees() -> str:
    """Get all employees from the local API.

    Returns:
        A formatted string containing all employees' information
    """
    url = f"{LOCAL_API_BASE}/employees"
    data = await make_local_request(url)

    if not data:
        return "Unable to fetch employees data."

    if not data:
        return "No employees found."

    # Format each employee's information
    employees = []
    for employee in data:
        employee_info = f"""
ID: {employee.get('id', 'N/A')}
Name: {employee.get('firstName', 'N/A')} {employee.get('lastName', 'N/A')}
Email: {employee.get('email', 'N/A')}
Position: {employee.get('position', 'N/A')}
Salary: LKR {float(employee.get('salary', 0)):,.2f}
Age: {employee.get('age', 'N/A')}
Location: {employee.get('location', 'N/A')}
Hire Date: {employee.get('hireDate', 'N/A')}
"""
        employees.append(employee_info)

    return "\n---\n".join(employees)

@mcp.tool()
async def get_employee_by_id(employee_id: int) -> str:
    """Get a specific employee by their ID.

    Args:
        employee_id: The ID of the employee to fetch

    Returns:
        A formatted string containing the employee's information
    """
    url = f"{LOCAL_API_BASE}/employees/{employee_id}"
    data = await make_local_request(url)

    if not data:
        return f"Unable to fetch employee data for ID {employee_id}."

    return f"""
ID: {data.get('id', 'N/A')}
Name: {data.get('firstName', 'N/A')} {data.get('lastName', 'N/A')}
Email: {data.get('email', 'N/A')}
Position: {data.get('position', 'N/A')}
Salary: LKR {float(data.get('salary', 0)):,.2f}
Age: {data.get('age', 'N/A')}
Location: {data.get('location', 'N/A')}
Hire Date: {data.get('hireDate', 'N/A')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')