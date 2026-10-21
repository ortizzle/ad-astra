#!/usr/bin/env python3
"""Biology 8 · Unit 5-1: Meiosis.

Sources, all Drive, all in her new Biology "Unit 5: Meiosis" folder:

  * "MEIOSIS+(1).pptx" — the teacher's own Unit 5 lecture deck. Read through
    Drive's own text representation (read_file_content). The file itself
    (~6.8 MB) could not be pulled down here: the download crashed the Drive
    connector on a message-size limit, so the slide PICTURES were not seen.
    Everything below that cites the deck cites its slide TEXT.
  * "meiosis+note+outlines.pdf" — the class's three-page guided-notes outline.
    Clean text layer; rendered with pypdfium2 as well, because page 1 carries
    the crossing-over and independent-assortment figures and page 3 has no
    text at all. Page 3 rendered BLANK, so nothing was missed there.
  * "Meiosis+directed+reading+questions.pdf" — a reading-response sheet
    (title, year, author, main idea, variables, control, five unfamiliar
    words) for a science ARTICLE that is not in the folder. It says nothing
    about meiosis itself, so it shapes nothing here; parentNote says so.

TWO PLACES THE SOURCES DISAGREE, both taught the correct way and flagged:

1. WHERE MEIOSIS STARTS. The note outline defines meiosis as making gametes
   "from diploid somatic cells of your body" — while the same page defines a
   somatic cell as one NOT used for sexual reproduction, produced by mitosis.
   The deck names the real starting cell: a germline cell (oogonium or
   spermatogonium). The unit teaches germline cells.

2. WHEN THE CELL TURNS HAPLOID. One deck slide reads "The second ends in
   haploid cells as chromatids are separated", which reads as though the cell
   only becomes haploid at the end of meiosis II. The note outline says
   telophase I ends with "two 1N cells (homologs were separated, chromosomes
   still in X-shape)", and the deck's own knowledge check agrees (30 in, 15
   chromosomes after meiosis I). The deck's practice question 11 asks exactly
   this, so the unit teaches the notes' version and one question targets it,
   with the slide's reading offered as the real wrong option.

Every chromosome and chromatid count is computed by stage() below and
asserted before it is written into a question, with numbers that are not the
deck's own (30/60/15, 46/23, 2^23, the gummy lab's 2N = 4).

No images: the outline's figures and the deck's pictures are textbook art,
not ours to republish from a public repo (the v176 / v197 call).
"""
import io, json, sys
sys.path.insert(0, '/home/user/ad-astra/tools/builders')
from unit_common import card, q, build

# ------------------------------------------------------------ the arithmetic

def stage(two_n):
    """Chromosomes and chromatids PER CELL at each point, for a diploid number 2N.
    A chromosome is counted by its centromere; a chromatid is one strand."""
    assert two_n % 2 == 0, 'a diploid number is always even'
    n = two_n // 2
    return {
        'g1':        (two_n, two_n),        # single strands, before S
        'after_s':   (two_n, 2 * two_n),    # every chromosome an X
        'tetrads':   n,                     # one tetrad per homologous pair
        'tetrad_chromatids': 4 * n,         # four chromatids per tetrad
        'after_m1':  (n, 2 * n),            # homologs split, chromatids still joined
        'anaphase2': (2 * n, 2 * n),        # each chromatid now a chromosome, briefly
        'after_m2':  (n, n),                # four cells, single strands
        'gamete':    n,
        'zygote':    2 * n,                 # N + N
        'mitosis_daughter': two_n,
        'assortment': 2 ** n,
    }

# The deck's own worked example, checked so the arithmetic is known to agree
# with the class before any fresh number is used.
_deck = stage(30)
assert _deck['after_s'] == (30, 60)
assert _deck['after_m1'] == (15, 30) and _deck['after_m2'] == (15, 15)
assert stage(46)['assortment'] == 2 ** 23 == 8388608
DECK_NUMBERS = {30, 60, 15, 46, 23}

def fresh(*nums):
    for x in nums:
        assert x not in DECK_NUMBERS, 'reuses a number from the deck: %r' % x

def uniq(opts):
    assert len(set(opts)) == 4, opts
    return opts

def pair(c, t):
    return '%d chromosomes, %d chromatids' % (c, t)

C, Q = [], []

# ------------------------------------------------------------------ cards

card(C, 'Meiosis',
     "**The cell division that makes haploid gametes for sexual reproduction, starting from a diploid "
     "germline cell.**\n"
     "• One diploid (2N) cell becomes four haploid (1N) cells\n"
     "• One interphase, then two divisions: meiosis I and meiosis II\n"
     "• It happens only in germline cells — the line of cells set aside to become eggs and sperm",
     hint="Mitosis copies. Meiosis halves, and it takes two divisions to do it.")

card(C, 'Asexual vs sexual reproduction',
     "**Asexual: one parent and identical offspring. Sexual: two parents each give a gamete, so every "
     "offspring is a new mix.**\n"
     "• Asexual is fast and needs no partner, but every offspring shares the parent's weaknesses\n"
     "• Sexual is slower and needs two parents, but it produces variety — the whole point of meiosis",
     hint="Speed and certainty against variety. Each way of reproducing pays for what it gets.",
     frm='added')

card(C, 'Somatic cells vs germline cells',
     "**Somatic cells are your ordinary body cells, made by mitosis; germline cells are the separate "
     "line set aside to make eggs and sperm.**\n"
     "• Somatic cells are diploid and do the body's work — most of your cells are somatic\n"
     "• Germline cells (oogonia in females, spermatogonia in males) form in the womb, and are also "
     "called primordial germ cells\n"
     "• Meiosis starts from a germline cell, never from an ordinary somatic one",
     hint="Body line and germ line. Only the germ line ever goes through meiosis.")

card(C, 'Diploid (2N)',
     "**Having two of each type of chromosome — one set from each parent.**\n"
     "• The human diploid number is 46\n"
     "• Written 2N, because it is twice the haploid number; it varies from species to species\n"
     "• Somatic cells are diploid",
     hint="Di- means two. Two of each, one from each parent.")

card(C, 'Haploid (N)',
     "**Having one of each type of chromosome.**\n"
     "• The human haploid number is 23\n"
     "• Written N; gametes are haploid\n"
     "• Haploid means one SET, not one chromosome — a human gamete still holds 23",
     hint="Half the diploid number, but still a complete set: one of every type.")

card(C, 'Gametes and the zygote',
     "**A gamete is a sex cell — an egg (ovum) or a sperm; a zygote is the diploid cell formed when two "
     "gametes fuse.**\n"
     "• N from one parent + N from the other = 2N\n"
     "• The zygote then divides by mitosis, building a body of somatic cells",
     hint="Two halves make a whole. After that, it is mitosis all the way.")

card(C, 'Autosomes and sex chromosomes',
     "**Autosomes are the chromosomes that do not decide reproductive sex; sex chromosomes are the ones "
     "that do.**\n"
     "• Humans have 22 pairs of autosomes and 1 pair of sex chromosomes — 23 pairs, 46 in all\n"
     "• XX for females, XY for males",
     hint="22 + 1 = 23 pairs. The last pair is the one with a letter name.")

card(C, 'Homologous chromosomes',
     "**A matching pair of chromosomes, one inherited from each parent, carrying the same genes in the "
     "same places — but not necessarily the same versions of them.**\n"
     "• Same genes, possibly different alleles\n"
     "• Diploid means having these pairs; haploid means having one from each pair",
     hint="Matching, not identical. Same list of genes, two different authors.")

card(C, 'Alleles',
     "**Different versions of the same gene.**\n"
     "• A pair of homologous chromosomes can carry two different alleles of one gene\n"
     "• Mixing alleles from two parents is why a child is not a copy of either",
     hint="Same gene, different edition.")

card(C, 'Homologous pair vs sister chromatids',
     "**Sister chromatids are identical copies joined at a centromere; a homologous pair is two "
     "different chromosomes, one from each parent.**\n"
     "• Sister chromatids are made in S phase by copying — they match exactly\n"
     "• Homologous chromosomes were never copies of each other; they only carry the same genes\n"
     "• Meiosis I separates the pairs; meiosis II separates the sisters",
     hint="Sisters are photocopies. Homologs are two different drafts of the same essay.")

card(C, 'Interphase before meiosis',
     "**G1, S and G2 — exactly the same as in the mitotic cell cycle, and the only time the DNA is "
     "copied.**\n"
     "• G1: the cytoplasm doubles. S: the chromatids double (I → X). G2: double check\n"
     "• There is NO interphase between meiosis I and meiosis II, so the DNA is never copied a second time",
     hint="One copy, two divisions. That mismatch is exactly how the count ends up halved.")

card(C, 'Two divisions, two jobs',
     "**Meiosis I separates homologous pairs; meiosis II separates sister chromatids.**\n"
     "• Meiosis I is the one that halves the chromosome number\n"
     "• Meiosis II works like mitosis — it splits X-shaped chromosomes into single strands",
     hint="First split the pairs, then split the copies.")

card(C, 'Tetrad',
     "**Two homologous chromosomes paired up, each made of two sister chromatids — four chromatids "
     "in all.**\n"
     "• Forms in prophase I and lines up in metaphase I\n"
     "• One tetrad per homologous pair, so a cell with diploid number 2N forms N tetrads",
     hint="Tetra- means four. Count the strands, not the chromosomes.")

card(C, 'Prophase I',
     "**Homologous chromosomes pair up into tetrads, and crossing over happens.**\n"
     "• This pairing never happens in mitosis\n"
     "• It is the only phase where crossing over occurs",
     hint="Pair up and swap. Everything special about meiosis starts here.")

card(C, 'Crossing over',
     "**The homologous chromosomes in a tetrad swap matching pieces, making chromatids with new "
     "combinations of alleles.**\n"
     "• Happens in prophase I, between the two homologs of a tetrad\n"
     "• The chromatids that come out are called recombinant — part mother's, part father's\n"
     "• Its purpose is variety: no gamete carries a chromosome exactly as a parent had it",
     hint="A swap between the pair, never between the sisters — swapping identical copies would change nothing.")

card(C, 'Metaphase I and independent assortment',
     "**The tetrads line up across the middle in pairs, and which side each parent's chromosome lands "
     "on is random — independently for every pair.**\n"
     "• So each new cell gets a random mix of the mother's and the father's chromosomes\n"
     "• That gives 2^N possible combinations; in humans, 2^23 = 8,388,608",
     hint="Every pair flips its own coin. N coins give 2^N outcomes.",
     eq='combinations = 2^N')

card(C, 'Anaphase I and telophase I',
     "**The homologous pairs are pulled apart while each chromosome's chromatids stay joined, leaving "
     "two haploid cells whose chromosomes are still X-shaped.**\n"
     "• The chromosome number halves here, not later\n"
     "• Cytokinesis then gives two 1N cells",
     hint="Anaphase I pulls pairs, not sisters. The X's arrive intact.")

card(C, 'When the cell becomes haploid',
     "**At the end of meiosis I — once the homologous pairs are split, each cell holds just one of each "
     "chromosome.**\n"
     "• Its chromosomes are still X-shaped, so it still has twice as many chromatids as chromosomes\n"
     "• Meiosis II separates those chromatids but leaves each new cell with the same N chromosomes",
     hint="Haploid counts SETS. One of each type is haploid, X-shaped or not.")

card(C, 'Meiosis II',
     "**Prophase II, metaphase II, anaphase II and telophase II — the sister chromatids are separated, "
     "ending with four haploid cells.**\n"
     "• No tetrads and no crossing over this time\n"
     "• Metaphase II lines the chromosomes up single file, not in pairs",
     hint="Mitosis, run on a haploid cell.")

card(C, 'Anaphase II and the count',
     "**As the sister chromatids separate, each becomes a chromosome of its own, so the count in that "
     "cell briefly doubles — then telophase II splits it between two cells.**\n"
     "• The same thing happens in anaphase of mitosis\n"
     "• Each of the four final cells ends with N single-strand chromosomes",
     hint="Count centromeres. Breaking each X makes two.",
     frm='added')

card(C, 'Counting through meiosis',
     "**2N single strands → 2N X-shapes after S → N X-shapes per cell after meiosis I → N single "
     "strands per cell after meiosis II.**\n"
     "• Chromatids go 2N → 4N → 2N per cell → N per cell\n"
     "• Meiosis I halves the chromosomes; meiosis II halves the chromatids",
     hint="Each division halves exactly one of the two counts.")

card(C, 'Five ways meiosis differs from mitosis',
     "**Meiosis makes four genetically different haploid cells in two divisions; mitosis makes two "
     "identical diploid cells in one.**\n"
     "• Mitosis: 1 (2N) → 2 (2N), identical. Meiosis: 1 (2N) → 4 (1N), all different\n"
     "• Homologous chromosomes pair up only in meiosis\n"
     "• Mitosis makes somatic cells; meiosis makes only sex cells",
     hint="Four, not two. Half, not the same. Different, not identical.")

card(C, 'What meiosis and mitosis share',
     "**Both start with the same interphase, both use a spindle to line chromosomes up and pull them "
     "apart, and both end with cytokinesis.**\n"
     "• The phase names — prophase, metaphase, anaphase, telophase — appear in both\n"
     "• Meiosis II follows the same steps as mitosis",
     hint="Same machinery, different jobs.",
     frm='added')

card(C, 'Eggs, sperm and polar bodies',
     "**Eggs and sperm both come from germline cells, but egg-making divides unequally, producing one "
     "large egg and small polar bodies.**\n"
     "• An oocyte, the egg's precursor, pauses in prophase I and is released at ovulation\n"
     "• The egg then waits at metaphase II until fertilization",
     hint="Unequal on purpose: one cell gets almost all the cytoplasm.")

card(C, 'Why body cells hold an even number',
     "**Because body cells hold their chromosomes in matched pairs, one of each pair from each parent — "
     "so the count is always 2 × N.**\n"
     "• Every type comes twice, so the total is always even\n"
     "• Copying DNA in S phase is not the reason: it doubles chromatids, not chromosomes",
     hint="Pairs, one from each parent. Count by twos.",
     frm='added')

card(C, 'Why gametes have to be haploid',
     "**So that egg plus sperm restores the diploid number instead of doubling it every generation.**\n"
     "• N + N = 2N, the same count the parents' body cells had\n"
     "• Two diploid gametes would give a 4N zygote, then 8N in the next generation",
     hint="Halve it now, so fertilization can put it back.",
     frm='added')

# -------------------------------------------------------------- questions

# ---- level 1: recall

q(Q, 1, "One diploid germline cell completes meiosis. What does it end up as?",
  ["Four haploid cells, each genetically different",
   "Two diploid cells, each genetically identical",
   "Four diploid cells, each genetically different",
   "Two haploid cells, each genetically identical"], 0,
  "Two divisions, and the chromosome number halves. Then ask whether the cells match.",
  ["Meiosis has two divisions, so one cell becomes two and then four.",
   "Meiosis I splits the homologous pairs, so each cell keeps one of each chromosome — haploid.",
   "Crossing over and independent assortment mix the alleles, so no two cells match.",
   "So it ends as four haploid cells, each genetically different."],
  "**Four haploid cells, each genetically different.** Two identical diploid cells is mitosis — the "
  "commonest mix-up between the two. Meiosis exists to make gametes, which need half the chromosomes "
  "and need to vary.",
  "Four, half, different. Mitosis is two, same, identical.")

q(Q, 1, "During which phase does crossing over happen?",
  ["Prophase I", "Metaphase I", "Prophase II", "Anaphase I"], 0,
  "Crossing over needs the homologous chromosomes pressed together in a tetrad.",
  ["Crossing over is a swap between the two chromosomes of a homologous pair.",
   "The pairs only come together as tetrads at the start of meiosis I.",
   "That pairing happens in prophase I.",
   "By meiosis II there are no tetrads left, so no crossing over."],
  "**Prophase I.** The homologous chromosomes pair up into tetrads there, and that is the only time "
  "they are close enough to swap pieces. Metaphase I is when the tetrads line up — and where "
  "independent assortment, the other source of variety, happens.",
  "Pair up, then swap — both in prophase I.")

q(Q, 1, "What is a tetrad?",
  ["Two homologous chromosomes paired up, each made of two sister chromatids",
   "Four separate chromosomes lined up single file across the middle",
   "The four daughter cells that a finished meiosis produces",
   "One chromosome whose DNA has been copied twice in S phase"], 0,
  "Tetra- means four. Four of what, exactly?",
  ["A tetrad forms when homologous chromosomes pair up in prophase I.",
   "Each of the two chromosomes is X-shaped — two sister chromatids.",
   "Two chromosomes × two chromatids each = four chromatids.",
   "So a tetrad is a homologous pair, four chromatids in all."],
  "**Two homologous chromosomes paired up, each made of two sister chromatids.** The four are "
  "chromatids, not chromosomes and not cells. DNA is copied only once, in one S phase, so nothing is "
  "ever copied twice.",
  "Count strands: two X's side by side.")

q(Q, 1, "A pair of homologous chromosomes both carry the gene for flower colour, but one carries a "
        "purple version and the other a white version. What are those two versions called?",
  ["Alleles", "Autosomes", "Sister chromatids", "Tetrads"], 0,
  "Same gene, two different editions of it.",
  ["Both chromosomes carry the same gene, for flower colour.",
   "The two carry different versions of that gene.",
   "Different versions of the same gene are alleles.",
   "Sister chromatids could not differ like this — they are identical copies."],
  "**Alleles.** Homologous chromosomes carry the same genes but can carry different alleles of them. "
  "Sister chromatids are photocopies of one chromosome, so they would carry the same allele.",
  "Same gene, different edition.")

q(Q, 1, "A chromosome inherited from your mother and the matching chromosome inherited from your "
        "father carry the same genes in the same places. What are the two of them called together?",
  ["Homologous chromosomes", "Sister chromatids", "Sex chromosomes", "Recombinant chromatids"], 0,
  "They came from two different people, so they cannot be copies of each other.",
  ["The two came from two different parents.",
   "They carry the same genes, possibly as different alleles.",
   "A matching pair like that is a homologous pair.",
   "Sister chromatids are identical copies made by one cell in S phase — a different thing."],
  "**Homologous chromosomes.** Sister chromatids are made by copying one chromosome, so they are "
  "identical; homologous chromosomes come from two parents and only share their list of genes. Sex "
  "chromosomes are just one particular pair.",
  "Homologs: one from each parent. Sisters: one copied.")

q(Q, 1, "Which division of meiosis separates the sister chromatids?",
  ["Meiosis II", "Meiosis I", "The S phase of interphase", "Cytokinesis after telophase I"], 0,
  "One division splits the pairs and the other splits the copies.",
  ["Meiosis I separates the homologous pairs.",
   "Each chromosome reaches the end of meiosis I still X-shaped.",
   "Meiosis II then pulls each X apart into its two chromatids.",
   "So the sister chromatids separate in meiosis II."],
  "**Meiosis II.** Meiosis I splits the homologous pairs and leaves the chromatids joined; meiosis II "
  "splits the chromatids, which is why it looks so much like mitosis. S phase does the opposite — it "
  "makes the sister chromatids.",
  "First the pairs, then the sisters.")

q(Q, 1, "How many rounds of DNA copying and how many cell divisions does meiosis include?",
  ["One round of copying, two divisions",
   "Two rounds of copying, two divisions",
   "One round of copying, one division",
   "Two rounds of copying, one division"], 0,
  "Is there an interphase between meiosis I and meiosis II?",
  ["The DNA is copied once, in the S phase of the interphase before meiosis starts.",
   "Meiosis I is the first division.",
   "There is no interphase before meiosis II, so nothing is copied again.",
   "So: one round of copying, two divisions."],
  "**One round of copying, two divisions.** That mismatch is exactly how meiosis halves the "
  "chromosome number: copy once, divide twice. Mitosis copies once and divides once, so the number "
  "stays the same.",
  "Copy once, divide twice — that is what makes half.")

# ---- level 2: apply (every number from stage(), every one fresh)

s = stage(24); fresh(24, s['gamete'])
assert s['gamete'] == 12
q(Q, 2, "An organism's body cells have a diploid number of 2N = 24. How many chromosomes are in each "
        "gamete it makes by meiosis?",
  uniq([str(s['gamete']), '24', '48', '6']), 0,
  "A gamete is haploid. What is N when 2N is 24?",
  ["A body cell is diploid: 2N = 24.",
   "Meiosis makes haploid gametes, with one of each chromosome: N.",
   "N is half of 2N, so 24 ÷ 2 = 12.",
   "Each gamete has 12 chromosomes."],
  "**12.** A gamete is haploid, so it carries N = 12 — one of each of the 12 types. 24 would be a "
  "mitosis daughter cell; 48 counts the chromatids after S phase; 6 halves twice, but meiosis halves "
  "the chromosome number only once.",
  "Gamete = N. Halve the diploid number once.")

s = stage(20); c, t = s['after_s']; fresh(20, c, t)
assert (c, t) == (20, 40)
q(Q, 2, "A germline cell with 2N = 20 finishes S phase, ready to begin meiosis. How many chromosomes "
        "and chromatids does it have?",
  uniq([pair(c, t), pair(40, 40), pair(20, 20), pair(40, 80)]), 0,
  "S phase copies every chromosome into an X. Does an X count as one chromosome or two?",
  ["Before S phase the cell has 20 single-strand chromosomes: 20 chromatids.",
   "S phase copies each one, so every chromosome becomes an X of two sister chromatids.",
   "An X is still one chromosome, because its chromatids share a centromere.",
   "So there are 20 chromosomes and 20 × 2 = 40 chromatids."],
  "**20 chromosomes, 40 chromatids.** Copying the DNA doubles the chromatids, never the chromosomes — "
  "an X counts once, by its centromere. Forty chromosomes would only appear if the chromatids came "
  "apart, which they do not do until meiosis II.",
  "Count centromeres for chromosomes, strands for chromatids.")

s = stage(18); c, t = s['after_m1']; fresh(18, c, t)
assert (c, t) == (9, 18)
q(Q, 2, "A germline cell with 2N = 18 goes through meiosis. At the end of meiosis I, how many "
        "chromosomes and chromatids does EACH of the two new cells have?",
  uniq([pair(c, t), pair(9, 9), pair(18, 18), pair(18, 36)]), 0,
  "Meiosis I splits the homologous pairs. Are the chromatids still joined afterwards?",
  ["After S phase the cell has 18 X-shaped chromosomes: 36 chromatids.",
   "Meiosis I separates the homologous pairs, so each new cell gets one of each pair: 9 chromosomes.",
   "The chromatids are still joined, so each of those 9 is still an X.",
   "So each cell has 9 chromosomes and 9 × 2 = 18 chromatids."],
  "**9 chromosomes, 18 chromatids.** Meiosis I halves the chromosome number but leaves every "
  "chromosome X-shaped. Nine chromatids is where a cell ends up only after meiosis II pulls those X's "
  "apart.",
  "After meiosis I: haploid, but still X-shaped.")

s = stage(14); c, t = s['after_m2']; fresh(14, c, t)
assert (c, t) == (7, 7)
q(Q, 2, "A germline cell with 2N = 14 completes both divisions of meiosis. How many chromosomes and "
        "chromatids does EACH of the four final cells have?",
  uniq([pair(c, t), pair(7, 14), pair(14, 14), pair(14, 28)]), 0,
  "Meiosis I halved the chromosomes. What did meiosis II do to the chromatids?",
  ["After meiosis I, each cell has 7 chromosomes, still X-shaped: 14 chromatids.",
   "Meiosis II pulls each X apart into its two chromatids.",
   "Each final cell gets one chromatid of every X: 7 single strands.",
   "So each final cell has 7 chromosomes and 7 chromatids."],
  "**7 chromosomes, 7 chromatids.** By the end, every chromosome is a single strand, so the two "
  "counts match. Seven chromosomes with 14 chromatids is the halfway point — the end of meiosis I.",
  "At the very end, chromosomes and chromatids are the same number: N.")

s = stage(16); fresh(16, s['tetrads'])
assert s['tetrads'] == 8 and s['tetrad_chromatids'] == 32
q(Q, 2, "A germline cell has a diploid number of 2N = 16. How many tetrads form during prophase I?",
  uniq([str(s['tetrads']), '16', '4', '32']), 0,
  "One tetrad forms for each homologous pair. How many pairs are there?",
  ["2N = 16 means 16 chromosomes, in matched homologous pairs.",
   "16 chromosomes make 16 ÷ 2 = 8 pairs.",
   "Each pair comes together as one tetrad in prophase I.",
   "So 8 tetrads form."],
  "**8.** A tetrad is a homologous PAIR, so there are as many tetrads as there are pairs — N. Thirty-two "
  "is the number of chromatids in those tetrads, four apiece, not the number of tetrads.",
  "One tetrad per pair: N tetrads.")

s = stage(12); fresh(12, s['assortment'])
assert s['assortment'] == 64
q(Q, 2, "A species has a diploid number of 2N = 12. Counting only independent assortment, and ignoring "
        "crossing over, how many different combinations of chromosomes can its gametes carry?",
  uniq([str(s['assortment']), '12', '36', '6']), 0,
  "Each homologous pair lines up at random, independently of the others. How many pairs are there?",
  ["2N = 12, so there are N = 6 homologous pairs.",
   "In metaphase I each pair can line up two ways: mother's on one side or the other.",
   "Six independent two-way choices give 2 × 2 × 2 × 2 × 2 × 2 combinations.",
   "That is 2^6 = 64."],
  "**64.** Independent assortment gives 2^N combinations, because every pair makes its own two-way "
  "choice. 36 is 6², squaring instead of raising 2 to the power; 12 and 6 just restate the chromosome "
  "counts. Crossing over then multiplies the variety further still.",
  "N coins, each heads or tails: 2^N outcomes.")

s = stage(32); fresh(32, s['gamete'], s['zygote'])
assert s['gamete'] == 16 and s['zygote'] == 32
q(Q, 2, "In one species, a sperm cell carries 16 chromosomes. How many chromosomes does a zygote of "
        "that species have?",
  uniq([str(s['zygote']), '16', '64', '8']), 0,
  "The sperm is haploid. Where does the zygote's other set come from?",
  ["The sperm is a gamete, so it is haploid: N = 16.",
   "The egg is also a gamete of the same species, also with N = 16.",
   "The zygote forms when the two fuse, so it has 16 + 16.",
   "That is 32, the diploid number."],
  "**32.** Fertilization adds two haploid sets: N + N = 2N. That restores exactly the number the "
  "parents' body cells have, which is why the gametes had to be halved in the first place.",
  "Egg + sperm = N + N = 2N.")

q(Q, 2, "Which of these happens in meiosis but NEVER in mitosis?",
  ["Homologous chromosomes pair up and line up together in the middle",
   "Sister chromatids are pulled apart toward opposite ends of the cell",
   "The DNA is copied during the S phase of interphase beforehand",
   "A spindle forms and lines the chromosomes up across the middle"], 0,
  "Three of these happen in both. Which step needs two chromosomes from two different parents?",
  ["Both processes start with the same interphase, so the DNA copying happens in both.",
   "Both use a spindle to line chromosomes up across the middle.",
   "Sister chromatids are pulled apart in mitosis and in meiosis II.",
   "Only meiosis I pairs homologous chromosomes up, as tetrads."],
  "**Homologous chromosomes pair up and line up together in the middle.** That pairing, in prophase I "
  "and metaphase I, is what lets meiosis split the pairs and halve the number. Mitosis lines each "
  "chromosome up on its own.",
  "Pairing up is meiosis's signature move.")

q(Q, 2, "A germline cell in an ovary completes meiosis. What does it end up producing?",
  ["One large egg cell and small polar bodies",
   "Four egg cells, all of an equal size",
   "Two diploid egg cells, both identical",
   "One egg cell with twice the haploid number"], 0,
  "Egg-making divides the cell unequally. Who gets the cytoplasm?",
  ["The germline cell goes through both divisions of meiosis.",
   "In an ovary, those divisions are unequal: one cell keeps almost all the cytoplasm.",
   "That large cell becomes the egg; the small leftover cells are polar bodies.",
   "So it produces one egg and small polar bodies."],
  "**One large egg cell and small polar bodies.** The unequal division puts almost all the cytoplasm "
  "into one cell, giving the egg the supplies an early embryo needs. Sperm-making divides evenly, so "
  "a male germline cell's four cells all become sperm. Either way, the gametes are haploid.",
  "Ovary: one big winner. Testis: four equal sperm.",
  frm='source')

# ---- level 3: analyze

q(Q, 3, "Put these events of meiosis in order, from earliest to latest.",
  ["Homologous chromosomes pair up into tetrads and cross over",
   "The tetrads line up across the middle of the cell in pairs",
   "The homologous pairs are pulled apart, chromatids still joined",
   "The sister chromatids are pulled apart in each of two cells"], 0,
  "Pair, line up, split the pairs — then split the sisters.",
  ["Pairing up and crossing over is prophase I.",
   "Lining up in pairs across the middle is metaphase I.",
   "Pulling the pairs apart is anaphase I.",
   "Pulling the sister chromatids apart is anaphase II, in the two cells meiosis I made."],
  "**Pair and cross over, line up in pairs, split the pairs, split the sisters.** Meiosis I handles the "
  "homologous pairs, and only then does meiosis II deal with the chromatids — the order is the reason "
  "the number halves once and not twice.",
  "Meiosis I is about pairs; meiosis II is about sisters.",
  kind='order')

q(Q, 3, "Two sperm cells made by the same person almost never carry the same combination of alleles. "
        "Which explanation accounts for that?",
  ["Crossing over swaps pieces between homologs, and independent assortment shuffles them",
   "The DNA is copied with new errors in every S phase, so each copy comes out different",
   "Meiosis II separates the homologous chromosomes at random into the four new cells",
   "Each sperm receives a full set of both parents' chromosomes, rearranged in a new order"], 0,
  "Two separate events in meiosis I mix the alleles. Name both.",
  ["In prophase I, crossing over swaps matching pieces between homologous chromosomes.",
   "In metaphase I, each pair lines up at random, so each cell gets a random mix of mother's and father's chromosomes.",
   "Together, those make an enormous number of possible combinations.",
   "So two sperm from one person are almost never alike."],
  "**Crossing over swaps pieces between homologs, and independent assortment shuffles them.** Both "
  "happen in meiosis I. Meiosis II separates sister chromatids, not homologs, and a sperm is haploid, "
  "so it carries one set — never both parents' full sets.",
  "Swap in prophase I, shuffle in metaphase I.")

q(Q, 3, "At what point in meiosis does the cell first become haploid?",
  ["At the end of meiosis I, though its chromosomes are still X-shaped",
   "Only at the end of meiosis II, once the sister chromatids separate",
   "In prophase I, as soon as the homologous pairs form tetrads",
   "Only once a gamete has fused with another at fertilization"], 0,
  "Haploid means one of each TYPE of chromosome. When does each cell stop having pairs?",
  ["Haploid means one chromosome of each type, rather than a pair.",
   "Meiosis I separates the homologous pairs into two cells.",
   "So each of those cells already has only one of each type — even though each one is still an X.",
   "Meiosis II then splits the X's, but each new cell keeps that same one-of-each set."],
  "**At the end of meiosis I, though its chromosomes are still X-shaped.** Haploid counts chromosome "
  "types, not strands, and the pairs are split in meiosis I. Meiosis II halves the chromatids, not "
  "the number of chromosome types. Fertilization does the opposite — it makes a cell diploid again.",
  "Pairs gone = haploid, X-shaped or not.",
  frm='source')

q(Q, 3, "Why do the body cells of every sexually reproducing organism contain an even number of "
        "chromosomes?",
  ["Body cells hold chromosomes in matched pairs, one of each pair from each parent",
   "S phase copies every chromosome once, and doubling any number makes it even",
   "Mitosis can only share an even number of chromosomes equally between two cells",
   "Crossing over needs every chromosome to have a partner to swap pieces with"], 0,
  "Where did each of a body cell's chromosomes come from?",
  ["A body cell started out as a zygote, made from an egg and a sperm.",
   "Each gamete gave one complete set of N chromosomes.",
   "So the body cell has every type of chromosome twice: one from each parent.",
   "Two of every type makes 2 × N, which is always even."],
  "**Body cells hold chromosomes in matched pairs, one of each pair from each parent.** The count is "
  "2N, and two times anything is even. S phase doubles chromatids, not chromosomes, and mitosis copies "
  "before it divides, so it could share an odd number equally too.",
  "Pairs, one from each parent: count by twos.",
  frm='added')

s = stage(12); c, t = s['anaphase2']; fresh(6, c)
assert s['after_m1'][0] == 6 and (c, t) == (12, 12)
q(Q, 3, "A cell has just finished meiosis I with 6 X-shaped chromosomes. During anaphase II, how many "
        "chromosomes does that cell briefly contain?",
  uniq([str(c), '6', '3', '24']), 0,
  "A chromosome is counted by its centromere. What happens to that count when each X comes apart?",
  ["The cell starts meiosis II with 6 chromosomes, each an X of two chromatids: 12 chromatids.",
   "In anaphase II each X is pulled apart into its two chromatids.",
   "Once separated, each chromatid counts as a chromosome of its own.",
   "So for a moment the cell holds 12 chromosomes, before telophase II splits them 6 and 6."],
  "**12.** Separating the sister chromatids briefly doubles the chromosome count in that cell, exactly "
  "as anaphase does in mitosis. Telophase II then shares them out, so each new cell ends with 6 — the "
  "haploid number.",
  "Break an X and you get two chromosomes.",
  frm='added')

s = stage(10)
assert s['zygote'] == 10 and 2 * s['mitosis_daughter'] == 20
q(Q, 3, "Suppose an organism made its sperm and eggs by mitosis instead of meiosis. What would "
        "happen to the chromosome number from one generation to the next?",
  ["It would double every generation",
   "It would stay the same every time",
   "It would halve every generation",
   "It would change at random each time"], 0,
  "Mitosis keeps the full diploid number. Then two of those cells fuse.",
  ["Mitosis gives daughter cells the same number as the parent: 2N.",
   "So each gamete would carry 2N instead of N.",
   "An egg and a sperm would fuse into a 2N + 2N = 4N zygote.",
   "The next generation would reach 8N, so the number would double every generation."],
  "**It would double every generation.** Gametes are haploid precisely so that N + N = 2N restores "
  "the parents' number. A 2N gamete would make a 4N zygote, and the doubling would never stop.",
  "Halve first, or fertilization doubles.",
  frm='added')

# Every graded count must come from stage(), and none may reuse the deck's
# own worked numbers. Checked once more over the finished question set.
for x in Q:
    for bad in ('30 chromosomes', '60 chromatids', '2^23', '8,388,608', '2N = 4'):
        assert bad not in x['q'], (x['id'], bad)

build('ad-astra', C, Q, 'unit-bio-u5',
      'Biology 8 · Unit 5-1: Meiosis', 'bio',

      "Her teacher's Unit 5 deck on meiosis and the class's meiosis note outline: haploid and diploid, "
      "somatic and germline cells, autosomes and sex chromosomes, homologous chromosomes and alleles, "
      "the tetrad, crossing over in prophase I and independent assortment in metaphase I, meiosis I "
      "and meiosis II phase by phase, counting chromosomes and chromatids through both divisions, "
      "eggs, sperm and polar bodies, and the five ways meiosis differs from mitosis.",

      "Every inheritance problem this year starts from meiosis: which alleles a gamete can carry, why "
      "siblings differ, why the chromosome number stays steady from parent to child. It is taught "
      "almost entirely by contrast with mitosis, so it is also the best test of whether Unit 4 stuck.",

      [("Say what meiosis produces, from what kind of cell, and how that differs from mitosis.", 'source'),
       ("Tell homologous chromosomes from sister chromatids, and say what a tetrad is.", 'source'),
       ("Name what happens in each phase of meiosis I and meiosis II, including where crossing over "
        "and independent assortment happen.", 'source'),
       ("Count chromosomes and chromatids at each point in meiosis for any diploid number.", 'source'),
       ("Say when in meiosis the cell becomes haploid, and why.", 'source'),
       ("Explain why gametes must be haploid and why body cells always hold an even number of "
        "chromosomes.", 'added')],

      "Built from her new Biology Unit 5 folder: the teacher's lecture deck (MEIOSIS (1).pptx) and "
      "the class's three-page meiosis note outline. The deck was read through Drive's text version; "
      "the file was too large to download here, so its slide pictures were not seen — if a slide "
      "carries a fact only in a picture, it is not in this unit. The third file, the directed-reading "
      "question sheet, asks for the title, author, variables and main idea of a science article that "
      "is not in the folder, so there was nothing on meiosis in it to build from.\n\n"
      "TWO PLACES THE SOURCES DISAGREE are worth your eye, and the unit teaches the correct version of "
      "each.\n\n"
      "FIRST — where meiosis starts. The note outline defines meiosis as making gametes 'from diploid "
      "somatic cells of your body', but the same page defines a somatic cell as one NOT used for "
      "sexual reproduction and made by mitosis. The deck names the real starting cell: a germline "
      "cell (oogonium or spermatogonium). The unit teaches germline cells, and one card keeps the two "
      "kinds apart.\n\n"
      "SECOND — when the cell becomes haploid. One slide reads 'The second ends in haploid cells as "
      "chromatids are separated', which sounds as if the cell only turns haploid at the end of meiosis "
      "II. The note outline says telophase I already ends with 'two 1N cells', and the deck's own "
      "knowledge check agrees (30 chromosomes in, 15 after meiosis I). The deck's practice question 11 "
      "asks exactly this, so the unit teaches the end of meiosis I and offers the end-of-meiosis-II "
      "reading as a wrong option. Worth a word with her teacher if her class marks it the other way.\n\n"
      "Some cards are our additions, because the material asks about them without answering: why body "
      "cells always hold an even number of chromosomes (practice question 3), what meiosis and mitosis "
      "have in common, the benefits and costs of asexual and sexual reproduction (blank on both the "
      "deck and the outline), what happens to the chromosome count in anaphase II (the outline asks), "
      "and why gametes must be haploid. They are tagged as study suggestions rather than class "
      "material.\n\n"
      "Every chromosome and chromatid count in the questions uses fresh numbers, computed and checked "
      "in the builder; none reuses the deck's own 30-chromosome example. The gummy-bear meiosis lab "
      "and the 'draw the phases' practice are hands-on and stay on paper. No pictures, deliberately: "
      "the outline's crossing-over and assortment figures are textbook art, not ours to republish.",

      ("Start with the cards on homologous pairs versus sister chromatids and on counting through "
       "meiosis — the counting questions lean on both. Say each answer out loud before you flip.", 25),
      'content/bio-unit-5-meiosis.json',
      'MEIOSIS (1).pptx and meiosis note outlines.pdf (Biology 8 · Unit 5, Drive)',
      'source', offset_hours=3, libv_=1)
