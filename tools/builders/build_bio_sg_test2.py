#!/usr/bin/env python3
"""Biology 8 · Test 2 Study Guide (Units 3 and 4).

Source: "unit 3 and 4 Study Guide.pdf", Drive, Biology Unit 4 folder, uploaded
2026-09-29 — the teacher's own "Test 2 (Wednesday 9/30) Study Guide", six
pages. A pure scan with NO text layer, so every page was rendered with
pypdfium2 and read as an image.

The copy in Drive is her filled-in one. Per the standing rule (v198), it was
read for what the guide ASKS — every blank, chart row and prompt gets
coverage here — and nothing on it was tallied, summarised or recorded.

Checked against the teacher's Unit 3 deck (G8_Cells_VA.pdf) before writing:

  * The deck lists eukaryotic cells as "animal, plant, algae, and fungal",
    while the guide's fourth-kingdom blank is followed by "(single
    cellular)", and the standard kingdom name is protists. The card teaches
    both words rather than guessing which one the key wants.
  * Viruses, archaea vs bacteria, cyanobacteria and the microscope are NOT
    in that deck. The guide states most of them in its own sentences, which
    is what these cards are sourced to; what it leaves as an open question
    (why viruses are not alive, the downside of asexual reproduction, why
    only the fine knob at high power) is flagged from='added'.
  * The cytoskeleton row asks whether prokaryotes have one. That is taught
    both ways at this level (they have related protein fibres), so the card
    states only the eukaryote half and does not pick.

Every question is a fresh scenario — the guide's own examples live on the
cards. Numbers were computed below and asserted before they reach a
question. The test is fill-in-the-blank on the guide's pattern, so six
kind:'spell' questions practise producing the words, not recognising them.
"""
import io, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

A = 'added'
C, Q = [], []

# ---------------------------------------------------------------- numbers
def sa(s): return 6 * s * s
def vol(s): return s ** 3
assert (sa(2), vol(2), sa(2) / vol(2)) == (24, 8, 3.0)
assert (sa(4), vol(4), sa(4) / vol(4)) == (96, 64, 1.5)
assert sa(3) / vol(3) == 2.0                  # q: side 3 -> 2 : 1
assert sa(5) / vol(5) == 1.2                  # q: side 2 vs side 5
# counting: an X is 1 chromosome / 2 chromatids, a single strand 1 / 1
def count(xs, singles): return xs + singles, 2 * xs + singles
assert count(2, 2) == (4, 6)                  # card example
assert count(3, 2) == (5, 8)                  # question
assert count(1, 2) != (5, 8)                  # fresh: not the guide's own 3/4 picture either
# a 5-chromosome animal cell through mitosis
assert 5 * 2 == 10                            # chromatids at metaphase; chromosomes in anaphase

# ================================================================= UNIT 3
card(C, 'The cell theory',
     "**All living things are made of one or more cells; the cell is the basic unit of all living "
     "things; and all cells come from existing cells.**\n"
     "• Three statements — the test asks for all three\n"
     "• 'Existing' is the load-bearing word: a cell never forms from non-living material",
     hint="Made of → unit of → comes from: what life is built from, how small it goes, where cells come from.")

card(C, 'The six characteristics of living things',
     "**Made of one or more cells · obtain and use energy · grow and develop · reproduce · sense and "
     "respond · have DNA as their hereditary material.**\n"
     "• Your class's slides add two riders: living things maintain homeostasis, and populations adapt and evolve\n"
     "• Something must show ALL six to count as alive",
     hint="Cells, energy, growth, offspring, reaction, instructions — one idea each.")

card(C, 'Why viruses are not alive',
     "**They fail most of the six characteristics: not made of cells, cannot obtain or use energy, do "
     "not grow, and cannot reproduce on their own.**\n"
     "• A virus can only be copied by taking over a living host cell's machinery\n"
     "• The one characteristic it DOES have is genetic material — DNA or RNA\n"
     "• Outside a host it is an inert particle that does nothing at all",
     hint="Name the one characteristic a virus has. Every other one is missing.", frm=A)

card(C, 'The parts of a virus',
     "**Genetic material — DNA or RNA — packed inside a protein coat.**\n"
     "• The protein coat is called the capsid; some viruses also wrap it in an outer envelope\n"
     "• No cytoplasm, no ribosomes, no membrane of its own — which is why it cannot run itself",
     hint="A set of instructions in a protein box. That is the whole virus.")

card(C, 'The lytic cycle',
     "**The virus IMMEDIATELY uses the host cell to make new virus particles.**\n"
     "• Examples: flu, chicken pox, COVID-19\n"
     "• The host usually gets sick within a few days, because the copies are made straight away",
     hint="Lytic → lyse → burst. Fast, and you notice it within days.")

card(C, 'The lysogenic cycle',
     "**The virus inserts its genes into the host cell, but they are NOT copied into new viruses "
     "right away.**\n"
     "• The viral genes can stay in the host cell for a long time, until conditions are right\n"
     "• Examples: shingles, HIV — illness can appear years after the infection",
     hint="Lysogenic lies low: in first, trouble later.")

card(C, 'The two prokaryotic domains',
     "**Archaea and bacteria.**\n"
     "• Archaea live only in extreme places — extreme heat, no oxygen, or very high salt — and some make methane\n"
     "• Bacteria live almost everywhere: in and on your body, in soil, in water, on most surfaces",
     hint="Archaea sounds ancient — and they live in the harsh conditions early Earth had.")

card(C, 'Cyanobacteria are autotrophs',
     "**An autotroph makes its own food — cyanobacteria do it by photosynthesis.**\n"
     "• Auto = self, troph = feeding: a self-feeder\n"
     "• Cyanobacteria make a large share of the world's oxygen\n"
     "• The opposite is a heterotroph, which has to eat other living things",
     hint="Auto-matic food: made in-house from sunlight.")

card(C, 'The four eukaryotic kingdoms',
     "**Animals, plants, fungi, and the mostly single-celled group — protists, with algae as the "
     "best-known members.**\n"
     "• Your class's slides list eukaryotic cells as animal, plant, algae and fungal\n"
     "• The standard name for that fourth kingdom is protists — check which word your teacher wants in the blank\n"
     "• All four are eukaryotes: every one of their cells has a nucleus",
     hint="Animals, plants, fungi — and the pond-scum group Leeuwenhoek found.")

# ---- the chart, one row per card: function first, then where it is found
card(C, 'Cell membrane',
     "**Controls what enters and leaves the cell.**\n"
     "• A phospholipid bilayer — selectively permeable\n"
     "• Prokaryotes: yes · Eukaryotes: yes — every cell has one",
     hint="The border guard. Every cell has one, no exceptions.")

card(C, 'Cell wall',
     "**Protects the cell and holds its shape, from outside the membrane.**\n"
     "• Prokaryotes: almost always · Eukaryotes: only some — plants, algae and fungi, never animals\n"
     "• A eukaryote's wall is made of different material from a prokaryote's",
     hint="Outside the membrane — and missing from every animal cell.")

card(C, 'Capsule',
     "**A sticky outer layer of sugars and proteins that protects the cell and lets it stick to surfaces.**\n"
     "• Sits OUTSIDE the cell wall\n"
     "• Prokaryotes: some · Eukaryotes: no — it is one of the extras only some prokaryotes carry",
     hint="The sticky coat that lets bacteria cling to your teeth as plaque.")

card(C, 'Nucleus',
     "**Stores the DNA and controls the cell's activities.**\n"
     "• Wrapped in a nuclear membrane with pores\n"
     "• Prokaryotes: no — having one is what MAKES a cell a eukaryote · Eukaryotes: yes",
     hint="The control centre — and the dividing line between the two kinds of cell.")

card(C, 'Nucleoid region',
     "**The area of a prokaryote where its single circular chromosome sits, with no membrane around it.**\n"
     "• A region, not a compartment — nothing walls it off\n"
     "• Prokaryotes: yes · Eukaryotes: no — they have a true nucleus instead\n"
     "• Not the nucleolus, which is the part of a eukaryote's nucleus that makes ribosomes",
     hint="Nucle-OID means nucleus-LIKE: where the DNA is, minus the wrapping.")

card(C, 'Ribosome',
     "**Makes (assembles) proteins for the cell.**\n"
     "• Tiny and has no membrane — which is how prokaryotes can have them\n"
     "• Prokaryotes: yes · Eukaryotes: yes",
     hint="The protein factory found in every cell there is.")

card(C, 'Plasmid',
     "**A small ring of DNA separate from the main chromosome, often carrying extra genes.**\n"
     "• Separate is the key word — it is not wrapped round or attached to the chromosome\n"
     "• Prokaryotes: some · Eukaryotes: no, for this course",
     hint="A bonus ring of DNA, off to one side.")

card(C, 'Chromosome',
     "**A package of DNA carrying the cell's genetic information.**\n"
     "• Prokaryotes: yes — usually ONE, circular, in the nucleoid region\n"
     "• Eukaryotes: yes — usually MANY, linear, in the nucleus",
     hint="Both kinds have them. One ring versus many strands.")

card(C, 'Cytoplasm',
     "**The fluid inside the membrane and everything suspended in it, except the nucleus.**\n"
     "• The liquid part alone is the cytosol, and most of the cell's chemistry happens here\n"
     "• Prokaryotes: yes · Eukaryotes: yes",
     hint="The inside of every cell — jelly plus contents.")

card(C, 'Rough endoplasmic reticulum',
     "**Folds and moves the proteins being made by the ribosomes stuck to its surface.**\n"
     "• The ribosomes are what make it look rough\n"
     "• Prokaryotes: no · Eukaryotes: yes",
     hint="Rough = ribosomes on it = proteins.")

card(C, 'Smooth endoplasmic reticulum',
     "**Makes lipids and breaks down toxins.**\n"
     "• The same kind of membrane sacs, with no ribosomes\n"
     "• Prokaryotes: no · Eukaryotes: yes",
     hint="Smooth = no ribosomes = not proteins. Fats and poisons instead.")

card(C, 'Vesicles',
     "**Small membrane sacs that move material around inside the cell, or store it.**\n"
     "• The cell's shipping boxes between compartments\n"
     "• Eukaryotes: yes · Prokaryotes: the teacher's own note on the guide says technically yes, but "
     "you do not need to know that for comps",
     hint="Parcels with a membrane for a skin.")

card(C, 'Vacuoles',
     "**Store water, salts, proteins and carbohydrates — and sometimes waste.**\n"
     "• Small and temporary in animal cells; one large permanent central vacuole in a plant cell\n"
     "• Prokaryotes: no · Eukaryotes: yes",
     hint="The storage tank — biggest in plants, where its water holds the cell up.")

card(C, 'Golgi apparatus',
     "**Finishes, sorts, labels and ships proteins.**\n"
     "• Receives them from the rough ER and sends them on in vesicles\n"
     "• Prokaryotes: no · Eukaryotes: yes",
     hint="The shipping department — the cell's UPS headquarters.")

card(C, 'Cytoskeleton',
     "**A network of protein fibres that gives the cell its shape and support, and lets it move.**\n"
     "• Anchors the organelles and builds cilia and flagella\n"
     "• Eukaryotes: yes",
     hint="Scaffolding inside the cell — a skeleton by name, but made of protein.")

card(C, 'Lysosomes',
     "**Digest food, recycle worn-out cell parts, and destroy pathogens.**\n"
     "• Membrane sacs of digestive enzymes, made by the Golgi apparatus\n"
     "• Prokaryotes: no — a lysosome is membrane-bound, and no prokaryote has those · "
     "Eukaryotes: some — animal cells; in some plant cells the vacuole does the job",
     hint="Membrane-bound means eukaryote-only. The clean-up crew.")

card(C, 'Centrosomes and centrioles',
     "**Organise cell division in animal cells.**\n"
     "• A centrosome is made of two centrioles — one pair per cell\n"
     "• Prokaryotes: no · Eukaryotes: some — animal cells\n"
     "• Not the centromere, which is the pinched middle of a chromosome",
     hint="Centro-SOME organises division; centro-MERE is the middle of a chromosome.")

card(C, 'Mitochondria',
     "**Carry out cellular respiration, releasing the energy stored in sugar as ATP.**\n"
     "• The powerhouse of the cell\n"
     "• Prokaryotes: no · Eukaryotes: yes — nearly all of them, plants included",
     hint="Plants have them too: photosynthesis makes the sugar, mitochondria spend it.")

card(C, 'Chloroplasts',
     "**Carry out photosynthesis, capturing sunlight to build sugar.**\n"
     "• Contain the green pigment chlorophyll\n"
     "• Prokaryotes: no · Eukaryotes: some — plants and algae, never animals",
     hint="Green = chlorophyll = only where sunlight gets captured.")

card(C, 'The pathway out of the cell',
     "**Ribosome → rough ER → vesicle → Golgi apparatus → vesicle → cell membrane.**\n"
     "• The six stops of a protein that is going to be excreted from the cell\n"
     "• Vesicle appears twice: one carries it INTO the Golgi, one carries it OUT",
     hint="Make, fold, box, finish, box, out.")

card(C, 'Form fits function',
     "**A cell's job predicts which organelle it is stocked with.**\n"
     "• Muscle → many mitochondria · Red blood cell → NO mitochondria (oxygen moves by diffusion, no energy input)\n"
     "• Macrophage → many lysosomes · Liver → a very large smooth ER · Gland → a very large Golgi apparatus",
     hint="Ask what the cell spends its day doing, then find the organelle that does that job.")

card(C, 'Endosymbiont theory',
     "**An early ancestor of eukaryotic cells engulfed an oxygen-using prokaryote, which lived on "
     "inside it and became an organelle.**\n"
     "• Applies to two organelles: mitochondria and chloroplasts\n"
     "• Evidence: both have their own DNA and their own ribosomes — plus double membranes, and they "
     "reproduce on their own schedule",
     hint="Swallowed but never digested — and it still carries its own DNA as proof.")

card(C, 'Cellular respiration',
     "**Glucose plus oxygen gives carbon dioxide plus water, and releases energy as ATP.**\n"
     "• Happens in the mitochondria\n"
     "• It is photosynthesis run backwards",
     eq="C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP",
     hint="Sugar and oxygen in; the two gases you breathe out come out.")

card(C, 'Photosynthesis',
     "**Carbon dioxide plus water, powered by sunlight, gives glucose plus oxygen.**\n"
     "• Happens in the chloroplasts\n"
     "• Every number is a 6 except the sugar's own formula",
     eq="6CO₂ + 6H₂O + sunlight → C₆H₁₂O₆ + 6O₂",
     hint="Six of each gas, one sugar — the respiration equation read right to left.")

card(C, 'Light vs electron microscope',
     "**A light microscope lets you see living things; an electron microscope cannot.**\n"
     "• The electron microscope uses a beam of ELECTRONS, which bounce off cell surfaces\n"
     "• It magnifies far more, but the specimen cannot be alive",
     hint="The electron microscope's clue is in its name: electrons, not light.")

card(C, 'Using a light microscope',
     "**Light on, lowest-power lens first, find the cell with the stage, focus with the coarse knob, "
     "then step up one lens at a time.**\n"
     "• Plug in → light → red lens → move the stage until you find the cell → coarse knob until clear\n"
     "• Yellow lens → make it clear → blue lens → ONLY the fine (small) knob from here → gray lens if you need more\n"
     "• The teacher's note: a test question may show a student making a mistake and ask for their next step",
     hint="Low to high, coarse to fine — and never the coarse knob once the blue lens is in.")

card(C, 'Why only the fine knob at high power',
     "**At high power the lens sits very close to the slide, so the coarse knob can crash the lens "
     "into it.**\n"
     "• The coarse knob moves the stage a long way per turn; the fine knob moves it a tiny amount\n"
     "• The lowest-power lens gives the widest view, which is why you FIND things there first",
     hint="Big knob, big moves — dangerous when the lens is almost touching the glass.", frm=A)

# ================================================================= UNIT 4
card(C, 'Surface area-to-volume ratio',
     "**Cells need a HIGH surface area to a LOW volume.**\n"
     "• For a cube with side s: surface area = 6s², volume = s³\n"
     "• Side 2: 24 ÷ 8 = 3. Side 4: 96 ÷ 64 = 1.5 — double the side, half the ratio",
     eq="SA : V = 6s² : s³",
     hint="Small cube, big ratio. The ratio shrinks as the cell grows.")

card(C, 'The cell cycle chart',
     "**Interphase — G1, then S, then G2 — followed by the M phase: mitosis (prophase, metaphase, "
     "anaphase, telophase) and cytokinesis.**\n"
     "• G0 branches off from G1: a cell that is not going to divide leaves the cycle there\n"
     "• Abbreviating the mitosis phases on the chart is fine: P, M, A, T",
     hint="Grow, Synthesise, Grow again, then PMAT and split. G0 is the side exit off G1.")

card(C, 'S phase',
     "**The DNA is replicated.**\n"
     "• S stands for synthesis\n"
     "• Afterwards every chromosome is two sister chromatids joined at the centromere",
     hint="S for synthesis — the copying happens here and nowhere else.")

card(C, 'How the 24 hours split',
     "**In a fast-growing area like an onion root tip, a 24-hour cycle is about 23 hours of "
     "interphase and about 1 hour of mitosis.**\n"
     "• So in any picture of a root tip, most cells are in interphase",
     hint="23 + 1. The dividing is the short part.")

card(C, 'Which cells sit in G0',
     "**Red blood cells, mature neurons and the outer layer of skin cells — they do not need to divide.**\n"
     "• The lower layer of skin is NEVER in G0: it is always dividing, to replace the outer layer as it wears away",
     hint="The outside skin is finished; the layer underneath never stops making more.")

card(C, 'G1 and G2',
     "**In G1 the cell does its normal job while building new proteins and organelles for the "
     "daughter cells; in G2 it makes the molecules and organelles mitosis itself needs.**\n"
     "• A cell that reaches G2 usually goes on to mitosis — unless there is a replication error\n"
     "• Uncorrected replication errors can lead to cancer",
     hint="G1 grows for the daughters; G2 gets ready for the division.")

card(C, 'Chromatin, histones and nucleosomes',
     "**Chromatin is DNA wound around proteins called histones; one bead of DNA wrapped round "
     "histones is a nucleosome.**\n"
     "• Chromatin is the loose, uncoiled form of DNA when the cell is not dividing; the histones stop "
     "chromosomes tangling when it does divide\n"
     "• Prokaryotic chromosomes have NO histones",
     hint="Thread (DNA) wound on spools (histones) makes beads (nucleosomes); the whole string is chromatin.")

card(C, 'Counting chromosomes and chromatids',
     "**Count centromeres for chromosomes; count strands for chromatids.**\n"
     "• One X = 1 chromosome, 2 chromatids · One single strand = 1 chromosome, 1 chromatid\n"
     "• Two X's and two single strands = 4 chromosomes, 6 chromatids",
     hint="Every pinch point is one chromosome. Every arm-pair strand is one chromatid.")

card(C, 'Drawing mitosis with 5 chromosomes',
     "**5 chromosomes as 10 chromatids through prophase and metaphase; 10 separate chromosomes "
     "moving apart in anaphase; 5 in each new cell.**\n"
     "• Prophase: condensed chromosomes, nuclear envelope breaking down, centrosomes moving apart\n"
     "• Metaphase: all 5 on the metaphase plate · Telophase/cytokinesis: two nuclear envelopes, a "
     "furrow pinched in by the contractile ring",
     hint="Double, line up, split, then two cells with the number you started with.")

card(C, 'The cell plate',
     "**A plant cell ends mitosis by building a new wall down its middle — the cell plate — instead "
     "of pinching in.**\n"
     "• Its rigid cell wall cannot be pulled inward\n"
     "• An animal cell pinches in with a furrow made by a contractile ring",
     hint="Plants build a wall across the middle; animals pinch in at the waist.")

card(C, 'What mitosis is for',
     "**Growth, development, and asexual reproduction — making genetically identical copies.**\n"
     "• In a multicellular organism, also repair: replacing worn-out or damaged cells",
     hint="Grow, develop, copy. Identical every time.")

card(C, 'The downside of reproducing by mitosis',
     "**Every offspring is genetically identical, so there is no variation — one disease or change "
     "in conditions that harms one can harm them all.**\n"
     "• No genes mixed from two parents means no new combinations\n"
     "• A population of clones cannot adapt as well when its environment changes",
     hint="Clones share every weakness.", frm=A)

card(C, 'Somatic cells and gametes',
     "**Mitosis happens in somatic (body) cells, which are diploid. It does not happen in gametes — "
     "sperm and eggs — which are haploid.**\n"
     "• Diploid = two sets of chromosomes; haploid = one set\n"
     "• Gametes are made by meiosis, which is next unit",
     hint="DI = two sets, in the body. HAP = half, in the gametes.")

# ================================================================ questions
def Qa(lv, text, opts, hint, steps, main, tip, frm='source', kind='mc'):
    q(Q, lv, text, opts, 0, hint, steps, main, tip, frm=frm, kind=kind)

# --- level 1: recall
Qa(1, "Which structure do BOTH prokaryotic and eukaryotic cells have?",
   ["Ribosomes", "A nucleus", "A Golgi apparatus", "Lysosomes"],
   "One of these has no membrane at all — that is how a prokaryote can have it.",
   ["Prokaryotes have no nucleus and no membrane-bound organelles.",
    "A nucleus, a Golgi apparatus and lysosomes are all membrane-bound, so they are eukaryote-only.",
    "Ribosomes have no membrane, and every cell needs them to make proteins.",
    "Ribosomes."],
   "**Ribosomes.** They are not membrane-bound, so prokaryotes have them too — every cell needs them to make proteins.",
   "Membrane-bound is the test: if it has a membrane, a prokaryote cannot have it.")

Qa(1, "What is the nucleoid region?",
   ["The area where a prokaryote's chromosome sits, with no membrane around it",
    "The part of a eukaryote's nucleus that builds ribosomes for the cell",
    "A membrane sac of enzymes that digests the cell's worn-out parts",
    "The pinched middle where two sister chromatids are held together"],
   "The -oid ending means 'like'. Nucleus-like — in a cell that has no nucleus.",
   ["Nucleoid means nucleus-like, so it belongs to a cell WITHOUT a true nucleus: a prokaryote.",
    "The part of a nucleus that builds ribosomes is the nucleolus, a different word.",
    "The pinched middle of a chromosome is the centromere; the digestive sac is a lysosome.",
    "The nucleoid region is where a prokaryote's chromosome sits, unwrapped."],
   "**It is where a prokaryote keeps its single circular chromosome, with no membrane around it.** The nucleolus — one letter-group different — makes ribosomes inside a eukaryote's nucleus.",
   "Nucleoid, nucleolus, nucleus, nucleosome: four look-alikes. The ending tells you which.")

Qa(1, "What do centrosomes do in an animal cell?",
   ["Organise cell division", "Hold two sister chromatids together",
    "Digest the pathogens the cell engulfs", "Finish, sort and ship proteins"],
   "Centrosome and centromere are one syllable apart. Which one is an organiser?",
   ["The centromere, not the centrosome, is where sister chromatids are joined.",
    "Digesting pathogens is the lysosome's job; shipping proteins is the Golgi's.",
    "A centrosome is a pair of centrioles, and its job is to organise cell division.",
    "Organise cell division."],
   "**They organise cell division.** A centrosome is two centrioles; the centromere is the pinched middle of a chromosome.",
   "SOME organises, MERE is the middle.")

Qa(1, "Someone catches a virus and is sick within a few days, because the virus made new virus particles straight away. Which cycle is this?",
   ["The lytic cycle", "The lysogenic cycle", "The cell cycle", "Endosymbiosis"],
   "Straight away is the clue. One of the virus cycles waits; this one did not.",
   ["The virus made new particles immediately.",
    "The lysogenic cycle is the one that waits, with its genes hidden in the host cell.",
    "Making new virus particles straight away, with illness in days, is the lytic cycle.",
    "The lytic cycle."],
   "**The lytic cycle.** It makes new virus particles immediately, which is why flu, chicken pox and COVID-19 make you sick within days.",
   "Lytic is fast; lysogenic lies low.")

Qa(1, "Which characteristic of living things does a virus actually have?",
   ["Genetic material — DNA or RNA", "Being made of one or more cells",
    "Obtaining and using its own energy", "Growing and developing over time"],
   "Think about what is packed inside the protein coat.",
   ["A virus is a protein coat with something inside it.",
    "It is not a cell, it uses no energy of its own, and it does not grow.",
    "What is inside the coat is genetic material — DNA or RNA.",
    "Genetic material."],
   "**Genetic material.** It is the one characteristic a virus has — and it still needs a host cell to do anything with it.",
   "When asked why a virus is not alive, list the ones it is missing.")

Qa(1, "Cyanobacteria are described as autotrophs. What does that tell you about them?",
   ["They make their own food", "They live only in extreme heat",
    "They must eat other living things", "They need a host cell to copy them"],
   "Auto means self. Troph means feeding.",
   ["Auto = self, troph = feeding: a self-feeder.",
    "A self-feeder makes its own food — cyanobacteria do it by photosynthesis.",
    "Eating other living things is the opposite, a heterotroph.",
    "They make their own food."],
   "**They make their own food**, by photosynthesis — which is how they come to make so much of the world's oxygen.",
   "Autotroph = makes food. Heterotroph = eats food.")

Qa(1, "On the cell cycle chart, from which phase can a cell leave the cycle to enter G0?",
   ["G1", "S", "G2", "Metaphase"],
   "A cell decides whether to divide before it copies its DNA.",
   ["G0 is where a cell goes when it is not going to divide.",
    "Copying the DNA in S would be wasted work for a cell that never divides.",
    "So the exit comes before S — from G1.",
    "G1."],
   "**G1.** The side branch to G0 leaves before DNA is copied, which is why the chart draws the G0 arrow off G1.",
   "Draw the G0 loop coming off G1 on the chart.")

Qa(1, "In a fast-growing onion root tip where one full cell cycle takes 24 hours, about how long does mitosis take?",
   ["About 1 hour", "About 6 hours", "About 12 hours", "About 23 hours"],
   "Most of the cycle is spent getting ready.",
   ["The cycle is 24 hours in total.",
    "About 23 of those hours are interphase — growing and copying DNA.",
    "That leaves about 1 hour for mitosis.",
    "About 1 hour."],
   "**About 1 hour.** Interphase takes about 23 of the 24 — and 23 is the distractor waiting for anyone who swaps the two.",
   "23 + 1: interphase is the long part.")

Qa(1, "What are histones?",
   ["Proteins that DNA winds around", "Small rings of DNA outside the chromosome",
    "The loose form DNA takes between divisions", "The points where sister chromatids join"],
   "Picture thread wound on spools. Which part is the spool?",
   ["DNA wraps around something to stay organised — those are the spools.",
    "The rings of DNA outside the chromosome are plasmids; the loose form is chromatin.",
    "The spools are proteins, and they are called histones.",
    "Proteins that DNA winds around."],
   "**Proteins that DNA winds around.** DNA plus histones is chromatin, and each wrapped bead is a nucleosome.",
   "Prokaryotic chromosomes have no histones — a likely test question.")

Qa(1, "DNA wrapped around a cluster of histone proteins forms one bead-like unit. What is that unit called?",
   ["A nucleosome", "A nucleolus", "A nucleoid", "A centromere"],
   "It is a body — a 'some' — built at the level of the nucleus's DNA.",
   ["The bead is one piece of DNA wrapped around histones.",
    "A nucleolus makes ribosomes; a nucleoid is a prokaryote's DNA region.",
    "The DNA-and-histone bead is a nucleosome.",
    "A nucleosome."],
   "**A nucleosome.** Beads of DNA on histone spools; the whole string of beads is chromatin.",
   "Nucleo-SOME: a small body on the DNA string.")

Qa(1, "Which cell is most likely resting in G0?",
   ["A mature neuron", "A cell in an onion root tip",
    "A cell in the lowest layer of the skin", "A cell in a healing cut"],
   "Which of these cells is finished growing and never needs to be replaced by division?",
   ["A root tip, the lowest skin layer and a healing cut are all places where cells keep dividing.",
    "A mature neuron does its job without dividing.",
    "Cells that do not need to divide sit in G0.",
    "A mature neuron."],
   "**A mature neuron.** Along with red blood cells and the outer layer of skin, it sits in G0 because it does not need to divide.",
   "G0 = the job without the dividing.")

Qa(1, "Which structure is found in SOME eukaryotic cells and in no prokaryotic cells?",
   ["Chloroplasts", "Ribosomes", "A cell membrane", "A nucleoid region"],
   "Some eukaryotes means plants yes, animals no.",
   ["Ribosomes and a cell membrane are in every cell.",
    "A nucleoid region is prokaryote-only.",
    "Chloroplasts are in plant and algae cells but never animal cells, and never prokaryotes.",
    "Chloroplasts."],
   "**Chloroplasts** — in plants and algae, never in animals and never in a prokaryote.",
   "Chart answers come in four kinds: both, prokaryote only, all eukaryotes, some eukaryotes.")

# --- level 2: apply
Qa(2, "Which pair of structures is found ONLY in some prokaryotes?",
   ["A capsule and plasmids", "Lysosomes and centrioles",
    "A nucleus and a nucleolus", "Chloroplasts and a large vacuole"],
   "Two of the extras a bacterium might carry — one sticky coat, one bonus ring of DNA.",
   ["Lysosomes, centrioles, a nucleus, chloroplasts and a large vacuole are all eukaryote structures.",
    "Some prokaryotes carry extras: a capsule, plasmids and flagella.",
    "A capsule and plasmids are both in that list.",
    "A capsule and plasmids."],
   "**A capsule and plasmids.** Both are extras only some prokaryotes carry; eukaryotes have neither.",
   "Some prokaryotes, no eukaryotes: capsule, plasmid.")

Qa(2, "Which statement about lysosomes is correct?",
   ["They are in eukaryotic cells such as animal cells, and never in prokaryotes",
    "They are in prokaryotic cells, and never in eukaryotic cells",
    "They are in every cell there is, prokaryote or eukaryote",
    "They are only in plant cells, inside the central vacuole"],
   "A lysosome is a membrane sac. What does that rule out?",
   ["A lysosome is a membrane-bound sac of digestive enzymes.",
    "Prokaryotes have no membrane-bound organelles, so they have no lysosomes.",
    "Animal cells have them; in some plant cells the vacuole does their job instead.",
    "They are in eukaryotes such as animal cells, never prokaryotes."],
   "**Eukaryotic cells such as animal cells, never prokaryotes.** Membrane-bound means eukaryote-only.",
   "Any membrane-bound organelle is a 'no' in the prokaryote column.")

Qa(2, "A cell's whole job is breaking down poisons in the blood. Which organelle should it have an unusually large amount of?",
   ["Smooth ER", "Golgi apparatus", "Chloroplasts", "Centrioles"],
   "Which organelle breaks down toxins?",
   ["Breaking down poisons is detoxification.",
    "The smooth ER makes lipids and breaks down toxins.",
    "A cell that spends its day on toxins needs a very large smooth ER — which is what liver cells have.",
    "Smooth ER."],
   "**Smooth ER** — it breaks down toxins, which is why liver cells have a very large one.",
   "Job first, then the organelle that does the job.")

Qa(2, "Red blood cells carry oxygen by diffusion. Which organelle do they lack, and why?",
   ["Mitochondria, because diffusion needs no energy input",
    "Ribosomes, because red cells never need any proteins",
    "Lysosomes, because red cells never engulf anything",
    "A cell membrane, because oxygen must pass freely"],
   "Diffusion moves things without the cell spending energy. Which organelle supplies energy?",
   ["Diffusion is movement from high to low concentration — it takes no energy input.",
    "Mitochondria are the organelles that supply energy.",
    "A cell whose job needs no energy input has no mitochondria.",
    "Mitochondria."],
   "**Mitochondria.** Carrying oxygen by diffusion takes no energy input, so red blood cells have none. Every cell keeps its membrane.",
   "Muscle is the opposite case: constant energy, many mitochondria.")

Qa(2, "A protein on its way out of a gland cell has just left the rough ER. Where does it go next?",
   ["In a vesicle to the Golgi apparatus", "Straight to the cell membrane",
    "Back to a ribosome to be finished", "Into a lysosome to be digested"],
   "Make, fold, box, finish, box, out.",
   ["The route is ribosome → rough ER → vesicle → Golgi → vesicle → cell membrane.",
    "After the rough ER comes a vesicle carrying it to the Golgi.",
    "It only reaches the membrane after the Golgi has finished and shipped it.",
    "In a vesicle to the Golgi apparatus."],
   "**In a vesicle to the Golgi apparatus**, which finishes and ships it in a second vesicle to the cell membrane.",
   "Vesicle appears twice in the pathway — once before the Golgi, once after.")

Qa(2, "A student has the blue lens in place and turns the coarse knob to sharpen the image. What should they do instead?",
   ["Use only the fine knob", "Switch to the gray lens first",
    "Turn the light off and start again", "Move the slide to the edge of the stage"],
   "At high power the lens is almost touching the slide.",
   ["The blue lens is high power, sitting very close to the slide.",
    "The coarse knob moves the stage a long way and can crash the lens into it.",
    "From the blue lens on, only the fine (small) knob is used.",
    "Use only the fine knob."],
   "**Use only the fine knob.** At high power the coarse knob can drive the slide into the lens.",
   "Coarse on low power, fine on high power.")

Qa(2, "A student turns on the light, puts the blue lens in place, and cannot find the cell anywhere on the slide. What is the best next step?",
   ["Go back to the red lens and find it there", "Turn the coarse knob until it appears",
    "Turn the light up as far as it will go", "Switch to the gray lens for more power"],
   "Which lens gives the widest view?",
   ["The student skipped the lowest-power lens.",
    "High power shows a tiny area, so finding anything there is hard — and the coarse knob is off-limits now.",
    "The red lens gives the widest view, which is where you find the cell first.",
    "Go back to the red lens and find it there."],
   "**Go back to the red lens.** Find the cell at low power, then step up — red, yellow, blue.",
   "Always start with the lowest-power lens.")

Qa(2, "Put these steps for using a light microscope in order, from first to last.",
   ["Turn on the light", "Find the cell with the red lens",
    "Focus with the coarse knob", "Switch to the yellow lens"],
   "Low power before high; coarse before fine.",
   ["Nothing can be seen until the light is on.",
    "Start on the lowest-power lens, the red one, and move the stage to find the cell.",
    "Focus it with the coarse knob while still on low power.",
    "Only then step up to the yellow lens."],
   "**Light → find it on red → coarse focus → yellow.** Then blue, fine knob only, then gray if needed.",
   "The order is the same every time; practise it until it is automatic.", kind='order')

Qa(2, "A single-celled organism with no nucleus is found in a boiling, salty hot spring, giving off methane. Which group does it most likely belong to?",
   ["Archaea", "Bacteria", "Algae", "Fungi"],
   "No nucleus narrows it to two. Where it lives decides between them.",
   ["No nucleus means a prokaryote, which rules out algae and fungi.",
    "The two prokaryotic domains are archaea and bacteria.",
    "Extreme heat, high salt and making methane are the marks of archaea.",
    "Archaea."],
   "**Archaea.** Both prokaryotic domains lack a nucleus; archaea are the ones that live in extreme heat or salt and can make methane.",
   "Bacteria are everywhere; archaea are in the extremes.")

Qa(2, "Why is a virus not considered alive?",
   ["It is not made of cells and cannot reproduce on its own",
    "It has no genetic material of any kind at all",
    "It is too small to see without an electron microscope",
    "Its genetic material is RNA rather than DNA"],
   "Run down the six characteristics. How many does it pass?",
   ["A virus does have genetic material — DNA or RNA — so that is not the reason.",
    "Size has nothing to do with being alive; plenty of bacteria are tiny.",
    "It is not a cell, uses no energy of its own, does not grow, and can only be copied inside a host.",
    "Not made of cells, and cannot reproduce on its own."],
   "**It is not made of cells and cannot reproduce on its own** — it fails most of the six characteristics.",
   "On a fill-in question, name the characteristics it is missing.")

Qa(2, "Someone had chicken pox as a child and, decades later, develops shingles from the same virus. Which cycle explains the long delay?",
   ["Lysogenic — its genes stayed in host cells until conditions were right",
    "Lytic — it made new virus particles straight away",
    "Mitosis — the virus divided along with the host's cells",
    "Endosymbiosis — the virus became part of the cell for good"],
   "Which cycle waits?",
   ["A delay of decades means the virus did not make new particles straight away.",
    "In the lysogenic cycle the viral genes go into the host cell and wait.",
    "They can stay there a long time, until conditions are right — which is how shingles appears later.",
    "Lysogenic."],
   "**Lysogenic.** The viral genes sit in host cells for a long time before they are copied — shingles and HIV are the guide's examples.",
   "Lysogenic lies low.")

Qa(2, "A student wants to watch a living single-celled organism swim across a slide. Which microscope should they use?",
   ["A light microscope, because it can show living specimens",
    "An electron microscope, because it magnifies much more",
    "An electron microscope, because electrons bounce off cells",
    "Either one, because both can show living specimens"],
   "Only one of the two can show something that is still alive.",
   ["The organism has to be alive to swim.",
    "An electron microscope uses a beam of electrons and cannot observe living organisms.",
    "A light microscope can.",
    "A light microscope."],
   "**A light microscope.** The electron microscope magnifies more, but its specimen cannot be alive.",
   "Electron = more magnification, never living.")

Qa(2, "A cube-shaped cell has sides of 3 µm. What is its surface area-to-volume ratio?",
   ["2 to 1", "1 to 2", "3 to 1", "6 to 1"],
   "Surface area is 6 faces of s × s. Volume is s × s × s.",
   ["Surface area = 6 × 3 × 3 = 54 µm².",
    "Volume = 3 × 3 × 3 = 27 µm³.",
    "54 ÷ 27 = 2.",
    "2 to 1."],
   "**2 to 1.** 54 µm² of surface for 27 µm³ of volume. 1 to 2 is the same numbers flipped; 6 to 1 forgets to divide by the side.",
   "For any cube the ratio is 6 ÷ side: 6 ÷ 3 = 2.")

Qa(2, "A cell contains three X-shaped chromosomes and two single strands. How many chromosomes and chromatids does it have?",
   ["5 chromosomes, 8 chromatids", "5 chromosomes, 10 chromatids",
    "3 chromosomes, 8 chromatids", "8 chromosomes, 5 chromatids"],
   "Chromosomes: count centromeres. Chromatids: count strands.",
   ["Each X is one chromosome with two chromatids: 3 chromosomes, 6 chromatids.",
    "Each single strand is one chromosome with one chromatid: 2 chromosomes, 2 chromatids.",
    "Add them: 3 + 2 = 5 chromosomes, and 6 + 2 = 8 chromatids.",
    "5 chromosomes, 8 chromatids."],
   "**5 chromosomes, 8 chromatids.** 10 would count every chromosome as an X; the single strands have one chromatid each.",
   "Centromeres for chromosomes, strands for chromatids.")

Qa(2, "An animal cell that started with 5 chromosomes reaches metaphase. How many chromatids line up on the metaphase plate?",
   ["10", "5", "20", "0"],
   "What happened to the DNA in S phase?",
   ["In S phase every chromosome was copied into two sister chromatids.",
    "5 chromosomes × 2 chromatids each = 10 chromatids.",
    "At metaphase they are still joined, lined up across the middle.",
    "10."],
   "**10.** Five chromosomes, each two sister chromatids, lined up on the metaphase plate. They only split in anaphase.",
   "Metaphase: 5 chromosomes, 10 chromatids. Anaphase: 10 chromosomes.")

Qa(2, "A cell's DNA has already been copied, and it is now making the molecules and organelles it will need for mitosis. Which phase is it in?",
   ["G2", "G1", "S", "G0"],
   "The DNA is copied, so it is past S.",
   ["DNA copying happens in S, so the cell is past S.",
    "G1 builds for the daughter cells, before the DNA is copied.",
    "Getting ready for mitosis itself, after S, is G2.",
    "G2."],
   "**G2** — after S, preparing the molecules and organelles mitosis needs.",
   "G1 → S → G2: grow, copy, get ready.")

Qa(2, "Which is true of a prokaryote's chromosome?",
   ["It is a single circular strand with no histones",
    "It is wound on histones inside a nucleus",
    "It is many linear strands in the nucleoid",
    "It is many circular strands wound on histones"],
   "No nucleus, no histones, and only one of them.",
   ["Prokaryotes have no nucleus, so the chromosome sits in the nucleoid region.",
    "Prokaryotic chromosomes have no histones.",
    "There is usually one, and it is circular.",
    "A single circular strand with no histones."],
   "**A single circular strand with no histones**, in the nucleoid region. Many linear strands on histones is the eukaryote pattern.",
   "One ring (prokaryote) vs many strands on spools (eukaryote).")

Qa(2, "A student says a new cell can form from non-living material if conditions are right. Which part of the cell theory does this contradict?",
   ["All cells come from existing cells",
    "All living things are made of one or more cells",
    "The cell is the basic unit of all living things",
    "All living things obtain and use energy"],
   "The claim is about where cells come FROM.",
   ["The claim is about the origin of a new cell.",
    "Only one statement of the cell theory is about where cells come from.",
    "It says all cells come from existing cells — never from non-living material.",
    "All cells come from existing cells."],
   "**All cells come from existing cells.** Obtaining energy is one of the six characteristics of life, not part of the cell theory.",
   "Cell theory: made of, unit of, comes from.")

# --- level 3: analyze
Qa(3, "Cell A is a cube with sides of 2 µm; cell B is a cube with sides of 5 µm. Which is better at moving materials in and out, and why?",
   ["A, because its ratio is 3 to 1 against B's 1.2 to 1",
    "B, because it has more total surface area than A",
    "B, because its larger volume can store more material",
    "Neither, because both cubes have the same shape"],
   "Work out 6 ÷ side for each.",
   ["For a cube, SA : V = 6 ÷ side.",
    "Cell A: 6 ÷ 2 = 3. Cell B: 6 ÷ 5 = 1.2.",
    "More membrane per unit of volume means faster exchange for the inside.",
    "A, because its ratio is higher."],
   "**Cell A.** B has more surface in total, but far less per unit of volume — 1.2 against 3 — so its middle is badly supplied.",
   "Total surface area is the trap. The RATIO is what matters.")

Qa(3, "An animal cell begins mitosis with 5 chromosomes. During anaphase, how many chromosomes are moving apart in total?",
   ["10 chromosomes", "5 chromosomes", "20 chromosomes", "15 chromosomes"],
   "When sister chromatids separate, what does each one count as?",
   ["Before anaphase there are 5 chromosomes, each two sister chromatids — 10 chromatids.",
    "In anaphase the sisters are pulled apart.",
    "The moment they separate, each chromatid counts as a chromosome of its own.",
    "10 chromosomes."],
   "**10 chromosomes** — 5 heading to each pole, so each new cell ends with the 5 it started with.",
   "The chromosome count doubles in anaphase and halves again at cytokinesis.")

Qa(3, "Why can a DNA copying error that slips past every check lead to cancer?",
   ["The cell keeps dividing and passes the error to every copy",
    "The error forces the cell into G0 for the rest of its life",
    "The error stops the cell from making any proteins at all",
    "The error shuts down the cell's mitochondria for good"],
   "What does a cell do after G2 if nothing stops it?",
   ["A cell that reaches G2 usually goes on to mitosis.",
    "Mitosis makes identical copies — including any uncorrected error.",
    "If the error affects how division is controlled, the copies keep dividing too.",
    "Uncontrolled division carrying the error is cancer."],
   "**The cell keeps dividing and copies the error into every daughter cell.** An error in the genes that control division is how growth becomes uncontrolled.",
   "Uncorrected replication errors → cancer. That blank is on the guide.")

Qa(3, "A field of banana plants is grown entirely from cuttings, so every plant is genetically identical. A fungus arrives that kills one of them. What is the biggest risk?",
   ["It can kill them all, since none of them differ in a way that could resist it",
    "Only the one plant is at risk, since each plant grows separately",
    "The others will quickly develop resistance on their own",
    "The fungus cannot spread between plants grown from cuttings"],
   "Clones share every weakness.",
   ["Cuttings grow by mitosis, so every plant is a genetic copy.",
    "Identical plants have identical defences — and identical weaknesses.",
    "If the fungus can kill one, nothing about the others is different enough to stop it.",
    "It can kill them all."],
   "**It can kill them all.** No genetic variation means no plant carries a difference that might resist the disease — the main downside of reproducing by mitosis.",
   "Asexual reproduction: fast and identical. The price is no variation.", frm=A)

Qa(3, "Which observation fits the idea that mitochondria were once free-living prokaryotes?",
   ["They carry their own DNA and ribosomes, like a prokaryote does",
    "They are found in almost every eukaryotic cell there is",
    "They release the energy stored in sugar as ATP",
    "They are made by the Golgi apparatus and shipped in vesicles"],
   "What would a cell that used to live on its own still be carrying?",
   ["A free-living cell needs its own genetic instructions and its own protein factories.",
    "Mitochondria still have both: their own DNA and their own ribosomes.",
    "Being common, or doing respiration, says nothing about where they came from.",
    "Their own DNA and ribosomes."],
   "**Their own DNA and ribosomes** — the leftovers of a cell that once lived independently. Chloroplasts carry the same evidence.",
   "Endosymbiont theory: mitochondria and chloroplasts; evidence DNA and ribosomes.")

Qa(3, "A cell has a cell wall, ribosomes and a cell membrane, but no nucleus and no lysosomes. Which one statement must be true?",
   ["It is a prokaryote", "It is a plant cell",
    "It is an animal cell", "It is a fungal cell"],
   "Which single missing structure decides it?",
   ["A cell wall, ribosomes and a membrane are all found in prokaryotes and in some eukaryotes.",
    "But every eukaryote — plant, animal, fungus — has a nucleus.",
    "No nucleus means a prokaryote.",
    "It is a prokaryote."],
   "**It is a prokaryote.** The missing nucleus decides it; a cell wall alone could be a plant, a fungus or a bacterium.",
   "Look for the structure that only one side of the chart has.")

# --- spelling: the real test is fill-in-the-blank
def sp(text, word, hint, steps, main, tip):
    q(Q, 1, text, [word], 0, hint, steps, main, tip, kind='spell')

sp("Spell the word for body cells — every cell except sperm and eggs.", 'somatic',
   "Soma means body. Three syllables: so · MA · tic.",
   ["Soma is Greek for body.", "Add -tic: so · ma · tic.", "somatic."],
   "**somatic.** Somatic cells are diploid and divide by mitosis.",
   "One m, one t.")
sp("Spell the word for a cell with only ONE set of chromosomes.", 'haploid',
   "Hap- as in half, then the same ending as diploid.",
   ["It starts hap-, as in half.", "It ends -loid, like diploid.", "haploid."],
   "**haploid.** Gametes are haploid; somatic cells are diploid.",
   "h-a-p-l-o-i-d: hap + loid.")
sp("Spell the word for sex cells — sperm and eggs.", 'gametes',
   "Two syllables: GAM · eets.",
   ["Say it: GAM-eets.", "Spell the sound 'eets' as -etes.", "gametes."],
   "**gametes.** Gametes are made by meiosis, not mitosis.",
   "It is game + tes.")
sp("Spell the name of the proteins that DNA winds around in a eukaryote's chromosomes.", 'histones',
   "His · tones — the word 'tones' is inside it.",
   ["Start with his-.", "Then the word tones.", "histones."],
   "**histones.** DNA on histones is chromatin; each wrapped bead is a nucleosome.",
   "his + tones.")
sp("Spell the name of the step that divides the cytoplasm to make two separate cells.", 'cytokinesis',
   "Cyto (cell) + kinesis (movement).",
   ["Cyto- means cell, as in cytoplasm.", "Kinesis means movement: ki · NEE · sis.", "cytokinesis."],
   "**cytokinesis.** Mitosis divides the nucleus; cytokinesis divides the cytoplasm.",
   "Cyto + kinesis, no letters dropped.")
sp("Spell the name of the prokaryotic domain that lives in extreme heat, high salt or no oxygen.", 'archaea',
   "It starts like archaeology — ancient — and ends with -aea.",
   ["It starts arch-, like archaeology.", "It ends -aea: ar · KEE · uh.", "archaea."],
   "**archaea.** The other prokaryotic domain is bacteria.",
   "Two a's around the e at the end: -aea.")

build('ad-astra', C, Q, 'unit-bio-sgt2', 'Biology 8 · Test 2 Study Guide', 'bio',
      "The teacher's study guide for Wednesday's Test 2 covers Units 3 and 4. Unit 3: the cell theory "
      "and the six characteristics of living things, viruses and the lytic and lysogenic cycles, the two "
      "prokaryotic domains, the four eukaryotic kingdoms, a nineteen-row chart of cell structures — what "
      "each does and whether prokaryotes and eukaryotes have it — the protein pathway out of the cell, "
      "which organelles different cells need, endosymbiont theory, the respiration and photosynthesis "
      "equations, and using a light microscope. Unit 4: surface area-to-volume ratio, the cell cycle and "
      "G0, chromatin, histones and nucleosomes, counting chromosomes and chromatids, mitosis in a "
      "five-chromosome cell, and what mitosis is for.",
      "The test follows the guide, and the guide is fill-in-the-blank — which means pulling the word out "
      "of your own head, not spotting it in a list. So the cards come first, answered out loud before "
      "you flip. The quiz then asks the same ideas from fresh angles, plus six words to spell, because a "
      "blank marks the spelling as well as the idea.",
      [("State the three parts of the cell theory and the six characteristics of living things", 'source'),
       ("Explain why viruses are not alive, and tell the lytic cycle from the lysogenic cycle", 'source'),
       ("Fill in the cell-structure chart: each structure's job, and whether prokaryotes and eukaryotes have it", 'source'),
       ("Use a light microscope in the right order, and spot a student's mistake in using one", 'source'),
       ("Work a cube's surface area-to-volume ratio and count chromosomes and chromatids", 'source'),
       ("Name each phase of the cell cycle, and which cells sit in G0", 'source')],

      "Built from the teacher's own Test 2 study guide (Wednesday 9/30), which covers Units 3 and 4. "
      "The copy in Drive is the filled-in one; it was read for what the guide ASKS, and every blank, "
      "chart row and prompt on it has a card here. Nothing on it was marked or recorded.\n\n"
      "The guide is a scan, so its pages were rendered and read as images. It was checked against the "
      "Unit 3 slide deck in the same Biology folders before anything was written, and four things came "
      "out of that worth knowing.\n\n"
      "FIRST — viruses, the two prokaryotic domains, cyanobacteria and the microscope are not in the "
      "Unit 3 deck. The guide states most of that in its own sentences, and those are what the cards use. "
      "Where the guide only asks (why viruses are not alive, the downside of reproducing by mitosis, why "
      "only the fine knob at high power), the answer is standard biology and is marked as a study "
      "suggestion rather than class material.\n\n"
      "SECOND — the fourth eukaryotic kingdom. The guide's blank is followed by '(single cellular)'. The "
      "class's own slides list eukaryotic cells as 'animal, plant, algae and fungal', while the standard "
      "name for that kingdom is protists, with algae as its best-known members. The card teaches both "
      "words; it is worth one question to the teacher about which one the key wants.\n\n"
      "THIRD — the chart's cytoskeleton row asks whether prokaryotes have one. That is taught both ways "
      "at this level (prokaryotes have related protein fibres), so the card gives only the eukaryote half "
      "and does not pick. Every other row is settled by the deck.\n\n"
      "FOURTH — the drawing tasks (a virus, the five-chromosome mitosis series, a cell plate, the chart's "
      "drawing column) are paper-only; the cards give the counts and features to check a drawing against. "
      "The teacher's note says the microscope may come up as a student making a mistake, so two questions "
      "do exactly that. The lens colours are the guide's own sequence.\n\n"
      "The test is Wednesday, so this is best approved straight away.",

      ("Flashcards first, twice through, saying each answer OUT LOUD before you flip — the test is "
       "fill-in-the-blank. Then quiz rounds, including the spelling ones, until the Growth Zone is quiet.", 35),
      'content/bio-sg-test2.json',
      'Test 2 (Wednesday 9/30) Study Guide — Units 3 and 4 (Drive)',
      "Biology 8, the teacher's own Test 2 study guide, covering Units 3 and 4",
      offset_hours=3, order_=1, prep_=True, libv_=1)

p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                 'content', 'bio-sg-test2.json')
d = json.load(io.open(p, encoding='utf-8'))
d['records']['unit-bio-sgt2']['book'] = True     # a study guide is not a race — no Beat the clock
io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
print('book set')
