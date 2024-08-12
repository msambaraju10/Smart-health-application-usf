import datetime
import math
import os
import time
from threading import Thread
from datetime import datetime
#import MySQLdb
from flask import Flask
from pymongo import MongoClient
# import bcrypt
import certifi 
import cv2
import mediapipe as mp
import numpy as np

from flask import Flask, render_template, Response, request, jsonify

# from flask_mysqldb import MySQL

global capture, rec_frame, grey, switch, neg, face, rec, out, shoulder, patientid, r, nc, ul, cursor, ang, ang1, filename_of_gridimage
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0
shoulder = 0
r = 0
nc = 0
ul = 0
ang = 0
ang1 = 0
filename_of_gridimage = 0

global cropfilename_left, cropfilename_right
cropfilename_left = ''
cropfilename_right = ''
# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
mp_pose = mp.solutions.pose

# instantiate flask app
app = Flask(__name__, template_folder='./templates')

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'smarthealth'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(app)

client = MongoClient("mongodb+srv://krishnajupally2000:Krishnausffall22@cluster0.qe1etdt.mongodb.net/?retryWrites=true&w=majority", tlsCAFile= certifi.where())
db = client['mycollection']
print(db)
collection = db['mycollection']
print(collection)

#doc = {"patientid":"2345","password":"2345","ifApprovedByAdmin": True ,"age":"30","images":""}

#result = collection.insert_one(doc)

#print(result.inserted_id)
#db = MySQLdb.connect(host="localhost", user="root", passwd="AMTSD_Password_2022", db="smarthealth")
#cursor = db.cursor()


camera = cv2.VideoCapture(0)


def record(out):
    global rec_frame
    while rec:
        time.sleep(0.05)
        out.write(rec_frame)


@app.route('/adminlogin', methods=['POST', 'GET'])
def adminLogin():
    app.logger.info('testing info log')
    # recaptchaResponse = request.form['g-recaptcha-response']
    userid = request.form['userid']
    password = request.form['password']
    # success = captchaValidation.validateCaptcha(recaptchaResponse)
    # if success:
    user = collection.find_one({"patientid": userid})
    if user and user["password"] == password:
        print("Login successful")
        patients = []
        data = collection.find({"patientid": userid,"ifApprovedByAdmin":True})
        print(data)
        for row in data:
            patient = {"patientId": row[0], "ifApprovedByAdmin": row[1]}
            patients.append(patient)
        return render_template('adminhome.html', patients=patients)    

    else:
        print("invalid patientid")
        return render_template('adminlogin.html')
        
    #query_string = "SELECT `userId`, `password` FROM user WHERE userId = %s and password = %s"
    #cursor.execute(query_string, (userid, password))
    #data = cursor.fetchall()
    #d = data[0][1]
    # for i in data:
    #     d = i['password'];
    # print(data);
    #cursor.close()
    #if data:
        #query_string = "SELECT `patientId`, `ifApprovedByAdmin` FROM patients;"
        #cursor.execute(query_string, ())
        #data = cursor.fetchall()
        #cursor.close()
    #patients = []
    #for row in data:
        #patient = {"patientId": row[0], "ifApprovedByAdmin": row[1]}
        #patients.append(patient)

        #print("login success")
        #return render_template('adminhome.html', patients=patients)
    #else:
        #print("invalid username")
        #return render_template('adminlogin.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('patientlogin.html', datetime=str(datetime.now()), patientid=patientid,
                           flag="default")


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('patientHomePage.html', datetime=str(datetime.now()), patientid=patientid,
                           flag="default")


@app.route('/login', methods=['POST', 'GET'])
def patientLogin():
    # recaptchaResponse = request.form['recaptchaResponse']
    global patientid
    patientid = request.form['patientid']
    password = request.form['password']
    # success = captchaValidation.validateCaptcha(recaptchaResponse)
    # if success:
    users = collection.find()
    for user in users:
        print(user)
    user = collection.find_one({"patientid": patientid})

    if user and user["password"] == password:
        print("Login successful")
        patients = []
        data = collection.find({"patientid": patientid,"ifApprovedByAdmin":True})
        print(data)
        camera = cv2.VideoCapture(0)
        global r, nc, ul
        r = 0
        nc = 0
        ul = 0
        return render_template('patientHomePage.html', datetime=str(datetime.now()), patientid=patientid,
                               flag="default")

    else:
        print("invalid patientid")
        return render_template('patientlogin.html', datetime=str(datetime.now()))
    # cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''', (name, age))
    #query_string = "SELECT `patientId`, `password` FROM patients WHERE patientId = %s and password = %s"
    #cursor.execute(query_string, (patientid, password))
    #data = cursor.fetchall()
    #camera = cv2.VideoCapture(0)
    #if data:
       # print("login success")
        #global r, nc, ul
        #r = 0
        #nc = 0
        #ul = 0
        #return render_template('patientHomePage.html', datetime=str(datetime.now()), patientid=patientid,
                            #   flag="default")
    #else:
        #print("invalid username")
        #return render_template('patientlogin.html', datetime=str(datetime.now()))


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def get_pts1(shape, x1, y1):
    relative_x1 = int(x1 * shape[1])
    relative_y1 = int(y1 * shape[0])

    pt1_x = relative_x1
    pt1_y = 0
    pt2_x = relative_x1
    pt2_y = shape[0]
    pt3_x = shape[1]
    pt3_y = 0
    pt4_x = shape[1]
    pt4_y = shape[0]

    points = []
    points.append([pt2_x, pt2_y])
    points.append([relative_x1, relative_y1])
    points.append([pt1_x, pt1_y])
    points.append([pt3_x, pt3_y])
    points.append([pt4_x, pt4_y])

    pts = np.array(points, np.int32)
    return pts


def get_pts2(shape, x1, y1):
    relative_x1 = int(x1 * shape[1])
    relative_y1 = int(y1 * shape[0])

    pt1_x = relative_x1
    pt1_y = 0
    pt2_x = relative_x1
    pt2_y = shape[0]
    pt3_x = 0
    pt3_y = 0
    pt4_x = 0
    pt4_y = shape[1]

    points1 = []
    points1.append([pt2_x, pt2_y])
    points1.append([relative_x1, relative_y1])
    points1.append([pt1_x, pt1_y])
    points1.append([pt3_x, pt3_y])
    points1.append([pt4_x, pt4_y])

    pts1 = np.array(points1, np.int32)
    return pts1


def saveCroppedPicture_Pose(image1, x1, y1, x2, y2):
    shape = image1.shape
    now = datetime.now()
    timeValue = now.strftime('%Y-%m-%dT%H-%M-%S') + ('-%02d' % (now.microsecond / 10000))
    filename = patientid + 'fullimage' + timeValue + '.png'
    path = 'shots'
    p = os.path.join(path, filename)
    mask = np.zeros(image1.shape[0:2], dtype=np.uint8)
    mask2 = np.zeros(image1.shape[0:2], dtype=np.uint8)
    cv2.imwrite(p, image1)

    pts1 = get_pts1(shape, x1, y1)
    cv2.drawContours(mask, [pts1], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res1 = cv2.bitwise_and(image1, image1, mask=mask)
    wbg1 = np.ones_like(image1, np.uint8) * 255
    cv2.bitwise_not(wbg1, wbg1, mask=mask)
    dst1 = wbg1 + res1

    cropfilename_left = patientid + '_cropped_leftshoulder' + timeValue + '.png'
    p1 = os.path.join(path, cropfilename_left)
    cv2.imwrite(p1, dst1)

    # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])

    pts2 = get_pts2(shape, x2, y2)
    cv2.drawContours(mask2, [pts2], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res2 = cv2.bitwise_and(image1, image1, mask=mask2)
    wbg2 = np.ones_like(image1, np.uint8) * 255
    cv2.bitwise_not(wbg2, wbg2, mask=mask2)
    dst2 = wbg2 + res2

    cropfilename_right = patientid + '_cropped_rightshoulder' + timeValue + '.png'
    p2 = os.path.join(path, cropfilename_right)
    cv2.imwrite(p2, dst2)
    return cropfilename_right, cropfilename_left


def writeAngle(descr1, angle1, cropfilename_right, descr2, angle2, cropfilename_left):
    global patientid
    collection_one = db['shoulderData']
    try:
        #query_string = "INSERT INTO `shouldermeasure`(`patientID`,`description1`, `angle1`, `cropfilename_right` ,`description2`, `angle2`, `cropfilename_left` ,`createdOn`) VALUES(%s, %s,%s,%s, %s,%s, %s, current_timestamp())"
        # print(query_string)
        document = {"patientid":patientid,"description1":descr1,"angle1":angle1,"cropfilename_right":cropfilename_right,"description2":descr2,"angle2":angle2,"cropfilename_left":cropfilename_left,"createdOn":time.time()}
        result = collection_one.insert_one(document)
        print(result.inserted_id)
        print(cropfilename_right)
        print(cropfilename_left)
        #cursor.execute(query_string, (patientid, descr1, angle1, cropfilename_right, descr2, angle2, cropfilename_left))
        #db.commit()
        # print("#######")
    except Exception as e:
        print(str(e))


def detect_pose(frame):
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            success, frame = camera.read()
            # ret, frame = camera.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # image = cv2.flip(image, 1)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shoulder1 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow1 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                # wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                #          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                hip1 = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                hip2 = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                # Calculate angle
                # angle = calculate_angle(shoulder, elbow, wrist)
                angle = calculate_angle(hip1, shoulder1, elbow1)

                angle1 = calculate_angle(hip2, shoulder2, elbow2)

                global ang, ang1
                ang = angle
                ang1 = angle1
                image1 = image
                global cropfilename_right, cropfilename_left
                cropfilename_right, cropfilename_left = saveCroppedPicture_Pose(image1, shoulder1[0], shoulder1[1],
                                                                                shoulder2[0], shoulder2[1])

                writeAngle('angle between left arm and left hip', angle, cropfilename_right,
                           'angle between right arm and right hip',
                           angle1, cropfilename_left)

                # cv2.putText(image, str(angle),
                #             tuple(np.multiply(shoulder1, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #             )
                #
                # cv2.putText(image, str(angle1),
                #             tuple(np.multiply(shoulder2, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #             )

                # Visualize angle
                # cv2.putText(image, str(angle),
                #             tuple(np.multiply(elbow, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #             )
                #
                # cv2.putText(image, str(angle),
                #             tuple(np.multiply(shoulder1, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #             )
                # cv2.putText(image, str(angle1),
                #             tuple(np.multiply(shoulder2, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #             )

                image1 = image
                # saveCroppedPicture_Pose(image1, shoulder1[0], shoulder1[1])

                # cv2.imshow("Blur Picutre", blur)  # Display Blur image


            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # cv2.waitKey(1)
            # cv2.destroyAllWindows()
            # camera.release()

            # cv2.imshow('Mediapipe Feed', image)
            return image


def writeDistanceRatio(nc, ul, r, mm, filename, x1, y1, r1):
    # print(" in write ")
    global patientid, filename_of_gridimage
    try:
        collection_two = db['mouthData']
        document = {"patientID":patientid,"nosechin":nc,"nosechin_actual":y1,"upperlowerlip":ul,"upperlowerlip_actual":x1,"distanceRatio":r,"distanceRatio_actual":r1,"valueOfEachSquareInMM" : mm,"filename_of_cropped_image":filename,"filename_of_gridimage":filename_of_gridimage,"craetedOn":time.time()} 
        result = collection_two.insert_one(document)
        print(result.inserted_id)
    # print()
    #query_string = "INSERT INTO `mouthmeasure` (`patiendID`,`nosechin`,`nosechin_actual`, `upperlowerlip`,`upperlowerlip_actual`," \
     #              "`distanceRatio`,`distanceRatio_actual`,`valueOfEachSquareInMM`,`filename_of_cropped_image`, `filename_of_gridimage`," \
      #             " `createdOn`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, current_timestamp())"
    #cursor.execute(query_string, (patientid, nc, y1, ul, x1, r, r1, mm, filename, filename_of_gridimage))
    #db.commit()
    except Exception as e:
        print(str(e))

def saveFile(dst, filename):
    path = 'shots'
    p = os.path.join(path, filename)
    # now = datetime.now()
    # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
    cv2.imwrite(p, dst)


def draw_grid(img1):
    color = (255, 0, 0)
    thickness = 1
    img = img1
    rows = int(img.shape[0] / 10)
    cols = int(img.shape[1] / 10)
    h, w, _ = img.shape
    # rows, cols = grid_shape

    dy = 10
    dx = 10

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w - dx, num=cols - 1):
        x = int(round(x))
        cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h - dy, num=rows - 1):
        y = int(round(y))
        cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

    # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
    path = 'shots'
    now = datetime.now()
    timeValue = now.strftime('%Y-%m-%dT%H-%M-%S') + ('-%02d' % (now.microsecond / 10000))
    filename = patientid + '_' + timeValue + '.png'
    p = os.path.join(path, filename)
    global filename_of_gridimage
    filename_of_gridimage = filename
    # cv2.imwrite(p, img)
    cv2.imwrite(p, img1)


def detect_face(frame):
    global mp_face_mesh
    with mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        dist = []

        while camera.isOpened():
            success, image = camera.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            # image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # now = datetime.now()
            # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
            # cv2.imwrite(p, frame)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_clone = image.copy()
            # image_clone = cv2.flip(image_clone, 1)
            image_clone = cv2.cvtColor(image_clone, cv2.COLOR_RGB2BGR)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            shape = image.shape
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    f1 = face_landmarks.landmark[94]
                    f2 = face_landmarks.landmark[0]
                    f3 = face_landmarks.landmark[17]
                    f4 = face_landmarks.landmark[152]

                    y = math.sqrt((f1.x - f4.x) ** 2 + (f1.y - f4.y) ** 2)
                    x = math.sqrt((f2.x - f3.x) ** 2 + (f2.y - f3.y) ** 2)
                    global r
                    r = x / y

                    relative_f1x = int(f1.x * shape[1])
                    relative_f1y = int(f1.y * shape[0])
                    relative_f2x = int(f2.x * shape[1])
                    relative_f2y = int(f2.y * shape[0])
                    relative_f3x = int(f3.x * shape[1])
                    relative_f3y = int(f3.y * shape[0])
                    relative_f4x = int(f4.x * shape[1])
                    relative_f4y = int(f4.y * shape[0])

                    y1 = math.sqrt((relative_f1x - relative_f4x) ** 2 + (relative_f1y - relative_f4y) ** 2)
                    x1 = math.sqrt((relative_f2x - relative_f3x) ** 2 + (relative_f2y - relative_f3y) ** 2)

                    r1 = x1 / y1

                    global nc, ul
                    nc = y
                    ul = x

                    dpi = 141
                    mm = (10 * 25.4) / dpi;

                    mask = np.zeros(image.shape[0:2], dtype=np.uint8)

                    ln = [93, 137, 123, 98, 205, 36, 129, 102, 48, 219, 218, 237,
                          44, 1, 274, 457, 438, 439, 294, 358, 266, 330, 280, 352,
                          366, 323]

                    points = []

                    # for l in face_landmarks:
                    for k in ln:
                        point = face_landmarks.landmark[k]
                        shape = image.shape
                        relative_x = int(point.x * shape[1])
                        relative_y = int(point.y * shape[0])
                        points.append([relative_x, relative_y])

                    pt1_x = shape[1]
                    pt1_y = face_landmarks.landmark[323].y * shape[0]

                    chin_point = face_landmarks.landmark[152]

                    pt2_x = shape[1]
                    pt2_y = int(chin_point.y * shape[0])

                    chin_x = int(chin_point.x * shape[1])
                    chin_y = int(chin_point.y * shape[0])

                    pt3_x = 0
                    pt3_y = chin_y

                    pt4_x = 0
                    pt4_y = face_landmarks.landmark[93].y * shape[0]

                    print(face_landmarks.landmark[323].x * shape[1], face_landmarks.landmark[323].y * shape[0])
                    print(pt1_x, pt1_y)
                    print(pt2_x, pt2_y)
                    print(chin_x, chin_y)
                    print(pt3_x, pt3_y)
                    print(pt4_x, pt4_y)

                    points.append([pt1_x, pt1_y])
                    points.append([pt2_x, pt2_y])
                    points.append([chin_x, chin_y])
                    points.append([pt3_x, pt3_y])
                    points.append([pt4_x, pt4_y])

                    # print(points)
                    pts = np.asarray(points)

                    cv2.drawContours(mask, np.int32([pts]), -1, (255, 255, 255), -1, cv2.LINE_AA)

                    res = cv2.bitwise_and(image, image, mask=mask)
                    wbg = np.ones_like(image, np.uint8) * 255
                    cv2.bitwise_not(wbg, wbg, mask=mask)
                    dst = wbg + res

                    now = datetime.now()
                    timeValue = now.strftime('%Y-%m-%dT%H-%M-%S') + ('-%02d' % (now.microsecond / 10000))
                    filename = patientid + '_cropped_' + timeValue + '.png'
                    saveFile(dst, filename)

                    # print("r : ", r)
                    writeDistanceRatio(nc, ul, r, mm, filename, x1, y1, r1)
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)

            # blur = cv2.GaussianBlur(image, (23, 23), 0)
            # cv2.imshow("Blur Picutre", blur)  # Display Blur image
            # cv2.imshow('MediaPipe FaceMesh', image)

            # img_src = cv2.imread('image.png')

            # ****************       # draw_grid(image_clone)

            path = 'shots'
            now = datetime.now()
            timeValue = now.strftime('%Y-%m-%dT%H-%M-%S') + ('-%02d' % (now.microsecond / 10000))
            filename = patientid + '_' + timeValue + '.png'
            p = os.path.join(path, filename)
            global filename_of_gridimage
            filename_of_gridimage = filename
            cv2.imwrite(p, image_clone)

            cv2.waitKey(1)
            cv2.destroyAllWindows()
            camera.release()

            return image
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break


@app.route('/getdata', methods=['GET'])
def getDistanceRatio():
    return jsonify(r, nc, ul, ang, ang1)


def gen_frames():  # generate frame by frame from camera
    global out, capture
    while True:
        success, frame = camera.read()
        if success:
            if face:
                frame = detect_face(frame)
                # now = datetime.now()
                # p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
                # cv2.imwrite(p, frame)
            if shoulder:
                frame = detect_pose(frame)
            # if grey:
            #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # if neg:
            #     frame = cv2.bitwise_not(frame)
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)

            # if rec:
            #     rec_frame = frame
            #     frame = cv2.putText(cv2.flip(frame, 1), "Recording...", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
            #                         (0, 0, 255), 4)
            #     frame = cv2.flip(frame, 1)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('patientlogin.html')


@app.route('/admin')
def admin():
    return render_template('adminlogin.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    flag_value = ''
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
        elif request.form.get('grey') == 'Grey':
            global grey
            grey = not grey
        elif request.form.get('neg') == 'Negative':
            global neg
            neg = not neg
        elif request.form.get('face') == 'Start/Stop':
            global face
            face = not face
            flag_value = 'mouth'
            if face:
                time.sleep(4)
            else:
                global r, nc, ul, ang
                r = 0,
                nc = 0,
                ul = 0,

        elif request.form.get('shoulder') == 'Start/Stop':
            global shoulder
            shoulder = not shoulder
            flag_value = 'shoulder'
            if shoulder:
                time.sleep(4)
            else:
                global ang, ang1
                ang = 0,
                ang1 = 0,
        # elif request.form.get('start') == 'Start':
        #     camera = cv2.VideoCapture(0)
        #     video_feed()

        # elif request.form.get('stop') == 'Stop':
        #     if switch == 1:
        #         switch = 0
        #         camera.release()
        #         cv2.destroyAllWindows()
        #     else:
        #     camera = cv2.VideoCapture(0)
        #         switch = 1
        elif request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec = not rec
            if rec:
                now = datetime.datetime.now()
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":", '')), fourcc, 20.0, (640, 480))
                # Start new thread for recording the video
                thread = Thread(target=record, args=[out, ])
                thread.start()
            elif rec is False:
                out.release()
        return render_template('patientHomePage.html', datetime=str(datetime.now()), patientid=patientid,
                               flag=flag_value)
    elif request.method == 'GET':
        return render_template('patientHomePage.html', datetime=str(datetime.now()), patientid=patientid)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
