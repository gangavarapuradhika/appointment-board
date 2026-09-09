# Appointment Board

Simple task for appointment scheduling with clash check.

## How to run

Backend:
cd Backend
pip install fastapi uvicorn
python -m uvicorn main:app --port 8000 --reload

Frontend:
Just open Frontend/index.html in browser. Keep backend running.

Backend will run on http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## Features Done

- Add appointment with date and time
- Edit appointment
- Mark as completed / cancelled
- Filter by date and status
- Time slot clash check - if already booked shows error
- Cancelled shown in red color

## Sample Data

I added 4 appointments as asked in task:
- 2 scheduled
- 2 completed  
- 1 cancelled

## Note / Assumption

- Used in-memory list, no database as task said
- Cancelled appointments are free, so new booking can use that slot