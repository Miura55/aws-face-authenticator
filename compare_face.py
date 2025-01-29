#! /usr/bin/env python3
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import os
from time import sleep
import boto3
import requests

def compare_faces(sourceFile, targetFile):
    
    # turn on yellow
    requests.get('http://192.168.10.1/api/control?alert=020000')

    session = boto3.Session(region_name='ap-northeast-1')
    client = session.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=90,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    # Check if any face matches
    if response['FaceMatches']:
        requests.get('http://192.168.10.1/api/control?alert=001000')
    else:
        requests.get('http://192.168.10.1/api/control?alert=100000')

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
              str(position['Left']) + ' ' +
              str(position['Top']) +
              ' matches with ' + similarity + '% confidence')

    imageSource.close()
    imageTarget.close()
    return len(response['FaceMatches'])

if __name__ == "__main__":
    source_file = 'source.jpg'
    target_file = 'target.jpg'
    face_matches = compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))
    sleep(30)
    os.remove('target.jpg')
    requests.get('http://192.168.10.1/api/control?alert=000000')
