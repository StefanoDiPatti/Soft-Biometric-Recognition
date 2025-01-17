# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 12:12:16 2021

@author: HashiramaYaburi
"""

#test_gender.py
import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")

def get_MFCC(sr,audio):
    features = mfcc.mfcc(audio,sr, 0.025, 0.01, 13,appendEnergy = False)
    feat     = np.asarray(())
    for i in range(features.shape[0]):
        temp = features[i,:]
        if np.isnan(np.min(temp)):
            continue
        else:
            if feat.size == 0:
                feat = temp
            else:
                feat = np.vstack((feat, temp))
    features = feat;
    features = preprocessing.scale(features)
    return features

#path to testing data
sourcepath = "D:\\prova\\pygender\\test_data\\AudioSet\\male_clips"      
#path to saved models    
modelpath  = "D:\\prova\\pygender\\"   

gmm_files = [os.path.join(modelpath,fname) for fname in 
              os.listdir(modelpath) if fname.endswith('.gmm')]
models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
genders   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
              in gmm_files]
    
def get_gender_from_audio(sr,audio):
    features   = get_MFCC(sr,audio)
    scores     = None
    log_likelihood = np.zeros(len(models)) 
    for i in range(len(models)):
        gmm    = models[i]         #checking with each model one by one
        scores = np.array(gmm.score(features))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)
    print("\tdetected as - ", genders[winner],"\n\tscores:female ",log_likelihood[0],",male ", log_likelihood[1],"\n")
    return genders[winner]