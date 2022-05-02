import threading
import cv2
import datetime, time
import boto3
import os

from PyQt5.QtWidgets import QMainWindow
from QtApp.QtUI.MainUI import Ui_MainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from CCTV.CcTv import CcTv
from kafka import KafkaProducer 
from json import dumps 


class MainWindow(QMainWindow):
    def initialize(self, mainForm: Ui_MainWindow):
        self.mainForm = mainForm
        self.producer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8')) 
        self.setWindowIcon(QIcon("icon.png"))
        self.cnt = 0
        self.cctv_1 = None
        self.cctv_2 = None
        self.cctv_3 = None
        self.cctv_4 = None
        self.s3 = self.s3_connection()
        self.CCTV_start()
        self.thread_CCTV = Worker(target = self.thread_CCTV_run)
        self.thread_CCTV.start()
    
    def s3_connection(self):
        try:
            s3 = boto3.client(
                service_name="s3",
                region_name="ap-northeast-2", # 자신이 설정한 bucket region
                aws_access_key_id="AKIAZM2UBXT27P5Z2PGL",
                aws_secret_access_key="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",
            )
        except Exception as e:
            print(e)

        else:
            print("s3 bucket connected!")
            return s3

    def s3_put_object(self,bucket, filepath, access_key):
        """
        s3 bucket에 지정 파일 업로드
        :param s3: 연결된 s3 객체(boto3 client)
        :param bucket: 버킷명
        :param filepath: 파일 위치
        :param access_key: 저장 파일명
        :return: 성공 시 True, 실패 시 False 반환
        """
        try:
            self.s3.upload_file(
                Filename=filepath,
                Bucket=bucket,
                Key=access_key,
                ExtraArgs={"ContentType": "video/avi", "ACL": "public-read"},
            )
            print("upload video to aws s3!")
        except Exception as e:
            return False
        return True

    def s3_get_image_url(self, filename):
        """
        s3 : 연결된 s3 객체(boto3 client)
        filename : s3에 저장된 파일 명
        """
        location = self.s3.get_bucket_location(Bucket="ssafit-01-bucket")["LocationConstraint"]
        return f"https://ssafit-01-bucket.s3.{location}.amazonaws.com/{filename}.avi"

    def thread_CCTV_run(self):
        Frame_1, Frame_2, Frame3, Frame4 = None, None, None, None
        if self.cctv_1 != None and self.cctv_1.grab():
            _, Frame_1 = self.cctv_1.retrieve()
            if Frame_1 is not None:
                width = (int)((self.mainForm.centralwidget.width()-227)/2)-10
                height = (int)((self.mainForm.centralwidget.height()-20)/2)-10
                pixmap = QtGui.QPixmap(
                    self.convert_image_to_QImage(
                        self.resize_image(Frame_1, width,height)))
                self.mainForm.cctv_1.setPixmap(pixmap)
                self.mainForm.cctv_1.update()
                #AI
                    # 상황이 발생하면.
                    # 형이 전처리한 이미지.

                if self.cnt == 0 :  # if 상황이 발생하면
                    self.cnt = 1
                    t = threading.Thread(target= self.record) # video 녹음 쓰레드
                    t.start()
                    
    # 형이 하나하나 전처리한 프레임을 리스트에 넣어서 주는 방식으로 하시는지
    # cctv(전처리) -> record

    def record(self):
        cctv_1 = CcTv.rtsp()
        trigger = True
        flag = True
        start = time.time()
        while trigger == True :
            Frame_1, Frame_2, Frame3, Frame4 = None, None, None, None
            if cctv_1 != None and cctv_1.grab():
                _, Frame_1 = cctv_1.retrieve()

                if flag == True :
                    print("video record start!")
                    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    path = "C:/Users/dlrjs/Desktop/S06P31E202/AI/" + str(now) + ".avi"
                    video = cv2.VideoWriter("C:/Users/dlrjs/Desktop/S06P31E202/AI/" + str(now) + ".avi", fourcc, 20.0, (Frame_1.shape[1], Frame_1.shape[0]))
                    flag = False
                
                video.write(Frame_1)
                if (time.time() - start) > 5 :
                    trigger = False
                    video.release()
                    print("video record end!")
                    print(self.s3_put_object("ssafit-01-bucket", path, str(now)+ ".avi"))
                    if os.path.isfile(path):
                        os.remove(path)
                    # connect to web
                    url = self.s3_get_image_url(str(now))
                    data = {'str' : url}
                    self.producer.send('kafka-demo2', value=data)
                    
    def CCTV_start(self):
        self.cctv_1 = CcTv.rtsp()

    def convert_image_to_QImage(self, img):

        height, width, channel = img.shape
        bytesPerLine = width * channel
        format = QtGui.QImage.Format_RGB888

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return QtGui.QImage(img.data, width, height, bytesPerLine, format)

    def resize_image(self, img, width, height):
        return cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)
class Worker(QThread):
    def __init__(self, target):
        assert callable(target)
        super().__init__()
        self.func = target
        self.isWorking = True

    def run(self):
        while self.isWorking:
            self.func()
            self.sleep(0)