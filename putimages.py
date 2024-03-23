
import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('image_01.jpg','Virat Kohli'),
      ('image_02.jpg','Virat Kohli'),
      ('image_03.jpg','Virat Kohli'),
      ('image_04.jpg','Virat Kohli'),
      ('image_05.jpg','Mahendra singh dhoni'),
      ('image_06.jpg','Mahendra singh dhoni'),
      ('image_07.jpg','Mahendra singh dhoni'),
      ('image_08.jpg','Mahendra singh dhoni'),
      ('image_09.jpg','Rohit sharma'),
      ('image_10.jpg','Rohit sharma'),
      ('image_11.jpg','Rohit sharma'),
      ('image_12.jpg','Rohit sharma'),
      ('image_13.jpg','Ben stokes'),
      ('image_14.jpg','Ben stokes'),
      ('image_15.jpg','Ben stokes'),
      ('image_16.jpg','Kane Williamson'),
      ('image_17.jpg','Jos Buttler'),
      ('image_18.jpg','DevOpsMaster'),
      ('image_19.jpg','DevOpsMaster')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('testansarbucket','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})
