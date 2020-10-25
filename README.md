# MidcurveNN
Midcurve by Neural Networks

Copyright (C) 2019 Yogesh H Kulkarni

## License:
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or any later version.

## Description
- Goal: Given a 2D closed shape (closed polygon) find its midcurve (polyline, closed or open)
- Input: set of points or set of connected lines, non-intersecting, simple, convex, closed polygon 
- Output: another set of points or set of connected lines, open/branched polygons possible
- Type: 
	- It is a translation problem. In 2D, input is the sketch profile, whereas the output is the midcurve. Input points are ordered (mostly forming closed loop, manifold). Output points may not be ordered, and can have branches (non-manifold)
	- It is a variable input and variable output problem. 
	- It is a network 2 network problem (not Sequence to Sequence) with variable size inputs and outputs
	- For Encoder Decoder like network, libraries like Tensorflow need fixed length inputs. If input has variable lengths then padding is done with some unused value. But the padding will be a big issue here as the padding value cannot be like 0,0 as it itself would be a valid point. 
	- Another problem of using seq2seq is that both input polygons and output branched midcurves are not linearly connected, they may have loops, or branches. Need to think more. (more details in LIMITATIONS below)
	- Instead of going to point list as i/o let’s look at well worked format of images. Images are of constant size, say 64x64 pixels. Let’s colour profile in the bitmap (b&w only) similarly midcurve in output bitmap. With this as i/o LSTM encoder decoder seq2seq can be applied. Variety in training data can be populated by shifting/rotating/scaling both i/o. Only 2D sketch profile for now. Only linear segments. Only single simple polygon with no holes.
	- How to vectorise? Each point as 2 floats/ints. So total input vector is polygon of m points is 2m floats/ints. Closed polygon with repeat the first point as last. Output is vector of 2n points. In case of closed figure, repeat the last point. Prepare training data using data files used in MIDAS. To make 100s, 1000s of input profiles, one can scale both input and output with different factors, and then randomly shuffle the entries. Find max num points of a profile, make that as fixed length for both input and output. Fill with 0,0??? As origin 0,0 could be valid part of profile…any other filler? NULL? Run simple feed forward NN, later RNN, LSTM, Seq2seq
	- See https://www.tensorflow.org/tutorials/seq2seq, https://www.youtube.com/watch?v=G5RY_SUJih4, A Neural Representation of Sketch Drawings, https://magenta.tensorflow.org/sketch_rnn  https://github.com/tensorflow/magenta/blob/master/magenta/models/sketch_rnn/README.md 
	- Add plotting capability, show polygons their midcurves etc, easy to debug and test unseen figures.

## Plan

###	Phase I (Image based, Encoder-Decoder fixed size based) : DONE
	- Img2Img: i/o fixed size 100x100 bitmaps
	- Populate many by scaling/rotating/translating both io shapes within the fixed size
	- Use Encode Decode like Semantic Segmentation or Pix2Pix to learn dimension reduction
	
###	Phase II (Geometric Points based, Variable size sequences i/o, once  such dynamic size encoder-decoder is available): *LIMITATIONS
	- Network 2 Network Encode Decoder (not graph, as graph is topological-connectivity based, and not spatial)
	- Different sizes of input and output
	- Closed->closed/open, Manifold->Manifold/Non-manifold
	
### LIMITATIONS
- Shapes can not be modeled as sequences. Although polygon shape L may appear as sequence of points, it is not. 
- All shapes can not be drawn without lifting a pencil, which is possible for sequences. Say, Shapes like Y or concentric O, cannot be modeled as sequences. So, Midcurve transformation cannot be modeled as Sequence 2 Sequence network.
- Shapes are not graphs as well. Graphs are topological and not geometrical. They represent only connectivity and not spatial positions. In 2D profiles even nodes have deterministic locations. So, even if Graph 2 Graph Encoder Decoder architecture is made available, it cannot model the Midcurve transformation.
- Assuming by "network" we mean Graph with nodes having spatial significance, we would need Network 2 Network Encoder Decoder architecture in place, to model Midcurve transformation.
- *Conclusion* With the study so far, the Phase I results, with Image to Image transformation architecture, the problem appears reasonably addressed, and Phase II is NOT NEEDED. HALTING THIS PROJECT FOR NOW AND WILL NOT PROCEED WITH PHASE II.

## Publications/Talks
- Vixra paper MidcurveNN: Encoder-Decoder Neural Network for Computing Midcurve of a Thin Polygon, viXra.org e-Print archive, viXra:1904.0429 http://vixra.org/abs/1904.0429 
- ODSC proposal https://confengine.com/odsc-india-2019/proposal/10090/midcurvenn-encoder-decoder-neural-network-for-computing-midcurve-of-a-thin-polygon


## Implementation Notes:
- Keras (TBD: Moving from independant Keras to Tensorflow.Keras, so wait for update here)
	- DON’T Conda install -c conda-forge keras DIRECTLY
	- Keras installation cribbed that tensorflow is not present
	- Reinstalled tensorflow by pip – U
	- Got error saying not able to load tensorflow. Looking at https://github.com/ContinuumIO/anaconda-issues/issues/10034 installing conda install vs2013_runtime
	- Go to Anaconda prompt and follow https://medium.com/@margaretmz/anaconda-jupyter-notebook-tensorflow-and-keras-b91f381405f8
	- If you get QT error for matplotlib, use “import matplotlib;matplotlib.use('TKAgg')”
	- Using https://blog.keras.io/building-autoencoders-in-keras.html to have a base code
	
- Pix2Pix
	- Github Keras-GAN code https://github.com/eriklindernoren/Keras-GAN/tree/master/pix2pix
	- Same Keras-GAN code in notebook format https://www.kaggle.com/vikramtiwari/pix-2-pix-model-using-tensorflow-and-keras/notebook
	- Google Colab based code (different from Keras-GAN) https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/r2/tutorials/generative/pix2pix.ipynb

## Why Pix2Pix may not be good
- In midcurveNN problem, both input and output are black and white images with with pixel width. 
- For given input image, exact and only one possible output is there. No other output would be correct.
- So, Loss function of such learning systems would be exact and can be specified by simple distance formulas like L1, L2, etc.
- Simple/Dense/CNN based Encoder Decoder have exact loss function.
- In case of GANs, like conditional GAN or Pix2Pix, the purpose of Discriminator is actually to learn the Cost Function itself. (Ref: Phillip pod cast video regarding Pix2Pix). There "goodness" of the output is learnt in the Cost Function, and not the Exactness as specified in the examples above.
- Thus, theoretically, GANs are not suitable for MidcurveNN problem. Comments?


## ToDOs
- Get Denoiser working in .py and .ipynb 
- Get cnn working in .py and .ipynb 
- Get pix2pix working in .py and .ipynb
- Generate more data from more profiles

## Errors and Solutions
- no library called "libcairo-2" was found
  https://stackoverflow.com/questions/28211418/python-oserror-cannot-load-library-libcairo-so-2
  Install GTK 3 runtime https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer and add to path
  
- Failed to create a directory: models/autoencoder_model.pkl\variables; No such file or directory
  use a forward slash with the checkpoint directory or os.paths.join("models","modelname")
  
- If using Keras pass *_constraint arguments to layers.

- Cuda lib error, https://www.joe0.com/2019/10/19/how-resolve-tensorflow-2-0-error-could-not-load-dynamic-library-cudart64_100-dll-dlerror-cudart64_100-dll-not-found/
  
## References
- Image-to-Image Translation with Conditional Adversarial Nets https://phillipi.github.io/pix2pix/

## Disclaimer:
Author (yogeshkulkarni@yahoo.com) gives no guarantee of the results of the program. It is just a fun script. Lot of improvements are still to be made. So, don’t depend on it at all.
	
