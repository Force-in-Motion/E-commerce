from datetime import datetime
from typing import Annotated

from fastapi import Query, HTTPException, status


class Inspector:

    @classmethod
    async def date_checker(
        cls,
        date_start: Annotated[
            datetime,
            Query(..., description="Start date (Format: YYYY-MM-DD HH:MM:SS)"),
        ],
        date_end: Annotated[
            datetime,
            Query(..., description="End date (Format: YYYY-MM-DD HH:MM:SS)"),
        ],
    ):
        if date_start >= date_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_start must be less than date_end",
            )

        return date_start, date_end
