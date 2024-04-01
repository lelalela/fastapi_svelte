#Controller

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud, question_schema
from domain.user.user_router import get_current_user
from models import User, Answer

router = APIRouter(
    prefix="/api/answer"
)

@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    answer_crud.create_answer(db, question=question, answer_create=_answer_create, user=current_user)

@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    return answer_crud.get_answer(db, answer_id=answer_id)      

@router.put("/modify", status_code=status.HTTP_204_NO_CONTENT)
def answer_modify(_answer_modify: answer_schema.AnswerModify,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    
    answer = answer_crud.get_answer(db=db, answer_id=_answer_modify.answer_id)
    
    if not answer:
        raise HTTPException(status_code=404, detail="답변 게시물이 없습니다.")
    
    answer_crud.modify_answer(db=db, db_answer=answer, answer_modify=_answer_modify, user=current_user)
    
@router.delete("/delete", response_model=question_schema.Question)    
def answer_delete(
    _answer_delete: answer_schema.AnswerDelete,
    db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db=db, answer_id=_answer_delete.answer_id)
    answer_crud.delete_answer(db=db, db_answer=answer)
    
    return question_crud.get_question(db=db, question_id=_answer_delete.question_id) 
    