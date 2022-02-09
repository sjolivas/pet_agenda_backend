from sqlalchemy.orm import Session
import models, schemas

# Item Create Utility Function
def create_shopping_item(
    db: Session,
    item: schemas.ItemCreate,
    shoppinglist_id: int,
):
    db_item = models.Item(**item.dict(), owner_id=shoppinglist_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Item READ utility functions
def get_all_items(
    db: Session,
    shoppinglist_id: int,
    skip: int = 0,
    limit: int = 20,
):
    return (
        db.query(models.Item)
        .filter(models.Item.owner_id == shoppinglist_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_item(db: Session, item_id: int, shoppinglist_id: int):
    return (
        db.query(models.Item)
        .filter(models.Item.owner_id == shoppinglist_id)
        .filter(models.Item.id == item_id)
        .first()
    )


# Item DELETE utility functions
def destroy_item(
    db: Session,
    item_id: int,
    shoppinglist_id: int,
):
    (
        db.query(models.Item)
        .filter(models.Item.owner_id == shoppinglist_id)
        .filter(models.Item.id == item_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"
