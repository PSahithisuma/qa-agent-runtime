# src/api/routes/patch_routes.py
from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user
from src.auth.rbac import require_role
from src.services.patch_service import PatchService
from src.models.patch_request import PatchRequest
from typing import List

router = APIRouter()
patch_service = PatchService()


@router.post("/generate")
async def generate_patch(
    failure: PatchRequest,
    user=Depends(get_current_user)
):
    """
    Generate AI patch suggestion.
    Uses Ollama LLaMA if available, falls back to rules.
    """
    require_role(user["role"], ["admin", "developer"])

    patch = patch_service.generate_patch(failure.dict())

    return {
        "patch_suggestion": patch,
        "test_name": failure.test_name,
        "file_path": failure.file_path,
        "ai_powered": patch_service.is_ollama_available()
    }


@router.post("/generate-batch")
async def generate_batch_patches(
    failures: List[PatchRequest],
    user=Depends(get_current_user)
):
    """
    Generate AI patch suggestions for multiple failures at once.
    """
    require_role(user["role"], ["admin", "developer"])

    results = patch_service.generate_batch_patches(
        [f.dict() for f in failures]
    )

    return {
        "total": len(results),
        "patches": results,
        "ai_powered": patch_service.is_ollama_available()
    }


@router.get("/status")
async def patch_service_status(
    user=Depends(get_current_user)
):
    """
    Check if AI patch service is available.
    """
    ollama_available = patch_service.is_ollama_available()
    return {
        "status": "ready",
        "ai_available": ollama_available,
        "model": patch_service.model,
        "mode": "AI (Ollama)" if ollama_available else "Rule-based fallback"
    }