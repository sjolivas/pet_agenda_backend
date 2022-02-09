from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# Shopping List Create utility function
def create_user_shoppinglist(
    db: Session, shoppinglist: schemas.PetCreate, user_id: int
):
    db_shoppinglist = models.ShoppingList(**shoppinglist.dict(), owner_id=user_id)
    db.add(db_shoppinglist)
    db.commit()
    db.refresh(db_shoppinglist)
    return db_shoppinglist


# Shopping List READ utility functions
def get_shoppinglist(db: Session, shoppinglist_id: int, user_id: int):
    return (
        db.query(models.ShoppingList)
        .filter(models.ShoppingList.owner_id == user_id)
        .filter(models.ShoppingList.id == shoppinglist_id)
        .first()
    )


# Note DELETE utility functions
def destroy_shoppinglist(db: Session, shoppinglist_id: int, user_id: int):
    (
        db.query(models.ShoppingList)
        .filter(models.ShoppingList.owner_id == user_id)
        .filter(models.ShoppingList.id == shoppinglist_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return {"message": "Successfully Deleted"}
