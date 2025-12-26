import requests
import csv
import json

# === CONFIG ===
GRAPHQL_ENDPOINT = "https://app.traceable.ai/graphql"
API_TOKEN = "Bearer <enter_your_private_token>"
    "LiveTraffic": """
    {
      issueConfigs(get: { issueSourceType: "Live Traffic" }) {
        results {
          displayName
          description
          issueCategory
          issueCategoryDisplayName
          issueType
          globalEnableStatus
          fallbackSeverity
          systemCompliance { enabled }
          liveTraffic { enabled }
          customCompliance { id enabled }
        }
      }
    }
    """,
    "Compliance": """
    {
      issueConfigs(get: { issueSourceType: "Compliance" }) {
        results {
          displayName
          description
          issueCategory
          issueCategoryDisplayName
          issueType
          globalEnableStatus
          fallbackSeverity
          systemCompliance { enabled }
          liveTraffic { enabled }
          customCompliance { id enabled }
        }
      }
    }
    """,
    "PCI_DSS": """
    {
      issueConfigs(
        get: {issueIdentifier: {issueCategory: "PCI DSS"}, issueSourceType: "Compliance"}
      ) {
        results {
          displayName
          description
          issueCategory
          issueCategoryDisplayName
          issueType
          globalEnableStatus
          fallbackSeverity
          systemCompliance { enabled }
          liveTraffic { enabled }
          customCompliance { id enabled }
        }
      }
    }
    """
}

def run_query(query):
    headers = {"Content-Type": "application/json"}
    if API_TOKEN:
        headers["Authorization"] = f"{API_TOKEN}"

    response = requests.post(
        GRAPHQL_ENDPOINT,
        headers=headers,
        json={"query": query}
    )
    response.raise_for_status()
    return response.json()


def flatten_result(record, issue_type):
    """Convert a single result record into a flat dict for CSV export"""
    return {
        "issueSourceType": issue_type,
        "displayName": record.get("displayName"),
        "description": record.get("description"),
        "issueCategory": record.get("issueCategory"),
        "issueCategoryDisplayName": record.get("issueCategoryDisplayName"),
        "issueType": record.get("issueType"),
        "globalEnableStatus": record.get("globalEnableStatus"),
        "fallbackSeverity": record.get("fallbackSeverity"),
        "systemCompliance_enabled": record.get("systemCompliance", {}).get("enabled") if record.get(
            "systemCompliance") else None,
        "liveTraffic_enabled": record.get("liveTraffic", {}).get("enabled") if record.get("liveTraffic") else None,
        "customCompliance_id": record.get("customCompliance", {}).get("id") if record.get("customCompliance") else None,
        "customCompliance_enabled": record.get("customCompliance", {}).get("enabled") if record.get(
            "customCompliance") else None
    }


def export_to_csv(all_records, filename="passive_vulnerabilities.csv"):
    if not all_records:
        print("No records to export.")
        return

    # Extract headers dynamically
    headers = list(all_records[0].keys())
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_records)
    print(f"Exported {len(all_records)} records to {filename}")


def main():
    all_records = []
    for issue_type, query in QUERIES.items():
        print(f"Fetching data for {issue_type}...")
        data = run_query(query)
        results = data.get("data", {}).get("issueConfigs", {}).get("results", [])
        for r in results:
            all_records.append(flatten_result(r, issue_type))

    export_to_csv(all_records)


if __name__ == "__main__":
    main()
