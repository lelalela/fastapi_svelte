#Repository

from datetime import datetime
from sqlalchemy.orm import Session
from domain.answer.answer_schema import AnswerCreate, AnswerModify, AnswerDelete
from models import Question, Answer, User

def create_answer(db: Session, question: Question, answer_create:AnswerCreate, user:User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user
                       )
    db.add(db_answer)
    db.commit()
    
def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def modify_answer(db: Session, db_answer: Answer, answer_modify:AnswerModify, user:User):
    db_answer.content = answer_modify.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()
    
def delete_answer(db: Session, db_answer:Answer):
    db.delete(db_answer)
    db.commit()