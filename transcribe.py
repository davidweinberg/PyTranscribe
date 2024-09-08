from PyTranscribe.core import JsonToDictation, AWSTranscribe
from dotenv import load_dotenv
import argparse
import json
import os
import boto3

# FOLLOWING ENVIRONMENT VARIABLES MUST BE SET
# AWS_ACCESS_KEY:_ID
# AWS_SECRET_ACCESS_KEY
# DEFAULT_LANGUAGE_CODE
# OUPUT_BUCKET
# INPUT_BUCKET
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("speakers", type=int, help="an integer number")
parser.add_argument("input_file_name", type=str, help="media audio file")
parser.add_argument("output_file_name", type=str, help="text output file")
args = parser.parse_args()

if __name__ == "__main__":
    output_bucket = os.environ['OUTPUT_BUCKET']
    input_bucket = os.environ['INPUT_BUCKET']


    awstrans = AWSTranscribe(input_bucket, output_bucket, args.speakers, args.input_file_name)
    awstrans.createTranscriptionJob()
    json_file = awstrans.downloadTranscription()

    print ("Reading json data...")
    with open(json_file) as file:
        json_data = json.load(file)

    speakers_list = []
    for x in range(1, args.speakers+1):
        speakers_list.append("SPEAKER" + str(x))

    #print (str(speakers_list))

    print ("Converting json to conversational text...")
    dictation = JsonToDictation(speakers_list, json_data)
    text = dictation.convert()

    print (f"Saving text to file ({args.output_file_name})...")
    f = open(args.output_file_name, "w")
    f.write(text)
    f.close()
    print ("success.")

