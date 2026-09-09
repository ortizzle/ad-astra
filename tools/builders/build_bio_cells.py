#!/usr/bin/env python3
"""Biology 8 · Unit 3: Cells and Cell Structures.

Source: "G8_Cells_VA.pdf" — the teacher's own lecture deck, Drive, uploaded
2026-09-09. Clean text layer, read straight through.

The diagrams are Wikimedia Commons, hotlinked via the stable
Special:FilePath redirect — the same mechanism and the same licence reasoning
as the ASL manual alphabet (v130): freely-licensed reference art is MEANT to
be reused, which is exactly why those embed while a commercial video
dictionary only ever gets a link. Every filename below was confirmed to exist
and confirmed public domain by search before it was written in; not one was
guessed or pattern-matched from the term. Note the punctuation traps that a
guess would have got wrong: the plant cell uses `-en`, the prokaryote uses
`-_en`, and the animal cell uses `_en`.
"""
import io, json, sys
sys.path.insert(0, '/home/user/ad-astra/tools/builders')
from unit_common import card, q, _balance, build

C, Q = [], []

FP = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
PD = 'Wikimedia Commons · public domain'


# ---------------------------------------------------------------- cards

card(C, 'The cell theory',
     "**All organisms are made of one or more cells, the cell is the basic unit of all living "
     "things, and all cells come from existing cells.**\n"
     "• Three statements, built up by many scientists over many years — not one discovery\n"
     "• The third is the one people forget, and it is the one that rules out cells appearing "
     "from nothing",
     hint="Made of, basic unit of, comes from.")

card(C, 'Hooke and Leeuwenhoek',
     "**Hooke named cells in 1665 looking at cork; Leeuwenhoek found living single-celled "
     "organisms in 1673.**\n"
     "• Hooke was looking at dead plant tissue, and the empty boxes reminded him of monks' rooms\n"
     "• Leeuwenhoek's pond scum held protists, and he was also first to see blood, bacterial and "
     "yeast cells",
     hint="Hooke saw the walls of dead plant cells; Leeuwenhoek saw things swimming.")

card(C, 'Surface area-to-volume ratio',
     "**A cell's outer surface compared with its volume — and it is what limits how big a cell "
     "can get.**\n"
     "• As a cell grows, volume increases FASTER than surface area\n"
     "• So a big cell has relatively less membrane to feed and clean the inside it has to serve\n"
     "• For a cube of side s the ratio works out at 6/s, so smaller means higher",
     hint="Volume outruns surface. That race is why cells stay small.")

card(C, 'Why a chicken egg yolk breaks the rule',
     "**It is one enormous cell that gets away with it because it is not taking nutrients in "
     "across its surface.**\n"
     "• The rule is about supply — a cell that must import and export across its membrane is "
     "limited by that membrane\n"
     "• A yolk carries its own stored food instead",
     hint="The limit is about traffic across the surface. Remove the traffic, remove the limit.")

card(C, 'Prokaryotic cell',
     "**A cell with no nucleus and no membrane-bound organelles.**\n"
     "• Bacteria and archaea; always unicellular\n"
     "• DNA is a single circular double-stranded chromosome, loose in a region called the "
     "nucleoid — a region, not a compartment\n"
     "• Still has a cell membrane, cytoplasm and ribosomes; most also have a cell wall\n"
     "• On average about ten times smaller than a eukaryotic cell",
     hint="No nucleus, no organelles — but never 'no structures'.",
     img=FP + 'Average_prokaryote_cell-_en.svg', imgWide=True,
     imgAlt='A labelled diagram of a typical prokaryotic cell, showing the cell wall, cell '
            'membrane, cytoplasm, ribosomes, the circular DNA in the nucleoid region, plasmids, '
            'pili and a flagellum.',
     imgCredit='Diagram: LadyofHats, ' + PD)

card(C, 'Extras some prokaryotes carry',
     "**Plasmids, flagella and a capsule.**\n"
     "• Plasmid — a small ring of DNA separate from the main chromosome, often carrying "
     "accessory genes\n"
     "• Flagellum — whips the cell along in liquid (plural: flagella)\n"
     "• Capsule — a sticky sugar-and-protein layer outside the cell wall that protects the cell "
     "and helps it stick to surfaces",
     hint="Spare genes, a propeller, and a sticky coat.")

card(C, 'Eukaryotic cell',
     "**A cell with a nucleus and membrane-bound organelles.**\n"
     "• Animals, plants, algae and fungi; may be unicellular or multicellular\n"
     "• DNA is usually several linear double-stranded chromosomes, stored inside the nucleus\n"
     "• Compartmentalisation is the payoff: separate compartments let different parts of one "
     "cell specialise in different jobs at once",
     hint="Rooms in a house. Each room can do a different job because it has walls.",
     img=FP + 'Animal_cell_structure_en.svg', imgWide=True,
     imgAlt='A labelled cross-section of an animal cell showing the nucleus and nucleolus, rough '
            'and smooth endoplasmic reticulum, Golgi apparatus, mitochondria, lysosomes, '
            'vesicles, ribosomes, centrioles, cytoskeleton and the plasma membrane.',
     imgCredit='Diagram: LadyofHats, ' + PD)

card(C, 'Plant cell',
     "**A eukaryotic cell that additionally has a cell wall, chloroplasts and one large "
     "permanent central vacuole.**\n"
     "• Everything an animal cell has, plus those three\n"
     "• The central vacuole pressing outward against the wall is what holds a plant up — that "
     "pressure is called turgor pressure\n"
     "• Animal cells have no cell wall and no chloroplasts at all",
     hint="Three additions, and one of them is doing the standing up.",
     img=FP + 'Plant_cell_structure-en.svg', imgWide=True,
     imgAlt='A labelled cross-section of a plant cell showing the cell wall, plasma membrane, '
            'large central vacuole, chloroplasts, nucleus, rough and smooth endoplasmic '
            'reticulum, Golgi apparatus and mitochondria.',
     imgCredit='Diagram: LadyofHats, ' + PD)

card(C, 'Organelle',
     "**Any membrane-enclosed structure with a specialised job inside the cytoplasm of a "
     "eukaryotic cell.**\n"
     "• The membrane is the part that matters in the definition — it is what makes a separate "
     "compartment possible\n"
     "• Ribosomes are sub-cellular structures but are NOT membrane-bound, which is why every "
     "cell can have them",
     hint="The definition has 'membrane-enclosed' in it for a reason.")

card(C, 'Plasma membrane',
     "**The cell's outer boundary — a phospholipid bilayer that controls what enters and "
     "leaves.**\n"
     "• Selectively permeable, which is how a cell holds its inside steady while the outside "
     "changes\n"
     "• A fluid mosaic: mostly phospholipids, with proteins, cholesterol, glycoproteins and "
     "glycolipids drifting in it\n"
     "• Carries receptors, so cells can read signals from other cells\n"
     "• A cell wall, where there is one, sits OUTSIDE it and is considered extracellular",
     hint="Fluid because things drift in it; mosaic because it is not made of one thing.")

card(C, 'Cytoplasm and cytosol',
     "**Cytoplasm is everything inside the membrane except the nucleus; cytosol is just the "
     "liquid part of it.**\n"
     "• The cytosol carries dissolved molecules the cell needs\n"
     "• Most of the cell's metabolism happens out here, not inside an organelle",
     hint="Cytoplasm includes the furniture. Cytosol is only the water.")

card(C, 'Nucleus',
     "**Stores the DNA and directs the cell by controlling which proteins get made.**\n"
     "• Holds the chromosomes — DNA wound together with proteins\n"
     "• Wrapped in a nuclear membrane whose pores let selected material move in and out\n"
     "• It does not build proteins itself; it holds the instructions for them",
     hint="A library, not a workshop.",
     img=FP + 'Diagram_human_cell_nucleus.svg', imgWide=True,
     imgAlt='A labelled diagram of a cell nucleus showing the nuclear envelope with its double '
            'membrane, nuclear pores, the nucleolus, chromatin and surrounding ribosomes.',
     imgCredit='Diagram: LadyofHats, ' + PD)

card(C, 'Nucleolus',
     "**A dense region inside the nucleus that builds ribosomes.**\n"
     "• rRNA is made here and combined with proteins to assemble ribosomes\n"
     "• Some cells have more than one\n"
     "• It has no membrane of its own — it is a region within the nucleus, not a separate "
     "organelle",
     hint="The ribosome factory, sitting inside the library.")

card(C, 'Ribosomes',
     "**Assemble proteins — and every cell has them, prokaryote and eukaryote alike.**\n"
     "• Free in the cytosol: usually making proteins the cell will use itself\n"
     "• Bound to the rough ER: usually making proteins that will be embedded in the membrane or "
     "shipped out of the cell\n"
     "• A cell's ribosome count varies enormously with what it does for a living",
     hint="Same machine, two postings — and the posting predicts the destination.")

card(C, 'Rough endoplasmic reticulum',
     "**A stack of interconnected membrane sacs studded with ribosomes, where proteins bound "
     "for export are folded and moved along.**\n"
     "• The 'rough' is the ribosomes on the outside\n"
     "• Proteins made by those bound ribosomes fold inside it",
     hint="Rough because of what is stuck to it.")

card(C, 'Smooth endoplasmic reticulum',
     "**The same kind of membrane sacs with NO ribosomes, making lipids and breaking down "
     "toxins.**\n"
     "• Builds the lipids that go into cell membranes\n"
     "• Depending on the cell, may also handle sugar metabolism or store calcium\n"
     "• Liver cells, which break down toxins, are loaded with it",
     hint="No ribosomes — so it works on fats, not proteins.")

card(C, 'Golgi apparatus',
     "**Finishes, sorts, labels and ships proteins that arrived from the rough ER.**\n"
     "• A stack of flattened membrane sacs\n"
     "• Sends its output out in vesicles — and lysosomes are vesicles that came from here\n"
     "• The shipping department, working on packages somebody else built",
     hint="Nothing is made here from scratch. It finishes and addresses.")

card(C, 'Vesicle',
     "**A small membrane-enclosed sac that moves material around inside the cell, or stores "
     "it.**\n"
     "• The cell's transport container between compartments\n"
     "• Vesicles bud from the ER and from the Golgi",
     hint="A bubble with cargo in it.")

card(C, 'Lysosome',
     "**A membrane sac of digestive enzymes that breaks down food and recycles worn-out cell "
     "parts.**\n"
     "• Digests broken organelles so the pieces can be reused\n"
     "• Some immune cells use them to destroy pathogens they have engulfed\n"
     "• Also has a role in programmed cell death — apoptosis",
     hint="The recycling plant, and it comes packaged from the Golgi.")

card(C, 'Vacuoles',
     "**Storage organelles — small and temporary in animal cells, one large permanent one in "
     "plant cells.**\n"
     "• Store water, salts, proteins and carbohydrates, and can hold waste\n"
     "• The plant central vacuole creates turgor pressure and can do a lysosome's job in some "
     "plant cells\n"
     "• A contractile vacuole lets a wall-less unicellular organism pump water back out\n"
     "• A food vacuole lets one store and digest a particle it has engulfed",
     hint="Same word, very different sizes depending on whose cell it is.")

card(C, 'The secretory pathway',
     "**Bound ribosome → rough ER → vesicle → Golgi apparatus → vesicle → cell membrane.**\n"
     "• That is the route a protein takes from being assembled to leaving the cell\n"
     "• Vesicles appear twice in it, because moving between compartments always needs a "
     "container\n"
     "• Knowing the order is what lets you predict which step fails when one organelle is "
     "disabled",
     hint="Built, folded, carried, finished, carried, out.",
     img=FP + 'Endomembrane_system_diagram_en.svg', imgWide=True,
     imgAlt='A labelled diagram of the endomembrane system showing the nucleus and nuclear '
            'envelope, rough and smooth endoplasmic reticulum, transport vesicles, the Golgi '
            'apparatus, a lysosome and the plasma membrane.',
     imgCredit='Diagram: Mariana Ruiz (LadyofHats), ' + PD)

card(C, 'Mitochondria',
     "**Release energy from sugar and store it in ATP — cellular respiration.**\n"
     "• C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP\n"
     "• Found in nearly all eukaryotes, plants very much included\n"
     "• Folds of the inner membrane are cristae; the fluid inside is the matrix\n"
     "• Has its own DNA and its own ribosomes",
     hint="Cristae are folds, and folds mean more surface to work on.",
     img=FP + 'Animal_mitochondrion_diagram_en.svg', imgWide=True,
     imgAlt='A labelled cutaway of a mitochondrion showing the outer membrane, the inner membrane '
            'folded into cristae, the intermembrane space, the matrix, ribosomes and mitochondrial '
            'DNA.',
     imgCredit='Diagram: LadyofHats, ' + PD)

card(C, 'Chloroplasts',
     "**Capture sunlight to build sugar — photosynthesis.**\n"
     "• 6CO₂ + 6H₂O + sunlight → C₆H₁₂O₆ + 6O₂\n"
     "• Found in plant and algae cells, never in animal cells\n"
     "• Contain the pigment chlorophyll\n"
     "• Has its own DNA and its own ribosomes, like mitochondria",
     hint="It makes the sugar. Mitochondria spend it.",
     img=FP + 'Chloroplast_diagram.svg', imgWide=True,
     imgAlt='A labelled cutaway of a chloroplast showing the outer and inner membranes, the '
            'stroma, thylakoids stacked into grana, and the lamellae connecting them.',
     imgCredit='Diagram: Wikimedia Commons, public domain')

card(C, 'Endosymbiont theory',
     "**Mitochondria and chloroplasts were once free-living prokaryotes that an ancestor of "
     "eukaryotic cells engulfed and never digested.**\n"
     "• The engulfed cell became an endosymbiont — a cell living inside another cell\n"
     "• Over time host and endosymbiont merged into one organism\n"
     "• The three pieces of evidence: both have double membranes, both have their own circular "
     "DNA and their own ribosomes, and both reproduce on their own schedule rather than with the "
     "cell",
     hint="Three pieces of evidence, and each one is a leftover of independent life.")

card(C, 'Cytoskeleton',
     "**A network of protein fibres running through the cytoplasm that holds the cell's shape "
     "and anchors what is inside it.**\n"
     "• Three kinds of fibre: microfilaments, intermediate filaments, microtubules\n"
     "• Supports organelles in place and enables movement, including cilia and flagella",
     hint="Skeleton and scaffolding at once — it holds shape AND holds things still.")

card(C, 'Centrioles and centrosomes',
     "**Organise cell division in animal cells.**\n"
     "• A centrosome is made of two centrioles\n"
     "• One pair per cell\n"
     "• Animal cells — this is one of the structures plant cells manage without",
     hint="They set up the division, they do not do the dividing.")

card(C, 'Form fits function',
     "**A cell's job predicts which organelle it is stocked with.**\n"
     "• Muscle cells need constant energy, so they carry many mitochondria\n"
     "• Macrophages destroy invaders, so they carry many lysosomes\n"
     "• Liver cells break down toxins, so they carry a lot of smooth ER",
     hint="Work backwards: name the job, then ask which organelle does it.")


# ------------------------------------------------------------ questions

q(Q, 1, "Which statement is NOT part of the cell theory?",
  ["Every cell arises from a cell that already existed",
   "All organisms are made of one or more cells",
   "The cell is the basic unit of all living things",
   "Every cell contains a nucleus that directs it"],
  3,
  "Three of these are the theory. One is a claim about structure that a whole domain of life "
  "breaks.",
  ["The cell theory has exactly three statements, and none of them is about a nucleus.",
   "Bacteria and archaea are cells, and they have no nucleus at all.",
   "So a claim that every cell has a nucleus is simply false, whatever else it sounds like.",
   "The nucleus claim is the one that is not part of the cell theory."],
  "**Every cell containing a nucleus is not part of the cell theory, and it is not even true.** "
  "Prokaryotes are cells and have no nucleus. The three real statements are about what organisms "
  "are made of, what the basic unit is, and where new cells come from.",
  "When a question offers three things from one list and one from nowhere, find the list first.")

q(Q, 1, "A biologist lists three things every known cell has. What are they?",
  ["A cell membrane, cytoplasm and ribosomes",
   "A cell wall, a nucleus and mitochondria",
   "A nucleus, chloroplasts and a vacuole",
   "Membrane-bound organelles, a nucleolus and cristae"],
  0,
  "Whatever is on the list has to be true of a bacterium as well as of a leaf cell.",
  ["Anything universal has to hold for prokaryotes, which have no nucleus and no organelles.",
   "That rules out every option naming a nucleus, an organelle or a structure inside one.",
   "A membrane, cytoplasm and ribosomes are present in prokaryotes and eukaryotes alike.",
   "The membrane, cytoplasm and ribosomes are the three."],
  "**A membrane, cytoplasm and ribosomes are the universal set.** Cell walls are absent from "
  "animal cells, and nuclei, chloroplasts and mitochondria are all absent from prokaryotes — so "
  "none of those can be on a list of what EVERY cell has.",
  "Test any 'all cells' claim against a bacterium. It is the one that breaks most of them.")

q(Q, 1, "What does the nucleolus do?",
  ["Builds ribosomes",
   "Copies DNA before the cell divides",
   "Packages proteins for shipping",
   "Breaks down worn-out organelles"],
  0,
  "It sits inside the nucleus and it is a factory for one specific machine.",
  ["The nucleolus is a dense region inside the nucleus.",
   "rRNA is made there and combined with proteins.",
   "That combination is what a ribosome is made of.",
   "So the nucleolus builds ribosomes."],
  "**The nucleolus builds ribosomes.** rRNA is synthesised there and joined with proteins to "
  "assemble them. Packaging is the Golgi's job and demolition is the lysosome's — the nucleolus "
  "makes the machine that builds proteins in the first place.",
  "Nucleolus and ribosome go together. One is where the other is made.")

q(Q, 1, "Where in a eukaryotic cell does cellular respiration release energy into ATP?",
  ["In the mitochondria", "In the chloroplasts", "In the smooth ER", "In the Golgi apparatus"],
  0,
  "One organelle spends sugar for energy and another makes sugar from sunlight.",
  ["Cellular respiration takes sugar and oxygen and releases energy stored as ATP.",
   "Chloroplasts run the opposite process, building sugar using sunlight.",
   "The smooth ER makes lipids and the Golgi finishes proteins; neither handles respiration.",
   "Respiration happens in the mitochondria."],
  "**Mitochondria run cellular respiration.** They take the energy stored in glucose and store it "
  "in ATP instead. Chloroplasts are the counterpart, not a synonym: they build the sugar that "
  "mitochondria later spend.",
  "Chloroplast makes the fuel, mitochondrion burns it. Plants have both.")

q(Q, 1, "What distinguishes rough endoplasmic reticulum from smooth?",
  ["Ribosomes are attached to the rough kind and not to the smooth kind",
   "The rough kind is found only in animal cells",
   "The smooth kind is enclosed by a double membrane",
   "The rough kind is made of protein fibres rather than membrane"],
  0,
  "The names describe how they look under a microscope, and the reason is stuck to the outside.",
  ["Both are networks of flattened, interconnected membrane sacs.",
   "The rough kind has ribosomes bound to its outer surface, which is what makes it look rough.",
   "The smooth kind has none, and works on lipids and toxins instead of proteins.",
   "The ribosomes are the difference."],
  "**Bound ribosomes are the whole difference.** They are what make the rough ER look rough, and "
  "they are why it handles proteins while the smooth ER handles lipids, sugars and toxins.",
  "The name is literal. Rough means covered in something.")

q(Q, 1, "What is a plasmid?",
  ["A small ring of DNA separate from a prokaryote's main chromosome",
   "The region of a prokaryote where the chromosome sits",
   "A sticky layer outside a bacterial cell wall",
   "A tail that moves a bacterium through liquid"],
  0,
  "All four are real prokaryotic terms. Only one of them is made of DNA.",
  ["A prokaryote's main chromosome is a single circular molecule in the nucleoid region.",
   "Some prokaryotes carry additional small DNA rings apart from it.",
   "Those rings often carry accessory genes, and they are called plasmids.",
   "A plasmid is that small separate ring of DNA."],
  "**A plasmid is a small ring of DNA outside the main chromosome**, often carrying accessory "
  "genes. The nucleoid is the region the main chromosome occupies, the capsule is the sticky "
  "outer layer, and the flagellum is what moves the cell — different structures entirely.",
  "Four prokaryote words worth keeping apart: nucleoid, plasmid, capsule, flagellum.")

q(Q, 2, "A cell is found to have ribosomes, a cell wall and a cell membrane, and nothing else can "
        "be determined. What could it be?",
  ["Either a prokaryote or a plant, algal or fungal cell",
   "Only a prokaryote, because of the cell wall",
   "Only an animal cell, because of the ribosomes",
   "Only a plant cell, because it has both a wall and a membrane"],
  0,
  "Ask which groups can have a cell wall, then check whether the other two facts narrow it "
  "further.",
  ["Every cell has ribosomes and a membrane, so those two facts exclude nothing at all.",
   "That leaves the cell wall as the only real clue.",
   "Most prokaryotes have a cell wall, and among eukaryotes so do plant, algal and fungal cells.",
   "Animal cells are the ones ruled out, leaving prokaryotes and those three eukaryote groups."],
  "**Only animal cells are excluded.** Ribosomes and a membrane are universal, so they carry no "
  "information here. A cell wall rules out animal cells and nothing else — plants, algae, fungi "
  "and most prokaryotes all have one.",
  "A fact that is true of every cell cannot narrow anything down. Spot those first.")

q(Q, 2, "A gland cell's whole job is manufacturing a hormone and releasing it into the "
        "bloodstream. Which organelles would you expect it to be unusually rich in?",
  ["Rough ER and Golgi apparatus",
   "Smooth ER and lysosomes",
   "Chloroplasts and central vacuole",
   "Centrioles and cytoskeleton"],
  0,
  "Trace the route an exported protein takes and see which stops do the most work.",
  ["A hormone released from the cell is a protein bound for export.",
   "Exported proteins are built by ribosomes bound to the rough ER and folded there.",
   "They are then finished, labelled and packaged for shipping by the Golgi apparatus.",
   "So rough ER and Golgi are the two the cell would need in quantity."],
  "**Rough ER and Golgi, because those are the export line.** Bound ribosomes and the rough ER "
  "build and fold the protein; the Golgi finishes and packages it for release. Smooth ER and "
  "lysosomes would point at a cell that breaks things down instead.",
  "Match the organelle to the verb in the question. 'Manufacturing and releasing' is the "
  "secretory pathway.")

q(Q, 2, "Put the stops on a secreted protein's route in the order it travels them.",
  ["Rough ER", "Transport vesicle", "Golgi apparatus", "Secretory vesicle to the membrane"],
  0,
  "It is built and folded first, and it can only cross open space inside a container.",
  ["Bound ribosomes on the rough ER build the protein and it folds inside the rough ER.",
   "It cannot cross the cytosol unpackaged, so a transport vesicle carries it onward.",
   "The Golgi apparatus finishes, sorts and labels it.",
   "A second vesicle carries the finished protein to the cell membrane to be released."],
  "**Rough ER, then a transport vesicle, then the Golgi, then a secretory vesicle to the "
  "membrane.** Vesicles show up twice because every move between compartments needs a container "
  "— that repetition is the part worth remembering.",
  "Anywhere the protein has to cross open cytosol, look for a vesicle.",
  kind='order')

q(Q, 2, "Four cube-shaped model cells have sides of 1, 2, 3 and 6 units. Which has the greatest "
        "surface area-to-volume ratio?",
  ["The cube with sides of 1 unit", "The cube with sides of 2 units",
   "The cube with sides of 3 units", "The cube with sides of 6 units"],
  0,
  "Work out both quantities for a cube in terms of its side, then divide and see what happens as "
  "the side grows.",
  ["A cube of side s has surface area 6s² and volume s³.",
   "Dividing gives a ratio of 6s² ÷ s³, which simplifies to 6/s.",
   "So the ratio depends only on s, and it gets SMALLER as s gets larger: 6, 3, 2 and 1.",
   "The 1-unit cube has the greatest ratio, at 6."],
  "**The smallest cube wins, at a ratio of 6.** For any cube the ratio is 6/s, so the four work "
  "out at 6, 3, 2 and 1. This is exactly why cells stay small: growing makes volume outrun the "
  "surface that has to supply it.",
  "Whenever a shape scales up, volume grows by the cube and surface only by the square.")

q(Q, 2, "A freshwater unicellular organism has no cell wall, and water constantly moves into it. "
        "Which structure keeps it from bursting?",
  ["A contractile vacuole", "A food vacuole", "A lysosome", "A capsule"],
  0,
  "The problem is too much water inside. Something has to actively put it back out.",
  ["Water entering constantly would swell and burst a cell that has no wall to resist it.",
   "A contractile vacuole collects that excess water and pumps it back out of the cell.",
   "A food vacuole stores and digests engulfed particles, and a lysosome digests material inside "
   "the cell — neither removes water.",
   "The contractile vacuole is what keeps it intact."],
  "**A contractile vacuole pumps the excess water out.** A walled cell can resist the pressure "
  "and does not need one; a wall-less freshwater organism does. Both other vacuole jobs here are "
  "about food, not water.",
  "Vacuoles do several different jobs. Read which one the scenario actually needs.")

q(Q, 2, "Two cells are examined. One has a large permanent central vacuole and chloroplasts; the "
        "other has neither, but has centrioles. What are they?",
  ["A plant cell and an animal cell",
   "A plant cell and a prokaryote",
   "An animal cell and a fungal cell",
   "A prokaryote and a eukaryote"],
  0,
  "Every structure named here belongs to eukaryotes, so the split is inside that group.",
  ["Chloroplasts and one large permanent central vacuole are plant cell features.",
   "Centrioles organise cell division in animal cells.",
   "All of these are organelles, so neither cell can be a prokaryote.",
   "That makes them a plant cell and an animal cell."],
  "**A plant cell and an animal cell.** Chloroplasts plus a large permanent central vacuole is a "
  "plant signature; centrioles are the animal one. Neither can be a prokaryote, because "
  "prokaryotes have no membrane-bound organelles to name.",
  "Prokaryote options are easy to eliminate: if the question names an organelle, it is out.")

q(Q, 3, "Which observation gives the strongest support for the endosymbiont theory?",
  ["Mitochondria have their own circular DNA and their own ribosomes",
   "Mitochondria are found in nearly every eukaryotic cell",
   "Mitochondria release energy that the whole cell then uses",
   "Mitochondria are much smaller than the cell that contains them"],
  0,
  "Ask which observation would be strange unless the organelle had once lived independently.",
  ["The theory claims mitochondria descend from a free-living prokaryote that was engulfed.",
   "Being common, being useful and being small are all equally true of organelles that were "
   "never independent, so none of those distinguishes the theory.",
   "Carrying its own circular DNA and its own ribosomes is what a free-living prokaryote has.",
   "That leftover machinery is the strongest evidence."],
  "**Its own circular DNA and ribosomes are the giveaway.** Those are exactly the equipment a "
  "free-living prokaryote needs and an ordinary organelle has no reason to keep. Being common, "
  "useful or small would be true whether or not the theory held, so none of them can test it.",
  "Evidence has to be able to come out the other way. If an observation fits both stories, it "
  "supports neither.")

q(Q, 3, "A toxin blocks the Golgi apparatus completely, leaving every other organelle working. "
        "What is the most direct consequence?",
  ["Proteins are made and folded but not finished or shipped out",
   "The cell can no longer build any proteins at all",
   "The cell immediately loses its ability to make ATP",
   "DNA can no longer be stored or copied"],
  0,
  "Find where the Golgi sits on the export route, and ask what still happens upstream of it.",
  ["Ribosomes build proteins and the rough ER folds them; both are upstream of the Golgi.",
   "So protein production itself carries on unaffected.",
   "The Golgi is where proteins are finished, sorted, labelled and packed into vesicles for "
   "shipping.",
   "Blocking it stops proteins being finished and exported, while they are still being made."],
  "**Production continues; finishing and shipping stop.** The Golgi sits downstream of the "
  "ribosomes and the rough ER, so proteins are still built and folded — they simply pile up "
  "unfinished. ATP and DNA storage are handled elsewhere entirely.",
  "Blocking one stop on a pathway breaks that stop and everything after it, never what came "
  "before.")

q(Q, 3, "Why does compartmentalisation let a eukaryotic cell do things a prokaryote cannot?",
  ["Separate compartments can hold different conditions, so incompatible processes run at once",
   "Compartments make the cell larger, and larger cells always work faster",
   "Compartments remove the need for a cell membrane around the whole cell",
   "Compartments allow the cell to survive without any DNA"],
  0,
  "Think about two reactions that would ruin each other if they happened in the same space.",
  ["An organelle is a membrane-enclosed compartment, so its contents are held apart from the "
   "cytosol.",
   "That lets one compartment keep conditions — enzymes, acidity — that would damage the rest of "
   "the cell.",
   "A lysosome full of digestive enzymes next to intact organelles is exactly that situation.",
   "So compartments let incompatible processes happen in one cell at the same time."],
  "**Separate compartments can maintain separate conditions.** That is what lets a lysosome hold "
  "digestive enzymes without the cell digesting itself, and it is why organelle specialisation is "
  "possible at all. Size is a consequence of that, not the cause.",
  "The membrane is the point of an organelle. Ask what the membrane keeps apart.")

q(Q, 3, "A student says a cell could grow to any size if it simply made more organelles to keep "
        "up. What is wrong with the reasoning?",
  ["Supply crosses the outer membrane, and surface area cannot keep pace with volume",
   "Nothing is wrong — cells grow to any size as long as they have enough organelles",
   "Organelles cannot be duplicated within a single cell",
   "A larger cell would lose its ability to hold its shape"],
  0,
  "The limit is not about what is inside. It is about the boundary everything has to cross.",
  ["Everything entering or leaving a cell has to cross the plasma membrane.",
   "As a cell grows, its volume increases faster than its surface area does.",
   "So a bigger cell has relatively less membrane serving relatively more interior.",
   "Adding organelles does not add membrane surface for supply, so the limit still holds."],
  "**More organelles does not create more outer surface.** Traffic in and out crosses the plasma "
  "membrane, and volume outgrows surface area, so a large cell starves at the boundary no matter "
  "how well equipped its interior is. That is why the egg yolk exception works — it is not "
  "importing nutrients across its surface.",
  "When something is limited by a boundary, adding to the inside never fixes it.")

q(Q, 3, "Mitochondria and chloroplasts both reproduce on their own schedule, independently of "
        "the cell dividing. Why does that fit the endosymbiont theory?",
  ["Free-living cells divide on their own, and that ability would have been inherited",
   "It shows the cell has lost control of its organelles and is damaged",
   "It proves mitochondria and chloroplasts are the same organelle",
   "It explains why both organelles have a single membrane"],
  0,
  "The theory says these organelles descend from something that used to be a whole organism.",
  ["A free-living prokaryote divides when it is ready, not when something else tells it to.",
   "The theory holds that mitochondria and chloroplasts descend from exactly such cells.",
   "Dividing on their own schedule is that independence surviving inside the host.",
   "So it fits as inherited behaviour from a formerly free-living ancestor."],
  "**It is inherited independence.** An engulfed free-living cell would already know how to "
  "divide by itself, and that ability persisting is what the theory predicts. Both organelles in "
  "fact have DOUBLE membranes, which is a separate piece of evidence for the same idea.",
  "Each piece of endosymbiont evidence is a leftover: double membrane, own DNA, own ribosomes, "
  "own division.")

q(Q, 1, "What is turgor pressure, and which structure creates it?",
  ["Pressure from the central vacuole pushing outward against the plant cell wall",
   "Pressure from the cytoskeleton holding an animal cell's shape",
   "Pressure from mitochondria releasing energy inside the cytosol",
   "Pressure from the capsule squeezing a bacterial cell inward"],
  0,
  "It is what makes a plant wilt when it runs out of water.",
  ["The plant central vacuole is large, permanent, and mostly full of water.",
   "A full vacuole presses outward on the cell contents and so against the cell wall.",
   "That outward push against a rigid wall is turgor pressure, and it is what holds the plant "
   "upright.",
   "The central vacuole creates it, pressing on the cell wall."],
  "**The central vacuole pressing outward on the cell wall.** It needs both parts — a full "
  "vacuole to push and a rigid wall to push against — which is why turgor is a plant "
  "phenomenon and why a plant short of water goes limp.",
  "Turgor needs a wall to push against. That is why animal cells never have it.")

_balance(Q)

build('ad-astra', C, Q,
      'unit-bio-u3c',
      'Biology 8 · Unit 3: Cells and Cell Structures',
      'bio',
      "Her teacher's Unit 3 lecture deck on cells: the cell theory and the two scientists behind "
      "its beginnings, why the surface area-to-volume ratio limits how big a cell can get, the "
      "prokaryote/eukaryote split, every organelle in a plant and animal cell with what it does, "
      "the route a secreted protein takes from ribosome to cell membrane, and the endosymbiont "
      "theory with the evidence for it.",
      "Almost everything else in biology sits on top of this vocabulary. Once the organelles are "
      "solid, questions stop being about memory and start being about reasoning — name a cell's "
      "job and you can predict what it is full of, block one organelle and you can predict what "
      "fails.",
      [("Say what the cell theory states, and name what Hooke and Leeuwenhoek each saw first.",
        'source'),
       ("Explain why the surface area-to-volume ratio limits cell size, and work the ratio out "
        "for a cube.", 'source'),
       ("Tell a prokaryote from a eukaryote from a list of structures, and say what "
        "compartmentalisation buys a cell.", 'source'),
       ("Name each organelle's function, and give the plant-only and animal-only ones.", 'source'),
       ("Put the secretory pathway in order and predict what fails when one stop is blocked.",
        'added'),
       ("State the three pieces of evidence for the endosymbiont theory and say why each one "
        "counts.", 'source')],

      "Built from the teacher's own Unit 3 deck (G8_Cells_VA.pdf), which is thorough — this unit "
      "follows it closely rather than adding outside material.\n\n"
      "TWO THINGS TO KNOW. First, the diagrams: seven cards carry a labelled cell diagram "
      "(prokaryote, animal cell, plant cell, nucleus, mitochondrion, chloroplast, and the "
      "endomembrane system). They are hotlinked from Wikimedia Commons and every one is public "
      "domain — mostly the LadyofHats scientific illustrations that Wikipedia's own cell "
      "articles use. They are NOT the teacher's slide images, which are likely textbook figures "
      "and are not ours to republish. Each filename was verified to exist and verified public "
      "domain before it shipped. They need a network connection to load; everything else in the "
      "unit works offline as usual.\n\n"
      "Second, and worth a look: this unit is numbered Unit 3 because both the Drive folder and "
      "the deck's own title slide say Unit 3, but the Enzymes unit already in her app is ALSO "
      "titled Unit 3 — that one came from a photographed packet with no unit number visible, so "
      "its number was inferred and is the one more likely to be wrong (enzymes are proteins, "
      "which would sit with Unit 2 Biomolecules). Nothing breaks either way; both shelve under "
      "Biology 8. Worth confirming with her which unit the enzymes packet actually belongs to, "
      "and it can be retitled in place if it needs to move.\n\n"
      "The questions deliberately do not ask her to name a structure from a diagram. Every "
      "diagram here is fully labelled, so the answer would be printed on the image — the picture "
      "is there to teach on the cards, and the questions test reasoning instead.",

      ("Start with the cards — seven of them carry a real labelled diagram, so this is a deck "
       "worth going through slowly before quizzing.", 25),
      'content/bio-unit-3-cells.json',
      'G8_Cells_VA.pdf (Biology 8 · Unit 3 lecture deck, Drive)',
      'source', offset_hours=3)

# libv rides alongside updatedAt so a later content fix cannot lose the
# approval race (v88). New file, so it starts at 1.
p = '/home/user/ad-astra/content/bio-unit-3-cells.json'
d = json.load(io.open(p, encoding='utf-8'))
d['records']['unit-bio-u3c']['libv'] = 1
io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
print('libv set to 1')
