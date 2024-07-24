from fastapi import APIRouter, File, UploadFile
from datetime import datetime
import boto3
import uuid
from pydantic import BaseModel

router = APIRouter()

# Initialiser DynamoDB
dynamodb = boto3.client('dynamodb')
upload_table = dynamodb.Table('FileUpload')
s3_client = boto3.client('s3')
bucket_name = 's3bucket'

class FileMetadata(BaseModel):
    file_name: str
    description: str

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), description: str = None):
    file_id = str(uuid.uuid4())
    upload_time = datetime.now().isoformat()
    file_content = await file.read()
    file_size = len(file_content)

    s3_client.put_object(Bucket=bucket_name, Key=file_id, Body=file_content)

    upload_table.put_item(
        Item={            
            "file_id": {
                "S": file_id
            },
            "file_name": {
                "S": file.filename
            },
            "file_size": {
                "N": file_size
            },
            "description": {
                "S": description
            },
            "upload_date": {
                "S": upload_time
            },
            "deletion_date": {
                "S": ""
            }
        }
    )

    return {"file_id": file_id, "filename": file.filename}