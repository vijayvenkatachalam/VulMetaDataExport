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
    "Authorization": "Bearer <enter_your_private_token>"

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
