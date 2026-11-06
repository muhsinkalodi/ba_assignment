import os
import glob
import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "Electric_Vehicle_Population_Data.csv")


def find_local_csv():
    """Locates the downloaded EV dataset in the project directory."""
    possible_files = (
        glob.glob("*.csv")
        + glob.glob("data/*.csv")
        + glob.glob("data/raw/*.csv")
    )

    if not possible_files:
        raise FileNotFoundError(
            "[ERROR] No CSV file found! Please place your CSV file in the project root folder."
        )

    # Ignore processed file if present
    possible_files = [f for f in possible_files if "ev_population_cleaned.csv" not in f]
    selected_file = possible_files[0]
    print(f"[INFO] Found local dataset: {selected_file}")
    return selected_file


def clean_ev_data():
    """Reads local CSV file, cleans dataset, and exports processed file."""
    csv_file = find_local_csv()

    print("[INFO] Loading dataset into memory...")
    df = pd.read_csv(csv_file)

    # Columns present in your real dataset
    columns_to_keep = [
        "Model Year",
        "Make",
        "Model",
        "Electric Vehicle Type",
        "Electric Range",
        "County",
    ]

    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df_cleaned = df[existing_columns].dropna(
        subset=[col for col in ["Electric Range", "Make", "Model Year"] if col in df.columns]
    )

    # Shorten EV Type label names for concise legends
    if "Electric Vehicle Type" in df_cleaned.columns:
        df_cleaned["Electric Vehicle Type"] = df_cleaned[
            "Electric Vehicle Type"
        ].replace(
            {
                "Battery Electric Vehicle (BEV)": "BEV",
                "Plug-in Hybrid Electric Vehicle (PHEV)": "PHEV",
            }
        )

    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df_cleaned.to_csv(PROCESSED_PATH, index=False)

    print(
        f"[SUCCESS] Cleaned dataset saved to {PROCESSED_PATH} ({len(df_cleaned)} records)"
    )
    return df_cleaned


if __name__ == "__main__":
    clean_ev_data()