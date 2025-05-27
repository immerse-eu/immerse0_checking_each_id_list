import pandas as pd
import os
import re


def collect_unique_id_maganamed(base_path, save_path, output_filename):
    unique_participants = set()

    if not os.path.exists(base_path):
        print(f"❌ The specified folder does not exist: {base_path}")
    os.makedirs(save_path, exist_ok=True)

    csv_files = [f for f in os.listdir(base_path) if f.endswith(".csv")]

    for file in csv_files:
        file_path = os.path.join(base_path, file)
        try:
            data = pd.read_csv(file_path, sep=";", encoding="utf-8", on_bad_lines='skip')
            if "participant_identifier" in data.columns:
                unique_participants.update(data["participant_identifier"].dropna().unique())
            else:
                print(f"❌️ 'participant_identifier' column not found in {file}")
        except Exception as e:
            print(f"❌ Error reading file: {file_path}, Error: {e}")

    sorted_unique_participants = sorted(unique_participants)

    unique_participants_df = pd.DataFrame(sorted_unique_participants, columns=['participant_identifier'])
    output_file = os.path.join(save_path, output_filename)
    unique_participants_df.to_csv(output_file, sep=';', index=False)

    if os.path.exists(output_file):
        print(f"✅ Unique MaganaMed IDs have been sorted and saved to {output_file}")
    else:
        print("Error in saving file")
    return unique_participants_df


def analyze_and_categorize_ids(input_folder, input_filename, save_path, valid_output_filename="valid_ids_maganamed.csv",
                               error_output_filename="error_ids_maganamed.csv"):
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
    valid_types = ["P", "C", "A"]

    valid_pattern_hyphen = re.compile(r"^I-(" + "|".join(valid_centers) + r")-(" + "|".join(valid_types) + r")-\d{3}$")
    valid_pattern_underscore = re.compile(
        r"^I_(" + "|".join(["WI", "MA"]) + r")_(" + "|".join(valid_types) + r")_\d{3}$")

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
