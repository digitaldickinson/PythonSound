# PythonSound
Experiments with turning images into sounds
This script loops through the images in the frames folder and creates midi notes based on the dominant colours. You can specify the number of notes. It uses k-means clustering to generate a list of dominant colours and a relative amount for each image. The RGB values are converted into notes values and the amounts of each colour are converted to the duration of the note. The notes are then sequenced in a midi file. This creates an ‘arpeggio’ effect for each image.
The bulk of this script and the related utilities in the utils.py file are based on code from Adrian Rosebrock at
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
