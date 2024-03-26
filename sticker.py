import requests
from bs4 import BeautifulSoup
import os

url_of_pack = "https://sticker.ly/s/GIFWU9"

response = requests.get(url_of_pack)
soup = BeautifulSoup(response.text, "lxml")


def get_sources_of_stickers():

    parent_list_of_stickers = soup.find("ul", id="content_images")

    stickers = parent_list_of_stickers.find_all("li")

    image_sources = []

    for sticker in stickers:
        image_sources.append(sticker.img["src"])

    return image_sources


def extract_extension_from_source(source):
    extension = ""
    for char in source[::-1]:
        if char == ".":
            break
        else:
            extension += char
    return extension[::-1]


def generate_unique_folder_name_for_sticker_pack():
    # Though less elegent but this implementation to extract sticker_code is better than url_of_pack[-6:] because code for a pack might be shorter or longer. ↓
    sticker_code = url_of_pack.strip("https://sticker.ly/s/")
    sticker_pack_name = soup.find("div", class_="sticker_name").strong.text.strip()
    sticker_author = soup.find("span", class_="sticker_author").text.strip()

    folder_name = f"{sticker_pack_name} - {sticker_author} - {sticker_code}"
    return folder_name


def folder_existence_check_and_creation(folder_name):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)


def download_and_save_files(image_sources, folder_name):

    extension = extract_extension_from_source(image_sources[1])
    for i, source in enumerate(image_sources, start=1):
        response_for_image = requests.get(source)
        file_name = f"{str(i)}.{extension}"
        print(f"writing file '{file_name}' to folder '{folder_name}'")
        with open(f"{folder_name}\\{file_name}", "wb") as f:
            f.write(response_for_image.content)


image_sources = get_sources_of_stickers()
folder_name = generate_unique_folder_name_for_sticker_pack()

folder_existence_check_and_creation(folder_name)
download_and_save_files(image_sources, folder_name)
print("end")
