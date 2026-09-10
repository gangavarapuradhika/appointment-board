from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- MODELS ---
class Appt(BaseModel):
    id: int
    title: str
    description: str = ""
    date: date
    start_time: time
    end_time: time
    status: str = "scheduled"

class ApptCreate(BaseModel):
    title: str
    description: str = ""
    date: date
    start_time: time
    end_time: time
    status: str = "scheduled" # THIS ENABLES STATUS EDIT

# --- DUMMY DATA ---
appointments: List[Appt] = [
    Appt(id=1, title="Team Standup Meeting", description="Daily Update", date=date(2026,8,12), start_time=time(10,0), end_time=time(10,30), status="completed"),
    Appt(id=2, title="Client Meeting", description="New project discussion", date=date(2026,9,10), start_time=time(11,0), end_time=time(12,0), status="scheduled"),
    Appt(id=3, title="Design Review", description="Reviewed on Design", date=date(2026,9,7), start_time=time(14,0), end_time=time(15,0), status="completed"),
    Appt(id=4, title="Doctor visit", description="Not available", date=date(2026,5,6), start_time=time(9,0), end_time=time(10,0), status="cancelled"),
]
next_id = 5

def clash(d, s, e, ignore=None):
    for a in appointments:
        if a.status == "cancelled":
            continue
        if ignore and a.id == ignore:
            continue
        if a.date!= d:
            continue
        if s < a.end_time and e > a.start_time:
            return True
    return False

# --- APIs ---
@app.get("/appointments")
def get_all(filter_date: Optional[date] = None, status: Optional[str] = None):
    res = appointments
    if filter_date:
        res = [x for x in res if x.date == filter_date]
    if status:
        res = [x for x in res if x.status == status]
    return res

@app.post("/appointments")
def add(data: ApptCreate):
    global next_id
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=400, detail="End must be after start")
    if clash(data.date, data.start_time, data.end_time):
        raise HTTPException(status_code=400, detail="Time slot already booked")
    new = Appt(id=next_id, title=data.title, description=data.description, date=data.date, start_time=data.start_time, end_time=data.end_time, status=data.status)
    next_id += 1
    appointments.append(new)
    return new

@app.put("/appointments/{id}")
def update(id: int, data: ApptCreate):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap:
        raise HTTPException(status_code=404, detail="Not found")
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=400, detail="End must be after start")
    if clash(data.date, data.start_time, data.end_time, ignore=id):
        raise HTTPException(status_code=400, detail="Time slot already booked")

    ap.title = data.title
    ap.description = data.description
    ap.date = data.date
    ap.start_time = data.start_time
    ap.end_time = data.end_time
    ap.status = data.status # THIS WILL UPDATE THE CARD BELOW
    return ap

@app.put("/appointments/{id}/complete")
def complete(id: int):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap: raise HTTPException(404, "Not found")
    ap.status = "completed"
    return ap

@app.put("/appointments/{id}/cancel")
def cancel(id: int):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap: raise HTTPException(404, "Not found")
    ap.status = "cancelled"
    return ap

@app.delete("/appointments/{id}")
def delete_appt(id: int):
    global appointments
    appointments = [x for x in appointments if x.id!= id]
    return {"message": "deleted"}