# Every Drum Beat ( In Development )
[![Pylint](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pylint.yml/badge.svg)](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pylint.yml)
[![Pytest](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pytest.yml/badge.svg)](https://github.com/cbradiodrums/Row_Eliminator_App/actions/workflows/pytest.yml)
- <b>Objective</b>: Generate Unique and Interesting DrumBeats
- <b>Language</b>: Python
- <b>License</b>: GNU
- <b>Filetype(s)</b>: .PY, .HTML, .XLS, & .CSV
- <b>Video Tutorial</b>:  ![Coming Soon]() 
- <b>Full Wiki Manual</b>:  ![Coming Soon]()
---
### Contributor(s):
- Chris Burrows (<i> Lead Programmer / Design)</i>
---
### Contents:
#### content.file
  - Description *00/00/202X
#### LICENSE
#### CHANGELOG.MD
  - Patch updates, Bug Fixes, and Design Implementations
---
### Setup / How-To:
1. Git Clone this Repository
2. Install Docker https://docs.docker.com/get-docker/
   * Setup Video: https://www.loom.com/share/2e4699aff1724867a7e99e79832aa826
3. In your terminal, cd (change directory) to the parent 'everydrumbeat_mvp'
    * GitBash may be useful for a terminal application: https://git-scm.com/downloads
4. Run the Dockerfile command `docker build -t ede_mvp .`
5. Run the Dockerfile command `docker run -p 5000:5000 ede_mvp`
6. Open a browser and navigate to the URL: `localhost:5000`
7. Follow the page displays and Submit all parameters
   * DEMO Video: https://www.loom.com/share/15da9e8fcd534940953618a748b446c4
8. 'Generate MIDI' button will write the MIDI file into the 'MIDI_files' folder.
---
### User Stories #1: IDEAL
The **IDEAL** USER story would look like this:

**LOGIN / PROFILE DASHBOARD**
1. USER SIGNS UP, registering EMAIL, LOGIN NAME, and PASSWORD
2. USER is presented DASHBOARD that houses all SAVED BEATS (and type ie. `rhythm_space`, `partial_preset`, etc.)

**BEAT INITIALIZATION OPTIONS**
1. USER can choose to GLOBAL LOAD a SAVED BEAT, or RANDOMLY generate
a STANDARD, ADVANCED, LUDICROUS, or POPULAR preset.
2. USER can choose to GLOBALLY SAVE their constructed beat STATE at any time.

**GENERATE SUBDIVISIONS (PARTIALS)**
1. USER chooses if they would like a PRESET, SHUFFLE, or create CUSTOM
2. USER chooses number of BARS they would like to see
3. USER chooses Time Signature that is the base
4. USER chooses RANDOM SEED (which determines how the `rhythm space` is generated) 

**GENERATE RHYTHM SPACE (PARTIALS)**
- We use SUBDIVISIONS as that's the more common verbiage; PARTIALS is synonymous.
- Here, the MIDI NOTE DISPLAY is active.

1. USER chooses if they would like a PRESET, SHUFFLE or CUSTOM
2. USER chooses the PARTIALS they would like
3. USER chooses each PARTIAL's BREAKABILITY

**GENERATE VOICINGS**
1. USER chooses if they would like a **FILL MODE** PRESET, SHUFFLE, or CUSTOM
2. USER chooses if they would like a **WEIGHT** PRESET, SHUFFLE, or CUSTOM
3. USER chooses each `timbre_weight` (including `RESTS`)

**ASSIGN DYNAMICS**
1. USER chooses if they would like a PRESET, SHUFFLE or CUSTOM
2. USER chooses each `dynamic_weight`

**MORPH ACCENTS**
1. USER chooses if they would like to SHUFFLE or CUSTOM
2. USER chooses each `morph_weight`

**PLAYBACK / EXPORT**
1. USER can PLAY, PAUSE, RESTART, STOP, or ADJUST VOLUME
2. USER can ADJUST TEMPO
3. USER can SAVE / LOAD BEAT STATE or EXPORT / IMPORT MIDI

**LINKS**
1. USER can visit ABOUT to learn about the PATHOS record and APP AUTHORS
2. USER can visit TUTORIAL to learn how to use the program and visit the DOCUMENTATION WIKI
3. USER can visit RANKINGS to see the most popular BEAT STATES in the USER DATABASE
---
### User Stories #2: MVP
The **Minimum Viable Product** USER story would look like this:

**DOCKERFILE FOR SUPER USER**
1. DEPLOYMENT is desirable, but a DOCKERFILE may be the MVP.

**GENERATE SUBDIVISIONS (PARTIALS)**
1. USER chooses number of BARS they would like to see
2. TIME SIGNATURE LOCKED at 4/4
3. RANDOM SEED locked at integer values

**GENERATE RHYTHM SPACE (PARTIALS)**
- NO MIDI NOTE DISPLAY

1. USER chooses the PARTIALS they would like
2. USER chooses each PARTIAL's BREAKABILITY

**GENERATE VOICINGS**

1. `timbre_weight` is automatically assigned for USER INTERPRETATION

**ASSIGN DYNAMICS**
- Expansion Feature

**MORPH ACCENTS**
- Expansion Feature

**PLAYBACK / EXPORT**
- PLAYBACK is an Expansion Feature
1. USER is directed to DOWNLOAD the MIDI FILE.

**LINKS**
- RANKINGS are an Expansion Feature
1. USER can visit ABOUT to learn about the PATHOS record and APP AUTHORS
2. USER can visit TUTORIAL to learn how to use the program and visit the DOCUMENTATION WIKI







