import os
import cv2
from django.shortcuts import render
from django.conf import settings
from .utils.image_processing import process_image
from django.core.files.storage import FileSystemStorage


def index(request):
    context = {}
    if request.method == 'POST':
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            image_path = fs.path(filename)

            results, display_image, cropped_plates = process_image(image_path)

            # Save the processed image to be displayed in the template
            processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_image.jpg')
            cv2.imwrite(processed_image_path, display_image)

            cropped_plate_urls = []
            for i, cropped_plate in enumerate(cropped_plates):
                cropped_plate_path = os.path.join(settings.MEDIA_ROOT, f'cropped_plate_{i}.jpg')
                cv2.imwrite(cropped_plate_path, cropped_plate)
                cropped_plate_urls.append(fs.url(f'cropped_plate_{i}.jpg'))

            context['results'] = [{'characters': res['characters'], 'confidence': res['confidence']} for res in results]
            context['processed_image_url'] = fs.url('processed_image.jpg')
            context['cropped_plate_urls'] = cropped_plate_urls
            context['image_path'] = uploaded_file.name  # Pass original image name for reference
        else:
            context['error'] = "No image uploaded. Please choose an image to upload."

    return render(request, 'detection/index.html', context)
