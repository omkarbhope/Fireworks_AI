from datetime import datetime

# Helper function to convert date to MM/DD/YYYY format and return parsed datetime
def parse_date(date_str, possible_formats):
    for date_format in possible_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            return parsed_date, date_format
        except ValueError:
            continue
    return None, None

# Function to compare dates and detect format
def get_passport_date_format(user_date_str, passport_date_str):
    # List of possible formats for passport dates
    possible_formats = [
        "%d/%m/%Y",          # DD/MM/YYYY
        "%m/%d/%Y",          # MM/DD/YYYY
        "%d %B %Y",          # DD Month YYYY
        "%B %d, %Y",         # Month DD, YYYY
        "%d-%m-%Y",          # DD-MM-YYYY
        "%m-%d-%Y",          # MM-DD-YYYY
        "%Y-%m-%d",          # YYYY-MM-DD
        "%Y/%m/%d",          # YYYY/MM/DD
        "%d %b %Y",          # DD Mon YYYY
        "%b %d, %Y"          # Mon DD, YYYY
    ]

    # Parse user's DOB
    try:
        user_date = datetime.strptime(user_date_str, "%m/%d/%Y")
    except ValueError:
        return "User date is not in a valid MM/DD/YYYY format."

    # Detect passport date format
    for date_format in possible_formats:
        try:
            passport_date = datetime.strptime(passport_date_str, date_format)

            # Check if the year, month, and day match
            if (user_date.year == passport_date.year and
                user_date.month == passport_date.month and
                user_date.day == passport_date.day):
                return True, date_format

        except ValueError:
            continue

    return False, "Could not determine a matching passport date format."

# Example usage
user_date_input = "03/09/2000"  # MM/DD/YYYY
passport_date_input = "9 March 2000"  # Example in a clear format

result = get_passport_date_format(user_date_input, passport_date_input)
print(result)
