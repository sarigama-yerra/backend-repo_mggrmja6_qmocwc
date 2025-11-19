import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Lead

app = FastAPI(title="Home Fixi API", description="Backend for Home Fixi service booking site", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Home Fixi Backend Running"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# Simple public content for services and areas
SERVICES = [
    {"slug": "deep-cleaning", "name": "Deep Cleaning", "category": "Cleaning"},
    {"slug": "commercial-cleaning", "name": "Commercial Cleaning", "category": "Cleaning"},
    {"slug": "kitchen-cleaning", "name": "Kitchen Cleaning", "category": "Cleaning"},
    {"slug": "cockroach-control", "name": "Cockroach Control", "category": "Pest Control"},
    {"slug": "bedbug-control", "name": "Bedbug Control", "category": "Pest Control"},
    {"slug": "mosquito-control", "name": "Mosquito Control", "category": "Pest Control"},
    {"slug": "termite-treatment", "name": "Termite Treatment", "category": "Pest Control"},
    {"slug": "rat-treatment", "name": "Rat Treatment", "category": "Pest Control"},
]

AREAS = ["Bangalore"]


@app.get("/api/services")
def list_services():
    return {"services": SERVICES}


@app.get("/api/areas")
def list_areas():
    return {"areas": AREAS}


# Lead intake endpoint
@app.post("/api/leads")
def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"success": True, "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional: list recent leads (for testing)
class LeadFilter(BaseModel):
    service_type: Optional[str] = None
    city: Optional[str] = None


@app.post("/api/leads/search")
def search_leads(filters: LeadFilter):
    filt = {}
    if filters.service_type:
        filt["service_type"] = filters.service_type
    if filters.city:
        filt["city"] = filters.city
    try:
        docs = get_documents("lead", filt, limit=50)
        # Convert ObjectId to string
        for d in docs:
            if isinstance(d.get("_id"), ObjectId):
                d["_id"] = str(d["_id"])
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
