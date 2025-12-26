---
title: Deploy to Render
description: Steps to deploy the Flask application and PostgreSQL database to Render.
---
# Deploying to Render

Follow these steps to deploy your Student Management System to Render.

## 1. Create a PostgreSQL Database
The application requires a PostgreSQL database to store student data.

1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** and select **PostgreSQL**.
3. Name your database (e.g., `student-db`).
4. Select the **Region** closest to you (e.g., Singapore, Frankfurt).
5. Choose the **Free** instance type.
6. Click **Create Database**.
7. Once created, find the **Internal Database URL** in the connection details. **Copy this URL**, you will need it shortly.

## 2. Create a Web Service
Now, deploy the Flask application.

1. Go back to the [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub account and select your repository: `Student-Management`.
4. Configure the service:
   - **Name**: `student-management` (or any name you prefer).
   - **Region**: Same as your database.
   - **Branch**: `main`.
   - **Runtime**: `Python 3`.
   - **Build Command**: `pip install -r requirements.txt`.
   - **Start Command**: `gunicorn app:app`.
5. Scroll down to **Environment Variables** and add the following:
   - **Key**: `SQLALCHEMY_DATABASE_URI`
   - **Value**: Paste the **Internal Database URL** you copied earlier.
     *   *Note: If the URL starts with `postgres://`, change it to `postgresql://` explicitly if needed, but modern Flask-SQLAlchemy usually handles both.*
   - **Key**: `SECRET_KEY`
   - **Value**: Generate a random secure string (e.g., `s3cr3t_k3y_12345`).
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.9.18` (Recommended for compatibility).
6. Click **Create Web Service**.

## 3. Monitor Deployment
Render will start building your application. You can watch the logs in the "Events" or "Logs" tab.
- It will install dependencies from `requirements.txt`.
- It will run `gunicorn` to start the server.
- Once you see "Your service is live", click the URL at the top to access your app.
