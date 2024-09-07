from PyTranscribe.core import JsonToDictation
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("speakers", type=int, help="an integer number")
parser.add_argument("input", type=str, help="json dictation file")
parser.add_argument("output", type=str, help="text output file")
args = parser.parse_args()


if __name__ == "__main__":
    print ("Reading json data...")
    with open(args.input) as file:
        json_data = json.load(file)

    speakers_list = []
    for x in range(1, args.speakers+1):
        speakers_list.append("SPEAKER" + str(x))

    print ("Converting json to conversational text...")
    dictation = JsonToDictation(speakers_list, json_data)
    text = dictation.convert()

    print (f"Saving text to file ({args.output})...")
    f = open(args.output, "w")
    f.write(text)
    f.close()
    print ("success.")

