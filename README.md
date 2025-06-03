# Weather MCP Server

This project provides an MCP (Modular Command Platform) server for weather information and employee data integration.

## Features

- **Employee Directory**: Fetch all employees or a specific employee from a local API.

## Endpoints (MCP Tools)

### Employees
- `get_all_employees() -> str`: Get all employees from the local API (`http://localhost:3000/api/employees`).
- `get_employee_by_id(employee_id: int) -> str`: Get a specific employee by their ID from the local API (`http://localhost:3000/api/employees/{id}`).

## Example Usage


### Get All Employees
```json
{"name": "get_all_employees", "parameters": {}}
```

### Get Employee by ID
```json
{"name": "get_employee_by_id", "parameters": {"employee_id": 5}}
```

## Requirements
- Python 3.10+
- [httpx](https://www.python-httpx.org/)
- [mcp-server](https://pypi.org/project/mcp-server/)

## Running the Server

1. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uv run weather.py
   ```

The server will listen for MCP requests via stdio.

## Notes
- The employee endpoints require a local API running at `http://localhost:3000/api/employees`.
- Weather data is fetched from the US National Weather Service (NWS) API.
