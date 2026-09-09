from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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

# --- SAMPLE DATA FOR STEP 06 ---
appointments: List[Appt] = [
    Appt(id=1, title="Team Standup", description="Daily sync", date=date(2026,9,10), start_time=time(10,0), end_time=time(10,30), status="scheduled"),
    Appt(id=2, title="Client Meeting", description="Acme project discussion", date=date(2026,9,10), start_time=time(11,0), end_time=time(12,0), status="scheduled"),
    Appt(id=3, title="Design Review", description="Reviewed UI - Done", date=date(2026,9,11), start_time=time(14,0), end_time=time(15,0), status="completed"),
    Appt(id=4, title="Doctor Visit", description="Not available", date=date(2026,9,9), start_time=time(9,0), end_time=time(10,0), status="cancelled"),
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
    if data.end_time <= data.start_time:
        raise HTTPException(400, "End must be after start")
    if clash(data.date, data.start_time, data.end_time):
        raise HTTPException(400, "Time slot already booked")
    global next_id
    new = Appt(id=next_id, **data.model_dump())
    next_id += 1
    appointments.append(new)
    return {"message": "added", "data": new}

@app.put("/appointments/{id}")
def update(id: int, data: ApptCreate):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap:
        raise HTTPException(404, "Not found")
    ap.title, ap.description, ap.date, ap.start_time, ap.end_time = data.title, data.description, data.date, data.start_time, data.end_time
    return {"message": "updated"}

@app.put("/appointments/{id}/complete")
def complete(id: int):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap:
        raise HTTPException(404, "Not found")
    ap.status = "completed"
    return {"message": "completed"}

@app.put("/appointments/{id}/cancel")
def cancel(id: int):
    ap = next((x for x in appointments if x.id == id), None)
    if not ap:
        raise HTTPException(404, "Not found")
    ap.status = "cancelled"
    return {"message": "cancelled"}