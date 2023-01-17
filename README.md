# Every Rock Beat Ever ( Drums )
[![Pylint](https://github.com/cbradiodrums/EveryRockBeatEver/actions/workflows/pylint.yml/badge.svg)](https://github.com/cbradiodrums/EveryRockBeatEver/actions/workflows/pylint.yml)
[![Pytest](https://github.com/cbradiodrums/EveryRockBeatEver/.github/workflows/pytest.yml/badge.svg)](https://github.com/cbradiodrums/EveryRockBeatEver/.github/workflows/pytest.yml)
- <b>Objective</b>: Generate Unique and Interesting Rock Drum Beat MIDI Files
- <b>Language</b>: Python, HTML, CSS
- <b>License</b>: GNU
- <b>Filetype(s)</b>: .PY, .HTML, Dockerfile, JSON
- APP Video Demo: https://www.loom.com/share/ac3e25eed1494cfca877b65aebff30eb
- <a href="https://urchin-app-z5fak.ondigitalocean.app/">
                <b>Deployment Server</b></a>
---
### Contributor(s):
- Chris Burrows (<i> Lead Programmer / Design)</i>
---
### Setup:
Local Machine Instance -- Docker
1. Git Clone this Repository
2. Create `.env` in top level using `dotenv_template.txt`
OR pass in environment variables (CONTEXT=LOCAL)
3. Install Docker https://docs.docker.com/get-docker/
4. In your terminal, cd (change directory) to the parent 'EveryRockBeatEver'
    * GitBash may be useful for a terminal application: https://git-scm.com/downloads
5. Run the Dockerfile command `docker build -t erbe .`
6. Run the Dockerfile command `docker run -p 5000:5000 erbe`
7. Open a browser and navigate to the URL: `localhost:5000`

Local Machine Instance -- IDE
1. Git Clone this Repository
2. Create `.env` in top level using `dotenv_template.txt`
3. In IDE Terminal: <br>
`$ python -m venv venv  # Virtual environment` <br>
`$ source venv/Scripts/activate`  # (bash terminal) <br>
`$ pip install -r requirements.txt` <br>
`$ flask --app EveryRockBeatEver --debug run`  # (debug tag optional)

Cloud / Deployment Instance
- Follow all the above steps, specifying `CONTEXT=CLOUD` in `.env`
- Make sure your server is configured with the necessary CORS parameters.

Test Both Environments Simultaneously
- Follow all the above steps, specifying `CONTEXT=FULL` in `.env`

---
### How To:
1. From **Home**, click on the `Quick Generate` Button.
2. Now, a MIDI File displays with Playback options or a Download Option.<br>
It should be a rock drum beat within a tempo of 80 - 160 BPM.
3. Feel free to repeat, using the `Quick Generate` to get a new beat!

---
### Additional Features:

There are additional plans to integrate more user control over the algorithm using
timbres, dynamics, breakability, and subdivisions. Machine Learning is also a prospect.

---
### Resources

This project would not have been possible without the use of some fantastic musical packages:<br>
MIDIUtil: https://midiutil.readthedocs.io/en/1.2.1/ <br>
html-midi-player: https://cifkao.github.io/html-midi-player/

---
### About
#### The Inspiration<br>
The "Every Rock Beat Ever" App was originated from the idea of creating an algorithm as the rhythmic foundation 
for a progressive metal album. The initial "code base" was a simple calculator in a Google Sheets field,
but after its Author attended an online Data Science Bootcamp it was quickly adopted into a Python App.
#### The Author<br>
Chris Burrows is an all around drummer with specialization in Progressive Metal and a Programmer with budding 
interests in Software Development and Data Science. You can also check out his contributions in musical projects 
on various platforms:
<br><br>- <a href="https://open.spotify.com/artist/5B7dQ1AUrxKGunRPsh01Jp?si=D24JJj3xRWWNpbmTz7GYAw">
                Coma Cluster Void (Former Drummer)</a>
    <br>- <a href="https://thoren.bandcamp.com/">
                Thoren (Current Drummer)</a>
    <br>- <a href="https://vihaanmusic.com/">
                Vihaan (Former Session / Live Drummer) </a>
    <br>- <a href="https://ropband.bandcamp.com/">
                R.O.P. (Former Session / Live Drummer)</a>
    <br>- <a href="https://open.spotify.com/artist/5pFx6otrNwzwA4x2gwXjeW?si=ntDvLWwQQ-WyxLi7jzI61A">
                Wonderbox (Former Producer / Engineer)</a>









