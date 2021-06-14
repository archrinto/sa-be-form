import uuid
import os

from flask import Flask, request, make_response, abort, jsonify

from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")


def require_client_id(api_method):
    @wraps(api_method)

    def check_client_id(*args, **kwargs):
        client_id = request.headers.get('Client-Id')
        valid = False
        try:
            uuid.UUID(client_id, version=4)
            valid = True
        except:
            valid = False

        if valid:
            return api_method(*args, **kwargs)
        else:
            abort(make_response(jsonify({ 'error': 'Invalid Client' }), 401))

    return check_client_id


@app.route("/")
def index():
    return "Hello world"


@app.route("/checkin", methods=["GET"])
def checkin():
    return jsonify({
        'client_id': str(uuid.uuid4())
    })

@app.route("/upload-image", methods=["POST"])
@require_client_id
def upload_image():
    client_id = request.headers.get('Client-Id')
    filename = datetime.now().strftime('%y%m%d-%H%M%S%f')
    if request.files and request.form.get('face'):
        image = request.files["image"]
        filename = request.form.get('face') + '-' + filename + '.jpeg'
        upload_dir = os.path.join(app.config['UPLOAD_DIR'], client_id)
        try:
            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)
            image.save(os.path.join(upload_dir, filename))
            return jsonify({'message': 'image uploaded' })
        except Exception as e:
            print(e)
            return jsonify({'error': 'image upload failed'}), 500
    else:
        return jsonify({'error': 'invalid request'}), 400


if __name__ == "__main__":
    app.run()
