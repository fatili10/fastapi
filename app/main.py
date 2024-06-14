from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models
from . import database
from app.database import SessionLocal, engine

dictionnaire_de_couse = {
"farine": [200,"grammes"],
"oeuf": [6,"unité"]
}

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# Dépendance de la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    """
    Retourne un message de bienvenue.
    """
    return {"message": "Bonjour bienvenue sur l'API liste de course"}

    
@app.get("/get_dictionnaire")
def get_dictionnaire(db: Session = Depends(get_db)):
    items = db.query(models.CourseItem).all()
    if not items:
        return {"message": "Le dictionnaire est vide"}
    return {"content": {item.name: [item.quantity, item.unit] for item in items}}



@app.post("/add_to_dictionnaire")
def add_to_dictionnaire(element: str, quantite: int, unite: str | None = None, db: Session = Depends(get_db)):
    db_item = db.query(models.CourseItem).filter(models.CourseItem.name == element).first()
    if db_item:
        if unite and db_item.unit != unite:
            raise HTTPException(status_code=400, detail=f"Not the good unit for element, {element} is in {db_item.unit}")
        db_item.quantity += quantite
    else:
        db_item = models.CourseItem(name=element, quantity=quantite, unit=unite)
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
        
@app.delete("/remove_from_dictionnaire")
def remove_from_dictionnaire(element: str, db: Session = Depends(get_db)):
    db_item = db.query(models.CourseItem).filter(models.CourseItem.name == element).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"detail": f"{element} has been removed"}
    else:
        raise HTTPException(status_code=404, detail="Element not found in the dictionnaire")


#  uvicorn main:app --reload