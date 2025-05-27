import pandas as pd
import os
import re


def collect_unique_id_movisens_esm(base_path, save_path, output_filename):
    os.makedirs(save_path, exist_ok=True)
    unique_ids = set()

    # Only subfolders starting with "IMMERSE_T"
    for folder_name in os.listdir(base_path):

        if folder_name.startswith("IMMERSE_T"):
            subfolder_path = os.path.join(base_path, folder_name)
            if not os.path.isdir(subfolder_path):
                continue

            for file in os.listdir(subfolder_path):
                if file.endswith(".xlsx") and not file.startswith("~$"):  # Ignore temporary Excel files
                    file_path = os.path.join(subfolder_path, file)
                    try:
                        df = pd.read_excel(file_path, engine="openpyxl")

                        if "participant_id" in df.columns:
                            unique_ids.update(df["participant_id"].dropna().unique())
                        else:
                            print(f"❌ 'participant_id' column not found in {file}")
                    except Exception as e:
                        print(f"❌ Error reading {file_path}: {e}")

    # Sort and save
    sorted_ids = sorted(str(i) for i in unique_ids)
    df_result = pd.DataFrame(sorted_ids, columns=["participant_identifier"])
    output_file = os.path.join(save_path, output_filename)
    df_result.to_csv(output_file, index=False)

    print(f"✅ Unique 'participant_id' values saved to: {output_file}")
    return df_result


def collect_unique_id_movisens_sensing(base_path, save_path, output_filename):
    os.makedirs(save_path, exist_ok=True)
    unique_ids = set()

    for folder_name in os.listdir(base_path):
        if folder_name.startswith("IMMERSE_Sensing_"):
            subfolder_path = os.path.join(base_path, folder_name)
            if not os.path.isdir(subfolder_path):
                continue

            for file in os.listdir(subfolder_path):
                if file.endswith(".xlsx") and not file.startswith("~$"):  # Ignore temporary Excel files
                    file_path = os.path.join(subfolder_path, file)
                    try:
                        df = pd.read_excel(file_path, engine="openpyxl")

                        if "study_id" in df.columns:
                            unique_ids.update(df["study_id"].dropna().unique())
                        else:
                            print(f"❌ 'study_id' column not found in {file}")
                    except Exception as e:
                        print(f"❌ Error reading {file_path}: {e}")

    # Sort and save
    sorted_ids = sorted(str(i) for i in unique_ids)
    df_result = pd.DataFrame(sorted_ids, columns=["participant_identifier"])
    output_file = os.path.join(save_path, output_filename)
    df_result.to_csv(output_file, index=False)

    if output_filename:
        print(f"✅ Unique 'participant_identifier' values saved to: {output_file}")
    return df_result


def analyze_and_categorize_ids_ESM(input_folder, input_filename, save_path, valid_output_filename="valid_ids_esm.csv", error_output_filename="error_ids_esm.csv"):

    input_file = os.path.join(input_folder, input_filename)
    print('input_file', input_file)
    os.makedirs(save_path, exist_ok=True)  # Create the output folder if it doesn't exist

    try:
        df = pd.read_csv(input_file)
        if "participant_identifier" not in df.columns:
            print("❌ Error: 'participant_identifier' column does not exist.")
            return
    except Exception as e:
        print(f"❌ Error reading file: {input_file}, Error: {e}")
        return

    # **Define valid ID formats**
    valid_centers = ["BI", "LE", "MA", "WI", "BR", "KO", "CA", "LO"]
    valid_types = ["P"]

    valid_pattern_hyphen = re.compile(r"^I-(" + "|".join(valid_centers) + r")-(" + "|".join(valid_types) + r")-\d{3}$")
    valid_pattern_underscore = re.compile(r"^I_(" + "|".join(["WI", "MA"]) + r")_(" + "|".join(valid_types) + r")_\d{3}$")

    # **Lists for classifying IDs**
    valid_ids = []
    error_ids = []

    for id_value in df["participant_identifier"].dropna().astype(str):
        if valid_pattern_hyphen.match(id_value) or valid_pattern_underscore.match(id_value):
            valid_ids.append(id_value)  # Store valid ID
        else:
            error_ids.append(id_value)  # Store invalid ID

    # **Save valid IDs**
    valid_ids_df = pd.DataFrame(sorted(valid_ids), columns=["valid_participant_identifier"])
    valid_output_file = os.path.join(save_path, valid_output_filename)
    valid_ids_df.to_csv(valid_output_file, index=False)

    # **Save invalid IDs**
    error_ids_df = pd.DataFrame(sorted(error_ids), columns=["error_participant_identifier"])
    error_output_file = os.path.join(save_path, error_output_filename)
    error_ids_df.to_csv(error_output_file, index=False)

    print(f"✅ Valid IDs have been saved to {valid_output_file}")
    print(f"✅⚠️ Invalid IDs have been saved to {error_output_file}")


def analyze_and_categorize_ids_Sensing(input_folder, input_filename, save_path, valid_output_filename="valid_ids_sensing.csv", error_output_filename="error_ids_sensing.csv"):

    input_file = os.path.join(input_folder, input_filename)
    os.makedirs(save_path, exist_ok=True)  # Create the output folder if it doesn't exist

    try:
        df = pd.read_csv(input_file)
        if "participant_identifier" not in df.columns:
            print("❌ Error: 'participant_identifier' column does not exist.")
            return
    except Exception as e:
        print(f"❌ Error reading file: {input_file}, Error: {e}")
        return

    # **Define valid ID formats**
    valid_centers = ["BI", "LE", "MA", "WI", "BR", "KO", "CA", "LO"]
    valid_types = ["P"]

    valid_pattern_hyphen = re.compile(r"^I-(" + "|".join(valid_centers) + r")-(" + "|".join(valid_types) + r")-\d{3}$")
    valid_pattern_underscore = re.compile(r"^I_(" + "|".join(["WI", "MA"]) + r")_(" + "|".join(valid_types) + r")_\d{3}$")

    # **Lists for classifying IDs**
    valid_ids = []
    error_ids = []

    for id_value in df["participant_identifier"].dropna().astype(str):
        if valid_pattern_hyphen.match(id_value) or valid_pattern_underscore.match(id_value):
            valid_ids.append(id_value)  # Store valid ID
        else:
            error_ids.append(id_value)  # Store invalid ID

    # **Save valid IDs**
    valid_ids_df = pd.DataFrame(sorted(valid_ids), columns=["valid_participant_identifier"])
    valid_output_file = os.path.join(save_path, valid_output_filename)
    valid_ids_df.to_csv(valid_output_file, index=False)

    # **Save invalid IDs**
    error_ids_df = pd.DataFrame(sorted(error_ids), columns=["error_participant_identifier"])
    error_output_file = os.path.join(save_path, error_output_filename)
    error_ids_df.to_csv(error_output_file, index=False)

    print(f"✅ Valid IDs have been saved to {valid_output_file}")
    print(f"✅⚠️ Invalid IDs have been saved to {error_output_file}")
