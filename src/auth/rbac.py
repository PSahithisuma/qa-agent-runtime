from fastapi import HTTPException


def require_role(

    user_role: str,

    allowed_roles: list
):
    """
    Enforce RBAC permissions.
    """

    if user_role not in allowed_roles:

        raise HTTPException(

            status_code=403,

            detail="Forbidden"
        )