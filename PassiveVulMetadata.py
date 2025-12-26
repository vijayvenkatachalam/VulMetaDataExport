import requests
import csv
import json

# === CONFIG ===
GRAPHQL_ENDPOINT = "https://app.traceable.ai/graphql"
API_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqYzBNell4UkRKRVJUSkVOMFZGTlVRMk4wVXlOVFZCTlVVME1rVTBSVUl6T0VZNVF6VTFPQSJ9.eyJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlc192MiI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvY3VzdG9tZXJfaWQiOiI4YmNhZjAyOS0zYTE5LTQ3OTctYjIzOS1lMDEzZTdjNTA5MWIiLCJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlcyI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvanRpIjoiMzFiNTlhNzgtMGEwMC00YTYxLWI2M2QtYzJkNmEyMzdkZTZjIiwiaHR0cHM6Ly90cmFjZWFibGUuYWkvcmljaF9yb2xlcyI6W3siZW52cyI6W10sImlkIjoidHJhY2VhYmxlUmVhZFdyaXRlIn1dLCJnaXZlbl9uYW1lIjoiVmlqYXkgU2hhbmthciIsImZhbWlseV9uYW1lIjoiVmVua2F0YWNoYWxhbSIsIm5pY2tuYW1lIjoidmlqYXkudmVua2F0YWNoYWxhbSIsIm5hbWUiOiJWaWpheSBTaGFua2FyIFZlbmthdGFjaGFsYW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvZGIyYjRmM2M2M2JhZTFmMjJjNDJiMDE5ODI2YzVjZGU_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ2cy5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNS0xMS0xOVQwMjowNToyMy42NTBaIiwiZW1haWwiOiJ2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJpc3MiOiJodHRwczovL2F1dGgudHJhY2VhYmxlLmFpLyIsImF1ZCI6InVzNWtkYm54Y2UzTmhlTGJ6TEN4dVpxWUlRWWdRZ204Iiwic3ViIjoic2FtbHB8U0FNTC1UcmFjZWFibGUtUHJvZHx2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJpYXQiOjE3NjM1MTc5MzgsImV4cCI6MTc2MzU1MzkzOCwic2lkIjoiSHAyMGxEODBuWjFaNXltbGlCUm4yTE5Bb3JfNkJpU0YiLCJub25jZSI6IjlQZGJIV29LaVRWTGc5QkRGRXVxLVV0M2ZSOGZiVXZFQ3dUNVVBN043eUUifQ.O5wfhJENz50XvzT6cuv6tb26b6VuwFKFdenZCxO8ZTaRAI7VPhgEGpNNKpGLbuM4MvQjXCTkLQvXc-fN5KTG_RAYhamwyuz8vAPFPZ4gbypRm_NkG6Bz_wpHsWqoH-NqcJrMTM5upPhoSsE98dHEC9Bz1nvBGVDEcmuvg04SjoltruXEkBhYQKEjzXSDWWJ06EslfV8yvZdd4f4BWD2201mW9VlF85PJQMPnNE4kbRIbhMqatYFQZlD8UC_DJpJ0xJR023jmK5PlPxH64oSGBEGlz1btTpRRrYkxg_uUPlFR9VEm0TwskpdcJCaMk58OxqDBV8vqrvtQ4MtE4q1Vjw"
QUERIES = {
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
