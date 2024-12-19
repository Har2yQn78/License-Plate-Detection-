import os
import cv2
from django.shortcuts import render
from django.conf import settings
from .utils.image_processing import process_image
from django.core.files.storage import FileSystemStorage


def index(request):
    context = {}
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        image_path = fs.path(filename)

        results, display_image = process_image(image_path)

        # Save the processed image to be displayed in the template
        processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_image.jpg')
        cv2.imwrite(processed_image_path, display_image)

        context['results'] = results
        context['processed_image_url'] = fs.url('processed_image.jpg')
        context['image_path'] = uploaded_file.name  # Pass original image name for reference

    return render(request, 'detection/index.html', context)
