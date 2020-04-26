import sys
sys.path.append('/usr/local/python')

import logging.handlers
import cv2
import numpy as np
import json
import base64

from openpose import pyopenpose as op

from flask import Flask, request, Response, abort, make_response, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 's_e_c_r_e_t'


# logging
logging.basicConfig()
fullHandler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=5048576, backupCount=1)
fullHandler.setLevel(logging.DEBUG)
fullHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(fullHandler)

logger = logging.getLogger(__name__)


# load model
#logger.debug('Loading Model')

# parameters
algorithm = 'openpose'
params = dict()
params["model_folder"] = "./algorithms_files/openpose/models/"
params["face"] = False
params["hand"] = False

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()


def decode_img(img_str):
    img_bytes = bytes(img_str, 'utf-8')
    img_buff = base64.b64decode(img_bytes)
    img_jpg = np.frombuffer(img_buff, dtype=np.uint8)
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)

    return img


def analyse_image(image):
    try:
        logger.debug('Analysing image with algorithm: {}'.format(algorithm))

        if algorithm == 'openpose':
            #logger.debug('Starting analysis')

            # Process Image
            datum.cvInputData = image
            opWrapper.emplaceAndPop([datum])

            #logger.debug('Analysis done')
        
            data = datum.cvOutputData

        else:
            raise KeyError('Specified algorithm not supported.')

        #logger.debug('Algorithm finished')

        return True, data

    except Exception as e:
        logger.error('An error occurred while analysing image')
        logger.error(e, exc_info=True)
        print(e)

        return False, str(e)


@app.route('/analyse_image', methods=['GET'])
def analyse_image_endpoint():
    try:
        #logger.debug('Receiving GET for /analyse_image')

        if not request.json or 'img' not in request.json:
            abort(204)

        image = request.json['img']
        image = decode_img(image)

        success, data = analyse_image(image)
        #logger.debug('Algorithm result: {}'.format(success))

        if success:
            #logger.debug('Returning result image')
            result = {'Status': success, 'data': data.tolist()}
            
            #res = Response(result, status=200, mimetype='application/json')
            
            #return res
            return make_response(jsonify(result), 200)

        else:
            # an error occurred, show the error message
            logger.debug('An error occurred in the algorithm')
            data = {'error': 'failed'}
            res = Response(data, status=400, mimetype='application/json')
            
            return res

    except Exception as e:
        logger.error('An error occurred while analysing image')
        logger.error(e, exc_info=True)
        print(e)
        data = {'error': 'error'}
        res = Response(data, status=400, mimetype='application/json')

        return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)