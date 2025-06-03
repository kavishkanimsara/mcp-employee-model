from typing import Any, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("employee")

LOCAL_API_BASE = "http://localhost:3000/api"

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


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')