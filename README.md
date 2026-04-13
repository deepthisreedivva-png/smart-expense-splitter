# Smart Expense Splitter

A simple Flask web app to split expenses among a group and calculate who owes whom.

## Features
- Add expenses
- Multiple people can pay (e.g., a:700,b:300)
- Automatic balance calculation
- Shows clear settlements (who pays whom)
- Reset all data

## How to Run

1. Clone or download project
2. Install dependencies:
   pip install -r requirements.txt

3. Run:
   python app.py

4. Open:
   http://127.0.0.1:5000

## Example

Input:
- Amount: 1000
- Paid by: a:700,b:300
- Members: a,b,c

Output:
- b pays a
- c pays a

## Tech Stack
- Python
- Flask
- HTML + Bootstrap
