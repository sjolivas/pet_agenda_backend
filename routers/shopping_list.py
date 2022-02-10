from fastapi import APIRouter, Depends, HTTPException, status
from crud.user import get_user
from crud.shopping_list import (
    create_user_shoppinglist,
    get_shoppinglist,
    destroy_shoppinglist,
)
import database, schemas


router = APIRouter(prefix="/users", tags=["Shopping List"])

# Create - post operation
@router.post(
    "/{user_id}/shoppinglist/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShoppingList,
)
def create_shoppinglist(
    user_id: int,
    shoppinglist: schemas.ShoppingListCreate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_user_shoppinglist(db=db, shoppinglist=shoppinglist, user_id=user_id)


# Read - get operation
@router.get(
    "/{user_id}/shoppinglist/{shoppinglist_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShoppingList,
)
def read_shoppinglist(
    shoppinglist_id: int,
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
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")

    return shoppinglist


# Update - patch operation
@router.patch(
    "/{user_id}/shoppinglist/{shoppinglist_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.ShoppingList,
)
def patch_shoppinglist_info(
    shoppinglist_id: int,
    user_id: int,
    shoppinglist: schemas.ShoppingListUpdate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id)
    db_shoppinglist = get_shoppinglist(
        db, shoppinglist_id=shoppinglist_id, user_id=user_id
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    shoppinglist_data = shoppinglist.dict(exclude_unset=True)
    for key, value in shoppinglist_data.items():
        setattr(db_shoppinglist, key, value)
    db.add(db_shoppinglist)
    db.commit()
    db.refresh(db_shoppinglist)
    return db_shoppinglist


# Delete - delete operation
@router.delete(
    "/{user_id}/shoppinglist/{shoppinglist_id}",
    status_code=status.HTTP_200_OK,
)
def delete_shoppinglist(
    shoppinglist_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(
        database.get_db,
    ),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    shoppinglist = get_shoppinglist(
        db,
        shoppinglist_id=shoppinglist_id,
        user_id=user_id,
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if shoppinglist is None:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    return destroy_shoppinglist(db, shoppinglist_id, user_id)
