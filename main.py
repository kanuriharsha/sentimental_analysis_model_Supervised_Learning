import re
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Load model once at startup ──────────────────────────────
with open("best_model.pkl", "rb") as f:
    pkg = pickle.load(f)
model = pkg["model"]

# ── Text cleaner (same as training) ─────────────────────────
def clean_text(text: str) -> str:
    text = str(text).strip('"').strip("'")
    text = re.sub(r"[^a-zA-Z0-9\s!?.,']", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

# ── App ──────────────────────────────────────────────────────
app = FastAPI(
    title="Sentiment Analysis API",
    description="Predicts positive / negative / neutral sentiment for any text.",
    version="1.0.0",
)

# ── CORS: accept requests from ANY website ───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # all origins allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response schemas ───────────────────────────────
class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    scores: dict

# ── Routes ───────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Sentiment Analysis API is running 🚀",
        "usage": "POST /predict  with JSON body: { \"text\": \"your sentence here\" }",
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="'text' field cannot be empty.")

    cleaned = clean_text(req.text)
    sentiment = model.predict([cleaned])[0]
    probas    = model.predict_proba([cleaned])[0]
    classes   = list(model.classes_)
    scores    = {cls: round(float(p), 4) for cls, p in zip(classes, probas)}
    confidence = round(float(max(probas)), 4)

    return PredictResponse(
        text=req.text,
        sentiment=sentiment,
        confidence=confidence,
        scores=scores,
    )
