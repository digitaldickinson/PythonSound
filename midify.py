'''
This script loops through the images in the frames folder and creates midi notes based on the dominant colours. You can specify the number of notes. It uses k-means clustering to generate a list of dominant colours and a relative amount for each image. The RGB values are converted into notes values and the amounts of each colour are converted to the duration of the note. The notes are then sequenced in a midi file. This creates an ‘arpeggio’ effect for each image.

The bulk of this script and the related utilities in the utils.py file are based on code from Adrian Rosebrock at

https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

The midi library is midiutil by Mark Conway Wirt

https://github.com/MarkCWirt/MIDIUtil

MIDUTIL, Copyright (c) 2009-2016, Mark Conway Wirt <emergentmusics) at (gmail . com>

Other parts of this code were made possible thanks to contributions to StackExchange like:

https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
https://medium.com/@manivannan_data/resize-image-using-opencv-python-d2cdbbc480f0

USAGE
Run the file with the following arguments
midify.py  --notes 4

You can tweak the number of notes but 4 works best
'''
# import the necessary packages
# this is quite bloated and I may see if there's a way to minimise it
# i.e. can I do with cv2 what i'm doing with PIL
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
import numpy as np
from glob import iglob #Grab files to do stuff with
from PIL import Image #Handle the image stuff
import re # Regex - This for the sorting of filenames
import os, os.path #using this to count images
from midiutil import MIDIFile

# Construct the argument parser and parse the arguments
# Do I need to get rid of this to make things less complicated?
# Although DON"T DELETE UNTIL YOU PASTE SOMEHWERE ELSE. ITS USEFUL
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--notes", required = True, type = int,
	help = "# of notes per image")
args = vars(ap.parse_args())

def numericalSort(value):
    #This is function that helps sort the images into the right order
	numbers = re.compile(r'(\d+)')
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

def get_values(path):
	# Create a list of all the images in the folder
	npath = [infile for infile in sorted(iglob(os.path.join(path, '*.png')), key=numericalSort)]
	print ("There are ", format(len(npath)), " to work through...")
	# Loop through each one and get some values to work with
	for filepath in npath:
		image = cv2.imread(filepath)
		#shrink the image to speed things up.
		newx,newy = image.shape[1]/5,image.shape[0]/5 #new size (w,h)
		image = cv2.resize(image,(int(newx),int(newy)))
		#Convert the image to RGB
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# 'reshape' the image to be a list of pixels
		image = image.reshape((image.shape[0] * image.shape[1], 3))
		# this fires up the K-means function based on the number of Clusters
		# I'm thnking I might use 8 for the notes scale so 4 clusters gives 4 notes of 2 beats each
		clt = KMeans(n_clusters = args["notes"])
		# .fit is the thing that does the k-means calculation on the image
		clt.fit(image)
		# build a histogram of clusters and then create a figure
		# representing the number of pixels labeled to each color
		# The function for this is over in utils.py
		hist = utils.centroid_histogram(clt)
		# Use the hist value and the cluster values(the colour) to create some values.
		# The function for this is over in utils.py
		values.append(utils.grab_values(hist, clt.cluster_centers_))
		print('Done:',filepath)
		# We could spit out the k-means viz here perhaps so we can create a thumbnail of notes in colour
		# 	bar = utils.plot_colors(hist, clt.cluster_centers_)
		#	plt.figure()
		#	plt.axis("off")
		#	plt.imshow(bar)
		#	plt.savefig('foo.png', bbox_inches='tight')
		#
	return values
#Define some lists for values and note data
values=[]
notes=[]
# Where are the images to midify
path = 'frames/'
# Some standard for the midi file.
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 240  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

# Define a new midi object. Essentially a list of notes to dump out as a midi file.
MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track automatically created)
MyMIDI.addTempo(track,time, tempo)

# Start the process by getting the dominent colour values from each image in the folder
get_values(path)
print("I've got the values I need")
# With that data collected we can convert it into midi. This is limited at the moment in terms of the 'music' but it works!
notes = utils.make_notes(values)
print ("I've now got enough notes to start creating the midi file.")
# Once we have that we can start to loop through the notes and build up the midi file.
for m in notes:
	# For every block of notes per image pull out the note (n) and the duration(d)
	for n,d in m:
		# This might be a good place to capture if a note has a 0 duration
		# This is caused when the percentage of colour in an image is so low it
		# Is rounded to zero. I need to sort this out because a 0 value crashes out the midi commands
		if d != 0:
			MyMIDI.addNote(track, channel, n, time, d, volume)
			time = time+d
		else:
			time = time+1
print ("Done. Saving out the file now...")
# Once we've looped through all the notes. Chuck it into the midi file.
with open("arpeggio.mid", "wb") as output_file: MyMIDI.writeFile(output_file)
# We are done
