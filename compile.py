from __future__ import division
#from moviepy.editor import *
import cv2
import sys, os
from pytube import YouTube


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
frames_count = 24
selected_frames = []

def cluster(data, maxgap):
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups

	
def detect_faces(img, counter):
	# counter = 0
	# for img in frames:
		# if counter%frames_count == 0:
	# sys.stdout.flush()
	# sys.stdout.write('\r')
	# sys.stdout.write(str(int(counter/frames_count)) + " seconds done...")
	faces = face_cascade.detectMultiScale(img, 1.3, 5)
	if len(faces) > 0:
		face_percentage = 0
		for f in faces:
			width = f[2]
			height = f[3]
			face_percentage += (width*height)/(len(img)*len(img[0]))*100
		if face_percentage > 15:
			selected_frames.append(counter)
	# counter += 1
	sys.stdout.write('\n')	
	return selected_frames

def compile(groups, clip):

	# clips = [clip.subclip(g[0], g[-1]) for g in groups]

	# return concatenate_videoclips([c for c in clips])
	concat_clips = []
	for g in groups:
		print g
		for i in range(g[0], g[-1]):
			clip.set(1, i)
			ret, frame = clip.read()
			concat_clips.append(frame)
	return concat_clips


def doIt(vlog_url):
	y = YouTube(vlog_url)
	if (y.filename + '.mp4') not in os.listdir("."):
		print "downloading"
		y.get('mp4','360p').download('.')
		print "downloaded"

	if y.filename + '_compile.mp4' not in os.listdir("."):
		#clip = VideoFileClip(y.filename + '.mp4') 
		clip = cv2.VideoCapture(y.filename + '.mp4')
		#frames = clip.iter_frames()
		print "yo"
		counter = 0
		success,image = clip.read()
		while(success):
			success,image = clip.read()
			if (counter%frames_count == 0):
				print counter
				detect_faces(image, counter)
			counter += 1

		groups = cluster(selected_frames, maxgap = 10*frames_count)

		final_clip = compile(groups, clip)
		print len(final_clip)

		final_video = cv2.VideoWriter("yolo.mp4", -1, frames_count,(640,360))

		for v in final_clip:
			final_video.write(v)
		
		print "written"

	return y.filename + "_compile.mp4"

if __name__ == '__main__':
	
	# input_file_name = sys.argv[1]
	# output_file_name = sys.argv[2]
	
	doIt("https://www.youtube.com/watch?v=Kk2VTtNR3JA")
	