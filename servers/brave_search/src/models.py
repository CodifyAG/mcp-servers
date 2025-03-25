# In models.py
from pydantic import BaseModel, Field, field_validator

MAX_RESULTS_PER_REQUEST = 20

class WebSearchRequest(BaseModel):
    q: str = Field(..., description="Search query string")
    count: int = Field(10, ge=1, le=MAX_RESULTS_PER_REQUEST, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Results offset for pagination")
    search_lang: str = Field("en", description="Search language code")
    
    # Pydantic v2 validator
    @field_validator('q')
    @classmethod
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Search query cannot be empty')
        return v

class LocalSearchRequest(BaseModel):
    q: str = Field(..., description="Search query string")  # Changed to 'q' for consistency
    count: int = Field(5, ge=1, le=MAX_RESULTS_PER_REQUEST, description="Number of results to return")
    search_lang: str = Field("en", description="Search language code")
    result_filter: str = Field("locations", description="Filter for location results")
    
    # Pydantic v2 validator
    @field_validator('q')
    @classmethod
    def query_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Search query cannot be empty')
        return v