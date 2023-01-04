# Music Theory meets Application: "Rhythm Space"
- <b>Objective</b>: Explain 'Rhythm Space' in context of the <b>Every Drumbeat Ever</b> application functionality
---
### Contributor(s):
- Chris Burrows (<i> Project Lead / Programmer</i> )
---
### Preface:
The initial instance of this algorithm to produce a 'randomized' drum beat actually
consisted of some steps with human discernment, shown below:
1. Excel Spreadsheet had columns marked 1 - 8 for each type of PARTIAL.
2. USER can specify how many partials are desired of each type, which sum to a TOTAL.
3. TOTAL was formatted so that it's formula would reflect when the user was out of range 
 with the USER selected amount of BARS.
4. It was on the USER to balance this total as they manipulated the PARTIAL columns.
5. The USER could then use the tallies to ARRANGE the `rhythm space` however they would like.
6. The USER could then user the `rhythm space` to add VOICINGS however they would like.

### The Problem:
Now, this isn't a bad idea to get the sketches going for coming up with some rhythms, but what 
if this was AUTOMATED? You would have an incredible amount to choose from!

Alas, to fully AUTOMATE this process and leave it to the USER to generate things above and 
beyond the scope of human capability, we need to look at what parameters a human should control and the machine infer.

---
### The Process:
The typical USER story would look like this:
1. USER chooses number of BARS they would like to see
2. USER chooses Time Signature that is the base
3. USER chooses RANDOM SEED (which determines how the `rhythm space` is generated) 

**GENERATE SUBDIVISIONS (PARTIALS)**
- We use SUBDIVISIONS as that's the more common verbiage; PARTIALS is synonymous.

1. USER chooses the PARTIALS they would like
2. USER chooses the PARTIAL's WEIGHT
3. USER chooses each PARTIAL's BREAKABILITY

**GENERATE RHYTHM SPACE**

- Now here is exactly where we have to describe what **RHYTHM SPACE** is!!
---
### RHYTHM SPACE:
Basically, want the algorithm to generate a MIDI FILE after the input of USER PARAMETERS.

Let's start with the basics; how would this APP fill in a 4/4 bar given certain parameters??

1. Process (1) BAR at a time:
   * We choose this initial rule to ensure we won't have any strange notes that go over the BARLINE. 
   This naturally builds a queue depending on the number of BARS the user gave us. <br></br>
   
2. Depending on the USER's PARTIAL MAP, we will have the algorithm do the following:
   1. Generate a RANDOM PARTIAL PICKER based on the USER's PARTIAL WEIGHTS
      * For example, a PARTIAL WEIGHT of '0' means it is effectively excluded. <br></br>
      
   2. PARTIAL is selected, APP now subtracts that partial value from the remaining RHYTHM SPACE. This LOOP
      repeats until there is no RHYTHM SPACE left.
      * An important caveat; this is where we need further explanation on how to handle multiple types of partials...
---
### APP ALGORITHM: STEP # 1 - SUBTRACTING RHYTHM SPACE
Let's take a look at a 4/4 Bar and see how the fractional PARTIAL values are obtained:
<table>
   <tr>
      <th> Partial Type </th>
      <th> Bar Fraction </th>
      <th> Partial Formula </th>
   </tr><tr>
      <td>2let (Dotted Whole)</td>
      <td>6.0_:_ 4.0</td>
      <td>(3 / 2) * 4</td>
   </tr><tr>
      <td>4let (Dotted Whole)</td>
      <td>6.0_:_ 4.0</td>
      <td>(3 / 4) * 8</td>
   </tr><tr>
      <td>Whole Note (8let)</td>
      <td>4.0_:_ 4.0</td>
      <td>(4 / 8) * 8</td>
   </tr><tr>
      <td>9let</td>
      <td>3.556_:_ 4.0</td>
      <td>(4 / 9) * 8</td>
   </tr><tr>
      <td>5let</td>
      <td>3.2_:_ 4.0</td>
      <td>(4 / 10) * 8</td>
   </tr><tr>
      <td>11let</td>
      <td>2.909_:_ 4.0</td>
      <td>(4 / 11) * 8</td>
   </tr><tr>
      <td>3let</td>
      <td>2.667_:_ 4.0</td>
      <td>(4 / 12) * 8</td>
   </tr><tr>
      <td>13let</td>
      <td>2.462_:_ 4.0</td>
      <td>(4 / 13) * 8</td>
   </tr>
</table>

![rspace_1](https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/rhythmic_space-bar_fractions.PNG?raw=true)

We can demonstrate that the fractional base values are all computed BASED on 4/4...
<table>
   <tr style="text-align: center">
      <th colspan="3">4/4</th>
      <th colspan="2">3/4</th>
      <th colspan="2">5/4</th>
   </tr>
      <tr>
         <th> Partial Type </th>
         <th> Bar Fraction </th>
         <th> Partial Formula </th>
         <th> Bar Fraction </th>
         <th> Partial Formula </th>
         <th> Bar Fraction </th>
         <th> Partial Formula </th>
      </tr><tr>
         <td>2let (Dotted Whole)</td>
         <td>6.0_:_ 4.0</td>
         <td>(3 / 2) * 4</td>
         <td>6.0_:_ 3.0</td>
         <td>(3 / 2) * 4</td>
         <td>6.0_:_ 5.0</td>
         <td>(3 / 2) * 4</td>
      </tr><tr>
         <td>4let (Dotted Whole)</td>
         <td>6.0_:_ 4.0</td>
         <td>(3 / 4) * 8</td>
         <td>6.0_:_ 3.0</td>
         <td>(3 / 4) * 8</td>
         <td>6.0_:_ 5.0</td>
         <td>(3 / 4) * 8</td>
      </tr><tr>
         <td>Whole Note (8let)</td>
         <td>4.0_:_ 4.0</td>
         <td>(4 / 8) * 8</td>
         <td>4.0_:_ 3.0</td>
         <td>(4 / 8) * 8</td>
         <td>4.0_:_ 5.0</td>
         <td>(4 / 8) * 8</td>
      </tr><tr>
         <td>9let</td>
         <td>3.556_:_ 4.0</td>
         <td>(4 / 9) * 8</td>
         <td>3.556_:_ 3.0</td>
         <td>(4 / 9) * 8</td>
         <td>3.556_:_ 5.0</td>
         <td>(4 / 9) * 8</td>
      </tr><tr>
         <td>5let</td>
         <td>3.2_:_ 4.0</td>
         <td>(4 / 10) * 8</td>
         <td>3.2_:_ 3.0</td>
         <td>(4 / 10) * 8</td>
         <td>3.2_:_ 5.0</td>
         <td>(4 / 10) * 8</td>
      </tr><tr>
         <td>11let</td>
         <td>2.909_:_ 4.0</td>
         <td>(4 / 11) * 8</td>
         <td>2.909_:_ 3.0</td>
         <td>(4 / 11) * 8</td>
         <td>2.909_:_ 5.0</td>
         <td>(4 / 11) * 8</td>
      </tr><tr>
         <td>3let</td>
         <td>2.667_:_ 4.0</td>
         <td>(4 / 12) * 8</td>
         <td>2.667_:_ 3.0</td>
         <td>(4 / 12) * 8</td>
         <td>2.667_:_ 5.0</td>
         <td>(4 / 12) * 8</td>
      </tr><tr>
         <td>13let</td>
         <td>2.462_:_ 4.0</td>
         <td>(4 / 13) * 8</td>
         <td>2.462_:_ 3.0</td>
         <td>(4 / 13) * 8</td>
         <td>2.462_:_ 5.0</td>
         <td>(4 / 13) * 8</td>
   </tr>
</table>

This is a fine way to process most of our method... but can we utilize LUDICROUS time signatures,
like '13 / 25', '9 / 6', or '11 / 7'??? <br></br>
***NOTE:** Not even Cubase has MIDI parsing for LUDICROUS time signatures... It could be best to adapt a 'Logos' 
expansion to automatically convert to tempo changes...?  

### APP ALGORITHM: STEP # 2 - FINDING THE NEAREST QUARTER EQUIVALENT
Because we are exporting a MIDI file that would be compatible with most DAW's, it makes sense
to ensure our RHYTHM SPACE generates partials that would actually round to the NEAREST QUARTER EQUIVALENT (1/4).

Here are some following examples:
1. 5let Partial (16th note) | 4/4 Bar
   * We know that we need at least (5) 5let partials to complete 1/4 of the 4/4 Bar
2. 5let Partial (8th note) | 4/4 Bar
   * We know that we need at least (5) 5let partials to complete 2/4 of the 4/4 Bar
   * Unfortunately, 2/4 is larger than our NEAREST QUARTER NOTE EQUIVALENT (1/4)
   * The APP ALGORITHM must now take into account we will NEED 5let Partials (16th) to round out a truncated phrase.
      * This will OVERRIDE any WEIGHT = 0 settings of the 5let Partials (16th) [not actually change the USER value, however]
        * The only way to compensate for something like this would be mid-BAR tempo / time-signature changes...??
   

