# from flask import Flask, request, jsonify
# import pytesseract
# from PIL import Image
# import os

# app = Flask(__name__)

# # Set Tesseract path if necessary (for Windows)
# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# @app.route("/upload-image", methods=['POST'])
# def upload_image():
#     """Endpoint to upload an image and extract text using Tesseract OCR."""
#     if "image" not in request.files:
#         return jsonify({"status": 0, "msg": "No image file provided", "class": "error"})

#     file = request.files["image"]

#     if file.filename == "":
#         return jsonify({"status": 0, "msg": "No selected file", "class": "error"})

#     # Save the file
#     filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
#     file.save(filepath)

#     # Process the image with Tesseract OCR
#     try:
#         image = Image.open(filepath)
#         extracted_text = pytesseract.image_to_string(image)  # Default language: English

#         return jsonify({
#             "status": 1,
#             "msg": "Text extracted successfully",
#             "extracted_text": extracted_text.strip(),
#             "class": "success"
#         })
    
#     except Exception as e:
#         return jsonify({"status": 0, "msg": str(e), "class": "error"})
    
# @app.route("/test-message", methods=['POST'])
# def test_message():
#     """Tests the text comparison logic separately."""
#     data = request.get_json()
#     input_text = data.get("text1", "").strip().lower()
#     extracted_text = data.get("text2", "").strip().lower()

#     if not input_text or not extracted_text:
#         return jsonify({"status": 0, "msg": "Both text1 and text2 are required", "class": "error"})

#     # Compare texts
#     if input_text == extracted_text:
#         return jsonify({"status": 1, "msg": "Text matched!", "class": "success"})
#     else:
#         return jsonify({"status": 0, "msg": "Text did not match!", "class": "error"})


# from flask import Flask, request, jsonify
# import pytesseract
# from PIL import Image
# import os

# app = Flask(__name__)

# # Set Tesseract path if necessary (for Windows)
# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# # ✅ **Predefined Text for Matching**
# PREDEFINED_TEXT = "This is test message"

# @app.route("/upload-image", methods=['POST'])
# def upload_image():
#     """Uploads an image, extracts text using Tesseract OCR, and compares with a predefined text."""
#     if "image" not in request.files:
#         return jsonify({"status": 0, "msg": "No image file provided", "class": "error"})

#     file = request.files["image"]

#     if file.filename == "":
#         return jsonify({"status": 0, "msg": "No selected file", "class": "error"})

#     # Save the file
#     filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
#     file.save(filepath)

#     # Process the image with Tesseract OCR
#     try:
#         image = Image.open(filepath)
#         extracted_text = pytesseract.image_to_string(image).strip().lower()  # Extracted text

#         # ✅ **Compare Extracted Text with Predefined Text**
#         if extracted_text == PREDEFINED_TEXT.lower():
#             return jsonify({
#                 "status": 1,
#                 "msg": "Text matched!",
#                 "extracted_text": extracted_text,
#                 "class": "success"
#             })
#         else:
#             return jsonify({
#                 "status": 0,
#                 "msg": "Text did not match!",
#                 "extracted_text": extracted_text,
#                 "expected_text": PREDEFINED_TEXT,
#                 "class": "error"
#             })

#     except Exception as e:
#         return jsonify({"status": 0, "msg": str(e), "class": "error"})


from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
from fuzzywuzzy import fuzz  

app = Flask(__name__)

# Set Tesseract path if necessary (for Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


PREDEFINED_TEXT = "Hello, this is a test message!"

@app.route("/upload-image", methods=['POST'])
def upload_image():
    """Uploads an image, extracts text using Tesseract OCR, and checks if it matches at least 90%."""
    if "image" not in request.files:
        return jsonify({"status": 0, "msg": "No image file provided", "class": "error"})

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"status": 0, "msg": "No selected file", "class": "error"})

    # Save the file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Process the image with Tesseract OCR
    try:
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image).strip().lower()  # Extracted text

        # ✅ **Calculate similarity percentage**
        match_percentage = fuzz.ratio(extracted_text, PREDEFINED_TEXT.lower())  # Compare texts

        # ✅ **Allow match if similarity is 90% or more**
        if match_percentage >= 90:
            return jsonify({
                "status": 1,
                "msg": "Text matched!",
                "extracted_text": extracted_text,
                "match_percentage": match_percentage,
                "class": "success"
            })
        else:
            return jsonify({
                "status": 0,
                "msg": "Text did not match!",
                "extracted_text": extracted_text,
                "expected_text": PREDEFINED_TEXT,
                "match_percentage": match_percentage,
                "class": "error"
            })

    except Exception as e:
        return jsonify({"status": 0, "msg": str(e), "class": "error"})


if __name__ == "__main__":
    app.run(debug=True)
