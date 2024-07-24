# main.py
from fastapi import FastAPI, File, UploadFile
import boto3
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import io

load_dotenv()

app = FastAPI()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Nom du bucket
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        file_obj = io.BytesIO()
        s3_client.download_fileobj(BUCKET_NAME, filename, file_obj)
        file_obj.seek(0)
        return StreamingResponse(file_obj, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ping")
async def ping():
    return "pong"
