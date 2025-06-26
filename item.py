from fastapi import APIRouter, Path
from typing import Annotated
from shemas import Item

router = APIRouter(prefix='/items', tags=['items'])


@router.get('/')
async def get_all_items():
    pass


@router.get('/{id}')
async def get_item_by_id(id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {'id': id, 'item': 'item'}


@router.post('/')
async def add_item(item: Item):
    pass