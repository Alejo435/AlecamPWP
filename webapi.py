import flask
from flask import request, jsonify, render_template, Response
import sqlite3
import hashlib
import cv2
import numpy as np

web = flask.Flask(__name__, template_folder='Templates')
web.config["DEBUG"] = True
def gen():
    source = cv2.VideoCapture('vroom3.mp4')

    # applies 5 by 5 kernal window to image
    def edges(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        return edges

    # determines height of cropped area, gets required measuerments of the image of interst, and vreates an image that masks everything else
    def crop(img):
        h = img.shape[0]
        poly = np.array([[(50, h), (1400, h), (800, 500)]])
        maskera = np.zeros_like(img)
        cv2.fillPoly(maskera, poly, 255)
        m_img = cv2.bitwise_and(img, maskera)
        return m_img

    # getsother point from coresponding point, and specfies coodinates to mark slope and y intercept
    def points(img, linesp):
        try:
            slope, intercepts = linesp
        except TypeError:
            slope, intercepts = 0.001, 0
        y1 = img.shape[0]
        x1 = int((y1 - intercepts) / slope)
        y2 = int(y1 * (3 / 5))
        x2 = int((y2 - intercepts) / slope)
        if x1 <= 0:
            x1 = 100
        if x1 >= 100000:
            x1 = 1000
        if x2 <= 0:
            x2 = 100
        if x2 >= 1000000:
            x2 = 1000
        print(x2)
        return np.array([x1, y1, x2, y2])

    # Average of lines
    def midline(img, lines):
        leftpoints = []
        rightpoints = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    leftpoints.append((slope, intercept))
                else:
                    rightpoints.append((slope, intercept))
            leftpoints_average = np.average(leftpoints, axis=0)
            rightpoints_average = np.average(rightpoints, axis=0)
            lline = points(img, leftpoints_average)
            rline = points(img, rightpoints_average)
            return np.array([lline, rline])

    def displayintime(img, lines):
        output = np.zeros_like(img)
        if lines is not None:
            for x1, y1, x2, y2 in lines:
                cv2.line(output, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10)

        return output

    while  source.isOpened():
        v, frame = source.read()
        if v:
            # can = edges(frame)
            # ROI = crop(can)
            # lines = cv2.HoughLinesP(ROI, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
            # mid = midline(frame, lines)
            # output = displayintime(frame, mid)
            # midimg = cv2.addWeighted(frame, 0.8, output, 1, 1)


            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame]r]n' 
                   b'Content-Type: img/jpeg\r\n\r\n' + frame + b'\r\n')

def test():
    source = cv2.VideoCapture('vroom.mp4')
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    while True:
        if cv2.waitKey(1) == ord('q'):
            _, buffer = cv2.imencode('.mp4', edge)
            edge = buffer.tobytes()
            yield (b'--frame]r]n'
                b'Content-Type: img/jpeg\r\n\r\n' + edge + b'\r\n')

@web.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

#Determines get method
@web.route("/", methods = ['GET'])
def login():
   return render_template('login.html')

@web.route('/ui')
def index():
    # Getting the Video Stream on the website
    return render_template('index.html')



@web.route('/register', methods = ['GET','POST'])
def register():

    return render_template('register.html')

@web.errorhandler(404)
def page_not_found(e):
   return "<h1>404 Error</h1><p>Aw man :( No resources??.</p>", 404

if __name__ == '__main__':
    web.run(host="0.0.0.0")
