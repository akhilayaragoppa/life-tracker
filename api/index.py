from main import app
from mangum import Mangum

# Vercel will call this
handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")

