import pandas as pd
import re
def preprocess(data):
    pattern_date = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2} (?:AM|PM))\]'

    # Regular expression pattern to extract the message
    pattern_message = r'\] (.*)$'

    # Using re.findall to extract all dates
    extracted_dates = re.findall(pattern_date, data)

    # Using re.findall to extract all messages
    extracted_messages = re.findall(pattern_message, data, flags=re.MULTILINE)

    # Create a DataFrame
    df = pd.DataFrame(list(zip(extracted_messages, extracted_dates)), columns=['user_message', 'date'])

    # Function to convert time to 24-hour format
    def convert_time_to_24_hour(time_str):
        time_obj = pd.to_datetime(time_str, format='%d/%m/%y, %I:%M:%S %p')
        return time_obj.strftime('%d/%m/%y, %H:%M:%S')

    # Apply the function to 'date' column (only convert time part)
    df['date'] = df['date'].apply(convert_time_to_24_hour)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df