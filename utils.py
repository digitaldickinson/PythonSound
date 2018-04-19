# import the necessary packages
import numpy as np
import cv2
import math #Use this to round up numbers

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	# We use this to gauge the amount of each color in a clusters
	# and use this for making the note duration amongst other things
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def grab_values(hist, centroids):
	# this grabs the hist and centroids
	# We use this to crete a set of values that we can then use to
	# make the midi notes. I'm leaving this in as a step as it also drives
	# the part that plots the colours from the original script in case
	# I want to use it.
	values = []
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# convert centroids to RGB
		c = color.astype("uint8").tolist()
		# Take a sum of the notes
		# Insert the percentage into the array so all info is in one element
		c.insert(3,percent)
		# Append this to that RGBZ list.
		values.append(c)
	#throw back a list with the RGBZ values for each cluster
	return values

def make_notes(values):
	# this takes the RGB and % info and turns it into midi note
	# data which we cram into  the notes[] list. This way we have orginal
	# data and midi
	# Lots to do here in terms of number of notes in arpeggio and the tunefullness of it
	# 1. Get the notes to conform to a key or have it as an option
	notes = []
	#set some values that help us normalise the rgb values to midi notes
	old_min = 0
	old_range = 765
	#Set the midi range
	#I've tweaked the range a little here so that we don't get mega low and hight notes.
	# 24-108 is C0 to C6
	new_range = 96
	new_min = 24
	# loop over each set of values and then each value
	for v in values:
		# to pull out RGB and % info we can use.
		for r,g,b,p in v:
			#produce a single value for a note normalised to midi range
			n = int((sum([r,g,b]) - old_min) / old_range * new_range + new_min)
			# Now work out the duration for each not by working out how many beats each note plays based on the % of that colour in clusters.
			d = int(round(8*p,0))
			# Add the note and percent as duration to m
			m = [n,d]
			# Append d to the values list
			notes.append([m])
	#throw back a list with a note and duration value for each cluster
	return notes

def plot_colors(hist, centroids):
	# This is from the original script by Adrian Rosebrock
	# It initializes the bar chart representing the relative frequency of each of the colors
	# I'm leaving this in as, at some point it might be worth generating a cinemaredux of video using the bar chart.Like a bar chart score!

	# create a 50x300 image with 3 channels RGB
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		# int endX is 0+300 e.g. 0.5x300
		endX = startX + (percent * 300)
		# Draw a rectangle wih coords startX and endX
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
		startX = endX

	# return the bar chart
	return bar
