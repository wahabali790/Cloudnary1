from flask import Flask, request
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Configure Cloudinary with your account details
cloudinary.config( 
  cloud_name = "deifbikqu", 
  api_key = "947884597289734", 
  api_secret = "uRiLAnL7HbI4UYTKzSpd6PkEhPI" 
)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        # Retrieve and return the URL of the uploaded image
        return {'url': upload_result['url']}




@app.route('/capture_image', methods=['POST'])
def capture_image():
    cap = cv2.VideoCapture(0)
    messages = []

    if not cap.isOpened():
        messages.append("Error: Could not open camera.")
        return jsonify({'messages': messages}), 500

    ret, frame = cap.read()

    if not ret:
        messages.append("Error: Cannot receive frame.")
        cap.release()
        return jsonify({'messages': messages}), 500

    # Save the captured image
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)

    # Release the capture
    cap.release()

    return jsonify({'image_path': image_path}), 200


@app.route('/authenticate', methods=['POST'])
def run_face_recognition():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'message': 'Both files are required'}), 400

    # Get the files from the request
    image1 = request.files['file1']
    image2 = request.files['file2']
    picture_of_me = face_recognition.load_image_file(image1)
    face_locations = face_recognition.face_encodings(picture_of_me)
    print("face length",face_locations)
    
    if len(face_locations) == 0:
        return jsonify({'message': 'Plaese set your face position'}), 401
            
    # If at least one face is detected, proceed with face recognition
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

    unknown_picture = face_recognition.load_image_file(image2)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    # Now we can see the two face encodings are of the same person with `compare_faces`!

    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    if results[0] == True:
        return jsonify({'message': 'Authentication successful'}), 200
    else:
        return jsonify({'message': 'not authenticated'}), 401




if __name__ == '__main__':
    app.run(debug=True)
