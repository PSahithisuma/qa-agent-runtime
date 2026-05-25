from fastapi import APIRouter
from fastapi import Depends

from src.auth.dependencies import (
    get_current_user
)

from src.auth.rbac import (
    require_role
)

from src.services.patch_service import (
    PatchService
)

router = APIRouter()

patch_service = PatchService()


@router.post("/generate")
async def generate_patch(

    failure: dict,

    user=Depends(get_current_user)
):
    """
    Generate AI patch suggestion.
    """

    require_role(

        user["role"],

        ["admin", "developer"]
    )

    patch = patch_service.generate_patch(
        failure
    )

    return {

        "patch_suggestion": patch
    }