from fastapi import APIRouter, Path, Query
from typing import Annotated
from shemas import Item

router = APIRouter(prefix='/items', tags=['items'])


@router.get('/')
async def get_all_items():
    pass


@router.get('/{id}')
async def get_item_by_id(id: Annotated[int, Path(...)]):
    return {'id': id, 'item': 'item'}


@router.post('/')
async def add_item(item: Item):
    pass