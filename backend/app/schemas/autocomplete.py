from pydantic import BaseModel, Field
from typing import Optional


class AutocompleteRequest(BaseModel):
    code: str = Field(..., description="Current code content")
    cursorPosition: int = Field(..., description="Current cursor position")
    language: str = Field(default="python", description="Programming language")


class AutocompleteResponse(BaseModel):
    suggestion: str = Field(..., description="Autocomplete suggestion")
    confidence: float = Field(default=0.8, description="Confidence score")
    type: str = Field(default="snippet", description="Type of suggestion")
