import requests
import json
from datetime import datetime

# Step 1: Download the data from the URL
url = 'https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json'
response = requests.get(url)
data = response.json()

# Step 2: Helper function to calculate the gap between two dates
def calculate_gap(end_date, next_start_date):
    # Convert the dates to datetime objects
    try:
        end_date = datetime.strptime(end_date, '%b/%d/%Y')
        next_start_date = datetime.strptime(next_start_date, '%b/%d/%Y')
        # Calculate the difference in days
        gap_days = (next_start_date - end_date).days
        return gap_days if gap_days > 0 else 0
    except ValueError:
        return 0

# Step 3: Function to process each candidate
def process_candidate(candidate):
    # Extract formatted name from contact_info
    name = candidate.get('contact_info', {}).get('name', {}).get('formatted_name', 'Unknown')
    output = f"Hello {name},\n"
    
    jobs = candidate.get('experience', [])
    if jobs:
        # Sort jobs by start date in ascending order (oldest first)
        jobs = sorted(jobs, key=lambda job: datetime.strptime(job['start_date'], '%b/%d/%Y'))

        for i in range(len(jobs)):
            job = jobs[i]
            role = job.get('title', 'Unknown Role')
            start_date = job.get('start_date', 'Unknown Start Date')
            end_date = job.get('end_date', 'Unknown End Date')
            location = job.get('location', {}).get('municipality', 'Unknown Location')

            # Append job experience to the output
            output += f"Worked as: {role}, From {start_date} To {end_date} in {location}\n"
            
            # Check for gaps between this job and the next one
            if i < len(jobs) - 1:
                next_job = jobs[i + 1]
                gap_days = calculate_gap(end_date, next_job['start_date'])
                if gap_days > 0:
                    output += f"Gap in CV for {gap_days} days\n"
    
    return output

# Step 4: Loop through all candidates and process them
for candidate in data:
    result = process_candidate(candidate)
    print(result)  # Display the results for each candidate
    print("\n" + "="*50 + "\n")  # Separate candidates by a line for clarity
