import json
import requests
from pymongo import MongoClient

# MongoDB connection setup
def connect_to_mongo():
    # Adjust the connection string if needed
    client = MongoClient('mongodb://localhost:27017/')
    db = client['candidate_db']  # You can name your database
    return db['filtered_candidates']  # Collection name

# Function to load candidate data from a JSON URL
def load_candidate_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return the JSON data as a Python dictionary
    else:
        raise Exception(f"Failed to load data from URL: {url}")

# Function to filter candidates based on industry, skills, and experience
def filter_candidates(candidates, industry=None, skills=None, min_experience=0):
    filtered_candidates = []
    
    for candidate in candidates:
        # Calculate total years of experience across all jobs
        total_experience = sum(exp['duration_in_month'] // 12 for exp in candidate.get('experience', []))
        
        # Check for industry match
        if industry:
            industry_match = any(
                exp.get('company_details') and industry in exp['company_details'].get('industry', '') 
                for exp in candidate.get('experience', [])
            )
            if not industry_match:
                continue
        
        # Check for skills match
        if skills:
            if not any(skill in candidate.get('extracted_skills', []) for skill in skills):
                continue
        
        # Check for minimum experience
        if total_experience < min_experience:
            continue
        
        filtered_candidates.append(candidate)

    return filtered_candidates

# Function to insert candidates into MongoDB
def insert_candidates_to_mongo(candidates, collection):
    if candidates:
        result = collection.insert_many(candidates)
        print(f'Inserted {len(result.inserted_ids)} candidates into MongoDB.')
    else:
        print('No candidates to insert.')

# Main function to orchestrate loading, filtering, and inserting
def main(url):
    # Load candidates
    candidates = load_candidate_data(url)

    # Prompt user for filtering criteria
    industry_filter = input("Enter industry to filter (or press Enter to skip): ")
    skills_filter = input("Enter skills to filter (comma separated, or press Enter to skip): ")
    min_experience_filter = input("Enter minimum years of experience (or press Enter to skip): ")

    # Process skills filter
    skills = [skill.strip() for skill in skills_filter.split(',')] if skills_filter else None
    # Process minimum experience filter
    min_experience = int(min_experience_filter) if min_experience_filter.isdigit() else 0

    # Filter candidates
    filtered_candidates = filter_candidates(candidates, industry_filter, skills, min_experience)

    # Connect to MongoDB and insert filtered candidates
    collection = connect_to_mongo()
    insert_candidates_to_mongo(filtered_candidates, collection)

# Example usage
if __name__ == "__main__":
    url = 'https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json'
    main(url)
