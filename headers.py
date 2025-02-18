import os
import pandas as pd
from datetime import datetime

def process_csv_files(input_folder, output_folder):

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Define column headers
    headers = ["Date", "Time", "Open", "High", "Low", "Close", "Volume", "Open Interest"]

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            try:
                # Load the CSV file
                df = pd.read_csv(file_path, header=None)

                # Assign headers
                df.columns = headers

                # Convert date column to YYYY-MM-DD format
                df['Date'] = df['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').strftime('%Y-%m-%d'))

                # Save the processed file
                output_path = os.path.join(output_folder, file_name)
                df.to_csv(output_path, index=False)

                print(f"Processed and saved: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Example usage
input_folder = "Nifty"
output_folder = "Nifty_processed"
process_csv_files(input_folder, output_folder)
