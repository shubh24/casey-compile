from __future__ import division
import cv2
import sys, os
from pytube import YouTube
import upload_video

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.CaseyBot.urls

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def cluster(data, maxgap):
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][0]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

def detect_faces(frames):
    selected_frames = []
    counter = 0
    for img in frames:
        if counter%frames_count == 0:
            sys.stdout.flush()
            sys.stdout.write('\r')
            sys.stdout.write(str(int(counter/frames_count)) + " seconds done...")
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            if len(faces) > 0:
                face_percentage = 0
                for f in faces:
                    width = f[2]
                    height = f[3]
                    face_percentage += (width*height)/(len(img)*len(img[0]))*100
                if face_percentage > 6:
                    selected_frames.append(counter/frames_count)
        counter += 1
    sys.stdout.write('\n')  
    return selected_frames

def compile(groups, clip):

    clips = [clip.subclip(g[0], g[-1]) for g in groups]

    return concatenate_videoclips([c for c in clips])


def doIt(vlog_url):
        
    try:    
        y = YouTube(vlog_url)
    except:
        print "oops"
        return 

    title = y.title.replace(" ","-")
    y.set_filename(title)

    matches = db.find({'title':title})
    if matches.count() > 0:
	for i in matches:
	    if 'compiled_url' in i:
		return_url = i['compiled_url']
     		return return_url
    else:
    	db.insert({"title":title})

    if (('%s.mp4'%(title)) not in os.listdir('.')):
        y.get('mp4','360p').download('.')
            
    if '%s_compile.avi'%(title) not in os.listdir("."):

        clip = VideoFileClip('%s.mp4'%(title))
	opencv_clip = cv2.VideoCapture("%s.mp4"%title)
	global frames_count
	frames_count  = int(round(opencv_clip.get(cv2.cv.CV_CAP_PROP_FPS))) 
	print frames_count
        frames = clip.iter_frames()
        selected_frames = detect_faces(frames)

        groups = cluster(selected_frames, maxgap = 10)

        final_clip = compile(groups, clip)

        final_clip.write_videofile('%s_compile.avi'%(title), codec='libx264', fps = frames_count)

    os.system('python upload_video.py --file="%s" --title="%s" --description="A compilation of the close-ups from Casey\'s vlog - %s" --category="22" --keywords="vlog, compilation, compile, casey, neistat, caseybot" --privacyStatus="public"'%('%s_compile.avi'%title, title, title))

    compiled_url = db.find({'title':title})[0]
    return compiled_url["compiled_url"]

if __name__ == '__main__':
        
    #doIt("https://www.youtube.com/watch?v=yGtza5cGgK0")
    print doIt("https://www.youtube.com/watch?v=hM1CNRq2byU")
