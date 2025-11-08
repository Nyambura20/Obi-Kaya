#!/bin/bash

set -e  # Exit on any error

echo "🚀 Starting SalesGenius AI Deployment to Google Cloud Run"
echo "=================================================="

# Check if .env file exists and load it FIRST
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your API keys before deploying."
        exit 1
    else
        echo "❌ Error: Neither .env nor .env.example found!"
        exit 1
    fi
fi

# Load environment variables from .env file
echo "📄 Loading configuration from .env file..."
export $(grep -v '^#' .env | xargs)

# Configuration (now reading from loaded env vars)
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="salesgenius-ai-agent"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Validate project ID
if [ "$PROJECT_ID" = "your-gcp-project-id" ]; then
    echo "❌ Error: GCP_PROJECT_ID not set in .env file"
    echo "Please edit .env and set GCP_PROJECT_ID to your actual Google Cloud project ID"
    exit 1
fi

echo "📋 Using project: ${PROJECT_ID}"
echo "📍 Using region: ${REGION}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed."
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ Error: Not authenticated with gcloud."
    echo "Run: gcloud auth login"
    exit 1
fi

# Set the project
echo "� Setting gcloud to use project: ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    aiplatform.googleapis.com

# Validate API key
if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your_google_api_key_here" ]; then
    echo "❌ Error: GOOGLE_API_KEY is not set in .env file"
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    exit 1
fi

# Build the container image
echo "🏗️  Building container image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    --set-env-vars APP_NAME="${APP_NAME}" \
    --set-env-vars ENVIRONMENT=production \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo ""
echo "=================================================="
echo "✅ Deployment completed successfully!"
echo "=================================================="
echo "🌐 Service URL: ${SERVICE_URL}"
echo ""
echo "📝 Next steps:"
echo "1. Visit ${SERVICE_URL} to access your agent"
echo "2. Test the agent with sample data from ./sample_data/"
echo "3. Monitor logs: gcloud run services logs read ${SERVICE_NAME} --region ${REGION}"
echo ""
echo "💰 Estimated costs: ~$0.10-$0.50 per day (with minimal usage)"
echo "=================================================="
