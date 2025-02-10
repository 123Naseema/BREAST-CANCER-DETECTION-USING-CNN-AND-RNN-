from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
import os
from keras.models import load_model
import matplotlib.pyplot as plt #use to visualize dataset vallues
import io
import base64
import cv2
import numpy as np

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Aboutus(request):
    if request.method == 'GET':
       return render(request, 'Aboutus.html', {})

def UserLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def UploadFile(request):
    if request.method == 'GET':
        return render(request, 'UploadFile.html', {})

#use this function to predict fish species uisng extension model
def predict(image_path, extension_model):
    labels = ['Benign', 'Malignant', 'Normal']
    image = cv2.imread(image_path)#read test image
    img = cv2.resize(image, (32,32))#resize image
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1,32,32,3)#convert image as 4 dimension
    img = np.asarray(im2arr)
    img = img.astype('float32')#convert image features as float
    img = img/255 #normalized image
    pred = extension_model.predict(img)#now predict dog breed
    predicts = np.argmax(pred)
    img = cv2.imread(image_path)
    img = cv2.resize(img, (650,400))#display image with predicted output
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.putText(img, labels[predicts]+" Score "+str(np.amax(pred)), (30, 45),  cv2.FONT_HERSHEY_SIMPLEX,1.5, (0, 255, 0), 2)    
    return img    
    
def UploadFileAction(request):
    if request.method == 'POST':
        global uname
        extension_model = load_model("model/cnn_weights.hdf5")
        myfile = request.FILES['t1'].read()
        fname = request.FILES['t1'].name
        if os.path.exists("CancerApp/static/test.jpg"):
            os.remove("CancerApp/static/test.jpg")
        with open("CancerApp/static/test.jpg", "wb") as file:
            file.write(myfile)
        file.close()
        img = predict("CancerApp/static/test.jpg", extension_model)
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        context= {'data': img_b64}
        return render(request, 'UploadFile.html', context)   
        


