import pandas as pd
import os

def collect_unique_id_4_pseudonimizatoin(base_path, save_path, output_filename="idlist4pseudonymization.csv"):
    """
    Reads specific CSV files and collects unique IDs based on filename-specific column rules.
    Sorts the IDs alphabetically and saves them to a CSV file.
    """
    if not os.path.exists(base_path):
        print(f"❌ The specified folder does not exist: {base_path}")
        return

    os.makedirs(save_path, exist_ok=True)

    # Unique ID container
    unique_ids = set()

    # Collect all relevant CSVs
    csv_files = [f for f in os.listdir(base_path) if f.endswith(".csv")]

    for file in csv_files:
        file_path = os.path.join(base_path, file)
        try:
            df = pd.read_csv(file_path, sep=";", encoding="utf-8", on_bad_lines='skip')

            if "extracted_ids_maganamed.csv" in file and "participant_identifier" in df.columns:
                unique_ids.update(df["participant_identifier"].dropna().astype(str).unique())
            elif "extracted_ids_dmmh.csv" in file and "Participant" in df.columns:
                unique_ids.update(df["Participant"].dropna().astype(str).unique())
            elif "extracted_ids_movisensESM.csv" in file and "participant_id" in df.columns:
                unique_ids.update(df["participant_id"].dropna().astype(str).unique())
            else:
                print(f"⚠️ No matching ID column found in: {file}")

        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

    # Sort and save
    sorted_ids = sorted(unique_ids)
    df_result = pd.DataFrame(sorted_ids, columns=["study_id"])
    output_file = os.path.join(save_path, output_filename)
    df_result.to_csv(output_file, index=False, sep=";")

    print(f"✅ Final ID list saved to: {output_file}")
    return df_result
