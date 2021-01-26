from django.contrib import messages
from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

csrf_protect
from .models import CropModel, CustomOrder
from io import BytesIO
from datetime import datetime as dt
import boto3
import urllib
import os


# Create your views here.
def index(request):
    return render(request,"index.html")
@csrf_protect
def upload(request):
    try:
        if request.method == 'GET':
            total_amount = request.GET.get('Value')
            amount = float(total_amount)
            order = CustomOrder.objects.create(amount=amount)
            order.save()
    except Exception as e:
        print("error", str(e))
    latest_order = CustomOrder.objects.latest('amount','created_at')
    print("\t + Amount :\t"+str(latest_order.amount)+"\t====\t"+str(latest_order.created_at)+"\tDate:\t")
    context ={
        'total_amount':latest_order.amount
    }
    if request.method == 'POST':
        # Get image data as "data url" and convert it to bytes
        data = request.POST['img_data']
        response = urllib.request.urlopen(data)

        # Temporarily save file in media folder for uploading

        io = BytesIO()
        # write the bytes data into the file
        io.write(response.file.read())
        file = File(io,name=f'{int(dt.now().timestamp())}.png')
        obj = CropModel.objects.create(image=file)


        # Here I upload file to wasabi cloud.
        print("test is working")
        s3 = boto3.resource('s3',
            endpoint_url = 'https://s3.us-central-1.wasabisys.com',
            aws_access_key_id = settings.WASABI_KEY,
            aws_secret_access_key = settings.WASABI_KEY_SECRET
        )
        buc = s3.Bucket(settings.BUCKET_NAME)
        buc.upload_file(obj.image.path,obj.image.name)



        obj.bucket_name = settings.BUCKET_NAME
        obj.bucket_url = f'https://s3.wasabisys.com/{settings.BUCKET_NAME}/{obj.image.name}'

        # Delete temporary saved file from media folder and set it to None
        #if os.path.exists(path=obj.image.path):
        os.remove(obj.image.path)
            #obj.image = None
        msg = messages.info(request,"Congratulate ! Your record has encountered successfully.")
        print(msg)
        obj.save()

    return render(request,"upload.html",context)
