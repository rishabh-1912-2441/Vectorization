import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm

def generate_time_vector():
    start_time = datetime.strptime("09:15", "%H:%M")
    return [(start_time + timedelta(minutes=i)).strftime("%H:%M") for i in range(375)]

def generate_date_range(expiry_date, days=10):
    expiry = datetime.strptime(expiry_date, "%y%m%d")
    return [(expiry - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)][::-1]

def process_and_save_consolidated(input_folder, output_file):
    time_vector = generate_time_vector()
    consolidated_data = {}
    files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

    with tqdm(total=len(files), desc="Processing Files") as file_bar:
        for file_name in files:
            try:
                parts = file_name.split("NIFTY")[-1].split(".")[0]
                expiry_date = parts[:6]  # YYMMDD
                strike_price = int(parts[6:-2])
                option_type = "Call" if parts[-2:] == "CE" else "Put"

                df = pd.read_csv(os.path.join(input_folder, file_name))
                required_cols = ["Date", "Time", "Open", "High", "Low", "Close", "Volume", "Open Interest"]
                if not all(col in df.columns for col in required_cols):
                    print(f"Skipping {file_name}: Missing columns.")
                    file_bar.update(1)
                    continue

                # Convert numeric columns to float explicitly
                numeric_cols = ["Open", "High", "Low", "Close", "Volume", "Open Interest"]
                df[numeric_cols] = df[numeric_cols].astype(float)

                date_range = generate_date_range(expiry_date)
                matrix = np.full((3750, 6), -1.0)  # Initialize with -1.0

                for day_idx, date in enumerate(tqdm(date_range, desc=f"{file_name} - Days", leave=False)):
                    for minute_idx, time in enumerate(time_vector):
                        row = df[(df["Date"] == date) & (df["Time"] == time)]
                        if not row.empty:
                            values = row.iloc[0][["Open", "High", "Low", "Close", "Volume", "Open Interest"]].values
                            matrix[day_idx * 375 + minute_idx] = values

                expiry_date_fmt = datetime.strptime(expiry_date, "%y%m%d").strftime("%Y-%m-%d")
                consolidated_data.setdefault(expiry_date_fmt, {}).setdefault(strike_price, {})[option_type] = matrix

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

            file_bar.update(1)

    np.save(output_file, consolidated_data)
    print(f"All data saved to {output_file}")

# Example usage
input_folder = "Nifty_processed"
output_file = "consolidated_data1.npy"
process_and_save_consolidated(input_folder, output_file)
