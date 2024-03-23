from flask import Flask, render_template, request
import boto3
import io
from PIL import Image

app = Flask(__name__)

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image_path']
        image = Image.open(image_file)
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        image_binary = stream.getvalue()

        response = rekognition.search_faces_by_image(
            CollectionId='cricketers',
            Image={'Bytes': image_binary}
        )

        found = False
        recognized_faces = []
        for match in response['FaceMatches']:
            face_id = match['Face']['FaceId']
            confidence = match['Face']['Confidence']

            face = dynamodb.get_item(
                TableName='cricketers_collection',
                Key={'RekognitionId': {'S': face_id}}
            )

            if 'Item' in face:
                recognized_faces.append(face['Item']['FullName']['S'])
                found = True

        if found:
            return render_template('result.html', recognized_faces=recognized_faces)
        else:
            return render_template('result.html', error="Person cannot be recognized")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
