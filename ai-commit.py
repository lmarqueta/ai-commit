#!/usr/bin/env python3

import os
import sys
import argparse
import configparser
import google.generativeai as genai


def generate_commit_msg(prompt):
    try:
        response = model.generate_content(prompt)
        return(response.text.rstrip('\n'))
    except:
        print("Error, could not get a response")
        raise
        sys.exit(1)

if __name__ == "__main__":
    # where to look for the configuration file
    dir = os.path.dirname(os.path.realpath(__file__))
    config_file = dir + "/config.ini"

    # parse configuration
    config_object = configparser.ConfigParser()
    with open(config_file,"r") as file_object:
        config_object.read_file(file_object)
        generative_model = config_object.get("general","generative_model")
        api_key = config_object.get("general","api_key")

    # setup model
    model = genai.GenerativeModel(generative_model)
    
    # check arguments
    parser = argparse.ArgumentParser(description="Generate a commit message from a diff")
    parser.add_argument('filename', help="The file containing the diff to generate a commit message from")
    args = parser.parse_args()
    
    # check if file filename exists
    if not os.path.isfile(args.filename):
        print("File {} does not exist".format(args.filename))
    f = args.filename
        
    # do we have an API key?
    try:
        genai.configure(api_key = api_key)
    except:
        print("Error, invalid API key.")
        raise
        sys.exit(1)

    # create prompt
    prompt = "create a short commit message (less than 80 characters long) from this diff:"

    # read diff from file
    diff = ""
    with open(f, "r") as f:
        diff = f.read()
        

    prompt = prompt + diff
    text = generate_commit_msg(prompt)

    print("{}".format(text))