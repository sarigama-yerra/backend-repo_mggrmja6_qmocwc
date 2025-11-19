"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Lead schema for service-call requests
class Lead(BaseModel):
    """
    Leads collection schema
    Collection name: "lead"
    """
    name: str = Field(..., min_length=2, max_length=100, description="Customer full name")
    phone: str = Field(..., min_length=8, max_length=20, description="Contact phone number")
    email: Optional[EmailStr] = Field(None, description="Optional email address")
    city: str = Field(default="Bangalore", description="City")
    address: Optional[str] = Field(None, max_length=300, description="Service address")
    service_type: Literal[
        "Deep Cleaning",
        "Commercial Cleaning",
        "Kitchen Cleaning",
        "Cockroach Control",
        "Bedbug Control",
        "Mosquito Control",
        "Termite Treatment",
        "Rat Treatment",
    ] = Field(..., description="Selected service type")
    preferred_date: Optional[str] = Field(None, description="Preferred date (string)")
    preferred_time: Optional[str] = Field(None, description="Preferred time window")
    message: Optional[str] = Field(None, max_length=500, description="Additional notes")
