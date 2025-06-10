# Open the json file and load the data
import json
from PIL import Image
import streamlit as st

file_path = "data/person_db.json"  # Replace with your actual file path

def load_user_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_all_names(data):
    """
    A function that uses the lisst of dictionaries to extract all names into a list
    """
    user_names = []
    for person_dict in data:
        user_names.append(person_dict["lastname"] + ", " + person_dict["firstname"])

    return user_names

def get_image(person_name):
    image = Image.open(get_image_path(person_name))
    return image

def get_image_path(current_user):
    """
    A function that uses the list of dictionaries to extract the image path
    """
    firstname = current_user.split(", ")[1]
    lastname = current_user.split(", ")[0]

    for person_dict in load_user_data(file_path):
        if person_dict["lastname"] == lastname and person_dict["firstname"] == firstname:
            path_to_image =  person_dict["picture_path"]
            return path_to_image

if __name__ == "__main__":
    file_path = "data\person_db.json"  # Replace with your actual file path
    user_data = load_user_data(file_path)
    print(user_data)
    name_list = get_all_names(user_data)
    print(name_list)