import requests
import csv

# GraphQL endpoint
GRAPHQL_ENDPOINT = "https://app.traceable.ai/graphql"

# GraphQL query
QUERY = """
{
  vulnerabilityMetadataList {
    total
    count
    results {
      metadataId
      subCategoryName
      categoryName
      subCategoryDisplayName
      categoryDisplayName
      cvssScore
      cvssVectorString
      estimatedFixTime
      vulnerabilityV2Severity
      vulnerabilityDetectionType
      description
      tags {
        key
        value
      }
      customTags {
        tagValues {
          key
          values
        }
      }
      sourcePlugins
      customVulnerabilityTypeDetails {
        yamlConfiguration
      }
    }
  }
}
"""

# Define headers for the request (update with appropriate authentication if required)
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqYzBNell4UkRKRVJUSkVOMFZGTlVRMk4wVXlOVFZCTlVVME1rVTBSVUl6T0VZNVF6VTFPQSJ9.eyJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlc192MiI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvY3VzdG9tZXJfaWQiOiI4YmNhZjAyOS0zYTE5LTQ3OTctYjIzOS1lMDEzZTdjNTA5MWIiLCJodHRwczovL3RyYWNlYWJsZS5haS9yb2xlcyI6WyJ0cmFjZWFibGVSZWFkV3JpdGUiXSwiaHR0cHM6Ly90cmFjZWFibGUuYWkvanRpIjoiMzFiNTlhNzgtMGEwMC00YTYxLWI2M2QtYzJkNmEyMzdkZTZjIiwiaHR0cHM6Ly90cmFjZWFibGUuYWkvcmljaF9yb2xlcyI6W3siZW52cyI6W10sImlkIjoidHJhY2VhYmxlUmVhZFdyaXRlIn1dLCJnaXZlbl9uYW1lIjoiVmlqYXkgU2hhbmthciIsImZhbWlseV9uYW1lIjoiVmVua2F0YWNoYWxhbSIsIm5pY2tuYW1lIjoidmlqYXkudmVua2F0YWNoYWxhbSIsIm5hbWUiOiJWaWpheSBTaGFua2FyIFZlbmthdGFjaGFsYW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvZGIyYjRmM2M2M2JhZTFmMjJjNDJiMDE5ODI2YzVjZGU_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ2cy5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNS0xMS0xOVQwMjowNToyMy42NTBaIiwiZW1haWwiOiJ2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJpc3MiOiJodHRwczovL2F1dGgudHJhY2VhYmxlLmFpLyIsImF1ZCI6InVzNWtkYm54Y2UzTmhlTGJ6TEN4dVpxWUlRWWdRZ204Iiwic3ViIjoic2FtbHB8U0FNTC1UcmFjZWFibGUtUHJvZHx2aWpheS52ZW5rYXRhY2hhbGFtQGhhcm5lc3MuaW8iLCJpYXQiOjE3NjM1MTc5MzgsImV4cCI6MTc2MzU1MzkzOCwic2lkIjoiSHAyMGxEODBuWjFaNXltbGlCUm4yTE5Bb3JfNkJpU0YiLCJub25jZSI6IjlQZGJIV29LaVRWTGc5QkRGRXVxLVV0M2ZSOGZiVXZFQ3dUNVVBN043eUUifQ.O5wfhJENz50XvzT6cuv6tb26b6VuwFKFdenZCxO8ZTaRAI7VPhgEGpNNKpGLbuM4MvQjXCTkLQvXc-fN5KTG_RAYhamwyuz8vAPFPZ4gbypRm_NkG6Bz_wpHsWqoH-NqcJrMTM5upPhoSsE98dHEC9Bz1nvBGVDEcmuvg04SjoltruXEkBhYQKEjzXSDWWJ06EslfV8yvZdd4f4BWD2201mW9VlF85PJQMPnNE4kbRIbhMqatYFQZlD8UC_DJpJ0xJR023jmK5PlPxH64oSGBEGlz1btTpRRrYkxg_uUPlFR9VEm0TwskpdcJCaMk58OxqDBV8vqrvtQ4MtE4q1Vjw"
}

# Send the GraphQL query
response = requests.post(
    GRAPHQL_ENDPOINT, json={"query": QUERY}, headers=HEADERS
)

# Check response status
if response.status_code != 200:
    print("Failed to fetch data:", response.status_code, response.text)
    exit()

# Parse JSON response
data = response.json()

# Extract results
results = data.get("data", {}).get("vulnerabilityMetadataList", {}).get("results", [])

# Output CSV file
CSV_FILE = "active_vulnerabilities.csv"

# Flatten and write data to CSV
with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Write header
    header = [
        "metadataId",
        "subCategoryName",
        "categoryName",
        "subCategoryDisplayName",
        "categoryDisplayName",
        "cvssScore",
        "cvssVectorString",
        "estimatedFixTime",
        "vulnerabilityV2Severity",
        "vulnerabilityDetectionType",
        "description",
        "tags",  # Concatenated tags as key:value pairs
        "customTags",  # Concatenated custom tags as key:values
        "sourcePlugins",  # Concatenated sourcePlugins
        "yamlConfiguration",
    ]
    writer.writerow(header)

    # Write rows
    # Write rows
    for item in results:
        custom_tags = item.get("customTags", {})
        tag_values = custom_tags.get("tagValues", []) if custom_tags else []

        row = [
            item.get("metadataId", ""),
            item.get("subCategoryName", ""),
            item.get("categoryName", ""),
            item.get("subCategoryDisplayName", ""),
            item.get("categoryDisplayName", ""),
            item.get("cvssScore", ""),
            item.get("cvssVectorString", ""),
            item.get("estimatedFixTime", ""),
            item.get("vulnerabilityV2Severity", ""),
            item.get("vulnerabilityDetectionType", ""),
            item.get("description", "").strip(),
            "; ".join([f"{tag['key']}:{tag.get('value', '')}" for tag in item.get("tags", [])]),
            "; ".join([f"{tag['key']}:{','.join(tag.get('values', []))}" for tag in tag_values]),
            ", ".join(item.get("sourcePlugins", [])),
            item.get("customVulnerabilityTypeDetails", {}).get("yamlConfiguration", ""),
        ]
        writer.writerow(row)

print(f"Data successfully written to {CSV_FILE}")
