import numpy as np
from datetime import datetime, timedelta
np.set_printoptions(precision=4, suppress=True)


def fetch_value(file_path, expiry_date, strike_price, option_type, date, time):
   
    try:
        # Load data
        data = np.load(file_path, allow_pickle=True).item()

        # Validate keys
        if expiry_date not in data:
            raise KeyError(f"Expiry date {expiry_date} not found.")
        if strike_price not in data[expiry_date]:
            raise KeyError(f"Strike price {strike_price} not found for expiry date {expiry_date}.")
        if option_type not in data[expiry_date][strike_price]:
            raise KeyError(f"Option type {option_type} not found for strike price {strike_price}.")

        # Get the matrix
        matrix = data[expiry_date][strike_price][option_type]

        # Calculate row index
        date_range = generate_date_range(expiry_date)
        if date not in date_range:
            raise ValueError(f"Date {date} is outside the 10-day range for expiry {expiry_date}.")
        day_index = date_range.index(date)
        time_vector = generate_time_vector()
        if time not in time_vector:
            raise ValueError(f"Time {time} is not valid.")
        time_index = time_vector.index(time)

        # Fetch row
        row_index = day_index * 375 + time_index
        return matrix[row_index].tolist()

    except Exception as e:
        return str(e)

# Helper functions
def generate_time_vector():
    start_time = datetime.strptime("09:15", "%H:%M")
    return [(start_time + timedelta(minutes=i)).strftime("%H:%M") for i in range(375)]

def generate_date_range(expiry_date, days=10):
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
    return [(expiry - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)][::-1]

# Example usage
file_path = "consolidated_data1.npy"
expiry_date = "2023-01-05"
strike_price = 16750
option_type = "Put"
date = "2024-12-18"
time = "11:29"
np.set_printoptions(precision=4, suppress=True)


result = fetch_value(file_path, expiry_date, strike_price, option_type, date, time)
print(f"Values at {date} {time}: {result}")

