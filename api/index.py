from mangum import Mangum
from main import app

# Mangum wraps FastAPI for serverless (AWS Lambda, Vercel, etc.)
handler = Mangum(app, lifespan="off")
