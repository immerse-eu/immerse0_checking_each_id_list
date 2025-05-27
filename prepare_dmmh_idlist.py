import pandas as pd
import os
import re


# If we received one single JSON file per center containing data across all dates, use this function
def collect_unique_id_dmmh_singleExport(base_path, save_path, output_filename):
    """
    Reads all CSV files in the specified folder, collects unique values from the 'Participant' column,
    sorts them alphabetically, and saves them to a CSV file.

    Parameters:
        base_path (str): Path to the folder containing the CSV files.
        save_path (str): Path to the folder where the result file will be saved.
        output_filename (str): Name of the output file (default: "idlist4pseudonymization.csv")
    """
    if not os.path.exists(base_path):
        print(f"❌ The specified folder does not exist: {base_path}")
        return

    os.makedirs(save_path, exist_ok=True)  # Create output folder if it doesn't exist

    unique_participants = set()  # Use a set to avoid duplicates

    # Search for all CSV files in the folder
    csv_files = [f for f in os.listdir(base_path) if f.endswith(".csv")]

    for file in csv_files:
        file_path = os.path.join(base_path, file)

        try:
            # data = pd.read_csv(file_path, sep=",", encoding="utf-8", on_bad_lines='skip')
            data = pd.read_csv(file_path, sep=",", encoding="utf-8", usecols=['Participant'],
                               dtype={'Participant': str})

            # Add values if "Participant" column exists
            if "Participant" in data.columns:
                unique_participants.update(data["Participant"].dropna().unique())
            else:
                print(f"❌️ Column 'Participant' not found in {file}")
        except Exception as e:
            print(f"❌ Error reading file: {file_path}, Error: {e}")

    # Sort alphabetically
    sorted_unique_participants = sorted(unique_participants)

    # Convert to DataFrame and save
    unique_participants_df = pd.DataFrame(sorted_unique_participants, columns=['Participant'])
    output_file = os.path.join(save_path, output_filename)
    unique_participants_df.to_csv(output_file, index=False)

    print(f"✅ Unique 'Participant' values have been sorted and saved to {output_file}")

    return unique_participants_df


# If we received multiple JSON files per center, separated by date, please use this function
def collect_unique_id_dmmh_multiple_export(base_path, save_path, output_filename):
    unique_participants = set()

    if not os.path.exists(base_path):
        print(f"❌ The specified folder does not exist: {base_path}")
    os.makedirs(save_path, exist_ok=True)

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    dmmh_df = pd.read_csv(file_path, sep=",", encoding="utf-8", usecols=['Participant'],
                                       dtype={'Participant': str})

                    if "Participant" in dmmh_df.columns:
                        unique_participants.update(dmmh_df["Participant"].dropna().unique())
                    else:
                        print(f"❌️ Column 'Participant' not found in {file_path}")
                except Exception as e:
                    print(f"❌ Error reading file: {file_path}, Error: {e}")

    # Sort and save results
    sorted_unique_participants = sorted(unique_participants)
    unique_participants_df = pd.DataFrame(sorted_unique_participants, columns=['participant_identifier'])
    output_file = os.path.join(save_path, output_filename)
    unique_participants_df.to_csv(output_file, index=False)

    if os.path.exists(output_file):
        print(f"✅ Unique 'Participant' values from all folders saved to: {output_file}")
        return unique_participants_df
    else:
        print("Error in saving file")


def analyze_and_categorize_ids(input_folder, input_filename, save_path, valid_output_filename="valid_ids_dmmh.csv",
                               error_output_filename="error_ids_dmmh.csv"):

    input_file = os.path.join(input_folder, input_filename)
    os.makedirs(save_path, exist_ok=True)  # Create output folder if it doesn't exist

    try:
        df = pd.read_csv(input_file)
        if "participant_identifier" not in df.columns:
            print("❌ Error: 'participant_identifier' column is missing.")
            return
    except Exception as e:
        print(f"❌ Error reading file: {input_file}, Error: {e}")
        return

    # Define valid ID formats
    valid_centers = ["BI", "LE", "MA", "WI", "BR", "KO", "CA", "LO"]
    valid_types = ["P"]

    valid_pattern_hyphen = re.compile(r"^I-(" + "|".join(valid_centers) + r")-(" + "|".join(valid_types) + r")-\d{3}$")
    valid_pattern_underscore = re.compile(
        r"^I_(" + "|".join(["WI", "MA"]) + r")_(" + "|".join(valid_types) + r")_\d{3}$")

    # Lists for classifying IDs
    valid_ids = []
    error_ids = []

    for id_value in df["participant_identifier"].dropna().astype(str):
        if valid_pattern_hyphen.match(id_value) or valid_pattern_underscore.match(id_value):
            valid_ids.append(id_value)  # Valid ID
        else:
            error_ids.append(id_value)  # Invalid ID

    # Save valid IDs
    valid_ids_df = pd.DataFrame(sorted(valid_ids), columns=["valid_participant_identifier"])
    valid_output_file = os.path.join(save_path, valid_output_filename)
    valid_ids_df.to_csv(valid_output_file, index=False)

    # Save invalid IDs
    error_ids_df = pd.DataFrame(sorted(error_ids), columns=["error_participant_identifier"])
    error_output_file = os.path.join(save_path, error_output_filename)
    error_ids_df.to_csv(error_output_file, index=False)

    print(f"✅ Valid IDs saved to {valid_output_file}")
    print(f"✅⚠️ Invalid IDs saved to {error_output_file}")
