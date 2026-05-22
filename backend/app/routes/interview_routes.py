from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.interview_round import InterviewRound
from app.models.weak_area import WeakArea
from app.schemas.interview_schema import InterviewRoundCreate, InterviewRoundUpdate, InterviewRoundResponse

router = APIRouter(prefix="/rounds", tags=["Interview Rounds"])
# some key points
WEAKNESS_MAP = {
    "graph": "Graph Algorithms",
    "graphs": "Graph Algorithms",
    "tree": "Trees & Binary Search",
    "trees": "Trees & Binary Search",
    "dp": "Dynamic Programming",
    "dynamic programming": "Dynamic Programming",
    "sql": "SQL & Databases",
    "database": "SQL & Databases",
    "system design": "System Design",
    "design": "System Design",
    "os": "Operating Systems",
    "operating system": "Operating Systems",
    "network": "Computer Networks",
    "networking": "Computer Networks",
    "array": "Arrays & Strings",
    "string": "Arrays & Strings",
    "linked list": "Linked Lists",
    "sorting": "Sorting & Searching",
    "binary search": "Sorting & Searching",
    "recursion": "Recursion & Backtracking",
    "backtracking": "Recursion & Backtracking",
    "communication": "Communication Skills",
    "soft skills": "Communication Skills",
}


def detect_weak_areas(feedback: str, application_id: int, db: Session):
    """Check feedback text for weakness keywords and save to weak_areas table"""
    if not feedback:
        return

    feedback_lower = feedback.lower()
    detected = set() 

    for keyword, topic in WEAKNESS_MAP.items():
        if keyword in feedback_lower and topic not in detected:
            detected.add(topic)
            weak = WeakArea(
                application_id=application_id,
                topic=topic,
                detected_from=f"Feedback: {feedback[:100]}"  # store first 100 chars
            )
            db.add(weak)

    db.commit()


@router.post("/{application_id}", response_model=InterviewRoundResponse)
def add_round(application_id: int, round_data: InterviewRoundCreate, db: Session = Depends(get_db)):
    new_round = InterviewRound(
        application_id=application_id,
        round_name=round_data.round_name,
        feedback=round_data.feedback,
        result=round_data.result
    )
    db.add(new_round)
    db.commit()
    db.refresh(new_round)

   
    detect_weak_areas(round_data.feedback, application_id, db)

    return new_round



@router.get("/{application_id}", response_model=List[InterviewRoundResponse])
def get_rounds(application_id: int, db: Session = Depends(get_db)):
    rounds = db.query(InterviewRound).filter(
        InterviewRound.application_id == application_id
    ).all()
    return rounds


# PUT 
@router.put("/update/{round_id}", response_model=InterviewRoundResponse)
def update_round(round_id: int, round_data: InterviewRoundUpdate, db: Session = Depends(get_db)):
    round_obj = db.query(InterviewRound).filter(InterviewRound.id == round_id).first()
    if not round_obj:
        raise HTTPException(status_code=404, detail="Round not found")

    if round_data.round_name is not None:
        round_obj.round_name = round_data.round_name
    if round_data.feedback is not None:
        round_obj.feedback = round_data.feedback
        
        detect_weak_areas(round_data.feedback, round_obj.application_id, db)
    if round_data.result is not None:
        round_obj.result = round_data.result

    db.commit()
    db.refresh(round_obj)
    return round_obj


# DELETE
@router.delete("/delete/{round_id}")
def delete_round(round_id: int, db: Session = Depends(get_db)):
    round_obj = db.query(InterviewRound).filter(InterviewRound.id == round_id).first()
    if not round_obj:
        raise HTTPException(status_code=404, detail="Round not found")
    db.delete(round_obj)
    db.commit()
    return {"message": "Round deleted successfully"}
