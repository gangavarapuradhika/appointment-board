# Appointment Board -Tak 

## How to Run
Backend:
cd Backend/appointment-board
pip install fastapi uvicorn
python -m uvicorn main:app --reload --port 8001

Frontend: Open Frontend/index.html

## Task Asked vs What I Did

1. Show list/board
Task: show all appointments
What I did: Board visible with 4 sample appointments - 1 scheduled, 2 completed, 1 cancelled

2. Add new appointment
Task: add form
What I did: Form on top. We can add 2 more appointments, total 6 will show. If 3rd one same time, it blocks

3. Edit appointment
Task: edit should work
What I did: Edit button fills form. Fixed bug ap.status = data.status so status changes both top and bottom

4. Cancel appointment
Task: cancel option
What I did: Cancel button, card becomes red. We have 1 cancelled sample

5. Filter by date and status
Task: filter
What I did: Filter by date and status working

6. Mark as completed
Task: complete option
What I did: Complete button, card green. We have 2 completed sample

7. Stop same time slot
Task: prevent clash
What I did: If same slot, error "Time slot already booked"

8. Show cancelled as marked
Task: cancelled visible
What I did: Red for cancelled, 1 sample added

## Sample Data
- 1 Scheduled (blue)
- 2 Completed (green)
- 1 Cancelled (red)
- You can add 2 more appointments (total 6)

## Files
Backend/appointment-board/main.py
Frontend/index.html