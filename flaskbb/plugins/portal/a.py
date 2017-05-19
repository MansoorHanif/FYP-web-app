#!/usr/bin/env python

# from keras.applications import InceptionV3
# from keras.applications.imagenet_utils import decode_predictions

# from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
# from keras.preprocessing import image

# import os
# import numpy as np
# import sys 

# model = InceptionV3(include_top=True, weights='imagenet')
	
# def preprocess_input_inceptionV3(x):
# 	x /= 255.
# 	x -= 0.5
# 	x *= 2.
# 	return x

# def process_image(img_path):
# 	img = image.load_img(img_path, target_size=(299, 299))
# 	x = image.img_to_array(img)

# 	x = np.expand_dims(x, axis=0)
# 	x = preprocess_input_inceptionV3(x)
	
# 	preds = model.predict(x)
# 	decoded = decode_predictions(preds)
# 	# decoded[0]
# 	#print 'Predicted:', decoded[0]

# 	classnames_f = ['lynx',
# 	 'black-and-tan_coonhound',
# 	 'beagle',
# 	 'bluetick',
# 	 'Persian_cat',
# 	 'English_foxhound',
# 	 'Egyptian_cat',
# 	 'tabby_cat',
# 	 'Afghan_hound',
# 	 'cougar',
# 	 'tiger_cat',
# 	 'Walker_hound',
# 	 'basset',
# 	 'redbone',
# 	 'bloodhound',
# 	 'Rhodesian_ridgeback',
# 	 'pug']
	            
		            
# 	_,name,score = decoded[0][0]
# 	score = score * 100
# 	tmp = np.array([name in n for n in classnames_f])
# 	if tmp.any():

# 		print "Predicted Breed : %s" + "Confidence(in %) : %d"% name , score
# 	else:
# 		print 'This Breed is not served, or could not be classified'




import numpy as np
from keras.optimizers import SGD
from keras.preprocessing import image
from convnetskeras.convnets import preprocess_image_batch, convnet
import sys

############################################# 		MODEL
# Optimizer
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

# Model
model = convnet('alexnet', weights_path= "/home/mansoor/pywork/catsanddogs/Alexnet/SGD_CC/allbest/weights--11-0.94.hdf5",
                heatmap=False,trainable=False)

# Compile model
model.compile(optimizer=sgd, loss='categorical_crossentropy')
print "Model successfully built."


def process_image(img_path):
	
	###########################################		 Predictions 
	print img_path

	img = image.load_img(img_path, target_size=(227, 227))
	x = image.img_to_array(img)

	x_pred = np.expand_dims(x, axis=0)
	# x_pred = preprocess_image_batch(img_path,
	# 	                       img_size=(230,230),
	# 	                       crop_size=(227,227),
	# 	                       color_mode="rgb")


	# predict here
	pred=model.predict(x_pred)

	a = pred[:,0]  > pred[:,1]
	pred = [[1,0] if i==True else [0,1] for i in a]
	pred = np.argmax(pred)

	if pred == 1:
		print "it's a Cat"
	else:
		print "it's a Dog"                        

if __name__ == '__main__':
	# Get arguments from user
	img_path = sys.argv[1]
	process_image(img_path)
	


