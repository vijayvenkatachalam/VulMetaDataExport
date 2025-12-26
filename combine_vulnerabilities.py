import pandas as pd
import os


def combine_csv_to_excel(csv_files, output_excel):
    """
    Combine multiple CSV files into an Excel workbook with individual tabs.

    Parameters:
        csv_files (list): List of CSV file paths to combine.
        output_excel (str): Path to save the output Excel file.
    """
    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
        for csv_file in csv_files:
            try:
                # Read each CSV file
                data = pd.read_csv(csv_file)
                # Use the file name (without extension) as the sheet name
                sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
                # Write to Excel workbook
                data.to_excel(writer, index=False, sheet_name=sheet_name)
                print(f"Added {csv_file} to Excel sheet '{sheet_name}'")
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")


# Example usage
csv_files = [
    "active_vulnerabilities.csv",
    "passive_vulnerabilities.csv",
    "compliance_vulnerabilities.csv"
]  # Replace with your list of CSV files
output_excel = "combined_vulnerabilities.xlsx"  # Specify the output Excel file name

combine_csv_to_excel(csv_files, output_excel)
print(f"Combined data written to {output_excel}")
