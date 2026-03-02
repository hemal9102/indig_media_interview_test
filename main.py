# //here we will give core logic
from fastapi  import FastAPI , Depends , Request , Form
from Fastapi.responses import HTMLResponse , RedirectResponse

from sqlalchemy.orm import Session
import models, database


# making databse table 
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title = "Online test system ")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# admin module
@app.post("/admin", response_class=HTMLResponse)
def admin(request: Request , db: Session = Depends(get_db) , subject: str = db.query(models.Subject).all()):
    question = db.query(models.Question).all()
    return templates.TemplateResponse("admin.html" , {"request": request , "subject": subject , "question": question})
@app.post("admin/subject")
def add_subject(name: str = FORM(...), db: Session = Depends(get_db)):
    new_subject = models.Subject(name=name)
    db.add(new_subject)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/question")
def add_question(subject_id: int = Form(...),text: str = Form(...), option_a: str = Form(...),
                  option_b: str = Form(...), 
                  option_c: str = Form(...), 
                  option_d: str = Form(...),
                    correct_option: str = Form(...), 
                    db: Session = Depends(get_db)):
    q= models.Question(subject_id=subject_id, text=text, option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, correct_option=correct_option)
    db.add(q)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.post("admin/question/{q_id}/delete")
def delete_question(q_id: int, db: Session =Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == q_id).first()
    if question:
        db.delete(question)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# user module
@app.get("/", response_class=HTMLResponse)
def index(request: Request , db: Session = Depends(get_db) , subject: str = db.query(models.Subject).all()):
    return templates.TemplateResponse("index.html" , {"request": request , "subject": subject})

@app.get("/quiz/{subject_id}", response_class=HTMLResponse)
def take_quiz(request: Request, subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    questions = db.query(models.Question).filter(models.Question.subject_id == subject_id).all()
    return templates.TemplateResponse("quiz.html", {"request": request, "subject": subject, "questions": questions})

@app.post("/submit_quiz/{subject_id}")
def submit_quiz(request: Request, subject_id: int, db: Session = Depends(get_db)):
    form_data = await request.form()
    questions = db.query(models.Question).filter(models.Question.subject_id == subject_id).all()
    score = 0
    total = len(questions)
    for q in questions:
        user_answer = form_data.get(f"question_{q.id}")
        if user_answer == q.correct_option:
            score += 1

        subject = db.query(models.Subbject).filter(models.Subject.id == subject_id).first()
    return templates.TemplateResponse("result.html", {
        "request": request, "score": score, "total": total, "subject": subject
    })