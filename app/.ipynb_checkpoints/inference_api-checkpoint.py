from fastapi import FastAPI, UploadFile, File
from typing import List
from PIL import Image
import torch
from .model_utils import load_model, transform_image, class_names

app = FastAPI()
model, device = load_model()

@app.post("/predict")
async def predict(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        image = Image.open(file.file).convert("RGB")
        img_tensor = transform_image(image).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(img_tensor)
            pred = outputs.argmax(1).item()
        results.append({"filename": file.filename, "prediction": class_names[pred]})
    return {"results": results}