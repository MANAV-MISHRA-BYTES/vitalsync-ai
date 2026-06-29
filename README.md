<div align="center">

<!-- LOGO & TITLE -->
<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=40&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&width=700&height=80&lines=VitalSync+AI+%F0%9F%8F%A5;Healthcare+Bottleneck+Predictor;Powered+by+NVIDIA+RAPIDS+%2B+Gemini" alt="VitalSync AI"/>

<br/>

<!-- LIVE DEMO BADGE -->
<a href="https://vitalsync-ai-taupe.vercel.app/" target="_blank">
  <img src="https://img.shields.io/badge/%F0%9F%9A%80%20LIVE%20DEMO-vitalsync--ai--taupe.vercel.app-00D4FF?style=for-the-badge&labelColor=0a0f1e" alt="Live Demo"/>
</a>

<br/><br/>

<!-- TECH STACK BADGES -->
<img src="https://img.shields.io/badge/Vue.js-3.4-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white&labelColor=0a0f1e"/>
<img src="https://img.shields.io/badge/Flask-3.0-FF6B35?style=for-the-badge&logo=flask&logoColor=white&labelColor=0a0f1e"/>
<img src="https://img.shields.io/badge/NVIDIA_RAPIDS-cuDF-76B900?style=for-the-badge&logo=nvidia&logoColor=white&labelColor=0a0f1e"/>
<img src="https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white&labelColor=0a0f1e"/>

<br/>

<img src="https://img.shields.io/badge/Deployed_on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white"/>
<img src="https://img.shields.io/badge/Backend_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
<img src="https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"/>
<img src="https://img.shields.io/github/last-commit/MANAV-MISHRA-BYTES/vitalsync-ai?style=for-the-badge&color=8B5CF6&labelColor=0a0f1e"/>

<br/><br/>

> **Real-time hospital resource bottleneck prediction powered by GPU-accelerated analytics and AI-driven clinical insights.**

</div>

---

## ⚡ What is VitalSync AI?

**VitalSync AI** is a production-grade healthcare intelligence platform that simulates and analyzes **200,000+ patient admission records** in real time — detecting which hospital wards are approaching critical resource bottlenecks before they happen.

Built for speed. Built for scale. Built to save lives.

```
200,000 patient records  →  cuDF groupby in <100ms  →  Risk scores per region  →  Gemini AI insights
```

---

## 🎯 Live Demo

<div align="center">

| Service | URL | Status |
|:---:|:---:|:---:|
| 🌐 **Frontend** | [vitalsync-ai-taupe.vercel.app](https://vitalsync-ai-taupe.vercel.app/) | ![Vercel](https://img.shields.io/badge/live-00C851?style=flat-square) |
| ⚙️ **Backend API** | [vitalsync-ai-pvre.onrender.com](https://vitalsync-ai-pvre.onrender.com/api/risk-scores) | ![Render](https://img.shields.io/badge/live-00C851?style=flat-square) |
| 💻 **Repository** | [github.com/MANAV-MISHRA-BYTES/vitalsync-ai](https://github.com/MANAV-MISHRA-BYTES/vitalsync-ai) | ![GitHub](https://img.shields.io/badge/public-0a0f1e?style=flat-square) |

</div>

> 🛑 **Note:** Render's free tier may have a **cold start** of ~30–60 seconds after inactivity. Give it a moment on first load!

---

## ✨ Feature Highlights

<table>
<tr>
<td width="50%">

### 🏥 Bottleneck Risk Dashboard
- **15 hospital wards** analyzed in real time
- Dynamic **risk scoring engine** (0–100)
- Status tiers: `🔴 CRITICAL` `🟡 HIGH` `🔵 MODERATE` `🟢 LOW`
- Sortable, searchable, filterable data matrix
- Live KPI cards with animated fill bars

</td>
<td width="50%">

### 🤖 Gemini Clinical AI Chat
- Natural language queries over live risk data
- Context-aware responses with actual numbers
- One-click suggestion prompts
- Streamed responses from **Gemini 2.0 Flash**
- Full conversation history UI

</td>
</tr>
<tr>
<td>

### ⚡ GPU-Accelerated Data Engine
- **NVIDIA RAPIDS cuDF** for GPU-parallel groupby
- Graceful pandas fallback on CPU environments
- Pre-warmed cache — zero latency on subsequent calls
- Fixed-seed reproducible mock dataset generation

</td>
<td>

### 🎨 Premium UI/UX
- Glassmorphism dark-mode design
- Animated background orbs & grid
- Micro-animations on every interaction
- Fully responsive layout
- Accessible ARIA labels throughout

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Vue 3 SPA (Vercel CDN)                 │    │
│  │  ┌─────────────────┐  ┌──────────────────────────┐ │    │
│  │  │ Risk Score Table │  │  Gemini Chat Interface   │ │    │
│  │  └────────┬────────┘  └────────────┬─────────────┘ │    │
│  └───────────┼────────────────────────┼───────────────┘    │
└──────────────┼────────────────────────┼────────────────────┘
               │ GET /api/risk-scores   │ POST /api/ask-gemini
               ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│               Flask REST API (Render)                        │
│  ┌──────────────────────┐   ┌───────────────────────────┐   │
│  │   data_processor.py  │   │      Gemini API Client    │   │
│  │                      │   │                           │   │
│  │  numpy seed=42 data  │   │  gemini-2.0-flash model   │   │
│  │  ──────────────────  │   │  + risk data context      │   │
│  │  cuDF / pandas       │   │                           │   │
│  │  groupby + agg       │   └───────────┬───────────────┘   │
│  │  ──────────────────  │               │                   │
│  │  in-memory cache     │       Google Gemini API           │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧮 Risk Score Algorithm

Each ward's **Bottleneck Risk Score** (0–100) is computed as:

```python
risk_score = (
    (avg_symptom_severity / 10.0) * 30    # Severity weight:  30pts
  + avg_bed_occupancy_rate        * 35    # Occupancy weight: 35pts
  + (avg_wait_minutes / 120.0)    * 20    # Wait time weight: 20pts
  + (1 - avg_staff_ratio)         * 15    # Staff penalty:    15pts
).clip(0, 100)
```

| Score Range | Status | Action |
|:-----------:|:------:|:-------|
| 75 – 100 | 🔴 **CRITICAL** | Immediate intervention required |
| 55 – 74 | 🟡 **HIGH** | Escalate resource allocation |
| 35 – 54 | 🔵 **MODERATE** | Monitor closely |
| 0 – 34 | 🟢 **LOW** | Normal operations |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:---:|:---:|:---|
| **Frontend** | Vue 3 + Vite | Reactive SPA, component system |
| **Styling** | Vanilla CSS | Glassmorphism, animations, dark mode |
| **Backend** | Flask 3 + Gunicorn | REST API, WSGI production server |
| **Data Engine** | NVIDIA RAPIDS cuDF | GPU-accelerated DataFrame operations |
| **CPU Fallback** | pandas + NumPy | Graceful CPU processing when no GPU |
| **AI/LLM** | Google Gemini 2.0 Flash | Clinical NLP insights |
| **Frontend Deploy** | Vercel | Global CDN, auto-deploy on push |
| **Backend Deploy** | Render | Python web service, auto-deploy on push |
| **CI/CD** | GitHub Actions | Build + import validation on every PR |

</div>

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Gemini API Key → [Get one free](https://aistudio.google.com/app/apikey)

### 1. Clone the repo

```bash
git clone https://github.com/MANAV-MISHRA-BYTES/vitalsync-ai.git
cd vitalsync-ai
```

### 2. Backend setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Start the Flask API
python app.py
# → Running on http://localhost:5000
```

### 3. Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (proxies /api → localhost:5000)
npm run dev
# → Running on http://localhost:3000
```

### 4. Open the app

```
http://localhost:3000
```

---

## 🔌 API Reference

### `GET /api/risk-scores`

Returns processed bottleneck risk scores for all hospital regions.

```bash
curl https://vitalsync-ai-pvre.onrender.com/api/risk-scores
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "data": [
    {
      "region": "ICU-North",
      "bottleneck_risk_score": 45.77,
      "status": "MODERATE",
      "avg_severity": 2.86,
      "avg_occupancy": 65.4,
      "avg_wait": 44.8,
      "avg_staff_ratio": 0.544,
      "total_admissions": 13519
    }
  ]
}
```

---

### `POST /api/ask-gemini`

Queries Gemini AI with a natural language question, grounded in live risk data.

```bash
curl -X POST https://vitalsync-ai-pvre.onrender.com/api/ask-gemini \
  -H "Content-Type: application/json" \
  -d '{"query": "Which ward is at highest risk?"}'
```

**Response:**
```json
{
  "success": true,
  "query": "Which ward is at highest risk?",
  "insight": "Based on the current data, Pediatrics leads with a bottleneck risk score of 45.77 (MODERATE), driven by 65.4% bed occupancy and an average wait time of 44.8 minutes. While no ward has reached CRITICAL status, I recommend pre-emptive staffing reviews in ICU-North and Ward-Beta, which show similar risk profiles."
}
```

---

## 📁 Project Structure

```
vitalsync-ai/
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions — backend + frontend CI
│
├── backend/
│   ├── app.py                  # Flask app + API endpoints
│   ├── data_processor.py       # cuDF/pandas engine + risk score computation
│   ├── requirements.txt        # Python dependencies (incl. gunicorn)
│   ├── Procfile                # Render/Heroku process definition
│   ├── runtime.txt             # Python 3.11 pin
│   └── .env.example            # Environment variable template
│
├── frontend/
│   ├── src/
│   │   ├── App.vue             # Main SPA component (dashboard + chat)
│   │   ├── main.js             # Vue app entry point
│   │   └── style.css           # Global design system & CSS variables
│   ├── index.html              # HTML shell
│   ├── vite.config.js          # Vite config + API proxy for local dev
│   └── package.json
│
├── vercel.json                 # Vercel build configuration
├── .gitignore
└── README.md
```

---

## 🌍 Deployment

### Frontend → Vercel

| Setting | Value |
|---|---|
| Framework | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Env Variable | `VITE_API_BASE_URL=https://vitalsync-ai-pvre.onrender.com` |

### Backend → Render

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| Env Variable | `GEMINI_API_KEY=<your_key>` |

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

**Built with ❤️ by [MANAV-MISHRA-BYTES](https://github.com/MANAV-MISHRA-BYTES)**

<br/>

*"The best way to predict the future of healthcare is to engineer it."*

<br/>

⭐ **Star this repo if you found it useful!** ⭐

<br/>

<img src="https://img.shields.io/github/stars/MANAV-MISHRA-BYTES/vitalsync-ai?style=social"/>
<img src="https://img.shields.io/github/forks/MANAV-MISHRA-BYTES/vitalsync-ai?style=social"/>

</div>
