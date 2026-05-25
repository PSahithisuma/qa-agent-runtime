from fastapi import APIRouter
from fastapi import Depends

from src.auth.dependencies import (
    get_current_user
)

from src.auth.rbac import (
    require_role
)

from src.services.vector_service import (
    VectorService
)

router = APIRouter()

vector_service = VectorService()


@router.get("/search")
async def search_failures(

    query: str,

    user=Depends(get_current_user)
):
    """
    Semantic failure search.
    """

    require_role(

        user["role"],

        ["admin", "developer", "viewer"]
    )

    results = vector_service.search_similar(
        query
    )

    formatted = []

    for item in results:

        formatted.append({

            "score": item.score,

            "metadata": item.payload
        })

    return {

        "query": query,

        "results": formatted
    }