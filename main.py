from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

import models, schemas, database, crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    """
    Get a database session.
    
    :yield: Database session
    :rtype: Generator[Session, None, None]
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/items/', response_model=schemas.Item)
def create(item: schemas.Item, db: Session = Depends(get_db)):
    """
    Create a new item.
    
    :param item: Item data
    :type item: schemas.Item
    :param db: Database session
    :type db: Session
    :return: Created item
    :rtype: schemas.Item
    """
    return crud.create(db=db, item=item)


@app.get('/items', response_model=List[schemas.Item])
def retrieve_all(db: Session = Depends(get_db)):
    """
    Retrieve all items.
    
    :param db: Database session
    :type db: Session
    :return: List of items
    :rtype: List[schemas.Item]
    """
    return crud.retrieve_all(db)


@app.get('/items/{item_id}', response_model=schemas.Item)
def retrieve(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param db: Database session
    :type db: Session
    :return: Item if found
    :rtype: schemas.Item
    :raises HTTPException: If item not found
    """
    item = crud.retrieve(item_id=item_id, db=db)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found.")
    return item


@app.put('/items/{item_id}', response_model=schemas.Item)
def update(item_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param item: Updated item data
    :type item: schemas.Item
    :param db: Database session
    :type db: Session
    :return: Updated item if found
    :rtype: schemas.Item
    :raises HTTPException: If item not found
    """
    updated_item = crud.update(item_id=item_id, item=item, db=db)
    if not updated_item:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found.")
    return updated_item


@app.delete('/items/{item_id}')
def delete(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param db: Database session
    :type db: Session
    :return: Success message
    :rtype: Dict[str, str]
    :raises HTTPException: If item not found
    """
    success = crud.delete(item_id=item_id, db=db)
    if not success:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found.")
    return {"message": f"Item with id {item_id} deleted successfully."}


@app.get('/items/search/', response_model=List[schemas.Item])
def search(
    name: Optional[str] = None, 
    description: Optional[str] = None, 
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None, 
    quantity: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    """
    Search items based on criteria.
    
    :param name: Name (partial match)
    :type name: Optional[str]
    :param description: Description (partial match)
    :type description: Optional[str]
    :param min_price: Minimum price
    :type min_price: Optional[float]
    :param max_price: Maximum price
    :type max_price: Optional[float]
    :param quantity: Exact quantity
    :type quantity: Optional[int]
    :param db: Database session
    :type db: Session
    :return: List of items matching criteria
    :rtype: List[schemas.Item]
    """
    return crud.search(
        name=name, description=description, min_price=min_price, 
        max_price=max_price, quantity=quantity, db=db
    )
