# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import numpy as np
# import sys
# import os

# # Load model
# model = tf.keras.models.load_model("model/rice_grain_classifier.keras")

# # Load image
# base_dir = os.path.dirname(os.path.abspath(__file__))
# img_path = os.path.join(base_dir, "data", "test", "rice_jeera_battis", 'IMG-20250829-WA0003.jpg')

# img = image.load_img(img_path, target_size=(128, 128))
# img_array = image.img_to_array(img) / 255.0

# img_array = np.expand_dims(img_array, axis=0)

# # Get the classes
# train_dir = os.path.join(base_dir, 'data', 'train')
# train_datagen = ImageDataGenerator(rescale=1./255)

# train_data = train_datagen.flow_from_directory(train_dir,
#                                                target_size=(128, 128),
#                                                batch_size=32,
#                                                class_mode='categorical')
# class_names = list(train_data.class_indices.keys())
# print(class_names)

# # Predict
# predictions = model.predict(img_array)
# print(predictions, np.argmax(predictions))
# predicted_class = class_names[np.argmax(predictions)]
# print(f"Predicted class: {predicted_class}")



from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
import io
import os

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST"]
    allow_headers=["*"],
)

# Load the model
model = tf.keras.models.load_model("model/rice_grain_classifier.keras")

def preprocess(img: Image.Image):
    img = img.resize((128, 128))   # resize to your input size
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0) / 255.0
    return arr
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # # Load image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # img_path = os.path.join(base_dir, "data", "test", "rice_jeera_battis", 'IMG-20250829-WA0003.jpg')

    # img = image.load_img(img_path, target_size=(128, 128))
    # img_array = image.img_to_array(img) / 255.0

    # Preprocess the image
    # img_array = img_array / 255.0

    # Add a batch dimension
    # img_array = np.expand_dims(img_array, axis=0)

    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Preprocess & predict
    img_array = preprocess(img)

    # Make a prediction
    prediction = model.predict(img_array)
    print(prediction, np.argmax(prediction))

    # Get the classes
    train_dir = os.path.join(base_dir, 'data', 'train')
    train_datagen = ImageDataGenerator(rescale=1./255)

    train_data = train_datagen.flow_from_directory(train_dir,
                                                target_size=(128, 128),
                                                batch_size=32,
                                                class_mode='categorical')
    class_names = list(train_data.class_indices.keys())
    print(class_names)

    predicted_class = class_names[np.argmax(prediction)]
   
    return JSONResponse(content={"prediction": predicted_class}, status_code=200)