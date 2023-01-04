# Music Theory meets Application: "Breakability"
- <b>Objective</b>: Explain 'Breakbility' in context of the <b>Every Drumbeat Ever</b> application functionality
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
2. USER chooses each PARTIAL's <b>BREAKABILITY</b>

**GENERATE RHYTHM SPACE**

- Now here is exactly where we have to describe what **BREAKBILITY** is!!
---
### BREAKABILITY:
Basically, we want to know whether or not we can **BREAK** certain PARTIALS apart
to complete the BAR or PHRASE(total collection of BARS). This should be USER selectable, 
as the USER may NOT want to have a fivelet split up before within a BAR. For example:
![5let_1](https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/5let_break.PNG?raw=true)
- The first BAR would be fairly difficult for any non-human to interpret; but the second
BAR is completely acceptable. This is the reason we want to give the USER control and
avoid generating lots of "impractical" `rhythm space`.

### The Solution:
So we've determined that we want the USER to choose how much BREAKABILITY they would
like in their generated `rhythm_space`. What PARTIALS does this actually apply to?? 

ANYTHING that wouldn't go over the BARLINE of the USER selected TIME SIGNATURE:
![normal_1](https://github.com/cbradiodrums/everydrumbeat/blob/main/theory/resources/normal_breaks.PNG?raw=true)

So, we actually need some kind of NUMERICAL control for BREAKABILITY. An advanced
player would certainly be able to digest the second BAR even though it is complex. 
So the BREAKABILITY should be a NUMERICAL drop down representing the range of the PARTIAL MAX 
down to 1. This way, we won't have single 16th note triplet stems placed like breadcrumbs 
along the way of our `rhythm space`...


