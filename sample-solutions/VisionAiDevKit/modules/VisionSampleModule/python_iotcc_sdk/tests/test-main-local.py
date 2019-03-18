# Copyright (c) 2018, The Linux Foundation. All rights reserved.
# Licensed under the BSD License 2.0 license. See LICENSE file in the project root for
# full license information.

import argparse
import sys
import time
import subprocess
import utility
import os
import iot
from iotcc.sdk.camera import CameraClient
import traceback
#import camera
#from camera import CameraClient
import numpy as np
from cv2 import cv2

def main(protocol=None):
    print("\nPython %s\n" % sys.version)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--pushmodel',help ='sets whether to push the model and required files to device or not', default=True)
    parser.add_argument('--ip', help='ip address of the camera', default=utility.getWlanIp())
    parser.add_argument('--username', help='username of the camera', default='admin')
    parser.add_argument('--password', help='password of the camera', default='admin')
    args = parser.parse_args()
    if args.pushmodel is not None:
        mypushmodel = args.pushmodel
        print("setting value from argu -p pushmodel to :: %s" % mypushmodel)
    ip_addr = args.ip
    username = args.username
    password = args.password

    #Please change this address to camer ip address can be found by using adb shell -> ifconfig
    ip_addr = '192.168.0.103'
    #hub_manager = iot.HubManager()
    utility.transferdlc()
    with CameraClient.connect(ip_address=ip_addr, username=username, password=password) as camera_client:
        #transferring model files to device
        #if mypushmodel == "True" :
        '''
        if mypushmodel.find("True") == -1 :
            print("Not transferring dlc  as per parameter passed")
        else :
            print("transferring dlc as per mypushmodel set in create option with -p %s passed" % mypushmodel)
            utility.transferdlc()
        '''
        
        
        print(camera_client.configure_preview(display_out=1))

        camera_client.toggle_preview(True)
        #time.sleep(5)
        rtsp_stream_addr = "rtsp://" + ip_addr + ":8900/live"
        print("RTSP address is ::" + rtsp_stream_addr)

        #hub_manager.iothub_client_sample_run(rtsp_stream_addr)


        camera_client.toggle_vam(True)

        camera_client.configure_overlay("inference")

        camera_client.toggle_overlay(True)
        try:
            with camera_client.get_inferences() as results:
                print_inferences(None,results)
        except KeyboardInterrupt:
            print("Stopping")
        try:
            while(True):
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping")

        #camera_client.toggle_overlay(False)

        camera_client.toggle_vam(False)

        camera_client.toggle_preview(False)


def print_inferences(hub_manager=None,results=None):
    print("")
   
    for result in results:
        if result is not None and result.objects is not None and len(result.objects):
            timestamp = result.timestamp
            #if timestamp:
                #print("timestamp={}".format(timestamp))
            #else:
                #print("timestamp= " + "None")
            for object in result.objects:
                id = object.id
                label = object.label
                confidence = object.confidence
                x = object.position.x
                y = object.position.y
                w = object.position.width
                h = object.position.height
                print("id={}".format(id))
                print("label={}".format(label))
                print("confidence={}".format(confidence))
                print("Position(x,y,w,h)=({},{},{},{})".format(x, y, w, h))
                print("")
                #hub_manager.SendMsgToCloud("I see " + str(label) + " with confidence :: " + str(confidence))
                time.sleep(1)
        else:
            print("No results")

if __name__ == '__main__':
    main()