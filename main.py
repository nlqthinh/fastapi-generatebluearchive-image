import services
import io
import base64
from io import BytesIO

from models import ImageRequest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Stable Diffusers API"}


@app.post("/api/v1/generate/")
async def generate_image(imgRequest: ImageRequest):
    image = await services.generate_image(imgRequest=imgRequest)

    # Convert image to memorystream to send to client
    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)

    # The API returns a PNG image, media type "image/png"
    return StreamingResponse(memory_stream, media_type="image/png")


@app.post("/api/v1/generatebase64/")
async def generate_base64_image(imgRequest: ImageRequest):
    image = await services.generate_image(imgRequest=imgRequest)

    # Convert image to base64 to send to client
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    # API returns a base64 image
    return {"image": img_str}