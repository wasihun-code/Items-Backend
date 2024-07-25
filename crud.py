from sqlalchemy.orm import Session
import models, schemas
from typing import List, Optional


def create(db: Session, item: schemas.Item) -> models.Items:
    """
    Create a new item in the database.
    
    :param db: Database session
    :type db: Session
    :param item: Item data
    :type item: schemas.Item
    :return: Created item
    :rtype: models.Items
    """
    db_item = models.Items(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def retrieve(item_id: int, db: Session) -> Optional[models.Items]:
    """
    Retrieves an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param db: Database session
    :type db: Session
    :return: Item if found, else None
    :rtype: Optional[models.Items]
    """
    return db.query(models.Items).filter(models.Items.id == item_id).first()


def retrieve_all(db: Session) -> List[models.Items]:
    """
    Retrieve all items.
    
    :param db: Database session
    :type db: Session
    :return: List of items
    :rtype: List[models.Items]
    """
    return db.query(models.Items).all()


def update(item_id: int, item: schemas.Item, db: Session) -> Optional[models.Items]:
    """
    Update an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param item: Updated item data
    :type item: schemas.Item
    :param db: Database session
    :type db: Session
    :return: Updated item if found, else None
    :rtype: Optional[models.Items]
    """
    existing_item = retrieve(item_id, db)
    if not existing_item:
        return None
    db.query(models.Items).filter(models.Items.id == item_id).update(item.dict(), synchronize_session='auto')
    db.commit()
    return retrieve(item_id, db)


def delete(item_id: int, db: Session) -> bool:
    """
    Delete an item by ID.
    
    :param item_id: Item ID
    :type item_id: int
    :param db: Database session
    :type db: Session
    :return: True if deleted, else False
    :rtype: bool
    """
    item = retrieve(item_id, db)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def search(
    db: Session, 
    name: Optional[str] = None, 
    description: Optional[str] = None, 
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None, 
    quantity: Optional[int] = None
) -> List[models.Items]:
    """
    Search items based on criteria.
    
    :param db: Database session
    :type db: Session
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
    :return: List of items matching criteria
    :rtype: List[models.Items]
    """
    query = db.query(models.Items)
    
    if name:
        query = query.filter(models.Items.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(models.Items.description.ilike(f"%{description}%"))
    if min_price is not None:
        query = query.filter(models.Items.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Items.price <= max_price)
    if quantity is not None:
        query = query.filter(models.Items.quantity == quantity)
    
    return query.all()
