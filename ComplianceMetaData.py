import requests
import csv

# GraphQL endpoint and token
GRAPHQL_ENDPOINT_POLICIES = "https://app.traceable.ai/graphql"
TOKEN_POLICIES = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqYzBNell4UkRKRVJUSkVOMFZGTlVRMk4wVXlOVFZCTlVVME1rVTBSVUl6T0VZNVF6VTFPQSJ9.eyJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlc192MiI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvY3VzdG9tZXJfaWQiOiI4YmNhZjAyOS0zYTE5LTQ3OTctYjIzOS1lMDEzZTdjNTA5MWIiLCJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlcyI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvanRpIjoiMzFiNTlhNzgtMGEwMC00YTYxLWI2M2QtYzJkNmEyMzdkZTZjIiwiaHR0cHM6Ly90cmFjZWFibGUuYWkvcmljaF9yb2xlcyI6W3siZW52cyI6W10sImlkIjoidHJhY2VhYmxlUmVhZFdyaXRlIn1dLCJnaXZlbl9uYW1lIjoiVmlqYXkgU2hhbmthciIsImZhbWlseV9uYW1lIjoiVmVua2F0YWNoYWxhbSIsIm5pY2tuYW1lIjoidmlqYXkudmVua2F0YWNoYWxhbSIsIm5hbWUiOiJWaWpheSBTaGFua2FyIFZlbmthdGFjaGFsYW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvZGIyYjRmM2M2M2JhZTFmMjJjNDJiMDE5ODI2YzVjZGU_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ2cy5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNS0xMS0xOVQwMjowNToyMy42NTBaIiwiZW1haWwiOiJ2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJpc3MiOiJodHRwczovL2F1dGgudHJhY2VhYmxlLmFpLyIsImF1ZCI6InVzNWtkYm54Y2UzTmhlTGJ6TEN4dVpxWUlRWWdRZ204Iiwic3ViIjoic2FtbHB8U0FNTC1UcmFjZWFibGUtUHJvZHx2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJpYXQiOjE3NjM1MTc5MzgsImV4cCI6MTc2MzU1MzkzOCwic2lkIjoiSHAyMGxEODBuWjFaNXltbGlCUm4yTE5Bb3JfNkJpU0YiLCJub25jZSI6IjlQZGJIV29LaVRWTGc5QkRGRXVxLVV0M2ZSOGZiVXZFQ3dUNVVBN043eUUifQ.O5wfhJENz50XvzT6cuv6tb26b6VuwFKFdenZCxO8ZTaRAI7VPhgEGpNNKpGLbuM4MvQjXCTkLQvXc-fN5KTG_RAYhamwyuz8vAPFPZ4gbypRm_NkG6Bz_wpHsWqoH-NqcJrMTM5upPhoSsE98dHEC9Bz1nvBGVDEcmuvg04SjoltruXEkBhYQKEjzXSDWWJ06EslfV8yvZdd4f4BWD2201mW9VlF85PJQMPnNE4kbRIbhMqatYFQZlD8UC_DJpJ0xJR023jmK5PlPxH64oSGBEGlz1btTpRRrYkxg_uUPlFR9VEm0TwskpdcJCaMk58OxqDBV8vqrvtQ4MtE4q1Vjw"
QUERY_POLICIES = """
{
  policies(filter: {policyActionTypes: [COMPLIANCE_VIOLATION]}) {
    results {
      id
      name
      disabled
      actions {
        type
        complianceViolation {
          name
          label
          severity
          description
        }
      }
    }
  }
}
"""

def fetch_data(query, token, endpoint):
    """Fetch data from the GraphQL endpoint."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}",
    }
    response = requests.post(endpoint, json={"query": query}, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)
        return []
    return response.json().get("data", {})

def filter_policies(data):
    """Filter policies with label 'Traceable'."""
    results = data.get("policies", {}).get("results", [])
    filtered = []
    for policy in results:
        for action in policy.get("actions", []):
            compliance_violation = action.get("complianceViolation", {})
            filtered.append([
                    policy.get("id", ""),
                    policy.get("name", ""),
                    policy.get("disabled", ""),
                    action.get("type", ""),
                    compliance_violation.get("name", ""),
                    compliance_violation.get("label", ""),
                    compliance_violation.get("severity", ""),
                    compliance_violation.get("description", "").strip(),
                ])
    return filtered

def write_csv(filename, data, columns):
    """Write data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(data)

# Main logic to fetch, filter, and write data
data_policies = fetch_data(QUERY_POLICIES, TOKEN_POLICIES, GRAPHQL_ENDPOINT_POLICIES)
filtered_policies = filter_policies(data_policies)
write_csv(
    "compliance_vulnerabilities.csv",
    filtered_policies,
    ["Policy ID", "Policy Name", "Disabled", "Action Type", "Compliance Name", "Label", "Severity", "Description"]
)

print("Filtered policies data export completed: filtered_policies.csv")
