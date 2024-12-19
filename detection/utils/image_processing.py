import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from .ocr_processing import read_license_plate, format_license, license_complies_format


def draw_bboxes(frame, bboxes, color, text=None):
    """Draw bounding boxes on the frame."""
    for bbox in bboxes:
        bbox_coords = np.array(bbox).reshape(-1, 2).astype(int)
        x1, y1 = bbox_coords.min(axis=0)
        x2, y2 = bbox_coords.max(axis=0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)


def process_image(image_path):
    """Process the selected image to detect and read all license plates."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image.")
        return

    display_image = image.copy()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detections = read_license_plate(gray_image)

    results = []

    for bbox, text, score in detections:
        formatted_text = format_license(text)
        is_compliant = license_complies_format(formatted_text)
        print(f"{'Compliant' if is_compliant else 'Non-compliant'} License Plate: {formatted_text} (Score: {score})")

        draw_bboxes(display_image, [bbox], (255, 0, 0))

        results.append({
            'bbox': bbox,
            'text': formatted_text,
            'score': score,
            'is_compliant': is_compliant
        })

    return results, display_image
