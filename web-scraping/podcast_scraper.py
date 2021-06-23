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
    # TODO: Make this string work to create a new file
    file_name: str = title + ".txt"
    with open("notes.txt", "w") as export_file:
        for p in parsed_description:
            export_file.write(f"{p}\n")

def retrieve_audio(audio_url: str, title: str) -> None:
    """
    Given a valid url, retrieve podcast audio and write to
    a local mp3 file named with the given title.
    """
    audio_object = requests.get(audio_url)
    # TODO: Make this string work to create a new file
    episode_name: str = title + ".mp3"

    with open("audio.mp3", "wb") as export_audio:
        audio_object = requests.get(audio_url)
        export_audio.write(audio_object.content)

def get_episodes(url: str) -> list:
    """Make list of episode URLs"""
    soup = build_soup(url)
    episode_list: list = []

    # Select multiple items using BeautifulSoup
    tags = soup.find_all("div", {"class": "uagb-post__image"})
    episode_list = [tag.findChild("a")["href"] for tag in tags]
    
    return episode_list

def build_soup(url: str):
    """Retrieve page contents with BeautifulSoup"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def process_page(soup: BeautifulSoup) -> tuple:
    """Process page contents"""
    # Get episode information using BeautifulSoup
    title: str = str(soup.title.text[:-23])

    # Check whether page was valid, if not, raise error and return
    if title == "Page not found":
        raise Exception("Episode not found, redirected to 404 page")
        return -1

    # Get episode show notes
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

def process_episode(url: str) -> str:
    """Process each episode given its URL"""
    soup: BeautifulSoup = build_soup(url)

    title: str = ""
    parsed_description: list = []
    audio_url: str = ""

    # Monitoring statement: start of episode processing
    print(f"Now Processing episode at {url}")

    # Get episode information from the page; if not found, return error
    try:
        title, parsed_description, audio_url = process_page(soup)
    except TypeError:
        return f"Episode at {url} not found, check URL for errors"

    # Export the episode notes and audio to files
    export_contents(parsed_description, audio_url, title)

    # Return with success message
    return f"{title} Processed Successfully"

def main():
    """Main script sequence"""
    mjb_episodes_url: str = "https://messyjesusbusiness.com/podcast-episodes/"
    episodes: list = get_episodes(mjb_episodes_url)

    with open("config/saved_episode_urls.txt", "r+") as saved_episodes:
        # Create a list of episode URL's that have already been processed
        saved_episodes_list: list = saved_episodes.read().split()

        # For each episode listed, process the ones not yet processed
        for episode in episodes[:3]:
            if episode not in saved_episodes_list:
                result: str = process_episode(episode)
                print(result)
                saved_episodes.write(f"{episode}\n")
            else:
                print(f"Episode at {url} has previously been processed, continuing to next episode")   

main()
