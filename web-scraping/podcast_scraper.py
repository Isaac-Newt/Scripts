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
import os
from bs4 import BeautifulSoup

def parse_shownotes(description) -> list:
    """Parse notes to a list of <p> element texts"""
    parsed_description: list = []

    for paragraph in description[4:]:
        paragraph: str = str(paragraph)
        paragraph = paragraph[3:-4]
        parsed_description.append(paragraph)

    return parsed_description

def write_shownotes(parsed_description: list, title: str) -> None:
    """Write shownotes to a text file"""
    file_name: str = title + ".txt"
    with open("notes.txt", "w") as export_file:
        for p in parsed_description:
            export_file.write(f"{p}\n")

def retrieve_audio(audio_url: str, title: str) -> None:
    """
    Given a valid url, retrieve podcast audio and write to
    a local mp3 file named with the given title.
    """
    # TODO: Make this part work. Fails to actually write to any file,
    #       even though running this code on its own works fine.
    audio_object = requests.get(audio_url)
    episode_name: str = title + ".mp3"

    with open("audio.mp3", "wb") as export_audio:
        audio_object = requests.get(audio_url)
        export_audio.write(audio_object.content)

def get_episodes(url: str) -> list:
    """Make list of episode URLs"""
    soup = build_soup(url)
    episode_list: list = []

    # TODO: Select multiple items using BeautifulSoup
    # article > div.uagb-post__inner-wrap > div.uagb-post__image > a: href

    return episode_list

def build_soup(url: str):
    """Retrieve page contents with BeautifulSoup"""
    # TODO: Automate this portion to retrieve URLs from "episodes" page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def process_page(soup: BeautifulSoup) -> tuple:
    """Process page contents"""
    # Get episode information using BeautifulSoup
    title: str = str(soup.title.text[:-23])

    description = soup.select("div.entry-content > p")
    parsed_description: list = parse_shownotes(description)

    # Get episode MP3 file
    audio_big_link = soup.select("a.powerpress_link_d")[0]
    abl_attributes: dict = audio_big_link.attrs
    audio_url: str = abl_attributes["href"]

    return title, parsed_description, audio_url

def export_contents(parsed_description: list, audio_url: str, title: str) -> None:
    """Write podcast data to files"""
    # Change current working directory to an episode folder
    title = "_".join(title.split(":")[0].split())
    os.makedirs(title)
    os.chdir("./" + title)

    # Write show notes to a text file
    write_shownotes(parsed_description, title)

    # Audio to an MP3 file
    retrieve_audio(audio_url, title)

    # Return cwd to program location
    os.chdir("..")

def main():
    """Main script sequence"""
    url: str = input("Please enter a URL: ")
    soup: BeautifulSoup = build_soup(url)

    title: str = ""
    parsed_description: list = []
    audio_url: str = ""
    title, parsed_description, audio_url = process_page(soup)

    export_contents(parsed_description, audio_url, title)

main()
