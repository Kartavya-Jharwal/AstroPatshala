from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class NumerologyRequest(BaseModel):
    """Request model for numerology calculation"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name for calculation")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", v.strip()):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip().title()
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v):
        try:
            date_obj = datetime.strptime(v, '%Y-%m-%d')
            # Check if date is reasonable (not in future, not too far in past)
            now = datetime.now()
            if date_obj > now:
                raise ValueError('Birth date cannot be in the future')
            if date_obj.year < 1900:
                raise ValueError('Birth date cannot be before 1900')
            return v
        except ValueError as e:
            if "Birth date cannot" in str(e):
                raise e
            raise ValueError('Invalid date format. Use YYYY-MM-DD format')

class CompatibilityRequest(BaseModel):
    """Request model for compatibility calculation"""
    person1_name: str = Field(..., min_length=1, max_length=100)
    person1_birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    person2_name: str = Field(..., min_length=1, max_length=100)
    person2_birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    
    @field_validator('person1_name', 'person2_name')
    @classmethod
    def validate_names(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if not re.match(r"^[a-zA-Z\s\-']+$", v.strip()):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip().title()
    
    @field_validator('person1_birth_date', 'person2_birth_date')
    @classmethod
    def validate_birth_dates(cls, v):
        try:
            date_obj = datetime.strptime(v, '%Y-%m-%d')
            now = datetime.now()
            if date_obj > now:
                raise ValueError('Birth date cannot be in the future')
            if date_obj.year < 1900:
                raise ValueError('Birth date cannot be before 1900')
            return v
        except ValueError as e:
            if "Birth date cannot" in str(e):
                raise e
            raise ValueError('Invalid date format. Use YYYY-MM-DD format')

class QuickCalculationRequest(BaseModel):
    """Request model for quick number calculations"""
    text: str = Field(..., min_length=1, max_length=200, description="Text to calculate numerology value")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()
