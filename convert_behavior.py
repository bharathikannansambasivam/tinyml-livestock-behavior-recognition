# convert_behavior.py

import tensorflow as tf

print("Loading model...")

model = tf.keras.models.load_model("behavior_model.h5")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

# TinyML optimizations (smaller + faster)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

with open("behavior_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ behavior_model.tflite created")
