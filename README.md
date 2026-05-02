# CS PhD Program Comparison Dashboard

## Overview
An interactive Streamlit dashboard that helps prospective CS PhD applicants
compare graduate programs across rankings, stipends, research areas, and
acceptance rates.

## Video Demo
[YouTube link — add after recording]

## Technologies Used
- Python 3.10
- Streamlit
- Pandas
- Matplotlib
- Seaborn

## Installation & Setup

1. Clone or download this repository
2. Navigate to the project folder:
   cd cs_phd_dashboard
3. Install dependencies:
   pip3 install streamlit pandas matplotlib seaborn

## How to Run

streamlit run app.py

Then open your browser to http://localhost:8501

## How to Run Tests

python3 tests/test_data.py

## Project Structure

cs_phd_dashboard/
├── app.py                   Main Streamlit dashboard
├── README.md                This file
├── data/
│   └── phd_programs.csv     Dataset of 20 CS PhD programs
├── tests/
│   └── test_data.py         Unit tests for data loading and filtering
├── docs/                    Screenshots
└── report/                  Final project report PDF

## Author
Ajitha Chittipothula — Virginia Tech