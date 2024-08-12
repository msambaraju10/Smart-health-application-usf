import os
from datetime import datetime

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


IMAGE_FILES = ['C:/Users/chint/PycharmProjects/FlaskTest/testingimage.png']
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    mask = np.zeros(image.shape[0:2], dtype=np.uint8)

    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(image)

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
      continue
    annotated_image = image.copy()
    for face_landmarks in results.multi_face_landmarks:
        # points = np.array([[[100, 350], [120, 400], [310, 350], [360, 200], [350, 20], [25, 120]]])
        # ln = [93, 137, 123, 50, 36, 49, 220, 45, 4, 275, 440, 344, 331, 358, 266, 280, 352,
        #         366, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 140, 150, 136,
        #         172, 56, 132, 93]

        # ln = [132, 177, 147, 187, 305, 36, 129, 102, 48, 219, 218, 237,
        #       44, 1, 274, 457, 438, 439, 294, 358, 266, 330, 280, 352,
        #       366, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
        #       176, 149, 150, 136, 172, 58]

        # ln = [93, 137, 123, 50, 101, 36, 129, 102, 48, 115, 220, 45, 4,
        #       275, 440, 344, 278, 331, 358, 266, 330, 280, 352,
        #       366, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
        #       176, 149, 150, 136, 172, 58, 132]

        ln = [93, 137, 123, 50, 101, 36, 129, 49, 131, 134, 51, 5, 261, 363, 360, 279, 358,
              266, 330, 280, 352, 366, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
              176, 149, 150, 136, 172, 58, 132]

        points = []
        # for l in face_landmarks:
        for k in ln:
            point = face_landmarks.landmark[k]
            shape = image.shape
            relative_x = int(point.x * shape[1])
            relative_y = int(point.y * shape[0])
            points.append([relative_x, relative_y])

        print(points)
        pts = np.asarray(points)

        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        # cv2.fillPoly(mask, pts, (255))

        res = cv2.bitwise_and(image, image, mask=mask)
        # rect = cv2.boundingRect(points)  # returns (x,y,w,h) of the rect
        # cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

        ## crate the white background of the same size of original image
        wbg = np.ones_like(image, np.uint8) * 255
        cv2.bitwise_not(wbg, wbg, mask=mask)
        # overlap the resulted cropped image on the white background
        dst = wbg + res

        now = datetime.now()
        p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
        # cv2.imwrite(p, dst)
        # cv2.imwrite(p, new_image)

        cv2.imshow('Original', image)
        cv2.imshow("Mask", mask)
        # cv2.imshow("Cropped", cropped)
        cv2.imshow("Samed Size Black Image", res)
        # cv2.imshow("Samed Size White Image", new_image)
        cv2.waitKey(0)




        # new_image = np.zeros(dst.shape, dst.dtype)
        # alpha = 1.5  # Simple contrast control
        # beta = 1.0  # Simple brightness control
        #
        # for y in range(dst.shape[0]):
        #     for x in range(dst.shape[1]):
        #         for c in range(dst.shape[2]):
        #             new_image[y, x, c] = np.clip(alpha * dst[y, x, c] + beta, 0, 255)
