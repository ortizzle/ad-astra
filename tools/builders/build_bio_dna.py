#!/usr/bin/env python3
"""Biology 8 · Unit 6-1: DNA.

Sources, both Drive, both in her Biology Unit 6 folder:

  * "Unit+6_+DNA+(1).pptx" — the class's Unit 6 lecture deck. Read through
    Drive's own text representation (read_file_content). The file is about
    10.7 MB, over the connector's 10 MB download cap, so the slide PICTURES
    were not seen. Everything below that cites the deck cites its slide TEXT:
    nucleotide parts, antiparallel strands, the A–T / C–G mnemonic, the RNA
    bases (GUAC), covalent backbone and hydrogen-bond rungs (each followed by a
    bare "Why?" whose answer is not in the text), the purine/pyrimidine
    mnemonics, 2 and 3 hydrogen bonds, Chargaff's rule, and a knowledge check.
  * "55+DNA+structure+and+replication+worksheet.pdf" — the "DNA Structure and
    Replication HW" video-question sheet: 15 structure blanks and 14
    replication blanks, plus two label-the-diagram tasks. Clean text layer,
    and rendered with pdftoppm as well so the two diagrams could be seen. The
    copy in Drive is BLANK — nothing of hers on it — so it was read for its
    questions, as it would have been anyway (the v198 rule).

NO OUTRIGHT SOURCE ERRORS were found. Three places are taught a little more
carefully than the sources word them, and parentNote says so:

1. The deck's "DNA and RNA have 3 parts" describes a NUCLEOTIDE, not the whole
   molecule. The cards say "each nucleotide has three parts".
2. The deck's "Purines = pyrimidines = 50%" (and the rest of Chargaff's rule)
   holds only for DOUBLE-stranded DNA. The deck does not say so; a card added
   here does, and one question turns on it.
3. Worksheet item 9 says purine-with-pyrimidine pairing "causes DNA to have the
   shape of a double helix". What the pairing does is keep every rung the same
   width, which is what lets the ladder twist into a smooth helix. The card
   says that.

The deck's two bare "Why?" prompts (why covalent for the backbone, why hydrogen
bonds between the strands) are answered on one card and one question, both
tagged `added`, since the answer is not in any text we have.

Every complementary strand, Chargaff percentage, base count and hydrogen-bond
total in a graded question is computed below and asserted before it is
written. None reuses the deck's own knowledge-check strand (GATTACATACG) or its
30% adenine example.

No images: the worksheet's two diagrams are for labelling on paper, and the
deck's pictures were not seen (and would be textbook art regardless).
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build, REPO

# ------------------------------------------------------------ the chemistry

PAIR = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
HB = {'A': 2, 'T': 2, 'C': 3, 'G': 3}
PURINE_SWAP = {'A': 'G', 'G': 'A', 'C': 'T', 'T': 'C'}   # a purine-for-purine slip

def comp(s):
    """The partner strand, written base for base underneath."""
    return ''.join(PAIR[b] for b in s)

def hbonds(s):
    """Hydrogen bonds holding a stretch together, given ONE of its strands."""
    return sum(HB[b] for b in s)

def chargaff(**given):
    """Fill in all four percentages from one base, for double-stranded DNA."""
    (k, v), = given.items()
    out = {k: v, PAIR[k]: v}
    rest = (100 - 2 * v) / 2
    for b in 'ATCG':
        out.setdefault(b, rest)
    assert sum(out.values()) == 100 and out['A'] == out['T'] and out['C'] == out['G']
    return out

# The deck's own knowledge check, so the method is known to agree with the class.
DECK_STRAND = 'GATTACATACG'
assert comp(DECK_STRAND) == 'CTAATGTATGC'
_d = chargaff(A=30)
assert (_d['T'], _d['A'] + _d['T'], _d['C'] + _d['G'], _d['C'], _d['G']) == (30, 60, 40, 20, 20)
DECK_NUMBERS = {30, 60, 40, 20}

def fresh(*nums):
    for x in nums:
        assert x not in DECK_NUMBERS, 'reuses a number from the deck: %r' % x

def uniq(opts):
    assert len(set(opts)) == 4, opts
    return opts

def pct(x):
    return '%g%%' % x

C, Q = [], []

# ------------------------------------------------------------------ cards

card(C, 'DNA',
     "**Deoxyribonucleic acid: the molecule that carries the codes for making proteins.**\n"
     "• It is a polymer — a long chain of smaller units called nucleotides\n"
     "• Two strands twist round each other into a double helix",
     hint="Deoxy-ribo-nucleic acid: the sugar's name is hiding inside the molecule's name.")

card(C, 'Nucleotide',
     "**The building block of DNA and RNA, with three parts: a phosphate group, a 5-carbon sugar and "
     "a nitrogenous base.**\n"
     "• The sugar is deoxyribose in DNA and ribose in RNA\n"
     "• The base is the part that varies — it is what makes one nucleotide different from the next",
     hint="Phosphate, sugar, base. Only the base changes from one link of the chain to the next.")

card(C, 'DNA vs RNA',
     "**DNA has deoxyribose and thymine and is double-stranded; RNA has ribose and uracil and is "
     "single-stranded.**\n"
     "• DNA bases: A, T, C, G. RNA bases: G, U, A, C — \"GUAC\"\n"
     "• Uracil takes thymine's place, so in RNA it is U that pairs with A",
     hint="GUAC has no T in it. That missing T is the whole difference in the bases.")

card(C, 'The four DNA bases',
     "**Adenine, thymine, cytosine and guanine — written A, T, C and G.**\n"
     "• The order of the bases along a strand is the code\n"
     "• You may always abbreviate them by their first letter",
     hint="Four letters, and every gene is written with only these four.")

card(C, 'Purines',
     "**Adenine and guanine — the bases with two rings.**\n"
     "• \"Two rings of pure silver\": PURines, and Ag (A and G) is silver's symbol\n"
     "• A purine always pairs with a pyrimidine, never with another purine",
     hint="Silver is Ag on the periodic table. A and G, double rings.")

card(C, 'Pyrimidines',
     "**Cytosine, thymine and uracil — the bases with one ring.**\n"
     "• \"CUT the PY\": C, U and T are the PYrimidines\n"
     "• Thymine is in DNA only, uracil in RNA only",
     hint="The longer name, pyrimidine, belongs to the smaller base.")

card(C, 'Base-pairing rules',
     "**A always pairs with T, and C always pairs with G.**\n"
     "• \"Apples in the Tree, Cars in the Garage\"\n"
     "• So one strand's sequence decides the other's completely",
     hint="Apples–Tree, Cars–Garage. Never mix the trees and the garages.")

card(C, 'Hydrogen bonds in each pair',
     "**A–T pairs are held by 2 hydrogen bonds; C–G pairs by 3.**\n"
     "• A stretch rich in C–G is held more tightly than one rich in A–T\n"
     "• Count them: each A or T adds 2, each C or G adds 3",
     hint="C and G both have curves in them, and three bonds. A and T are straight lines, two bonds.")

card(C, 'Complementary',
     "**Molecules that fit and bind together are complementary — like an enzyme and its substrate.**\n"
     "• The two strands of DNA are complementary: every base faces its partner\n"
     "• Knowing one strand gives you the other",
     hint="Complementary means they complete each other, not that they match.")

card(C, 'The double helix',
     "**Two strands twisted round each other like a twisted ladder.**\n"
     "• The rails are the sugar-phosphate backbones; the rungs are base pairs\n"
     "• Every rung is one purine (two rings) plus one pyrimidine (one ring), so every rung is the same "
     "width — that even width is what lets the ladder twist smoothly",
     hint="Two rings plus one ring, every single rung. That is why the ladder never bulges.")

card(C, 'Sugar-phosphate backbone',
     "**The rail of each strand: sugars and phosphates joined to each other by covalent bonds.**\n"
     "• The bases stick out from the backbone toward the other strand\n"
     "• Covalent bonds are strong, so the strand holds its order",
     hint="Sugar, phosphate, sugar, phosphate — the rail of the ladder.")

card(C, 'Why two kinds of bond',
     "**The backbone is covalent so the code never falls apart; the rungs are hydrogen bonds so the two "
     "strands can be unzipped to be copied.**\n"
     "• Strong bonds hold the ORDER of bases along a strand\n"
     "• Weak bonds hold the two strands TOGETHER, and weak is the point: helicase has to pull them apart",
     hint="Strong where it must never break, weak where it has to.",
     frm='added')

card(C, 'Antiparallel strands',
     "**The two strands run in opposite directions: if one runs 5′ → 3′, its partner runs 3′ → 5′.**\n"
     "• 5′ and 3′ (\"five prime\", \"three prime\") name the two ends of a strand\n"
     "• Read side by side, one strand is always upside-down compared with the other",
     hint="Like two lanes of a road: side by side, opposite ways.")

card(C, "Chargaff's rule",
     "**In double-stranded DNA, %A = %T and %G = %C, because A always pairs with T and C with G.**\n"
     "• All four add to 100%\n"
     "• Purines (A + G) make up exactly 50%, and so do pyrimidines (C + T)",
     hint="Partners always match. The other pair shares whatever is left.",
     eq='%A = %T,  %G = %C,  A + T + C + G = 100%')

card(C, 'Solving a Chargaff problem',
     "**Match the given base with its partner, take both from 100%, and split what is left between the "
     "other pair.**\n"
     "• Example: T = 18% → A = 18%, so A + T = 36%\n"
     "• Then C + G = 100 − 36 = 64%, so C = 32% and G = 32%",
     hint="Partner, subtract, halve. Three moves, every time.")

card(C, "Where Chargaff's rule stops",
     "**It only holds for double-stranded DNA, where every base has a partner.**\n"
     "• RNA is single-stranded, so its A and U need not match\n"
     "• So a DNA sample whose A and T differ cannot be ordinary double-stranded DNA — or the "
     "measurement is wrong",
     hint="No partner, no rule.",
     frm='added')

card(C, 'Where and when DNA is copied',
     "**In eukaryotes, in the nucleus, during the S phase of interphase.**\n"
     "• S stands for synthesis — from Unit 4\n"
     "• Each copy becomes one of the two sister chromatids",
     hint="The DNA lives in the nucleus, so that is where it is copied.")

card(C, 'Helicase',
     "**The enzyme that unzips DNA, breaking the hydrogen bonds between base pairs to pull the two "
     "strands apart.**\n"
     "• It starts at an origin of replication, opening a Y-shaped replication fork\n"
     "• Only the hydrogen bonds break; the backbones stay whole",
     hint="Helic-ase: it opens the helix. Enzymes end in -ase.")

card(C, 'Primase and RNA primers',
     "**Primase lays down short RNA primers, which give DNA polymerase a starting point on each "
     "strand.**\n"
     "• The primers are RNA, not DNA\n"
     "• They go on before any new DNA is built",
     hint="Prime a wall before you paint it. Primase primes the strand.")

card(C, 'DNA polymerase',
     "**The enzyme that adds nucleotides one by one to build a new strand complementary to each "
     "template strand — then double-checks its own work.**\n"
     "• It follows the base-pairing rules: an A on the template gets a T, a C gets a G\n"
     "• Its proofreading catches mistakes, reducing errors and mutations",
     hint="Polymer-ase: it makes the polymer, then proofreads it.")

card(C, 'Ligase',
     "**The enzyme that joins fragments of DNA together into one continuous strand.**\n"
     "• One new strand, the lagging strand, is built in short pieces\n"
     "• Ligase seals the gaps between them",
     hint="Liga- means tie, as in ligament. Ligase ties pieces together.")

card(C, 'Why the lagging strand comes in pieces',
     "**DNA polymerase can only build in one direction, and the two templates run opposite ways — so "
     "one new strand is built smoothly and the other in short fragments.**\n"
     "• The smooth one is the leading strand; the pieced one is the lagging strand\n"
     "• That is the job ligase exists for",
     hint="One-way builder, two-way road. One side has to be done in stretches.",
     frm='added')

card(C, 'The four steps of replication',
     "**Helicase unzips; primase adds RNA primers; DNA polymerase builds the new strands; DNA polymerase "
     "proofreads.**\n"
     "• Step 1 happens at the origin of replication\n"
     "• Ligase joins the fragments on the lagging strand",
     hint="Unzip, prime, build, check.")

card(C, 'Semi-conservative replication',
     "**Each new DNA molecule keeps one original strand and gets one new strand.**\n"
     "• Semi- means half: half of each molecule is conserved, kept from the original\n"
     "• So each sister chromatid holds one old strand and one new one",
     hint="Half kept, half new — in every copy.")

# -------------------------------------------------------------- questions

# ---- level 1: recall

q(Q, 1, "Which three parts make up a single nucleotide?",
  ["A phosphate group, a 5-carbon sugar and a nitrogenous base",
   "An amino acid, a 5-carbon sugar and a nitrogenous base",
   "A phosphate group, a fatty acid and a nitrogenous base",
   "A phosphate group, a 5-carbon sugar and a hydrogen bond"], 0,
  "One part makes the backbone with its neighbours, one sugar sits beside it, one part varies.",
  ["A nucleotide is the building block of DNA and RNA.",
   "Its phosphate and sugar join with other nucleotides' to make the backbone.",
   "Its third part is a nitrogenous base: A, T, C or G in DNA.",
   "So: a phosphate group, a 5-carbon sugar and a nitrogenous base."],
  "**A phosphate group, a 5-carbon sugar and a nitrogenous base.** Amino acids build proteins and "
  "fatty acids build lipids — different biomolecules. A hydrogen bond is not part of a nucleotide at "
  "all; it is what holds two bases on opposite strands together.",
  "Phosphate, sugar, base.")

q(Q, 1, "Which pair of features belongs to DNA but not to RNA?",
  ["Deoxyribose sugar and the base thymine",
   "Ribose sugar and the base thymine",
   "Deoxyribose sugar and the base uracil",
   "Ribose sugar and the base uracil"], 0,
  "DNA's sugar is hidden in its name. Which base is missing from GUAC?",
  ["DNA stands for deoxyribonucleic acid, so its sugar is deoxyribose.",
   "RNA's sugar is ribose.",
   "RNA's bases are G, U, A and C — no thymine.",
   "So DNA alone has deoxyribose and thymine."],
  "**Deoxyribose sugar and the base thymine.** RNA has ribose and swaps thymine for uracil, so ribose "
  "with uracil is RNA's pair. The two mixed options each borrow one feature from each molecule.",
  "Deoxyribose with T; ribose with U.")

q(Q, 1, "Which two bases are purines, the ones with two rings?",
  ["Adenine and guanine", "Cytosine and thymine", "Adenine and thymine", "Cytosine and guanine"], 0,
  "Two rings of pure silver. What is silver's chemical symbol?",
  ["Purines are the double-ringed bases.",
   "\"Two rings of pure silver\": silver's symbol is Ag.",
   "A and G — adenine and guanine.",
   "C and T (and U in RNA) are the single-ringed pyrimidines."],
  "**Adenine and guanine.** \"Two rings of pure silver\" — Ag. Cytosine and thymine are pyrimidines. "
  "Adenine with thymine and cytosine with guanine are the base PAIRS, each one purine plus one "
  "pyrimidine.",
  "Ag: A and G, double rings.")

q(Q, 1, "What kind of bond joins a base on one strand of DNA to its partner on the other strand?",
  ["Hydrogen bonds", "Covalent bonds", "Ionic bonds", "Peptide bonds"], 0,
  "The rungs of the ladder have to come apart when DNA is copied.",
  ["The backbone of each strand is held by covalent bonds.",
   "The two strands are held together by their base pairs.",
   "Those base pairs are joined by hydrogen bonds — two for A–T, three for C–G.",
   "Weak hydrogen bonds are what let helicase unzip the strands."],
  "**Hydrogen bonds.** Covalent bonds hold each strand's own backbone together. Peptide bonds join "
  "amino acids in a protein, not bases in DNA.",
  "Rails covalent, rungs hydrogen.")

q(Q, 1, "What does helicase do during DNA replication?",
  ["Unzips the DNA by breaking the hydrogen bonds between base pairs",
   "Adds new nucleotides to build a complementary strand on each side",
   "Joins short fragments of new DNA into one continuous strand",
   "Lays down short RNA primers so that building has a place to start"], 0,
  "Helic-ase: which job has to happen to a helix before anything can be copied?",
  ["Copying starts with the two strands being separated.",
   "Helicase does that, at an origin of replication.",
   "It breaks only the hydrogen bonds between the base pairs.",
   "Building is DNA polymerase's job, primers are primase's, and joining is ligase's."],
  "**Unzips the DNA by breaking the hydrogen bonds between base pairs.** It is the first step of "
  "replication. The other three options are the jobs of DNA polymerase, ligase and primase.",
  "Helicase opens the helix.")

q(Q, 1, "In a eukaryotic cell, where and when is the DNA copied?",
  ["In the nucleus, during the S phase of interphase",
   "In the cytoplasm, during the S phase of interphase",
   "In the nucleus, during prophase of mitosis",
   "At the ribosomes, during the G2 phase of interphase"], 0,
  "Where does a eukaryote keep its DNA? And which phase is named for synthesis?",
  ["A eukaryote keeps its DNA inside the nucleus.",
   "So the DNA is copied there.",
   "Copying happens in S phase — S for synthesis — before the cell divides.",
   "By prophase the DNA has already been copied into sister chromatids."],
  "**In the nucleus, during the S phase of interphase.** Prophase is too late: the chromosomes are "
  "already X-shaped by then. Ribosomes build proteins, not DNA.",
  "Nucleus, S phase.")

q(Q, 1, "On the lagging strand, new DNA is built in short separate pieces. Which enzyme joins those "
        "pieces into one continuous strand?",
  ["Ligase", "Helicase", "Primase", "Lactase"], 0,
  "Liga- means tie, as in ligament.",
  ["The lagging strand is built in fragments.",
   "Something has to seal the gaps between them.",
   "That enzyme is ligase.",
   "Helicase unzips and primase adds primers; neither joins anything."],
  "**Ligase.** It ties the fragments together. Helicase unzips and primase lays down RNA primers. "
  "Lactase is a digestive enzyme that breaks down milk sugar — nothing to do with DNA.",
  "Ligase ties.")

# ---- level 2: apply (every number computed, every one fresh)

S1 = 'TACGGATC'
ans = comp(S1)
rna = ans.replace('T', 'U')
swap = ''.join(PURINE_SWAP[b] for b in S1)
oneoff = ans[:4] + PAIR[ans[4]] + ans[5:]     # one base copied rather than paired
assert ans == 'ATGCCTAG' and rna == 'AUGCCUAG'
assert S1 != DECK_STRAND and len({ans, rna, swap, oneoff}) == 4
q(Q, 2, "One strand of a DNA molecule reads %s. Which sequence is its partner strand, written base for "
        "base beneath it?" % S1,
  uniq([ans, rna, swap, oneoff]), 0,
  "Apples in the Tree, Cars in the Garage. Pair each base in turn.",
  ["Pair each base with its partner: A with T, C with G.",
   "T→A, A→T, C→G, G→C, G→C, A→T, T→A, C→G.",
   "That gives %s." % ans,
   "This is DNA, so the partner uses T, never U."],
  "**%s.** %s uses U, which only RNA has. %s pairs each base with the other base of its own "
  "kind — purine with purine — which DNA never does. %s has one base copied instead of paired."
  % (ans, rna, swap, oneoff),
  "Pair, never copy: every base gets its partner.")

S2 = 'GCTAAGTC'
right2 = comp(S2)
proposed = right2[:4] + 'C' + right2[5:]
bad = [(a, b) for a, b in zip(S2, proposed) if PAIR[a] != b]
assert right2 == 'CGATTCAG' and bad == [('A', 'C')]
pairs_present = {(a, b) for a, b in zip(S2, proposed)}
assert {('G', 'C'), ('T', 'A'), ('C', 'G')} <= pairs_present
q(Q, 2, "A student wrote the partner of the strand %s as %s. Which one pair in that answer breaks the "
        "base-pairing rules?" % (S2, proposed),
  ["The A paired with C", "The G paired with C", "The T paired with A", "The C paired with G"], 0,
  "Line the two strands up and check each pair against A–T and C–G.",
  ["Line them up: %s over %s." % (S2, proposed),
   "Check each pair: G–C, C–G, T–A and A–T are all allowed.",
   "The fifth pair puts A opposite C.",
   "A must pair with T, so that A–C pair is the mistake."],
  "**The A paired with C.** A always pairs with T. G–C, T–A and C–G all follow the rules. "
  "The correct partner is %s." % right2,
  "Check pair by pair, not the whole strand at a glance.")

c = chargaff(T=22); fresh(22, c['G'])
assert c['A'] == 22 and c['G'] == 28
q(Q, 2, "A sample of double-stranded DNA is %d%% thymine. What percentage of it is guanine?" % c['T'],
  uniq([pct(c['G']), pct(22), pct(56), pct(78)]), 0,
  "Thymine's partner first, then what is left for the other pair.",
  ["T pairs with A, so A = 22% too.",
   "A + T = 44%.",
   "That leaves 100 − 44 = 56% for C + G.",
   "C and G are equal, so G = 56 ÷ 2 = 28%."],
  "**28%.** 22% would be adenine, thymine's partner. 56% is C and G together, before halving, and "
  "78% is everything but thymine.",
  "Partner, subtract, halve.")

c = chargaff(G=35); fresh(35, c['A'])
assert c['C'] == 35 and c['A'] == 15
q(Q, 2, "A sample of double-stranded DNA is %d%% guanine. What percentage of it is adenine?" % c['G'],
  uniq([pct(c['A']), pct(35), pct(30), pct(65)]), 0,
  "Guanine's partner matches it. Adenine and thymine share what is left.",
  ["G pairs with C, so C = 35% too.",
   "G + C = 70%.",
   "That leaves 100 − 70 = 30% for A + T.",
   "A and T are equal, so A = 30 ÷ 2 = 15%."],
  "**15%.** 35% is cytosine, guanine's partner. 30% is A and T together before halving, and 65% is "
  "100 minus guanine alone, forgetting that cytosine matches it.",
  "Halve what is left — the leftover belongs to a pair.")

at = 46; cg = 100 - at; cpc = cg / 2; fresh(at, cg)
assert cg == 54 and cpc == 27
q(Q, 2, "In a double-stranded DNA molecule, adenine and thymine together make up %d%% of the bases. "
        "What percentage is cytosine?" % at,
  uniq([pct(cpc), pct(54), pct(23), pct(46)]), 0,
  "All four add to 100%. Which pair has the rest, and how do they split it?",
  ["A + T = 46%.",
   "So C + G = 100 − 46 = 54%.",
   "C and G are equal.",
   "C = 54 ÷ 2 = 27%."],
  "**27%.** 54% is cytosine and guanine together. 23% is half of A + T — the percentage of adenine, "
  "not cytosine.",
  "Whatever A + T is, C + G is the rest.")

bp = 200; bases = 2 * bp; nA = 60; nT = nA; nG = (bases - nA - nT) // 2
assert bases == 400 and nG == 140
q(Q, 2, "A stretch of double-stranded DNA holds %d bases in all, and %d of them are adenine. How many "
        "are guanine?" % (bases, nA),
  uniq([str(nG), '60', '280', '170']), 0,
  "Chargaff's rule works with counts as well as percentages.",
  ["Adenine pairs with thymine, so there are %d thymine too." % nT,
   "A + T = %d bases." % (nA + nT),
   "That leaves %d − %d = %d bases for C + G." % (bases, nA + nT, bases - nA - nT),
   "C and G are equal, so G = %d ÷ 2 = %d." % (bases - nA - nT, nG)],
  "**%d.** 280 is cytosine and guanine together. 170 forgets thymine: it splits what is left after "
  "only the adenine is taken away. 60 is thymine, adenine's partner." % nG,
  "Counts or percentages, the rule is the same.")
assert (bases - nA) // 2 == 170

S3 = 'GCATGCCG'
hb = hbonds(S3)
assert hb == 2 * 2 + 3 * 6 == 22 and hbonds(comp(S3)) == hb
q(Q, 2, "One strand of a short stretch of DNA reads %s. How many hydrogen bonds hold this stretch to "
        "its partner strand?" % S3,
  uniq([str(hb), str(len(S3)), str(2 * len(S3)), str(3 * len(S3))]), 0,
  "Each A or T pair has 2 hydrogen bonds; each C or G pair has 3.",
  ["%s has %d C or G bases and %d A or T bases." % (S3, sum(b in 'CG' for b in S3), sum(b in 'AT' for b in S3)),
   "Each C–G pair has 3 hydrogen bonds: 6 × 3 = 18.",
   "Each A–T pair has 2: 2 × 2 = 4.",
   "18 + 4 = %d." % hb],
  "**%d.** 8 counts the pairs, not the bonds. 16 and 24 treat every pair as two or as three bonds; "
  "the real total depends on the mix." % hb,
  "C–G: 3. A–T: 2. Count each pair.")

q(Q, 2, "One strand of a DNA molecule runs 5′ → 3′ from left to right. How does its partner strand "
        "run from left to right?",
  ["3′ → 5′", "5′ → 3′", "It has no 5′ or 3′ end", "Either way, at random"], 0,
  "The two strands are antiparallel.",
  ["DNA's two strands are antiparallel — they run in opposite directions.",
   "The first strand runs 5′ → 3′ left to right.",
   "So its partner must run the opposite way.",
   "Left to right, the partner runs 3′ → 5′."],
  "**3′ → 5′.** Antiparallel means side by side but opposite ways, like two lanes of a road. Every "
  "strand has a 5′ end and a 3′ end, and the direction is never random.",
  "Anti-parallel: opposite ways.")

# ---- level 3: analyze

q(Q, 3, "Put the four steps of DNA replication in order, from first to last.",
  ["Helicase unzips the two strands at an origin of replication",
   "Primase adds short RNA primers to both strands",
   "DNA polymerase builds a new strand on each template",
   "DNA polymerase double-checks its work for errors"], 0,
  "Open it, give the builder a start, build, then check.",
  ["Nothing can be copied until the strands are apart: helicase first.",
   "DNA polymerase needs a starting point, so primase adds RNA primers next.",
   "Then DNA polymerase builds the new complementary strands.",
   "Last, DNA polymerase proofreads to reduce errors."],
  "**Unzip, prime, build, check.** Each step needs the one before it: primers need an open strand, "
  "building needs a primer, and there is nothing to proofread until a strand exists.",
  "Unzip, prime, build, check.",
  kind='order')

strands = {'GCCGATGC': None, 'GACTAGCT': None, 'ATCAATGA': None, 'TATAATTA': None}
for s in strands: strands[s] = hbonds(s)
best = max(strands, key=strands.get)
assert sorted(strands.values()) == [16, 18, 20, 22] and best == 'GCCGATGC'
assert all(len(s) == 8 for s in strands)
q(Q, 3, "Each sequence below is one strand of an 8-base-pair stretch of DNA. Which stretch takes the "
        "most energy to unzip?",
  list(strands), 0,
  "Unzipping breaks hydrogen bonds. Which stretch has the most?",
  ["Unzipping means breaking the hydrogen bonds between the pairs.",
   "Each C or G pair has 3 bonds; each A or T pair has 2.",
   "Totals: %s." % ', '.join('%s = %d' % (s, n) for s, n in strands.items()),
   "%s has the most, with six C–G pairs." % best],
  "**%s.** It has the most C–G pairs, so the most hydrogen bonds to break: %d against 20, 18 and 16. "
  "Every stretch is the same length, so only the mix of pairs makes the difference." % (best, strands[best]),
  "More C–G, more bonds, harder to pull apart.")

q(Q, 3, "Why are the two strands of DNA held together by hydrogen bonds instead of the strong "
        "covalent bonds that hold each backbone together?",
  ["Weak bonds let the strands be unzipped and copied while each strand stays whole",
   "Hydrogen bonds are stronger than covalent bonds, so the helix holds its shape",
   "Covalent bonds can only form between sugars and phosphates, not between bases",
   "Hydrogen bonds stop the two strands ever coming apart, which protects the code"], 0,
  "Think about what has to happen to DNA every time a cell divides.",
  ["Before a cell divides, its DNA must be copied.",
   "Copying needs the two strands separated, so each can act as a template.",
   "Weak hydrogen bonds can be broken by helicase without damaging anything else.",
   "The strong covalent backbone keeps the order of bases on each strand intact meanwhile."],
  "**Weak bonds let the strands be unzipped and copied while each strand stays whole.** Hydrogen "
  "bonds are weaker than covalent ones, not stronger, and the strands do come apart — they must, every "
  "time the DNA is copied.",
  "Strong where it must never break, weak where it has to.",
  frm='added')

data = {'A': 32, 'T': 18, 'G': 26, 'C': 24}
assert sum(data.values()) == 100 and data['A'] != data['T'] and data['G'] != data['C']
fresh(*data.values())
q(Q, 3, "A lab reports that a sample with thymine in it is %d%% adenine, %d%% thymine, %d%% guanine and "
        "%d%% cytosine. What is the best conclusion?" % (data['A'], data['T'], data['G'], data['C']),
  ["It cannot be ordinary double-stranded DNA, because A and T do not match",
   "It must be RNA, because its four percentages add up to exactly 100%",
   "It is double-stranded DNA that simply has more A–T pairs than C–G pairs",
   "It is normal double-stranded DNA, because purines add up to 58%"], 0,
  "In double-stranded DNA, what must be true of A and T?",
  ["In double-stranded DNA every A pairs with a T, so %A must equal %T.",
   "Here A is 32% but T is only 18%.",
   "G (26%) and C (24%) do not match either.",
   "So this cannot be ordinary double-stranded DNA — it may be single-stranded, or the measurement is off."],
  "**It cannot be ordinary double-stranded DNA, because A and T do not match.** It contains thymine, "
  "so it is not RNA, and adding to 100% proves nothing — any sample does. Purines should be exactly "
  "50% in double-stranded DNA; 32 + 26 = 58% is a second sign something is off.",
  "Partners must match. If they do not, there is no partner.")
assert data['A'] + data['G'] == 58

q(Q, 3, "Adenine and guanine never pair with each other in DNA. What would go wrong if they did?",
  ["Two double-ringed bases would make an extra-wide rung and bulge the ladder",
   "Adenine and guanine would form too many hydrogen bonds to ever unzip",
   "Two purines would make the two strands run in the same direction",
   "The two bases would turn into uracil, which only RNA can use"], 0,
  "How many rings does each purine have? What does every normal rung contain?",
  ["Adenine and guanine are purines, each with two rings.",
   "Every normal rung is one purine plus one pyrimidine: three rings across.",
   "An A–G rung would be four rings across, wider than every other rung.",
   "The ladder would bulge there instead of keeping the even width that lets it twist smoothly."],
  "**Two double-ringed bases would make an extra-wide rung and bulge the ladder.** Purine-with-"
  "pyrimidine is what keeps every rung the same width. The pairing has nothing to do with the strands' "
  "direction, and bases do not turn into one another.",
  "Two rings plus one ring, every rung.")

rounds = 2; molecules = 2 ** rounds; with_old = 2; old_strands = 2; all_strands = 2 * molecules
assert (molecules, with_old, all_strands) == (4, 2, 8)
q(Q, 3, "A single DNA molecule is copied, and then both copies are copied again. Of the DNA molecules "
        "that result, how many still contain a strand from the very first molecule?",
  uniq(['%d of the %d' % (with_old, molecules), '%d of the %d' % (molecules, molecules),
        '1 of the %d' % molecules, '0 of the %d' % molecules]), 0,
  "Replication is semi-conservative. Does an original strand ever get split or thrown away?",
  ["The first molecule has 2 original strands.",
   "Copying is semi-conservative: each new molecule keeps one old strand and gets one new one.",
   "After the first copying there are 2 molecules, each holding one original strand.",
   "After the second there are 4 molecules — but still only 2 original strands, so only 2 molecules contain one."],
  "**2 of the 4.** The two original strands are never broken up or replaced; each one simply ends up "
  "in a different molecule. All 4 would need the old strands to be shared out further, which "
  "semi-conservative copying never does.",
  "Two original strands can only ever be in two molecules.")

q(Q, 3, "Suppose DNA polymerase built new strands as usual but skipped its final double-check. What "
        "would most likely increase?",
  ["Mistakes in the copied DNA — mutations",
   "The speed at which helicase unzips DNA",
   "The number of RNA primers on each strand",
   "The number of hydrogen bonds in each pair"], 0,
  "What is the fourth step of replication for?",
  ["DNA polymerase's last job is to check its own work.",
   "That proofreading catches wrongly paired bases.",
   "Without it, more wrong bases would stay in the new strand.",
   "A lasting change in the DNA's sequence is a mutation."],
  "**Mistakes in the copied DNA — mutations.** The double-check exists to reduce errors. Skipping it "
  "changes nothing about helicase or primase, and each pair's hydrogen bonds are set by which bases "
  "it holds.",
  "Build, then check — skip the check and errors stay.")

# Fresh numbers only: none of the deck's own knowledge check in a graded stem.
for x in Q:
    assert '%%' not in json.dumps(x), ('unformatted %%', x['id'])
    assert DECK_STRAND not in x['q'] and comp(DECK_STRAND) not in x['q'], x['id']
    assert '30%' not in x['q'], x['id']

NOTE = (
    "Built from her Biology Unit 6 folder: the class's DNA lecture deck (Unit 6_ DNA (1).pptx) and "
    "the DNA Structure and Replication homework (the video-question sheet, 55 DNA structure and "
    "replication worksheet.pdf). The deck was read through Drive's text version; at about 10.7 MB it "
    "was too large to download here, so its slide pictures were not seen — if a slide carries a fact "
    "only in a picture, it is not in this unit. The homework was read in full, and the copy in Drive "
    "is blank, so it was used for what it asks.\n\n"
    "No outright errors turned up in either source. Three places are taught a little more carefully "
    "than they are worded, in case her class marks them differently. FIRST, the deck says 'DNA and RNA "
    "have 3 parts'; it is each NUCLEOTIDE that has the three parts, and the cards say so. SECOND, the "
    "deck's Chargaff slide (A = T, G = C, purines = pyrimidines = 50%) never says it applies only to "
    "double-stranded DNA; a card adds that, and one question turns on it. THIRD, the homework says "
    "purine-with-pyrimidine pairing 'causes DNA to have the shape of a double helix'; strictly, the "
    "pairing keeps every rung the same width, which is what lets the ladder twist smoothly. The test "
    "answer is still 'double helix'.\n\n"
    "Some cards are our additions, tagged as study suggestions: why the backbone is covalent and the "
    "rungs are hydrogen bonds (the deck asks 'Why?' twice and the answer is not in its text), where "
    "Chargaff's rule stops, and why the lagging strand is built in pieces (the homework names ligase "
    "and the lagging strand but not the reason).\n\n"
    "Every complementary strand, Chargaff percentage, base count and hydrogen-bond total uses fresh "
    "numbers, computed and checked in the builder; none reuses the deck's GATTACATACG strand or its "
    "30% adenine example. The two label-the-diagram tasks stay on paper. No pictures, deliberately.")

build('ad-astra', C, Q, 'unit-bio-u6',
      'Biology 8 · Unit 6-1: DNA', 'bio',

      "Your class's Unit 6 deck on DNA and the DNA structure and replication homework: the three parts "
      "of a nucleotide, DNA vs RNA, purines and pyrimidines, the base-pairing rules and their hydrogen "
      "bonds, the sugar-phosphate backbone, antiparallel strands, Chargaff's rule, and the four steps "
      "of replication with helicase, primase, DNA polymerase and ligase.",

      "DNA is where the rest of genetics starts: how a cell copies its instructions before it divides, "
      "why a copy is almost always perfect, and how one strand's sequence decides its partner's. "
      "Unit 4's S phase and Unit 5's sister chromatids both depend on it.",

      [("Name the three parts of a nucleotide and tell DNA from RNA.", 'source'),
       ("Sort the bases into purines and pyrimidines, and pair them with the right number of hydrogen "
        "bonds.", 'source'),
       ("Write the complementary strand of any DNA sequence.", 'source'),
       ("Use Chargaff's rule to find every base's percentage from one.", 'source'),
       ("Put the four steps of replication in order and name the enzyme behind each.", 'source'),
       ("Explain why the strands are held by hydrogen bonds and why replication is "
        "semi-conservative.", 'added')],

      NOTE,

      ("Start with the base-pairing and Chargaff cards — half the questions lean on them. Say each "
       "answer out loud before you flip.", 25),
      'content/bio-unit-6-dna.json',
      'Unit 6_ DNA (1).pptx and DNA Structure and Replication HW (Biology 8 · Unit 6, Drive)',
      'source', offset_hours=3, libv_=1)

# build() stamps quarter 1; this unit is taught in quarter 2.
path = os.path.join(REPO, 'content/bio-unit-6-dna.json')
d = json.load(io.open(path, encoding='utf-8'))
d['records']['unit-bio-u6']['quarter'] = 2
io.open(path, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
