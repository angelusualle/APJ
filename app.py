import logging
from flask import Flask
from flask_ask import Ask, statement, audio, current_stream
import requests


app = Flask(__name__)
ask = Ask(app, "/")

logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)

APIUrl = 'https://api.desiringgod.org/'


@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)



@ask.intent("PlayLatestIntent")
def playLatest():
    url = APIUrl + '/v0/collections/p1ocqa9u/resources?page[size]=1&page[number]=1'
    r = requests.get(url, headers={'Authorization': 'Token token="e6f600e7ee34870d05a55b28bc7e4a91"'})
    if r.status_code != 200:
        return statement('I am having trouble searching. Please try again later.')
    data = r.json()
    soundURL = data['data'][0]['attributes']['audio_download_url']
    return audio('Playing newest ask pastor john episode.').play(soundURL)

    return "{}", 200


@ask.intent("PlayEpisodeIntent")
def play(episodenumber):
    url = APIUrl + '/v0/collections/p1ocqa9u/resources?page[size]=99999&page[number]=1' #note its max assumed for this life :)
    r = requests.get(url, headers={'Authorization': 'Token token="e6f600e7ee34870d05a55b28bc7e4a91"'})
    if r.status_code != 200:
        return statement('I am having trouble searching. Please try again later.')
    data = r.json()
    soundURL = ''
    for episode in data['data']:
        episodeNum = episode['attributes']['apj_episode_number']
        if str(episodeNum) == episodenumber:
            soundURL = episode['attributes']['audio_download_url']
            break
    if soundURL == '':
        return statement('Episode ' + episodenumber + 'Not found.')
    return audio('Playing Ask Pastor John episode ' + episodenumber).play(soundURL)


@ask.intent("AskPastorJohnIntent")
def ask(searchterm):
    url = APIUrl + '/v0/collections/p1ocqa9u/resources?page[size]=99999&page[number]=1'  # note its max assumed for this life :)
    r = requests.get(url, headers={'Authorization': 'Token token="e6f600e7ee34870d05a55b28bc7e4a91"'})
    if r.status_code != 200:
        return statement('I am having trouble searching. Please try again later.')
    data = r.json()
    titles = []
    for episode in data['data']:
        title = episode['attributes']['title']
        if searchterm.upper() in title.upper():
            titles.append('Episode ' + str(episode['attributes']['apj_episode_number']) + ' ' + title)
            if len(titles) > 3:
                break;
    return statement('Here are some Ask Pastor John Episodes related to ' + searchterm + ': ' + ', '.join(titles))


if __name__ == '__main__':
    app.run(debug=True)
