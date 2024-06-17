from datetime import datetime
import pytz

# Define the timezone you want
target_timezone = 'Asia/Kolkata'

# Get the current time in UTC
utc_now = datetime.now(pytz.utc)

# Convert UTC time to the target timezone
target_time = utc_now.astimezone(pytz.timezone(target_timezone)).strftime('%Y-%m-%d %H:%M:%S')
print(target_time)
