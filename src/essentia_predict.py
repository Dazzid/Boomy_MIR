import os
import numpy as np
from essentia.standard import TensorflowPredictMusiCNN, MonoLoader
import json

# import models from models.py
from models import models

# Our models take audio streams at 16kHz
sr = 16000
patch_hop_size = 0  # No overlap for efficiency
batch_size = 256
model_type = "musicnn-msd-2"
frame_size = 512
hop_size = 256
patch_size = 187
nbands = 96


def analyse(path):
    # Instantiate a MonoLoader and run it in the same line
    audio = MonoLoader(filename=path, sampleRate=sr)()
    # out file is the path but instead of .mp3, it's .json
    out_file = path.replace('.mp3', '.json')

    results = []

    for model in models:
        model_name = model["name"]
        # print(model_name)

        modelFilename = f"./models/{model_name}-{model_type}.pb"
        activations = TensorflowPredictMusiCNN(
            graphFilename=modelFilename,
            patchHopSize=patch_hop_size,
            patchSize=patch_size,
            batchSize=batch_size
        )(audio)

        model_results = {"model_name": model_name, "activations": {}}

        for label, activation in zip(model["labels"], np.mean(activations, axis=0)):
            # activation_value = activation.round(2)
            # print(label, activation_value)
            model_results["activations"][label] = str(activation)

        results.append(model_results)
        # print('----')

    # Save the results to a JSON file
    with open(out_file, 'w') as json_file:
        json.dump(results, json_file, indent=2)

# load all files from 'wobinn_boomy_files.txt'
with open('/workspace/Boomy_MIR/wobinn_boomy_files.txt', 'r') as f:
    files = f.read().splitlines()

for file in files:
    analyse(file)