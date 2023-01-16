# Every Rock Beat Ever ( Drums )
[![Pylint](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pylint.yml/badge.svg)](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pylint.yml)
[![Pytest](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pytest.yml/badge.svg)](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pytest.yml)
- <b>Objective</b>: Generate Unique and Interesting Rock Drum Beat MIDI Files
- <b>Language</b>: Python
- <b>License</b>: GNU
- <b>Filetype(s)</b>: .PY, .HTML, .XLS, & .CSV
- <b>Deployment Server</b>:  ![Coming Soon]()
- <b>Video Tutorial</b>:  ![Coming Soon]()
- <b>Full Wiki Manual</b>:  ![Coming Soon]()
---
### Contributor(s):
- Chris Burrows (<i> Lead Programmer / Design)</i>
---
### Setup:
Local Machine Instance
1. Git Clone this Repository
2. Create `.env` in top level using `dotenv_template.txt`
OR pass in environment variables (CONTEXT=LOCAL)
3. Install Docker https://docs.docker.com/get-docker/
   * Setup Video: https://www.loom.com/share/2e4699aff1724867a7e99e79832aa826
4. In your terminal, cd (change directory) to the parent 'EveryRockBeatEver'
    * GitBash may be useful for a terminal application: https://git-scm.com/downloads
5. Run the Dockerfile command `docker build -t erbe .`
6. Run the Dockerfile command `docker run -p 5000:5000 erbe`
7. Open a browser and navigate to the URL: `localhost:5000`
8. Follow the page displays and Submit all parameters
   * DEMO Video: https://www.loom.com/share/15da9e8fcd534940953618a748b446c4

Cloud / Deployment Instance
- Follow all the above steps, specifying CONTEXT=CLOUD in `.env`
- Make sure your server is configured with the necessary CORS parameters.

Test Both Environments Simultaneously
- Follow all the above steps, specifying CONTEXT=FULL in `.env`

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

This project would not have been possible without the use of some fantastic musical packages:
MIDIUtil: https://midiutil.readthedocs.io/en/1.2.1/ <br>
html-midi-player: https://cifkao.github.io/html-midi-player/

---
### 

This project would not have been possible without the use of some fantastic musical packages:
MIDIUtil: https://midiutil.readthedocs.io/en/1.2.1/
html-midi-player: https://cifkao.github.io/html-midi-player/










