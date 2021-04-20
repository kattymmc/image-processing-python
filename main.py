# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from opencvscanner import scan
import uvicorn
from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from server.procesar import read_image

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
async def bienvenido():
    return "Bienvenido al sistema para procesar imagenes"

@app.post('/api/procesar')
async def predict_image(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "JPG")
    if not extension:
        return "Image must be jpg or png format!"
    
    file_location = f"opencvscanner/images/{file.filename}"

    print(file_location)
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    finally:
        procesamientoImagenes(f"opencvscanner/images/{file.filename}")

    return f'{file.filename} guardado en {file_location}'

@app.get('/api/retornar')
async def return_image(file: str):
    file_path = f"opencvscanner/output/{file}"

    return FileResponse(file_path)

def procesamientoImagenes(path_image: str):
    im_file_path = path_image
    #print(im_file_path)
    
    scanner = scan.DocScanner(False)

    if im_file_path:
        scanner.scan(im_file_path)

if __name__ == "__main__":
    #procesamientoImagenes("opencvscanner/images/chart.jpg")
    uvicorn.run(app, port=8080, host='0.0.0.0')
