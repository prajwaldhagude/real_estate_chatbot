# Deployment Guide for Render

This guide will help you deploy the Real Estate Chatbot to Render.

## Prerequisites

1. A GitHub account with this repository pushed
2. A Render account (sign up at https://render.com)

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables in Render Dashboard**
   After the service is created, go to the service settings and add:
   - `ALLOWED_HOSTS`: Set this to your Render service URL (e.g., `your-app-name.onrender.com`)
   - `SECRET_KEY`: Will be auto-generated, but you can set a custom one if needed

### Option 2: Manual Setup

1. **Create a new Web Service**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the Service**
   - **Name**: real-estate-chatbot (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free (or choose a paid plan)

3. **Set Environment Variables**
   - `SECRET_KEY`: Generate a secure random key (you can use: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render URL (e.g., `your-app-name.onrender.com`)
   - `PYTHON_VERSION`: `3.11.9` (optional, but recommended)

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## Important Notes

- **Database**: The app currently uses SQLite. For production, consider upgrading to PostgreSQL (Render offers free PostgreSQL databases).
- **Static Files**: Static files are automatically collected during build.
- **Migrations**: Database migrations run automatically during build.
- **First Deployment**: The first deployment may take 5-10 minutes.

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version matches `runtime.txt`

2. **Application Crashes**
   - Check logs in Render dashboard
   - Verify environment variables are set correctly
   - Ensure `ALLOWED_HOSTS` includes your Render URL

3. **Static Files Not Loading**
   - Verify `STATIC_ROOT` is set correctly in settings.py
   - Check that `collectstatic` runs during build

4. **Database Errors**
   - Ensure migrations run successfully
   - Check that the database file path is correct

## Post-Deployment

After successful deployment:
1. Your app will be available at `https://your-app-name.onrender.com`
2. Check the logs to ensure everything is running correctly
3. Test your API endpoints

## Updating Your Deployment

Simply push changes to your GitHub repository, and Render will automatically redeploy your application.

