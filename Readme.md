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

## Télécharger des données sur Firebase

Seule le bibliothèque pyrebase4 suivante peut fonctionner : https://github.com/nhorvath/Pyrebase4.
```py
pip install pyrebase4
```