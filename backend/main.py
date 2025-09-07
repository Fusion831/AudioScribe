from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from PIL import Image
import io
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="AudioScribe API",
    description = "an API for transcribing audio files for the visually impaired."
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/describe-image")
async def describe_image(file: UploadFile = File(...)):
    """
    This endpoint receives an image file and returns a description of the image.
    """
    logger.info("Received image for description.")
    if file.content_type is not None and not file.content_type.startswith("image/"):
        logger.warning(f"Invalid file type uploaded: {file.content_type}")
        # Return a 400 Bad Request error if it's not an image.
        raise HTTPException(status_code=400, detail=f"File provided is not an image. Type was: {file.content_type}")
    try:
        image_data = await file.read()
        logger.info(f"Image size: {len(image_data)} bytes")
        image = Image.open(io.BytesIO(image_data))
        logger.info(f"Image format: {image.format}, size: {image.size}, mode: {image.mode}")

        #TODO: AI model to integrate here
        final_description = "A placeholder description of the image."
        logger.info(f"Generated description: {final_description}")
        return {"description": final_description}
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the image.")


@app.get("/")
def read_root():
    return {"message": "Welcome to the AudioScribe API. Use the /api/describe-image endpoint to describe images."}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)

        




