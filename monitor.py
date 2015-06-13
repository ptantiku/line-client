#!/usr/bin/env python

import sys
sys.path.append('./LINE')
from line import LineClient, LineGroup, LineContact
from PIL import Image
import datetime
import pynotify
import traceback

try:
    #Login with username & password
    client = LineClient('myemail@example.com', 'mypassword', is_mac=False, com_name='myPC')

    # login with authToken (get from MitM)
    # client = LineClient(authToken='myauthtoken', is_mac=False, com_name='myPC')
    print client
except:
    print "Login failed"
    exit(1)

# print profile
profile = client.profile
print profile

# print contacts
#print client.contacts

imageID=0
pynotify.init("markup")

# print recent messages
while True:
    try:
        for op in client.longPoll():
            sender = op[0]
            receiver = op[1]
            message = op[2]
            time = op[3]
            strtime = datetime.datetime.fromtimestamp(int(time)/1000.0).strftime('%Y-%m-%d %H:%M:%S')
            if(message.contentType==0):
                print "[m] %s[ %s -> %s ]:TEXT: %s" % (strtime, sender, receiver, message.text)
                pynotify.Notification("Line", 
                    "[m] %s[ %s -> %s ]:TEXT: %s" % (strtime, sender, receiver, message.text)).show()
            elif(message.contentType==7):
                stickerVersion = int(message.contentMetadata['STKVER'])
                stickerPackageID = int(message.contentMetadata['STKPKGID'])
                stickerID = int(message.contentMetadata['STKID'])
                # generate sticker url
                # ref: http://altrepo.eu/git/line-protocol.git/blob/HEAD:/line-protocol.md
                stickerVersionStr = "%d/%d/%d" % (stickerVersion/1000000, stickerVersion/1000, stickerVersion%1000)
                stickerURL = "http://dl.stickershop.line.naver.jp/products/%s/%d/PC/stickers/%d.png" % (stickerVersionStr, stickerPackageID, stickerID)
                print "[m] %s[ %s -> %s ]:STICKER: %s" % (strtime, sender.name, receiver.name, stickerURL)
                pynotify.Notification("Line", 
                    "[m] %s[ %s -> %s ]:STICKER: <a href='%s'>View Sticker</a>" % (strtime, sender.name, receiver.name, stickerURL)).show()

            elif(message.contentType==1 or message.contentType==2):
                imageID += 1
                filename = '/tmp/line%d.jpg' % imageID
                open(filename, 'w').write(message.contentPreview)
                print "[m] %s[ %s -> %s ]:IMAGE: %s" % (strtime, sender.name, receiver.name, filename)
                #Image.open(filename).show()
                pynotify.Notification("Line", "[m] %s[ %s -> %s ]:IMAGE: <a href='file://%s'>View Image</a>" % (strtime, sender.name, receiver.name, filename)).show()
            else: #
                print "[m] %s[ %s -> %s ]:OTHER: %s" % (strtime, sender.name, receiver.name, message)
                pynotify.Notification("Line", "[m] %s[ %s -> %s ]:OTHER: %s" % (strtime, sender.name, receiver.name, message)).show()

    #        msg = message.text
    #        receiver.sendMessage("[%s] %s" % (sender.name, msg))
    except:
        traceback.print_exc()
