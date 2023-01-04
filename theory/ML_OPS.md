# Music Theory meets Machine Learning: "ML OPS"
- <b>Objective</b>: Lay out some initial theory for how this APP could tune with Machine Learning.
---
### Contributor(s):
- Chris Burrows (<i> Project Lead / Programmer</i> )
---
### Preface:
  The parameters of the Every Drum Beat ever include Genre (like Rock or Jazz) or 
 Artists (like, Meshuggah or AC/DC). In order to achieve this, we need to:
1) Clean / Archive the SAMPLE DATA
2) Transform / Encode the SAMPLE DATA
3) Compile the SAMPLE DATA into a Training / Test / Validation Set
4) Instantiate the Model
5) Make Model Predictions
6) Collect Model Feedback
7) Repeat above steps with NEW DATA
---
## Explanation of Preface Steps:
### 1) Clean / Archive the SAMPLE DATA

What data would we start with? 
- Artist
  - Ensure that the MIDI files are accurate of the Artist's songs
    - Pros: Very specific dataset
    - Cons: Very small dataset; HEAVILY reliant on USER FEEDBACK to produce new material
- Genre
   - Utilize a comping book / online sources to produce MIDI
      - Pros: Very large dataset
      - Cons: Less specific

Artist Ideas: Meshuggah, AC/DC, Rush, Led Zeppelin, The Beatles, Iron Maiden
Genre Ideas: Rock, Jazz, Metal

### 2) Transform / Encode the SAMPLE DATA

The MIDI File must be parsed into a format that can be interpreted by a machine. Initial thoughts are reproducing
a DataFrame of Time (Note On / Note Off), Duration, Tempo, Time Signature, Volume and Pitch (Drumset Piece).

Here, our observational data is actually comprised of arrays.
<table>
   <tr>
      <th colspan="6" style="text-align: center; font-size: large">
         AC/DC MIDI List
      </th>
   </tr>
   <tr>
      <th>MIDI File</th>
      <th>Tempo</th>
      <th>Time Data</th>
      <th>Duration Data</th>
      <th>Pitch</th>
      <th>Volume</th>
   </tr>
   <tr>
      <td>"You Shook Me All Night Long"</td>
      <td>105</td>
      <td>[0, 1, 2.5, 3...]</td>
      <td>[1, 1.5, .5, 1...]</td>
      <td>[36, 38, 36, 38...]</td>
      <td>[100, 100, 100, 100...]</td>
   </tr>
   <tr>
      <td>"Back in Black"</td>
      <td>85</td>
      <td>[0, 1, 2, 3...]</td>
      <td>[1, 1, 1, 1...]</td>
      <td>[36, 38, 36, 38...]</td>
      <td>[100, 100, 100, 100...]</td>
   </tr>
</table>

#### Encoding Considerations:

Perhaps it would be better to flatten a table by pitch, as multiple pitches can occupy a single point in time.
For example, if the Snare, Tom, and Kick Drum were all hit on Beat 1, it would look like: `{Time: 0, Pitch: [36, 38, 43]}`

To flatten this for Machine Learning, an 8th Note High Hat Groove, with "4 on the floor" Kick Drums and Snares on the 
"Backbeats" (2 and 4) would look like:

<table>
   <tr>
      <th colspan="6" style="text-align: center; font-size: large">
         Rock Groove: Array-Like
      </th>
   </tr>
   <tr>
      <th colspan="8" style="justify-content: center">
         <img src="https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/RockBeat.PNG?raw=true" 
            alt="8th Note HH, 4 On the Floor Kick, Snare Backbeats"/>
      </th>
   </tr>
   <tr>
      <th>Time</th>
      <th>Duration</th>
      <th>Pitch0</th>
      <th>Pitch1</th>
      <th>Pitch2</th>
   </tr>
   <tr>
      <td>0</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>0</td>
   </tr>
   <tr>
      <td>0.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>1</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>38</td>
   </tr>
   <tr>
      <td>1.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>2</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>0</td>
   </tr>
   <tr>
      <td>2.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>3</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>38</td>
   </tr>
   <tr>
      <td>3.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
   </tr>
</table>

Or maybe more necessarily, One Hot Encoded?

<table>
   <tr>
      <th colspan="6" style="text-align: center; font-size: large">
         Rock Groove: OHE
      </th>
   </tr>
   <tr>
      <th colspan="8" style="justify-content: center">
         <img src="https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/RockBeat.PNG?raw=true" 
            alt="8th Note HH, 4 On the Floor Kick, Snare Backbeats"/>
      </th>
   </tr>
   <tr>
      <th>Time</th>
      <th>Duration</th>
      <th>Pitch_36</th>
      <th>Pitch_38</th>
      <th>Pitch_42</th>
   </tr>
   <tr>
      <td>0</td>
      <td>0.5</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
   </tr>
   <tr>
      <td>0.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
   </tr>
   <tr>
      <td>1</td>
      <td>0.5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
   </tr>
   <tr>
      <td>1.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
   </tr>
   <tr>
      <td>2</td>
      <td>0.5</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
   </tr>
   <tr>
      <td>2.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
   </tr>
   <tr>
      <td>3</td>
      <td>0.5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
   </tr>
   <tr>
      <td>3.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
   </tr>
</table>

But wait, we haven't even accounted VOLUME. The hi hats could alternate between accented and ghost notes, while
the snare is consistent rim shots! <br>
`{Time: 0, Pitch: {36:100}`, `{Time: 0, Pitch: {42:100}`, `{Time: 0.5, Pitch: {42:40}`, `{Time: 1, Pitch: {38:120}`<br>
`{Time: 0, Pitch: {36:100}`, `{Time: 0, Pitch: {42:100}`, `{Time: 0.5, Pitch: {42:40}`, `{Time: 1, Pitch: {38:120}`<br>
`{Time: 0, Pitch: {36:100}`, `{Time: 0, Pitch: {42:100}`, `{Time: 0.5, Pitch: {42:40}`, `{Time: 1, Pitch: {38:120}`<br>
`{Time: 0, Pitch: {36:100}`, `{Time: 0, Pitch: {42:100}`, `{Time: 0.5, Pitch: {42:40}`, `{Time: 1, Pitch: {38:120}`<br>

<table>
   <tr>
      <th colspan="8" style="text-align: center; font-size: large">
         Rock Groove: Array-Like
      </th>
   </tr>
   <tr>
      <th colspan="8" style="justify-content: center">
         <img src="https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/RockBeat_Accented.PNG?raw=true" 
            alt="8th Note HH, 4 On the Floor Kick, Snare Backbeats"/>
      </th>
   </tr>
   <tr>
      <th>Time</th>
      <th>Duration</th>
      <th>Pitch0</th>
      <th>Pitch1</th>
      <th>Pitch2</th>
      <th>Volume0</th>
      <th>Volume1</th>
      <th>Volume2</th>
   </tr>
   <tr>
      <td>0</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>0</td>
      <td>100</td>
      <td>100</td>
      <td>0</td>
   </tr>
   <tr>
      <td>0.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>1</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>38</td>
      <td>100</td>
      <td>100</td>
      <td>127</td>
   </tr>
   <tr>
      <td>1.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>2</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>0</td>
      <td>100</td>
      <td>100</td>
      <td>0</td>
   </tr>
   <tr>
      <td>2.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
      <td>0</td>
      <td>0</td>
   </tr>
   <tr>
      <td>3</td>
      <td>0.5</td>
      <td>42</td>
      <td>36</td>
      <td>38</td>
      <td>100</td>
      <td>100</td>
      <td>127</td>
   </tr>
   <tr>
      <td>3.5</td>
      <td>0.5</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
      <td>0</td>
      <td>0</td>
   </tr>
</table>
<table>
   <tr>
      <th colspan="8" style="text-align: center; font-size: large">
         Rock Groove: OHE
      </th>
   </tr>
   <tr>
      <th colspan="8" style="justify-content: center">
         <img src="https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/RockBeat_Accented.PNG?raw=true" 
            alt="8th Note HH, 4 On the Floor Kick, Snare Backbeats"/>
      </th>
   </tr>
   <tr>
      <th>Time</th>
      <th>Duration</th>
      <th>Pitch_36</th>
      <th>Pitch_38</th>
      <th>Pitch_42</th>
      <th>Volume_36</th>
      <th>Volume_38</th>
      <th>Volume_42</th>
   </tr>
   <tr>
      <td>0</td>
      <td>0.5</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>100</td>
      <td>0</td>
      <td>100</td>
   </tr>
   <tr>
      <td>0.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
   </tr>
   <tr>
      <td>1</td>
      <td>0.5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>100</td>
      <td>127</td>
      <td>100</td>
   </tr>
   <tr>
      <td>1.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
   </tr>
   <tr>
      <td>2</td>
      <td>0.5</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>100</td>
      <td>0</td>
      <td>100</td>
   </tr>
   <tr>
      <td>2.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
   </tr>
   <tr>
      <td>3</td>
      <td>0.5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>100</td>
      <td>127</td>
      <td>100</td>
   </tr>
   <tr>
      <td>3.5</td>
      <td>0.5</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>40</td>
   </tr>
</table>

But wait, we haven't even considered individual note DURATION. Fortunately, duration only matters in drum set 
literature in instances like choking a cymbal. You can't truncate the transient waveform of the drum sound through 
much other than *fairly* obscure techniques.

**However**, we need duration to appease a pleasant format for a typical MIDI Sequencer. We should be able to achieve
this by subtracting the difference in Time for now.

### 3) Compile the SAMPLE DATA into a Training / Test / Validation Set

So we,ve figured out a way to Clean, Transform, and Encode our data... but how do we reflect one song in a single row..?

<table>
   <tr>
      <th colspan="6" style="text-align: center; font-size: large">
         AC/DC MIDI List + Rock Beat
      </th>
   </tr>
   <tr>
      <th>MIDI File</th>
      <th>Tempo</th>
      <th>Time Data</th>
      <th>Duration Data</th>
      <th>Pitch</th>
      <th>Volume</th>
   </tr>
   <tr>
      <td>"You Shook Me All Night Long"</td>
      <td>105</td>
      <td>[0, 1, 2.5, 3...]</td>
      <td>[1, 1.5, .5, 1...]</td>
      <td>[36, 38, 36, 38...]</td>
      <td>[100, 100, 100, 100...]</td>
   </tr>
   <tr>
      <td>"Back in Black"</td>
      <td>85</td>
      <td>[0, 1, 2, 3...]</td>
      <td>[1, 1, 1, 1...]</td>
      <td>[36, 38, 36, 38...]</td>
      <td>[100, 100, 100, 100...]</td>
   </tr>
    <tr>
      <td>"Accented Rock Beat (from Above)"</td>
      <td>130</td>
      <td>[0, 0.5, 1, 1.5...]</td>
      <td>[0.5, 0.5, 0.5, 0.5...]</td>
      <td>[36, 42, 38, 42...]</td>
      <td>[100, 40, 120, 40...]</td>
   </tr>
</table>

We may have to flatten our data horizontally *yet again*! Let's look at how this might appear
for the first three 8th notes in each song.

<table>
   <tr>
        <th colspan="20" style="text-align: center; font-size: large">
            AC/DC MIDI List + Rock Beat: Array-Like
        </th>
   </tr>
   <tr>
        <th>MIDI File</th>
        <th>Tempo</th>
        <th>Time_0</th>
        <th>Pitch_0_0</th>
        <th>Volume_0_0</th>
        <th>Pitch_0_1</th>
        <th>Volume_0_1</th>
        <th>Time_0.5</th>
        <th>Pitch_0.5_0</th>
        <th>Volume_0.5_0</th>
        <th>Time_1</th>
        <th>Pitch_1_0</th>
        <th>Volume_1_0</th>
        <th>Pitch_1_1</th>
        <th>Volume_1_1</th>
        <th>Pitch_1_2</th>
        <th>Volume_1_2</th>
   </tr>
   <tr>
        <td>"You Shook Me All Night Long"</td>
        <td>105</td>
        <td>1</td>
        <td>36</td>
        <td>100</td>
        <td>42</td>
        <td>100</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>38</td>
        <td>120</td>
        <td>42</td>
        <td>100</td>
        <td>0</td>
        <td>0</td>
   </tr>
   <tr>
        <td>"Back in Black"</td>
        <td>85</td>
        <td>1</td>
        <td>36</td>
        <td>100</td>
        <td>42</td>
        <td>100</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>38</td>
        <td>120</td>
        <td>42</td>
        <td>100</td>
        <td>0</td>
        <td>0</td>
   </tr>
    <tr>
        <td>"Accented Rock Beat (from Above)"</td>
        <td>130</td>
        <td>1</td>
        <td>36</td>
        <td>100</td>
        <td>42</td>
        <td>100</td>
        <td>1</td>
        <td>42</td>
        <td>40</td>
        <td>1</td>
        <td>36</td>
        <td>100</td>
        <td>42</td>
        <td>100</td>
        <td>38</td>
        <td>120</td>
   </tr>
</table>

<table>
   <tr>
        <th colspan="20" style="text-align: center; font-size: large">
            AC/DC MIDI List + Rock Beat: OHE
        </th>
   </tr>
   <tr>
        <th>MIDI File</th>
        <th>Tempo</th>
        <th>Time_0</th>
        <th>Pitch_0_36</th>
        <th>Volume_0_36_40</th>
        <th>Volume_0_36_100</th>
        <th>Volume_0_36_120</th>
        <th>Pitch_0_38</th>
        <th>Volume_0_38_40</th>
        <th>Volume_0_38_100</th>
        <th>Volume_0_38_120</th>
        <th>Pitch_0_42</th>
        <th>Volume_0_42_40</th>
        <th>Volume_0_42_100</th>
        <th>Volume_0_42_120</th>
        <th>Time_0.5</th>
        <th>Pitch_0.5_36</th>
        <th>Volume_0.5_36_40</th>
        <th>Volume_0.5_36_100</th>
        <th>Volume_0.5_36_120</th>
        <th>Pitch_0.5_38</th>
        <th>Volume_0.5_38_40</th>
        <th>Volume_0.5_38_100</th>
        <th>Volume_0.5_38_120</th>
        <th>Pitch_0.5_42</th>
        <th>Volume_0.5_42_40</th>
        <th>Volume_0.5_42_100</th>
        <th>Volume_0.5_42_120</th>
        <th>Time_1</th>
        <th>Pitch_1_36</th>
        <th>Volume_1_36_40</th>
        <th>Volume_1_36_100</th>
        <th>Volume_1_36_120</th>
        <th>Pitch_1_38</th>
        <th>Volume_1_38_40</th>
        <th>Volume_1_38_100</th>
        <th>Volume_1_38_120</th>
        <th>Pitch_1_42</th>
        <th>Volume_1_42_40</th>
        <th>Volume_1_42_100</th>
        <th>Volume_1_42_120</th>
   </tr>
   <tr>
        <td>"You Shook Me All Night Long"</td>
        <td>105</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
   </tr>
   <tr>
        <td>"Back in Black"</td>
        <td>85</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
   </tr>
    <tr>
        <td>"Accented Rock Beat (from Above)"</td>
        <td>130</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
        <td>0</td>
        <td>1</td>
        <td>1</td>
        <td>0</td>
        <td>1</td>
        <td>0</td>
   </tr>
</table>

#### OHE vs. Array-Like
A One Hot Encoded DataFrame *may* be preferable over an array-like, as we have a categorical truth at each space in
time whether a note has occurred. This could make compiling the DataFrame easier, it just depends on the algorithm to
unflatten it back into a MIDI File.

### 4) Instantiate the Model

Alright! So we have a method to display our song data within one observational row...but, how do we ensure
that our Model can make reasonable predictions for features NOT utilized in our DataFrame?? ( Think of this akin to
making sure we aren't simply removing / keeping notes to an AC/DC drum lick, but potentially *adding* notes that
would make sense as well! )

#### Template DataFrame
While a flattened MIDI file looks good and all, we are missing one **CRUCIAL** thing...
How do we determine a STANDARD for our ML Model??

Every Model needs its own template to forgo ridiculous amounts of conclusions! For example, there would be
NO reason to include 13th partials in an AC/DC Model!!

Let's look at only Time Data possibilities within One Quarter Note

<table>
   <tr>
        <th colspan="20" style="text-align: center; font-size: large">
            1 Beat: 16th Notes
        </th>
    </tr>
        <th>Time_0</th>
        <th>Time_1/4</th>
        <th>Time_2/4</th>
        <th>Time_3/4</th>
        <th>Time_1</th>
</table>
<table>
   <tr>
        <th colspan="20" style="text-align: center; font-size: large">
            1 Beat: 16th Notes and Triplet 8th Notes
        </th>
    </tr>
        <th>Time_0</th>
        <th>Time_1/4</th>
        <th>Time_1/3</th>
        <th>Time_2/4</th>
        <th>Time_2/3</th>
        <th>Time_3/4</th>
        <th>Time_1</th>
</table>
<table>
   <tr>
        <th colspan="20" style="text-align: center; font-size: large">
            1 Beat: 16th Notes, Triplet 8th Notes, and 5th Partial 16ths (Quintuplet / Fivelet 16ths)
        </th>
    </tr>
        <th>Time_0</th>
        <th>Time_1/5</th>
        <th>Time_1/4</th>
        <th>Time_1/3</th>
        <th>Time_2/5</th>
        <th>Time_2/4</th>
        <th>Time_3/5</th>
        <th>Time_2/3</th>
        <th>Time_3/4</th>
        <th>Time_4/5</th>
        <th>Time_1</th>
</table>

So, we MUST make sure to start our Model on a Template DataFrame that makes sense, and could evolve into great
predictions!! (Time Signature and Tempo ranges should be included in something like this )

Alternatively, we could Adjust our Template DataFrame to include some very random things DESPITE being geared towards
a certain output.

### 6) Make Model Predictions

One of the aspects of Machine learning is that the prediction is aimed at a Target Column, rather than an **entire row** 
being the target prediction.

There are two methods I can think of using to circumvent this:

#### Cosine Similarity vs. Incremental Prediction

- Cosine Similarity
    - **Process:** We have our model randomly generate our 1's and 0's and then evaluate the Cosine Similarity
      - Pros: Can build model(s) quickly
      - Cons: Model won't be especially ambitious, Overfitting is very real, Random Number Generator is the only tuner.
<br></br>
- Incremental Prediction
    - **Process:** Use the entire Dataframe to iterate predictions one column at a time
      - Pros: Model will be more ambitious in creating something new / "stylistic"
      - Cons: Research heavy, not sure if possible or purely theoretical, is a "Model of Models", like a CNN.

### 7) Collect Model Feedback

#### Automated vs USER Feedback

There are two ways we could collect feedback to tune our model...
- Automated
    - **Process:** We consistently evaluate if our model has a certain Accuracy against our Library
      - Pros: Can build model(s) quickly
      - Cons: Model won't be especially ambitious, Dataset could be too small (depending on Library)
<br></br>
- USER Feedback
    - **Process:** USERS use the Model and RATE on its performance. Accurate Models are carried on.
      - Pros: Model will be more ambitious in creating something new / "stylistic"
      - Cons: _Entirely_ dependent on USER activity and Constructive Feedback; takes more time / submissions.

One of the ways we could employ both is allowing the USER to select the type of MODEL they would like to use.