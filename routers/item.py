from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from crud.item import create_shopping_item, get_item, destroy_item, get_all_items
from crud.shopping_list import get_shoppinglist
from crud.user import get_user
import database, schemas


router = APIRouter(prefix="/users", tags=["Item"])

# Create - post operation
@router.post(
    "/{user_id}/shoppinglist/{shoppinglist_id}/items",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Item,
)
def create_item(
    user_id: int,
    shoppinglist_id: int,
    item: schemas.ItemCreate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    shoppinglist = get_shoppinglist(
        db, shoppinglist_id=shoppinglist_id, user_id=user_id
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    return create_shopping_item(db=db, item=item, shoppinglist_id=shoppinglist_id)


# Read - get operation
@router.get(
    "/{user_id}/shoppinglist/{shoppinglist_id}/items/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Item],
)
def read_items(
    user_id: int,
    shoppinglist_id: int,
    skip: int = 0,
    limit: int = 50,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    items = get_all_items(db, user_id, skip=skip, limit=limit)
    db_user = get_user(db, user_id=user_id)
    db_shoppinglist = get_shoppinglist(
        db, shoppinglist_id=shoppinglist_id, user_id=user_id
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    return items


@router.get(
    "/{user_id}/shoppinglist/{shoppinglist_id}/items/{item_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Item,
)
def read_item(
    shoppinglist_id: int,
    item_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    db_shoppinglist = get_shoppinglist(
        db, shoppinglist_id=shoppinglist_id, user_id=user_id
    )
    db_item = get_item(db, item_id, shoppinglist_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# Update - patch operation
@router.patch(
    "/{user_id}/shoppinglist/{shoppinglist_id}/items/{item_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Item,
)
def patch_item(
    item_id: int,
    shoppinglist_id: int,
    user_id: int,
    item: schemas.ItemUpdate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    db_shoppinglist = get_shoppinglist(
        db,
        shoppinglist_id=shoppinglist_id,
        user_id=user_id,
    )
    db_item = get_item(db, item_id, shoppinglist_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Delete - delete operation
@router.delete(
    "/{user_id}/shoppinglist/{shoppinglist_id}/items/{item_id}",
    status_code=status.HTTP_200_OK,
)
def delete_item(
    shoppinglist_id: int,
    item_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    shoppinglist = get_shoppinglist(
        db,
        shoppinglist_id=shoppinglist_id,
        user_id=user_id,
    )
    item = get_item(db, item_id, shoppinglist_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return destroy_item(db, item_id, shoppinglist_id)
