# NAC-python-GUI

## Chemin du dossier

```
├─.gitattributes
├─.gitignore
├─images
├─Readme.md
├─videos
│  └─002.mp4
├─yolo-coco
│  ├─coco.names
│  ├─custom-yolov4-detector.cfg
│  ├─custom-yolov4-detector_final.weights
│  ├─yolov4-tiny.cfg
│  ├─yolov4-tiny.weights
│  └─yolov4.cfg
├─yolo_video_with_webcam.py
```

Le fichier `custom-yolov4-detector_final.weights` (plus de 250 Mo) et les fichiers vidéos sont trop gros et ne sont donc pas inclus.



## Suivre des cibles par yolov4-deepsort

[theAIGuysCode/yolov4-deepsort: Object tracking implemented with YOLOv4, DeepSort, and TensorFlow. (github.com)](https://github.com/theAIGuysCode/yolov4-deepsort)

### Conda (Recommended)

```
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov4-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov4-gpu
```

### Downloading  YOLOv4 trained Weights

### Running the Tracker with YOLOv4

To implement the object tracking using YOLOv4, first we convert the .weights into the corresponding TensorFlow model which will be saved to a checkpoints folder. Then all we need to do is run the object_tracker.py script to run our object tracker with YOLOv4, DeepSort and TensorFlow.

```
# Convert darknet weights to tensorflow model
python save_model.py --model yolov4 

# Run yolov4 deep sort object tracker on video
python object_tracker.py --video ./data/video/test.mp4 --output ./outputs/demo.avi --model yolov4

# Run yolov4 deep sort object tracker on webcam (set video flag to 0)
python object_tracker.py --video 0 --output ./outputs/webcam.avi --model yolov4
```

YOLOv4-Tiny

```
# save yolov4-tiny model
python save_model.py --weights ./data/yolov4-tiny.weights --output ./checkpoints/yolov4-tiny-416 --model yolov4 --tiny

# Run yolov4-tiny object tracker
python object_tracker.py --weights ./checkpoints/yolov4-tiny-416 --model yolov4 --video ./data/video/test.mp4 --output ./outputs/tiny.avi --tiny
```

