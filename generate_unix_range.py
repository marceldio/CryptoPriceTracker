import time

def generate_unix_range():
    current_time = int(time.time())  # Текущее время в секундах
    start_date = current_time - 24 * 60 * 60  # Минус 24 часа
    end_date = current_time

    print(f"Start date: {start_date}, End date: {end_date}")

if __name__ == "__main__":
    generate_unix_range()
