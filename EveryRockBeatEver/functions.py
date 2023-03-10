from midiutil import MIDIFile
from fractions import Fraction as Fr
from flask import current_app
import random
from copy import deepcopy

from flask import Blueprint

bp = Blueprint("functions", __name__)


def generate_MIDI(USER_PRESETS: dict = None, LOGGER: any = None, print_stmnt: any = None):
    def build_rhythm_space(USER_PRESETS: dict = None, print_stmnt: any = None, LOGGER: any = None):
        """ IN: USER parsed BARS, TEMPO, & PARTIAL DICTIONARY
            OUT: MIDI FILE Write Schematic """

        # DeepCopy USER_PRESETS to Avoid Errors
        UP = deepcopy(USER_PRESETS)

        # Assign USER_PRESETS to variables for Generation;
        bars = int(USER_PRESETS['step1[]']['step1_bars'])
        time_signature = USER_PRESETS['step1[]']['step1_time_signature']
        partial_map = USER_PRESETS['step2[]']['step2_partial_map']
        if print_stmnt:
            print(f'bars: {bars}, time_signature: {time_signature}\n partial_map: {partial_map}\n')
        if LOGGER:
            LOGGER.info(f'bars: {bars}, time_signature: {time_signature}\n partial_map: {partial_map}\n')

        # Partial Map Note Randomizer / Weight Shuffler:
        partial_bowl = []
        for note in partial_map:
            p_wgt = partial_map[note]['WGT']
            if p_wgt not in ['False', 'None', '0']:
                for part in range(int(p_wgt) ** 2):
                    partial_bowl.append(note)

        if print_stmnt:
            print(f'partial bowl: {partial_bowl}\n partial_bowl_set: {set(partial_bowl)}')
        if LOGGER:
            LOGGER.info(f'partial bowl: {partial_bowl}\n partial_bowl_set: {set(partial_bowl)}')

        # Determine which bar we are working on / Instantiate Rhythm Space
        rhythm_space = []
        for bar in range(bars):
            if print_stmnt:
                print(f"\nBar Number: # {bar + 1} / {bars}, Time Signature: {time_signature}\n")  # VERIFY!!
            if LOGGER:
                LOGGER.info(f"\nBar Number: # {bar + 1} / {bars}, Time Signature: {time_signature}\n")

            # Instantiate the Available Bar Length, Rhythm Map, and (initial) PARTIAL BOWL
            bar_rhythm_map, bar_space = [], Fr(time_signature) * 4
            legal_partial_bowl = partial_bowl.copy()
            if print_stmnt:
                print(f"\nLegal Partial Bowl: {legal_partial_bowl}\n")  # VERIFY!!

            # Subtract from the rhythm space until it reaches 0
            while bar_space > 0:

                # LEGALIZE SET(BOWL) to REMOVE Unbreakable PARTIALS. (Prevents LOOP of PARTIAL BREAKABILITY > BAR_SPACE)
                for note in set(legal_partial_bowl):
                    legal_ct = 0
                    for brk in USER_PRESETS['step2[]']['step2_partial_map'][note]['BRK']:
                        if Fr(brk) <= bar_space:
                            legal_ct += 1
                    if legal_ct == 0:
                        legal_partial_bowl = [i for i in legal_partial_bowl if i != note]

                # Choose a RANDOM LEGAL PARTIAL in the LEGAL set (by Partial Fractional Value):
                partial = legal_partial_bowl[random.randint(0, len(legal_partial_bowl) - 1)]
                if print_stmnt:
                    print(f'Stripped legal_partial_bowl: {set(legal_partial_bowl)}\n '
                          f'PARTIAL Selected: {partial}')  # VERIFY!!
                if LOGGER:
                    LOGGER.info(f'Stripped legal_partial_bowl: {set(legal_partial_bowl)}\n '
                                f'PARTIAL Selected: {partial}')

                # The ABOVE LEGAL Conditions ensured that there is enough space for the partial.
                # Now we must consider its Breakability Weight to use...
                # Partial Map Breakability Randomizer / Weight Shuffler:
                brk_bowl, part_space = [], Fr(partial_map[partial]['VAL'])
                for brk in partial_map[partial]['BRK']:
                    brk_wgt = partial_map[partial]['BRK'][brk]

                    # Ensure the breakability can fit in the bar space and is desired
                    brk_space = Fr(brk, _normalize=False).numerator * part_space
                    if brk_wgt not in ['False', 'None', '0'] and brk_space <= bar_space:
                        for part in range(int(brk_wgt)):
                            brk_bowl.append(brk)
                if print_stmnt:
                    print(f'breakability bowl: {brk_bowl}\n brk_bowl_set: {set(brk_bowl)}')
                if LOGGER:
                    LOGGER.info(f'breakability bowl: {brk_bowl}\n brk_bowl_set: {set(brk_bowl)}')

                # If the breakability bowl is empty; the user selected weights and zero breakability...
                if not brk_bowl:

                    # Remove partial from bowl because there is nothing legal left...
                    legal_partial_bowl = [i for i in legal_partial_bowl if i != partial]

                else:
                    # Choose a RANDOM LEGAL PARTIAL BREAKABILITY:
                    breakability = Fr(brk_bowl[random.randint(0, len(brk_bowl) - 1)], _normalize=False)
                    if print_stmnt:
                        print('BREAKABILITY Selected:', breakability)

                    # RANDOMLY Select the BREAKABILITY or its INVERSE (if < Bar Space and > 0):
                    if 0 < (1 - breakability) <= bar_space:
                        shuffle = random.randint(1, 4)
                        if shuffle >= 3:
                            breakability = Fr(breakability.denominator - breakability.numerator,
                                              breakability.denominator, _normalize=False)
                            if print_stmnt:
                                print('Inverse Selected:', breakability)  # VERIFY!!
                        else:
                            if print_stmnt:
                                print('Standard Select:', breakability)  # VERIFY!!
                    else:
                        if print_stmnt:
                            print('Standard Select:', breakability)  # VERIFY!!

                    # Partial Space in range(BREAKABILITY (NUMERATOR)) = NOTE BLOCK to Append!
                    note_block = []
                    for i in range(breakability.numerator):
                        note_block.append(part_space)
                    bar_rhythm_map.append(note_block)

                    # Subtract the NOTE BLOCK from the BAR SPACE:
                    bar_space -= sum(note_block)
                    if print_stmnt:
                        print(f'===\nBAR RHYTHM MAP:, {bar_rhythm_map}\nBAR SPACE Remaining: {bar_space}'
                              f'\nNOTE BLOCK selected:, {note_block}\n===')  # VERIFY!!
                    if LOGGER:
                        LOGGER.info(f'===\nBAR RHYTHM MAP:, {bar_rhythm_map}\nBAR SPACE Remaining: {bar_space}'
                                    f'\nNOTE BLOCK selected:, {note_block}\n===')

            # Tally the PARTIAL BREAKABILITY Assignments to Finish the BAR
            rhythm_space.append(bar_rhythm_map)
            if print_stmnt:
                print(f'***RHYTHM SPACE ( Bar # {bar + 1} / {bars} Time Signature: {time_signature} ):'
                      f'\n {rhythm_space}\n')
            if LOGGER:
                LOGGER.info(f'***RHYTHM SPACE ( Bar # {bar + 1} / {bars} Time Signature: {time_signature} ):'
                            f'\n {rhythm_space}\n')
        if print_stmnt:
            print('\n---&&&___RHYTHM SPACE FILLED___&&&---\n')
        if LOGGER:
            LOGGER.info('\n---&&&___RHYTHM SPACE FILLED___&&&---\n')
        return rhythm_space, time_signature

    def rock_MIDI(rhythm_space: list, tempo: float = 120, time_signature: str = '4/4',
                  LOGGER: any = None, print_stmnt: any = None):
        """ IN: Rhythm Space MIDI Map / Partial Breakability (Step 2)
            OUT: MIDI File for USER to download OR regenerate (FUTURE: Playback)"""

        track, channel = 0, 9  # Channel 9 is the percussion channel
        degrees_list = [36, 38]  # FUTURE TIMBRE MAP (i.e. 36 = Kick #1, 38 = Snare #2)
        volume = 100  # FUTURE DYNAMICS MAP [0 - 127]
        time = 0  # Where the Note is Placed (i.e. Count #1 = 0, Count #2 = 1)
        duration = 0  # How long the Note is held (i.e. Quarter = 1.0, 8th = 0.5)
        # tempo = USER_PRESETS['tempo']  # Placeholder for USER Input
        bpm = random.randint(80, 160)  # In BPM

        # Parse Time Signature -- Must exist in the power of 2**
        ts_power2 = [str(2 ** i) for i in range(0, 7)]
        ts_num, ts_den = time_signature.split('/')[0], str(ts_power2.index(time_signature.split('/')[1]))

        MyMIDI = MIDIFile(1, file_format=1)  # One track, defaults to format 1 (tempo track created)
        MyMIDI.addTempo(track=1, time=0, tempo=bpm)
        bar_ct = 0

        for bar in rhythm_space:
            bar_ct += 1
            if print_stmnt:
                print(f"\n+++ BAR #{bar_ct} / {len(rhythm_space)}, Time Signature: {ts_num}/{ts_den} +++\n")
            if LOGGER:
                LOGGER.info(f"\n+++ BAR #{bar_ct} / {len(rhythm_space)}, Time Signature: {ts_num}/{ts_den} +++\n")
            MyMIDI.addTimeSignature(track=1, time=time, numerator=int(ts_num), denominator=int(ts_den),
                                    clocks_per_tick=24)
            for note_group in bar:
                for partial in note_group:
                    degrees = degrees_list[random.randint(0, len(degrees_list) - 1)]
                    duration = partial
                    if print_stmnt:
                        print(f'Insert Time: {time}, Partial / Duration: {partial}, Pitch: {degrees}')
                    if LOGGER:
                        LOGGER.info(f'Insert Time: {time}, Partial / Duration: {partial}, Pitch: {degrees}')
                    MyMIDI.addNote(track, channel, degrees, time, duration, volume)
                    time += duration
                    if print_stmnt:
                        print(f'Duration Added to Time!: {time}')
                    if LOGGER:
                        LOGGER.info(f'Duration Added to Time!: {time}')

        # Reset time to overwrite with hi hats test -- MVP
        time = 0

        for bar in rhythm_space:
            if print_stmnt:
                print(f"\n[[[ Just Adding Hi Hats ]]]\n")

            for i in range(8):
                degrees = 42
                duration = 0.5
                MyMIDI.addNote(track, channel, degrees, time, duration, volume)
                time += duration

        return MyMIDI

    # -- Testing / FUNCTION Drivers --

    # Build MIDI File
    rhythm_space, time_signature = build_rhythm_space(USER_PRESETS=USER_PRESETS,
                                                      LOGGER=LOGGER, print_stmnt=print_stmnt)
    MIDI_file = rock_MIDI(rhythm_space=rhythm_space, time_signature=time_signature,
                          LOGGER=LOGGER, print_stmnt=print_stmnt)

    # Temp MIDI File Overwrites. Utilizes USER Session ID
    session_id = USER_PRESETS['session_id']
    MIDI_filepath = f'{current_app.instance_path}/users/usr_{session_id}/temp_MIDI_File.mid'

    # Write the MIDI File if the directory exists
    with open(MIDI_filepath, 'wb') as f:
        MIDI_file.writeFile(f)

    return MIDI_filepath
