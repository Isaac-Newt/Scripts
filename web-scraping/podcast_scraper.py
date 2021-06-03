"""
@author: Isaac List
@copyright: 2021
@license: MIT

A Script to archive the text descriptions of each episode of the podcast
"Messy Jesus Business" produced by Sr. Julia Walsh, FSPA.
"""

# This Source Code Form is subject to the terms of the MIT license.
# If a copy of the MIT license was not distributed with this file,
# You can obtain one at https://mit-license.org/.

import requests
from bs4 import BeautifulSoup

#
# Retrieve Page Contents
#

# TODO: Automate this portion to retrieve URLs from "episodes" page
url: str = input("Please enter a URL: ")
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#
# Process Page Contents
#

# Get episode information using BeautifulSoup
title: str = soup.title.text[:-23]

parsed_description: list = []
description = soup.select("div.entry-content > p")

for paragraph in description[4:]:
    paragraph: str = str(paragraph)
    paragraph = paragraph[3:-4]
    parsed_description.append(paragraph)

# Get episode MP3 file
audio_big_link = soup.select("a.powerpress_link_d")[0]
abl_attributes: dict = audio_big_link.attrs
audio_url: str = abl_attributes["href"]

#
# Export processed contents
#

# Show notes to a text file
with open("export.txt", "w") as export_file:
    for p in parsed_description:
        export_file.write(f"{p}\n")

# Audio to an MP3 file
# TODO: Make this part work. Fails to actually write to any file,
#       even though running this code on its own works fine.
audio_object = requests.get(audio_url)

episode_name: str = title + ".mp3"
print(f"episode name: {episode_name}")
print(f"Audio URL: {audio_url}")
"""
with open(episode_name, "wb") as export_audio:
    audio_object = requests.get(audio_url)
    export_audio.write(audio_object.content)
"""
