import sys
sys.path.insert(0, '/home/ansar/awsdevops/FaceRecognition')

activate_this = '/home/ansar/awsdevops/FaceRecognition'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))

from app import app as application
