from django.shortcuts import render, render_to_response
from django.http import JsonResponse
import base64
import os
from PIL import Image
from io import BytesIO
import json
import cv2
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib as mpl
import numpy as np
from matplotlib.transforms import Bbox
# from . import predict as p

def validate_files(files):
    for file in files:
        image_extensions = ['ras', 'xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif', 'gif', 'ppm', 'xbm',
                            'tiff', 'rgb', 'pgm', 'png', 'pnm']
        ext = file.name.split('.')
        ext = ext[len(ext) - 1]
        if ext.lower() not in image_extensions:
            return False
    return True


def img_to_results(file):

    classes = ['Normal', 'Pneumonia']
    img = file
    pred = classes[0]
    try:
        name = file.name.split("/")
    except AttributeError:
        name = file.split("/")
    name = name[len(name) - 1].split(".")[0]

    prediction = {
        'name': name,
        'pred': pred,
    }

    # mpl.use('Agg')
    # plt.ioff()
    # plt.axis('off')
    fig = Image.open(img)
    buf = BytesIO()
    fig.save(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    prediction['image'] = string.decode("utf-8")
    print(prediction['image'])
    return prediction


# Create your views here.
def home(request):
    args = {'title': 'Home | PneumoScan.ai'}
    return render(request, 'home.html', args)


def team(request):
    args = {'title': 'Team | PneumoScan.ai'}
    return render(request, 'team.html', args)


def about(request):
    args = {'title': 'About | PneumoScan.ai'}
    return render(request, 'about.html', args)


def live_scan(request):
    args = {'title': 'Live Scan | PneumoScan.ai'}
    return render(request, 'scan.html', args)

def demo(request):
    args = {'title': 'Demo | PneumoScan.ai'}
    return render(request, 'demo.html', args)

def upload_data(request):
    args = {'title': 'Live Scan | PneumoScan.ai'}
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        files = request.FILES.getlist('files')
        print(files)
        if username and email and len(files) > 0:
            if not validate_files(files):
                args.update({'message': 'Please upload an appropriate image file',
                             "status": 0})
                return JsonResponse(args)

            images = []
            for i in range(len(files)):
                # img = Image.open(files[i])
                # # img.show()
                # buf = BytesIO()
                # img.save(buf, format='png', bbox_inches='tight')
                # buf.seek(0)
                # string = base64.b64encode(buf.read())
                # print(string)
                prediction = img_to_results(files[i])
                images.append(prediction)

            args.update({'message': 'Files are cool',
                         "images": images,
                         "status": 1,
                         "username": username,
                         "email": email})

            # return render(request, 'results.html', args)
            return JsonResponse(args)
        else:
            args.update({'message': 'Please provide all the details',
                         "status": 0})
            return JsonResponse(args)

    else:
        return render(request, 'home.html', args)


def demo_data(request):
    args = {'title': 'Demo | PneumoScan.ai'}
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        filename = request.POST.get('filename')
        if username and email and filename:

            images = []
            f = filename.split('/')
            filename = f[len(f) - 1]
            file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static','img', 'sample', filename)
            prediction = img_to_results(file)
            images.append(prediction)

            args.update({'message': 'Files are cool',
                         "images": images,
                         "status": 1,
                         "username": username,
                         "email": email})

            # return render(request, 'results.html', args)
            return JsonResponse(args)
        else:
            args.update({'message': 'Please provide all the details',
                         "status": 0})
            return JsonResponse(args)

    else:
        return render(request, 'home.html', args)


def ppe_scan(request):
    args = {'title': 'PPE Scan | PneumoScan.ai'}
    return render(request, 'ppe.html', args)


def badge_scan(request):
    args = {'title': 'Badge Scan | PneumoScan.ai'}
    return render(request, 'badge.html', args)


def decode(request):
    if request.POST:
        decodedData = request.POST['imgBase64']
        print(decodedData)
        if decodedData:
            json_data = json.dumps(decodedData)
            print(json_data)
            return JsonResponse(json_data, safe=False)

        return JsonResponse({"code": 'NO BarCode Found'})
