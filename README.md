# WaW — Eye Blink Detection System

A cross-platform prototype for real-time eye-blink tracking with an offline-first desktop client, a secure NestJS backend, and a read-only React dashboard. Focused on privacy-aware design and cloud-ready architecture.

---

## Table of contents

- [Architecture](#architecture)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Database schema](#database-schema)
- [Authentication & API security](#authentication--api-security)
- [Privacy & consent](#privacy--consent)
- [Offline-first sync behaviour](#offline-first-sync-behaviour)
- [Dashboard metrics](#dashboard-metrics)
- [Quick start](#quick-start)
- [Firestore rules (example)](#firestore-rules-example)
- [Roadmap](#roadmap)

---

## Architecture

Desktop App (PyQt6 + OpenCV/dlib)
→ POST blink events to /blinks/:userId  
NestJS Backend (protected endpoints)
→ SQLite local dev / Firestore in production  
React Web Dashboard (read-only)

---

## Features

- Real-time eye-blink detection using webcam + OpenCV/dlib
- Offline-first: local SQLite buffer with automatic sync
- Lightweight per-user login (email-based identifier) for user-level isolation
- API protected with an API key guard (dev) — replace with JWT/Firebase Auth in production
- Read-only web dashboard for per-user aggregated metrics
- Privacy-first: no video/images are uploaded; only anonymized blink events & timestamps

---

## Tech stack

- Desktop: PyQt6, OpenCV, dlib, SQLite  
- Backend: NestJS (TypeScript), SQLite (dev), Firestore (prod)  
- Web: React  
- Cloud: Firebase Firestore, Google Cloud Run (conceptual)

---

## Database schema

UserProfile (collection / table)
- id: string (auto)
- name: string
- email: string (used as userId)
- consent: boolean
- createdAt: timestamp

BlinkEvent (collection / table)
- id: string (auto)
- userId: string (FK → UserProfile)
- timestamp: timestamp
- blinkCount: number
- duration: number (ms)
- synced: boolean
- source: string (e.g., "desktop")

Relationship: One-to-many (UserProfile → BlinkEvent)

---

## Authentication & API security

Development guard: x-api-key header
- Example header:
  x-api-key: demo-secret

Protected endpoints (dev)
- POST /blinks/:userId — ingest blink events
- GET  /dashboard/:userId — fetch aggregated dashboard data

Note: Store secrets in a secret manager and migrate to JWT or Firebase Auth for production.

---

## Privacy & consent

- Explicit consent is requested at login and stored in UserProfile
- No images or raw video are stored or transmitted
- Only blink counts, timestamps, and coarse session metrics are sent
- Users can revoke consent or request data deletion
- No biometric templates or facial embeddings are generated or stored

---

## Offline-first sync behaviour

1. Desktop app writes blink events to local SQLite with synced = 0
2. App attempts to POST events to backend
3. On success, event is marked synced = 1
4. Failed syncs are retried on next connection
5. Dashboard shows only successfully synced data

---

## Dashboard metrics

- Total blinks (hourly / daily)
- Blink rate trends
- Session duration summaries
- Aggregated per-user insights (read-only)

---

## Quick start

1. Run backend (NestJS)
```bash
cd backend
npm install
npm run start:dev
# backend: http://localhost:3000
# env: API_KEY=demo-secret
```

2. Run desktop app (PyQt6)
```bash
cd desktop
pip install -r requirements.txt
python main.py
# env: BACKEND_URL=http://localhost:3000
# env: API_KEY=demo-secret
```

3. Run web dashboard (React)
```bash
cd web
npm install
npm start
# dashboard: http://localhost:3001
```

---

## Firestore rules (example)
```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /blinks/{blinkId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
    }
  }
}
```

---

## Roadmap / Next steps

- Integrate Firebase Auth (email/SSO)
- Replace API-key auth with JWT / role-based access
- Add rate limiting & request validation
- Add CI for linting, tests, and security checks
- Formal DPIA for eye-tracking data


