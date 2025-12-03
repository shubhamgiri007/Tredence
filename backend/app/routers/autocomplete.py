from fastapi import APIRouter
from app.services.autocomplete_service import AutocompleteService
from app.schemas.autocomplete import AutocompleteRequest, AutocompleteResponse

router = APIRouter()


@router.post("/autocomplete", response_model=AutocompleteResponse)
async def get_autocomplete(request: AutocompleteRequest):
    """
    Get AI autocomplete suggestions (mocked)
    
    Args:
        request: AutocompleteRequest with code, cursorPosition, and language
        
    Returns:
        AutocompleteResponse with suggestion and confidence
    """
    result = AutocompleteService.get_suggestion(
        code=request.code,
        cursor_position=request.cursorPosition,
        language=request.language
    )
    
    return AutocompleteResponse(
        suggestion=result["suggestion"],
        confidence=result["confidence"],
        type=result["type"]
    )
