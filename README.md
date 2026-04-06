# Sentiment Analysis API

A REST API that predicts **positive / negative / neutral** sentiment for any text.  
Built with FastAPI + scikit-learn. CORS is open to all origins.

---

## 📁 Files

```
sentiment_api/
├── main.py            ← FastAPI app
├── best_model.pkl     ← Trained ML model
├── requirements.txt   ← Python dependencies
├── render.yaml        ← Render auto-deploy config
└── README.md
```

---

## 🚀 Deploy on Render (step-by-step)

1. **Push this folder to a GitHub repo**
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Go to [render.com](https://render.com)** → Sign in → Click **"New +"** → **"Web Service"**

3. **Connect your GitHub repo**

4. Fill in these settings:
   | Field | Value |
   |-------|-------|
   | Environment | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Plan | Free |

5. Click **"Create Web Service"** — Render will build and deploy automatically.

---

## 📡 API Usage

### `GET /`
Health check — returns API info.

### `GET /health`
Returns `{"status": "ok"}`

### `POST /predict`

**Request:**
```json
{
  "text": "I love this product, it works amazingly!"
}
```

**Response:**
```json
{
  "text": "I love this product, it works amazingly!",
  "sentiment": "positive",
  "confidence": 0.9542,
  "scores": {
    "negative": 0.0231,
    "neutral": 0.0227,
    "positive": 0.9542
  }
}
```

### Example with curl:
```bash
curl -X POST https://YOUR-APP.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible!"}'
```

### Example with JavaScript (fetch):
```javascript
const res = await fetch("https://YOUR-APP.onrender.com/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "I feel great today!" })
});
const data = await res.json();
console.log(data.sentiment); // "positive"
```

---

## 🌐 CORS
The API accepts requests from **any website** (`Access-Control-Allow-Origin: *`).  
No configuration needed on your frontend.
