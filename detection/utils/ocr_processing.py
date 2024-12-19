import easyocr

# Initialize the OCR reader for Persian (Farsi)
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
CHAR_TO_INT_MAP = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
INT_TO_CHAR_MAP = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S'}

# Mapping for Persian (Farsi) numbers
PERSIAN_CHAR_TO_INT_MAP = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
}
PERSIAN_INT_TO_CHAR_MAP = {v: k for k, v in PERSIAN_CHAR_TO_INT_MAP.items()}


def write_csv(results, output_path):
    """Write the results to a CSV file."""
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format(
            'frame_nmr', 'car_id', 'car_bbox',
            'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
            'license_number_score'
        ))
        for frame_nmr, cars in results.items():
            for car_id, data in cars.items():
                if 'car' in data and 'license_plate' in data:
                    f.write('{},{},{},{},{},{},{}\n'.format(
                        frame_nmr, car_id,
                        '[{} {} {} {}]'.format(*data['car']['bbox']),
                        '[{} {} {} {}]'.format(*data['license_plate']['bbox']),
                        data['license_plate']['bbox_score'],
                        data['license_plate']['text'],
                        data['license_plate']['text_score']
                    ))


def license_complies_format(text):
    """Check if the license plate text complies with the required format for Iranian plates."""
    # Format: '11 X 111 22'
    if len(text) != 9:
        return False
    if not (text[0:2].isdigit() and
            text[2].isalpha() and
            text[3:6].isdigit() and
            text[6:9].isdigit()):
        return False
    return True


def format_license(text):
    """Format the license plate text by converting characters using the mapping dictionaries."""
    formatted_text = ''.join(
        INT_TO_CHAR_MAP.get(PERSIAN_CHAR_TO_INT_MAP.get(ch, ch),
                            CHAR_TO_INT_MAP.get(ch, ch))
        for ch in text
    )
    return formatted_text


def read_license_plate(license_plate_crop):
    """Read the license plate text from the given cropped image."""
    detections = reader.readtext(license_plate_crop)
    return detections
