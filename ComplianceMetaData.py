import requests
import csv

# GraphQL endpoint and token
GRAPHQL_ENDPOINT_POLICIES = "https://app.traceable.ai/graphql"
TOKEN_POLICIES = "Bearer <enter_your_private_token>"
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
