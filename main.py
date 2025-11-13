import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Message, Project

app = FastAPI(title="Demon Slayer Video Editor Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Demon Slayer Portfolio API is running"}

@app.get("/api/projects", response_model=List[Project])
def list_projects():
    # Static showcase data for now (videos hosted externally)
    return [
        Project(
            id="1",
            title="Hinokami Chronicles AMV",
            description="High-energy cuts synced to drum and bass with fiery color grading.",
            tags=["AMV", "Action", "D&B"],
            video_url="https://player.vimeo.com/video/76979871?h=8272103f6e",
            thumbnail="https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1200&auto=format&fit=crop"
        ),
        Project(
            id="2",
            title="Breath of Thunder Montage",
            description="Whip pan transitions and lightning VFX with hit-markers.",
            tags=["Montage", "VFX", "Transitions"],
            video_url="https://player.vimeo.com/video/357274789",
            thumbnail="https://images.unsplash.com/photo-1504805572947-34fad45aed93?q=80&w=1200&auto=format&fit=crop"
        ),
        Project(
            id="3",
            title="Calm Before the Storm Edit",
            description="Cinematic pacing, ambience build-up, subtle film grain.",
            tags=["Cinematic", "Color Grade"],
            video_url="https://player.vimeo.com/video/90509568",
            thumbnail="https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1200&auto=format&fit=crop"
        ),
    ]

@app.post("/api/contact")
def submit_contact(payload: Message):
    try:
        # Persist contact messages to database
        inserted_id = create_document("message", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        from database import db
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
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
