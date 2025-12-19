# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## GDPR & Privacy Considerations

This prototype was designed with GDPR principles in mind, even though it is not production-grade yet.[web:13][web:19]

- **Lawful basis & consent**  
  - The desktop app is intended to present a clear consent screen before any eye-tracking starts, explaining what is collected (blink counts, timestamps, coarse device performance stats) and why.  
  - A consent flag is stored per user profile; if consent is not given, no data is sent to the backend.

- **Data minimization & purpose limitation**  
  - Only the minimum data required for the “wellness at work” use case is processed: blink count, timestamps, CPU %, memory %, and a pseudonymous user ID.[web:7][web:10]  
  - No raw video frames, facial images, or full eye-tracking traces are stored by the backend; the eye tracker runs locally and emits only aggregate blink counts.

- **Rights of the data subject**  
  - The backend is structured so that it can support:  
    - Right of access: an endpoint to export all blink events for a user.  
    - Right to erasure: an endpoint to delete all data associated with a user ID.  
    - Right to rectification/objection: configuration to stop tracking and delete existing data.

- **Storage & retention**  
  - Local SQLite is intended as a short-lived buffer for offline use; data can be purged automatically after a defined retention period (e.g. 30 days) in a production system.  
  - Cloud storage would be on a managed, encrypted database (e.g. Postgres on RDS or Firestore) with strict access controls and audit logging.

- **Security controls (current & planned)**  
  ## API Security and Protected Endpoints

  The NestJS backend uses a simple API key–based mechanism to protect the core endpoints.[web:22][web:23][web:24]

  - A custom **ApiKeyGuard** checks every request for the header: 
  - API layer would enforce per-user access control so that users and districts only see their own data.  
  - In a full implementation, JWT-based auth, rate limiting, input validation, and secure secrets management (e.g. environment variables in the cloud environment) would be added.

## User Authentication

The desktop application implements a simple authentication flow:

- On startup, a PyQt6 **login dialog** prompts the user for an email address (and optional name).
- The entered email is used as the `userId` for the entire session, and is:
  - Stored alongside each blink event in the local SQLite database.
  - Sent in the URL path for all backend calls: `POST /blinks/:userId` and `GET /dashboard/:userId`.
- This keeps the UX lightweight while still modeling per‑user data separation and enabling user‑specific dashboards.

In a production system this dialog would be replaced or backed by a real identity provider (e.g. SSO/Firebase Auth) so the email is verified and associated with an account in the district’s IdP.[web:22][web:32]

### Offline-First Sync Behaviour

- Each blink event is written immediately to a local **SQLite** table with a `synced` flag defaulting to `0`.
- The app then attempts to send the event to the backend API; on success it marks the corresponding row as `synced = 1`.
- If the network call fails, the row remains unsynced and can be retried on the next successful connection, providing graceful handling of offline periods.[web:21][web:38]

### If given more time

- Integrate a managed identity provider (e.g. Firebase Auth or district SSO) to avoid handling passwords directly.[web:38]  
- Implement real storage and aggregation (RDS/Firestore) plus data export/erasure endpoints.  
- Conduct a DPIA focused on eye-tracking data and document it for district customers.  
- Add automated privacy and security tests in CI to guard against regressions.


