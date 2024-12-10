import os
import json

# Path to the main CVE directory (example: './cvelistV5/cves/')
CVE_BASE_PATH = './cvelistV5/cves/'
# List of years for the CVEs we want to process
YEARS = [str(year) for year in range(1999, 2025)]

# Function to replace "n/a" with "not specified"
def replace_na(value):
    return 'not specified' if value == 'n/a' else value

# Function to retrieve values from the latest CVSS version
def get_latest_cvss(metrics):
    priority_order = ["cvssV3_1", "cvssV3_0", "cvssV2_0"]
    for version in priority_order:
        for metric in metrics:
            cvss_data = metric.get(version, {})
            if cvss_data:
                base_score = cvss_data.get('baseScore', 'not specified')
                base_severity = cvss_data.get('baseSeverity', 'not specified')
                return base_score, base_severity
    return "not specified", "not specified"

# Function to generate question-answer pairs with instructions
def generate_qa(cve_data):
    cve_id = cve_data.get('cveMetadata', {}).get('cveId', 'not specified')
    descriptions = cve_data.get('containers', {}).get('cna', {}).get('descriptions', [])
    description = descriptions[0].get('value', 'not specified') if descriptions else 'not specified'
    datepublished = cve_data.get('cveMetadata', {}).get('datePublished', 'not specified')
    references = cve_data.get('containers', {}).get('cna', {}).get('references', [])
    reference_links = [replace_na(ref.get('url', 'not specified')) for ref in references]    

    # Retrieve CVSS scores
    cvss_metric = cve_data.get('containers', {}).get('cna', {}).get('metrics', [])
    cvss_score, severity = get_latest_cvss(cvss_metric)

    # Access 'affected' and retrieve versions
    affected_items = cve_data.get('containers', {}).get('cna', {}).get('affected', [])
    affected_product = replace_na(cve_data.get('containers', {}).get('cna', {}).get('affected', [{}])[0].get('product', 'not specified'))

    # Retrieve all affected versions
    affected_versions = []
    for item in affected_items:
        versions = item.get('versions', [])
        if versions:
            for version_item in versions:
                version = replace_na(version_item.get('version', 'not specified'))
                affected_versions.append(version)
        else:
            affected_versions.append('not specified')

    qa_list = []

    if description != "not specified": 
        qa_list.append({"instruction": f"Describe {cve_id}.","input": f"What is {cve_id}?","output": f"{description}."})

    if affected_product != "not specified" and affected_versions != ["not specified"]:
        qa_list.append({"instruction": f"Identify the affected product in {cve_id}.","input": f"Which product is affected by {cve_id}?","output": f"The affected product is {affected_product} and version: {', '.join(affected_versions)}." })

    if cvss_score != "not specified" and severity != "not specified":
        qa_list.append({"instruction": f"State the CVSS score for {cve_id}.","input": f"What is the CVSS score of {cve_id}?","output": f"The CVSS score and severity for {cve_id} is {cvss_score}({severity})."})

    if reference_links:
        qa_list.append({"instruction": f"Provide references for {cve_id}.","input": f"Where can I find more information about {cve_id}?","output": f"References are available at: {', '.join(reference_links)}." })

    if datepublished != "not specified":
        qa_list.append({"instruction": f"State the publication date of {cve_id}.","input": f"When was {cve_id} published?", "output": f"{cve_id} was published on {datepublished}."})

    return qa_list

# Main function to read CVE files and generate the dataset
def process_cve_files():
    output_file = 'traincve.jsonl'
    total_processed = 0
    total_files = 0
    total_years = len(YEARS)

    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Loop through directories by year
        for i, year in enumerate(YEARS, start=1):
            year_path = os.path.join(CVE_BASE_PATH, year)
            print(f"[INFO] ({i}/{total_years}) Processing year {year}...")

            # Check that the directory exists
            if not os.path.isdir(year_path):
                print(f"[WARNING] The directory for year {year} is missing and will be skipped.")
                continue

            # Iterate through JSON files in the year's directory
            for root, dirs, files in os.walk(year_path):
                for file in files:
                    if file.endswith(".json"):
                        total_files += 1
                        file_path = os.path.join(root, file)

                        # Read the JSON file
                        with open(file_path, 'r') as f:
                            try:
                                cve_data = json.load(f)
                                qa_entries = generate_qa(cve_data)

                                # Write each question-answer pair to the JSONL file
                                for qa_entry in qa_entries:
                                    outfile.write(json.dumps(qa_entry, ensure_ascii=False) + '\n')
                                
                                total_processed += 1
                                print(f"[SUCCESS] {file} processed successfully.")
                            except json.JSONDecodeError:
                                print(f"[ERROR] Error reading JSON file: {file_path}")

    print(f"\n[COMPLETED] Dataset successfully generated in file {output_file}!")
    print(f"Statistics:")
    print(f"  - Total years processed: {i}")
    print(f"  - Total files found: {total_files}")
    print(f"  - Total files processed successfully: {total_processed}")

# Execute the script
if __name__ == "__main__":
    process_cve_files()
