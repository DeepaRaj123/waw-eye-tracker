# WaW – Web Dashboard

Read-only React dashboard for visualizing eye-blink metrics collected by the WaW desktop application.

This module is part of the **Wellness at Work Eye Tracker** MVP and focuses on privacy-safe, per-user analytics.

---

## Features

- 📊 Blink count trends (hourly / daily)
- 📈 Blink rate visualization
- ⏱ Session duration summaries
- 🔒 Read-only access (no data mutation)
- 👁️ No webcam, images, or raw video data

---

## Tech Stack

- React (Create React App)
- REST API integration (NestJS backend)
- Charting library (e.g., Recharts / Chart.js)

---

## Data Source

The dashboard fetches aggregated data from the backend:

- `GET /dashboard/:userId`

Only **successfully synced** blink events are displayed.

---

## Environment Variables

Create a `.env` file:

```env
REACT_APP_API_BASE_URL=http://localhost:3000
REACT_APP_API_KEY=demo-secret

Running Locally
cd web
npm install
npm start

Runs on:
http://localhost:3001
