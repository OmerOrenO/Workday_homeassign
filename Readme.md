# Candidate Processing Scripts

This repository contains two Python scripts for processing candidate data:

1. `extract_candidates.py`: Extracts and formats candidate information.
2. `filter_candidates.py`: Filters candidates based on specified criteria and stores them in MongoDB.

## Requirements

- Python 3.x
- `requests` library
- `pymongo` library

## Installation

Install the required libraries:
   ```
   pip install requests pymongo
   ```

## Usage

### extract_candidates.py

This script downloads candidate data from a specified URL, processes it, and prints formatted information for each candidate.

To run:
```
python extract_candidates.py
```

### filter_candidates.py

This script loads candidate data, filters it based on user input, and stores the filtered results in MongoDB.

To run:
```
python filter_candidates.py
```

Follow the prompts to enter filtering criteria (industry, skills, minimum years of experience).

## Note

Ensure you have MongoDB running locally on the default port (27017) before running `filter_candidates.py`.
