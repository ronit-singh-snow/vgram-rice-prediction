import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
train_dir = os.path.join(base_dir, 'data', 'train')
val_dir = os.path.join(base_dir, 'data', 'test')

# Image properties
img_height, img_width = 128, 128
batch_size = 32

# Data generator
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=(img_height, img_width),
                                               batch_size=batch_size,
                                               class_mode='categorical')

val_data = val_datagen.flow_from_directory(val_dir,
                                           target_size=(img_height, img_width),
                                           batch_size=batch_size,
                                           class_mode='categorical')

# CNN model
model = models.Sequential([
   layers.Conv2D(32, (3,3), activation='relu', input_shape=(img_height, img_width, 3)),
   layers.MaxPooling2D(2,2),
   layers.Conv2D(64, (3,3), activation='relu'),
   layers.MaxPooling2D(2,2),
   layers.Conv2D(128, (3,3), activation='relu'),
   layers.MaxPooling2D(2,2),
   layers.Flatten(),
   layers.Dense(128, activation='relu'),
   layers.Dropout(0.3),
   layers.Dense(train_data.num_classes, activation='softmax')
])

model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

# # Train the model
history = model.fit(train_data, validation_data=val_data, epochs=10)

# # Save model
model.save('model/rice_grain_classifier.keras')

# # Plot accuracy
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend()
plt.show()
