# YOLO object detection using a webcam
# Exact same demo as the read from disk, but instead of disk a webcam is used.
# import the necessary packages
import numpy as np
import imutils
import time
import cv2
import os
import PySimpleGUI as sg
import pandas as pd
import firebase_login

i_vid = r'videos\003_x264.mp4'
o_vid = r'output\car_chase_01_out.mp4'
y_path = r'yolo-coco'
sg.ChangeLookAndFeel('Reddit')
layout = 	[
		[sg.Text('Test vidéo pour YOLOv4 - NAC', size=(28,1), font=('Helvetica',18),text_color='#1c86ee' ,justification='left'),\
             sg.Image(r'images\nac-logo.png',key = "-WEATHER-IMG-",size=(100, 50))],
		[sg.Text('Chemin de la vidéo'), sg.In(i_vid,size=(40,1), key='input'), sg.FileBrowse()],
		[sg.Text('Chemin de la Yolo'), sg.In(y_path,size=(40,1), key='yolo'), sg.FolderBrowse()],
		[sg.Text('Confiance'), sg.Slider(range=(0,1),orientation='h', resolution=.1, default_value=.5, size=(15,15), key='confidence')],
		[sg.Text('Seuil'), sg.Slider(range=(0,1), orientation='h', resolution=.1, default_value=.3, size=(15,15), key='threshold')],
		[sg.Text(' '*8), sg.Checkbox('Utiliser la webcam', key='_WEBCAM_')],
		[sg.Button('Connecxion avec votre compte'),sg.OK(), sg.Cancel()]
			]

win = sg.Window('Test vidéo pour YOLOv4 - NAC',
				default_element_size=(21,1),
				text_justification='left',
				auto_size_text=False).Layout(layout)
event, values = win.Read()
if event is None or event =='Cancel':
	exit()
if event == 'Connecxion avec votre compte':
 	firebase_login.firebaseLogin()
use_webcam = values['_WEBCAM_']
args = values

win.Close()


# imgbytes = cv2.imencode('.png', image)[1].tobytes()  # ditto
gui_confidence = args["confidence"]
gui_threshold = args["threshold"]
# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n") #打开标签

# initialize a list of colors to represent each possible class label 
# 每个对象配备了不一样的颜色，以便在图片中标记时便于区分。
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "custom-yolov4-detector_final.weights"])
configPath = os.path.sep.join([args["yolo"], "custom-yolov4-detector.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

# loop over frames from the video file stream
win_started = False
loopTimes = 1; loopInterval = 50;
if use_webcam:
	cap = cv2.VideoCapture(0)

while True:
	# read the next frame from the file or webcam
	if use_webcam:
		grabbed, frame = cap.read()
	else:
		grabbed, frame = vs.read()
		# 分辨率-宽度
		zone_width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))/4
		# 分辨率-高度
		zone_height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))/2

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs 循环提取每个输出层
	for output in layerOutputs:
		# loop over each of the detections 循环提取每个框
		for detection in output:
			# extract the class ID and confidence (i.e., probability) 提取当前目标的类 ID 和置信度
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
            # 通过确保检测概率大于最小概率来过滤弱预测
			if confidence > gui_confidence:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
                # 将边界框坐标相对于图像的大小进行缩放，YOLO 返回的是边界框的中心(x, y)坐标，
                # 后面是边界框的宽度和高度
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
                # 转换出边框左上角坐标
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
                # 更新边界框坐标、置信度和类 id 的列表
                # boxes：对象的边界框
                # confidences ：YOLO 分配给对象的置信度值，较低的置信度值表示该对象可能不是网络认为的对象。
                # classIDs：检测到的对象的类标签
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes 非最大值抑制，确定唯一边框
    # bboxes：一组边框
    # scores：一组对应的置信度
    # score_threshold：置信度的阈值
    # nms_threshold：非最大抑制的阈值
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, gui_confidence, gui_threshold)
	targetPosition = []
	targetDetailNumber = []
	zone_info = []
    
# 	print('idxs.flatten() 的长度为 %d，内容为 %s' %(len(idxs.flatten()),idxs.flatten()))
# 	print(boxes)
# 	print(confidences)

	# ensure at least one detection exists 确定每个对象至少有一个框存在
	if len(idxs) > 0:
		# loop over the indexes we are keeping 循环画出保存的边框
		for i in idxs.flatten():
			# extract the bounding box coordinates 提取坐标和宽度
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
            
			targetDetailNumber.append(classIDs[i])
			targetPosition.append([x+w/2,y+h/2]) # 每一帧的目标数量和位置

			# [[793.0, 517.0], [796.5, 423.0], [841.5, 367.0], [889.5, 499.5], 
            # [1001.5, 584.0], [254.5, 480.5], [204.0, 420.5], [693.5, 343.5], 
            # [73.0, 504.0], [123.5, 368.5], [752.0, 280.0], [1017.0, 508.5], 
            # [1232.0, 683.0], [14.5, 473.5], [398.0, 86.0], [1225.0, 374.5], 
            # [1097.0, 139.5], [1098.0, 600.5], [61.5, 172.5], [723.0, 140.0], 
            # [863.0, 174.0]]
			print(targetPosition)
            # [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]
			print(targetDetailNumber)

			# draw a bounding box rectangle and label on the frame 画出边框和标签
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    # 组合 targetPositionObject 的数据，以便传送 Start #
	targetPositionObject = dict() # 构建对象
	targetDetailNumberUnique = list(set(targetDetailNumber)) # 数组去重
	targetDetailUnique = []
	for i in range(len(targetDetailNumberUnique)): # 通过序列索引迭代
		targetDetailUnique.append(LABELS[targetDetailNumberUnique[i]])
		targetTemp = [] # 这是个临时的数组，里面将存有每种目标的所有坐标值。
		for j in range(len(targetDetailNumber)):
			if targetDetailNumber[j] == targetDetailNumberUnique[i]:
				targetTemp.append(targetPosition[j])
        # 更新构建的对象 targetPositionObject
		targetPositionObject.update({targetDetailUnique[i]:targetTemp})
	print(targetPositionObject)
    # 组合 targetPositionObject 的数据，以便传送 End #

	imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto

	if not win_started: # if win_started is not None
		win_started = True
		sg.SetOptions(text_justification='Center') 
        
        # 左边栏
		left_col =  [
			[sg.Text('Observer votre NAC par Yolov4 et OpenCV-Python', size=(50,1), justification='center')],
			[sg.Image(data=imgbytes, key='_IMAGE_')],
			[sg.Text('Confiance',size=(8, 1), font=('Helvetica', 10)),
			sg.Slider(range=(0, 1), orientation='h', resolution=.1, default_value=.5, size=(20, 15), key='confidence'),
			sg.Text('Seuil',size=(8, 1), font=('Helvetica', 10)),
			 sg.Slider(range=(0, 1), orientation='h', resolution=.1, default_value=.3, size=(20, 15), key='threshold')],
			[sg.Exit()]
		]

        # 右边栏
		right_col = [[sg.Text('Les positions des cibles',size=(20, 2), font=('Helvetica', 15), justification='center'),
			sg.Text(size=(20, 2), font=('Helvetica', 15), justification='center', key='_POSITION_')],
			[sg.Text('Le nombre de cible total',size=(20, 2), font=('Helvetica', 15), justification='center'),
			sg.Text(size=(20, 2), font=('Helvetica', 15), justification='center', key='_TARGETNUM_')],
			[sg.Text('Maintenant, il y a',size=(15, 2), font=('Helvetica', 12), justification='left'),
			sg.Text(size=(2, 2), font=('Helvetica', 15), justification='center', key='_TARGET_DETAIL_NUM_'),
			sg.Text(size=(10, 2), font=('Helvetica', 15), justification='center', key='_TARGET_NAME_'),
			sg.Text("dans l'écran.",size=(15, 2), font=('Helvetica', 12), justification='left')
            ],
            [sg.Text('LoopTimes',size=(15, 2), font=('Helvetica', 12), justification='left'),
			sg.Text(size=(2, 2), font=('Helvetica', 15), justification='center', key='_LOOP_TIMES_')
            ],
            [sg.Output(size=(60,10))]
            ]
        
        
		layout = [
			[sg.Column(left_col, element_justification='c'), sg.VSeperator(),
			sg.Column(right_col, element_justification='c')]
		]
        
		win = sg.Window('YOLO Output',
						default_element_size=(14, 1),
						text_justification='left',
						auto_size_text=False).Layout(layout).Finalize()
		image_elem = win.FindElement('_IMAGE_')
		position_elem = win.FindElement('_POSITION_')
		number_elem = win.FindElement('_TARGETNUM_')
		targetDetailNumber_elem = win.FindElement('_TARGET_DETAIL_NUM_')
		targetName_elem = win.FindElement('_TARGET_NAME_')
		loopTimes_elem = win.FindElement('_LOOP_TIMES_')
	else:
		image_elem.Update(data=imgbytes)
		position_elem.Update(targetPosition)
		number_elem.Update(len(targetPosition))
		if len(targetDetailNumber) == 0:
		    targetDetailNumber_elem.Update(0)
		else:
		    targetDetailNumber_elem.Update(pd.value_counts(targetDetailNumber)[0])
		targetName_elem.Update(LABELS[0])
		loopTimes_elem.Update(loopTimes)
    
	for coordinate in targetPosition:
		if coordinate[0] <= zone_width:
			if coordinate[1] <= zone_height:
				zone_info.append('Zone 1A')
			else:
				zone_info.append('Zone 1B')
		elif  coordinate[0] <= zone_width*2 and coordinate[0] > zone_height:    
			if coordinate[1] <= zone_height:
				zone_info.append('Zone 2A')
			else:
				zone_info.append('Zone 2B')
		elif  coordinate[0] <= zone_width*3 and coordinate[0] > zone_height*2:    
			if coordinate[1] <= zone_height:
				zone_info.append('Zone 3A')
			else:
				zone_info.append('Zone 3B')
		elif  coordinate[0] <= zone_width*4 and coordinate[0] > zone_height*3:    
			if coordinate[1] <= zone_height:
				zone_info.append('Zone 4A')
			else:
				zone_info.append('Zone 4B')

	event, values = win.Read(timeout=0)
	print(zone_info)
    
	if event is None or event == 'Exit':
		break
	gui_confidence = values['confidence']
	gui_threshold = values['threshold']
    
	# 每隔 time.sleep(1)，识别一次
	##time.sleep(1)
	# 每隔 loopInterval，向 firebase 保存数据
	loopTimes=loopTimes+1

	if loopTimes % loopInterval == 0:
		firebase_login.firebaseUploadData(targetPositionObject)
        
win.Close()

# release the file pointers
print("[INFO] cleaning up...")
writer.release() if writer is not None else None
vs.release()