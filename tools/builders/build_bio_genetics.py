#!/usr/bin/env python3
"""Biology 8 · Unit 7-1: Genetics.

Source: the class's Unit 7 Genetics lecture deck, read through Drive's text
representation. Two copies are in Drive and the second is a superset of the
first, so the second was used. The slide PICTURES were not seen; everything
below that cites the deck cites its slide TEXT: the Mendelian vocabulary,
Mendel and his three laws, the widow's-peak and polar/black-bear prompts, the
four Punnett-square steps, a six-item knowledge check, non-Mendelian genetics
(codominance, blood type), polygenic traits, sex-linked traits, karyotypes and
autosomes, the four sex-chromosome conditions, and four practice problems (dog
ears, an IA i x IB i blood cross, a Y-linked webbed-toes cross, a hemophilia
cross).

Four calls are taught more carefully than the deck words them, and parentNote
says so:

1. Knowledge-check Q2 prints "All of the above" as an option, and it is NOT
   correct. A dominant allele is not "better" and not necessarily "more
   common" (polydactyly is dominant and rare). The unit teaches the one true
   option: a dominant allele can hide the recessive one's trait.
2. Knowledge-check Q1's "every time unless told not to" is a classroom
   convention, not biology. It is taught as the class's default assumption:
   assume complete dominance unless the problem says otherwise.
3. The deck names incomplete dominance but never defines it. A card added here
   does (the heterozygote is a blend), and contrasts it with codominance (both
   show in full). The deck's dog-ears problem (semi-floppy in between) reads as
   incomplete dominance though the deck calls it codominant; that is in the
   note only, and no graded question turns on it.
4. The deck asks how the extra sex chromosomes "get there" and "which cells
   would they be in". A card added here answers: nondisjunction during meiosis,
   so the extra chromosome is in the first cell and so in every cell after.

Every Punnett percentage and ratio in a graded question is computed below by
actually crossing the alleles, and asserted before it is written. None of the
deck's own crosses is used in a graded stem (they appear on cards only).
"""
import io, json, os, re, sys
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build, REPO

# ------------------------------------------------------------- the crossing

SUP = {'A': 'ᴬ', 'B': 'ᴮ', 'R': 'ᴿ', 'W': 'ᵂ', 'w': 'ʷ'}

def cross(mom, dad):
    """Every zygote of a Punnett square: one allele from each parent, 4 boxes."""
    return [(m, d) for m in mom for d in dad]

def pct(n, total):
    f = Fraction(n, total) * 100
    assert f.denominator == 1, f
    return int(f)

# One gene, complete dominance. Alleles are single letters; upper = dominant.
def mono(g1, g2):
    boxes = cross(list(g1), list(g2))
    geno = Counter(''.join(sorted(b, key=lambda a: (a.islower(), a))) for b in boxes)
    dom = sum(1 for b in boxes if any(a.isupper() for a in b))
    return {'geno': geno, 'dom': pct(dom, 4), 'rec': pct(4 - dom, 4)}

# Blood type: IA and IB codominant, i recessive.
def blood_type(z):
    s = set(z)
    if 'IA' in s and 'IB' in s: return 'AB'
    if 'IA' in s: return 'A'
    if 'IB' in s: return 'B'
    return 'O'

def blood(g1, g2):
    boxes = cross(g1, g2)
    c = Counter(blood_type(b) for b in boxes)
    return {t: pct(c[t], 4) for t in ('A', 'AB', 'B', 'O')}, c

def blood_ratio(c):
    return ' : '.join('%d type %s' % (c[t], t) for t in ('A', 'AB', 'B', 'O') if c[t])

def bgeno(g):
    return ''.join({'IA': 'Iᴬ', 'IB': 'Iᴮ', 'i': 'i'}[a] for a in g)

# Two alleles where the heterozygote is its own phenotype (codominance or
# incomplete dominance: the arithmetic is the same, only the look differs).
def het(g1, g2):
    boxes = cross(g1, g2)
    h = sum(1 for b in boxes if b[0] != b[1])
    return pct(h, 4)

def cgeno(g):
    return ''.join('C' + SUP[a[-1]] for a in g)

# X-linked, recessive: mother XX, father XY.
def xlinked(mom, dad):
    boxes = cross(mom, dad)
    sons = [b for b in boxes if b[1] == 'Y']
    daus = [b for b in boxes if b[1] != 'Y']
    rec = lambda xs: all(a[1].islower() for a in xs if a != 'Y')
    return {'sons': pct(sum(rec(b) for b in sons), len(sons)) if sons else None,
            'daughters': pct(sum(rec(b) for b in daus), len(daus)) if daus else None,
            'all': pct(sum(rec(b) for b in boxes), 4)}

def xgeno(g):
    return ''.join('Y' if a == 'Y' else 'X' + SUP[a[1]] for a in g)

# Y-linked: only the Y carries the gene.
def ylinked(mom, dad):
    boxes = cross(mom, dad)
    sons = [b for b in boxes if 'Yt' in b or 'Y' in b]
    daus = [b for b in boxes if b not in sons]
    return {'sons': pct(sum('Yt' in b for b in sons), len(sons)),
            'daughters': pct(sum('Yt' in b for b in daus), len(daus)) if daus else 0}

# The deck's own crosses, worked here so the method agrees with the class.
_wp = mono('Rr', 'Rr'); assert (_wp['dom'], _wp['rec']) == (75, 25)       # its Q6 shape
_d, _ = blood(['IA', 'i'], ['IB', 'i']); assert _d == {'A': 25, 'AB': 25, 'B': 25, 'O': 25}
_cb = xlinked(['XR', 'Xr'], ['XR', 'Y']); assert _cb == {'sons': 50, 'daughters': 0, 'all': 25}
assert ylinked(['X', 'X'], ['X', 'Yt']) == {'sons': 100, 'daughters': 0}

def uniq(opts):
    assert len(set(opts)) == 4, opts
    return opts

def pct_opts(ans, pool=(0, 25, 50, 75, 100)):
    """Four percentages including the answer; never let '100%' be the only
    longest option when it is the answer."""
    others = [p for p in pool if p != ans]
    # keep the three nearest the answer, so a guess cannot rule out extremes
    others.sort(key=lambda p: (abs(p - ans), p))
    pick = sorted([ans] + others[:3])
    if ans != 100 and 100 not in pick and len(str(ans)) < 3:
        pass
    o = ['%d%%' % p for p in pick]
    return uniq(o), o.index('%d%%' % ans)

C, Q = [], []

# ------------------------------------------------------------------ cards

card(C, 'Gene',
     "**The basic unit of heredity: a stretch of DNA that codes for one characteristic.**\n"
     "• Genes sit on chromosomes, and you inherit them from your parents",
     hint="Gene → genetics → generations: the thing handed down.")

card(C, 'Chromosome',
     "**A package of DNA wrapped around proteins, carrying the genetic information.**\n"
     "• Each gene sits at its own spot on one chromosome\n"
     "• Humans have 46 in each body cell, in 23 pairs",
     hint="Chroma = color: they were named for how they take up stain under the microscope.")

card(C, 'Trait',
     "**One version of a characteristic, such as brown eyes or a flat hairline.**\n"
     "• Eye color is the characteristic; brown is the trait",
     hint="The characteristic is the question; the trait is the answer.")

card(C, 'Allele',
     "**One of two or more versions of the same gene.**\n"
     "• You carry two alleles for each gene, one from each parent\n"
     "• Written as letters: a capital for dominant, lowercase for recessive",
     hint="Alleles are alternatives: different versions of one gene.")

card(C, 'Genotype',
     "**The two alleles an organism has for a gene, written as letters, such as Bb.**\n"
     "• It is the code, not the look",
     hint="GENotype is the GENes.")

card(C, 'Phenotype',
     "**The trait you can actually observe, such as green pods or type O blood.**\n"
     "• Two different genotypes can give the same phenotype (BB and Bb)",
     hint="Phenotype is the physical look; pheno- sounds like 'show'.")

card(C, 'Dominant allele',
     "**An allele that shows its trait with only one copy.**\n"
     "• Written with a capital letter, such as B\n"
     "• In a heterozygote (Bb) it hides the recessive allele's trait",
     hint="One capital letter is enough for it to show.")

card(C, 'Recessive allele',
     "**An allele whose trait shows only when there are two copies.**\n"
     "• Written lowercase, such as b; only bb shows the recessive trait",
     hint="It recedes into the background unless it has company.")

card(C, 'Heterozygous',
     "**Having two different alleles for a gene, such as Bb.**\n"
     "• Also called a hybrid\n"
     "• For a recessive trait, a heterozygote is a carrier: it carries the allele without showing it",
     hint="Hetero = different, as in heterogeneous.")

card(C, 'Homozygous',
     "**Having two identical alleles for a gene: BB (homozygous dominant) or bb (homozygous recessive).**\n"
     "• Also called true-breeding: crossed with its own kind, it always gives the same trait",
     hint="Homo = same.")

card(C, 'Dominant is not "better" or "more common"',
     "**Dominant only means one copy is enough to show; it says nothing about how good or how common an allele is.**\n"
     "• Polydactyly (extra fingers or toes) is caused by a dominant allele and is rare\n"
     "• What a dominant allele always CAN do is hide the recessive trait in a heterozygote",
     hint="Dominant describes who shows up in Bb, not who wins in nature.",
     frm='added')

card(C, 'Law of dominance',
     "**In a heterozygote, the dominant allele's trait is the one that shows.**\n"
     "• Gregor Mendel worked out his laws of heredity by breeding pea plants\n"
     "• Following these laws is called Mendelian genetics, or simple (complete) dominance",
     hint="Mendel's peas: one capital letter is enough.")

card(C, 'Law of segregation',
     "**Each parent passes on only one of its two alleles for a gene to each offspring.**\n"
     "• The two alleles separate when gametes form, so every egg or sperm carries one",
     hint="Segregate = separate. The pair splits into the gametes.")

card(C, 'Law of independent assortment',
     "**Which allele you inherit for one gene does not affect which you inherit for another.**\n"
     "• The exception: genes close together on the same chromosome tend to be inherited together",
     hint="Independent: like flipping two separate coins — unless they are glued together.")

card(C, 'Complete dominance is the default',
     "**Unless a problem says otherwise, your class assumes complete dominance: the dominant allele hides the recessive one.**\n"
     "• This is a convention for problems, not a rule of nature\n"
     "• If a problem names codominance, a blend or a sex chromosome, use that instead",
     hint="No other pattern named? Treat the capital letter as the one that shows.",
     frm='added')

card(C, 'Worked examples: widow\'s peak and the bears',
     "**With R for widow's peak and r for a flat hairline, R is dominant: RR and Rr show a widow's peak, and rr is flat.**\n"
     "• A polar bear crossed with a black bear gives all-black cubs, so black is dominant\n"
     "• Written out: black parent BB × polar parent bb, and every cub Bb",
     hint="If every offspring shows one parent's trait, that trait is dominant.",
     frm='added')

card(C, 'Punnett square',
     "**A grid that shows every way two parents' alleles can combine, giving the chance of each offspring genotype.**\n"
     "• 1 Write both parents' genotypes. 2 Split each parent's two alleles along its own side (top or left): these are the gametes\n"
     "• 3 Fill each box with the allele from its row and its column: these are the zygotes. 4 Count how often each genotype appears",
     hint="Gametes on the edges, zygotes in the boxes.")

card(C, 'Two heterozygous parents',
     "**Bb × Bb gives 1 BB : 2 Bb : 1 bb, so 75% show the dominant trait and 25% the recessive one.**\n"
     "• Each box is one chance in four, or 25%\n"
     "• Two parents can both hide a recessive trait and still have a child who shows it",
     hint="Three boxes have a capital, one box does not.",
     frm='added')

card(C, 'Codominance',
     "**Both alleles show in full in a heterozygote, side by side.**\n"
     "• Blood type AB: the A and B antigens are both made\n"
     "• Roan cattle: a red allele and a white allele give a coat of red hairs AND white hairs",
     hint="Co- = together. Both show, neither hides.")

card(C, 'Incomplete dominance',
     "**Neither allele fully hides the other, so the heterozygote is a blend in between.**\n"
     "• Red snapdragon × white snapdragon gives pink flowers\n"
     "• Compare codominance: there both show in full (red and white hairs), not a mixed color",
     hint="Incomplete: the dominant allele only gets partway, so you see a blend.",
     frm='added')

card(C, 'Blood type alleles',
     "**The blood-type gene has three alleles, Iᴬ, Iᴮ and i, but each person carries only two.**\n"
     "• Iᴬ makes the A antigen and Iᴮ the B antigen; both are dominant to i, which makes nothing\n"
     "• Iᴬ and Iᴮ are codominant, so IᴬIᴮ is type AB",
     hint="Three alleles in the population, two in any one person.")

card(C, 'Six blood genotypes, four blood types',
     "**IᴬIᴬ and Iᴬi are type A; IᴮIᴮ and Iᴮi are type B; IᴬIᴮ is type AB; ii is type O.**\n"
     "• So types A and B can each hide an i, and type O needs two\n"
     "• The class cross Iᴬi × Iᴮi gives all four types, 25% each",
     hint="Only O needs both alleles to be i.",
     frm='added')

card(C, 'Polygenic trait',
     "**A trait controlled by many genes, so it varies smoothly in a bell-shaped curve.**\n"
     "• Eye color is controlled by about 16 genes; height by hundreds\n"
     "• Skin and hair color: a few genes with big effects and many with small ones",
     hint="Poly = many. Many genes, each adding a little, makes a smooth range.")

card(C, 'Sex chromosomes and autosomes',
     "**In humans, females have two X chromosomes (XX) and males have an X and a Y (XY).**\n"
     "• Every other chromosome is an autosome\n"
     "• A picture of all of an organism's chromosomes, in pairs, is a karyotype",
     hint="Auto- = self: the 'ordinary' chromosomes everyone has in matching pairs.")

card(C, 'Sex-linked trait',
     "**A trait whose gene is on a sex chromosome, usually the X.**\n"
     "• Red-green colorblindness is recessive and on the X\n"
     "• The class cross Xᴿ Xʳ × Xᴿ Y gives 25% colorblind children: 50% of the sons and none of the daughters",
     hint="Write the allele as a superscript on the X, and give the Y nothing.")

card(C, 'Why males show X-linked recessive traits more',
     "**A male has only one X, so a single recessive allele on it shows: there is no second X to mask it.**\n"
     "• A female needs the allele on BOTH X chromosomes to show the trait\n"
     "• A son gets his X from his mother and his Y from his father",
     hint="One X, no backup.",
     frm='added')

card(C, 'Y-linked trait',
     "**A trait whose gene is on the Y chromosome passes from a father to every son and to no daughter.**\n"
     "• Only males have a Y, and every son gets his father's Y\n"
     "• The class example is webbed toes",
     hint="Father to son, every time, and never to a daughter.",
     frm='added')

card(C, 'Sex-chromosome conditions',
     "**Rarely, a person has a different number of sex chromosomes, and each pattern has a name.**\n"
     "• Klinefelter syndrome: XXY. Trisomy X: XXX\n"
     "• Turner syndrome: a single X. XYY syndrome: XYY",
     hint="Read the letters: the name tells you which sex chromosomes are there.")

card(C, 'Where an extra sex chromosome comes from',
     "**From nondisjunction: during meiosis a chromosome pair fails to separate, so an egg or sperm gets one too many or too few.**\n"
     "• That gamete forms the first cell of the new person\n"
     "• So the difference is in every cell with a nucleus, not just a few (see Unit 5-1, meiosis)",
     hint="Non-disjunction: the pair did not dis-join.",
     frm='added')

# ------------------------------------------------------------------ questions

# --- level 1: vocabulary and recall
q(Q, 1, "What is one of two or more versions of the same gene called?",
  uniq(['An allele', 'A genotype', 'A phenotype', 'A chromosome']), 0,
  "Think of the word for 'alternative versions'.",
  ["A gene is the unit of heredity for one characteristic.",
   "A gene can come in different versions, such as B and b.",
   "A genotype is the PAIR of letters, and a phenotype is the look.",
   "Each single version is an allele."],
  "**An allele.** B and b are two alleles of one gene. The genotype is the pair you carry (Bb), the "
  "phenotype is the trait you see, and a chromosome is the package that holds the gene.",
  "Allele = one version; genotype = the pair.")

q(Q, 1, "Which of these is a phenotype?",
  uniq(['Green pods', 'Gg', 'Homozygous dominant', 'G']), 0,
  "Which one could you see if you looked at the plant?",
  ["A phenotype is a trait you can observe.",
   "Gg is a genotype, written in letters.",
   "G on its own is a single allele, and 'homozygous dominant' describes a genotype.",
   "Green pods can be seen, so that is the phenotype."],
  "**Green pods.** A phenotype is what you can observe. Letters (Gg, G) and words about the letters "
  "(homozygous dominant) all describe the genotype or an allele.",
  "If you could photograph it, it is a phenotype.")

q(Q, 1, "In pea plants, stem height is controlled by one gene with the alleles T and t. Which of these "
        "is a dominant allele?",
  uniq(['T', 't', 'Tt', 'Tall stems']), 0,
  "How are dominant alleles written?",
  ["A dominant allele is written with a capital letter.",
   "Tt is two alleles together, so it is a genotype.",
   "Tall stems is a trait you can see, so it is a phenotype.",
   "The single capital letter, T, is the dominant allele."],
  "**T.** An allele is ONE letter, and the capital is the dominant one. Tt is a genotype (two "
  "alleles) and tall stems is a phenotype.",
  "One letter = an allele; a capital = dominant.")

q(Q, 1, "For a recessive trait, which term describes a carrier?",
  uniq(['Heterozygous', 'Homozygous recessive', 'Homozygous dominant', 'True-breeding']), 0,
  "A carrier has the allele but does not show it. What genotype does that take?",
  ["A carrier holds the recessive allele without showing the trait.",
   "Two recessive alleles (bb) would SHOW the trait, so that is not a carrier.",
   "Two dominant alleles (BB) carry no recessive allele at all.",
   "One of each (Bb) carries it and hides it: heterozygous."],
  "**Heterozygous.** A carrier has one recessive allele hidden behind a dominant one, as in Bb. "
  "Homozygous recessive (bb) shows the trait, and homozygous dominant (BB) does not carry it; "
  "true-breeding means homozygous, so it is wrong too.",
  "Carrier = Bb.")

q(Q, 1, "Which of Mendel's laws says that each parent passes on only one of its two alleles for a "
        "gene to each offspring?",
  uniq(['The law of segregation', 'The law of dominance', 'The law of independent assortment',
        'The rule of complementary base pairing']), 0,
  "Which law is about the pair of alleles splitting up?",
  ["Each parent has two alleles for each gene.",
   "When eggs or sperm form, the two alleles separate.",
   "So each gamete, and so each offspring, gets just one from that parent.",
   "Separating is segregation: the law of segregation."],
  "**The law of segregation.** Segregate means separate: the two alleles split into different "
  "gametes. The law of dominance is about which allele shows, independent assortment is about two "
  "DIFFERENT genes, and base pairing belongs to DNA, not to Mendel.",
  "Segregation = the pair separates.")

q(Q, 1, "A person has the blood genotype IᴬIᴮ. What is their blood type?",
  uniq(['Type AB', 'Type A', 'Type B', 'Type O']), 0,
  "Iᴬ and Iᴮ are codominant. What happens when both are present?",
  ["Iᴬ makes the A antigen and Iᴮ makes the B antigen.",
   "They are codominant, so neither hides the other.",
   "Both antigens are made.",
   "That is type AB."],
  "**Type AB.** In codominance both alleles show in full, so both antigens are made. Neither Iᴬ nor "
  "Iᴮ hides the other, which is why this is not type A or type B; type O needs ii.",
  "Codominant: both show.")

q(Q, 1, "A karyotype shows 45 chromosomes, with one X and no second sex chromosome. Which condition "
        "is this?",
  uniq(['Turner syndrome', 'Klinefelter syndrome', 'Trisomy X', 'XYY syndrome']), 0,
  "Which condition is the one with a single sex chromosome?",
  ["The usual count is 46, with two sex chromosomes.",
   "Here there is only one sex chromosome, an X.",
   "Klinefelter is XXY, trisomy X is XXX and XYY syndrome is XYY: all have extra.",
   "A single X is Turner syndrome."],
  "**Turner syndrome.** It is the one pattern with a missing sex chromosome (X). The other three "
  "each have an EXTRA one: XXY (Klinefelter), XXX (trisomy X) and XYY.",
  "Turner is the only one with fewer, not more.")

# --- level 2: crosses, computed
def mono_q(org, orgs, dom, D, rec, d, verb, g1, g2, asked, lv=2):
    r = mono(g1, g2)
    want = r['dom'] if asked == dom else r['rec']
    assert asked in (dom, rec)
    opts, a = pct_opts(want)
    boxes = [''.join(sorted(b, key=lambda x: (x.islower(), x))) for b in cross(list(g1), list(g2))]
    shown = sum(1 for b in boxes if (asked == dom) == any(x.isupper() for x in b))
    assert pct(shown, 4) == want
    text = ("In %s, %s (%s) %s dominant over %s (%s). Two %s with the genotypes %s × %s are crossed. "
            "What percentage of the offspring are expected to have %s?"
            % (org, dom, D, verb, rec, d, orgs, g1, g2, asked))
    return text, opts, a, boxes, want

t, o, a, boxes, want = mono_q('pea plants', 'plants', 'green pods', 'G', 'yellow pods', 'g', 'are',
                              'Gg', 'gg', 'yellow pods')
assert want == 50
q(Q, 2, t, o, a,
  "Put Gg on one side and gg on the other, then count the boxes with no capital G.",
  ["Gametes: G and g from one parent, g and g from the other.",
   "The four boxes are %s." % ', '.join(boxes),
   "Yellow pods need gg: two boxes out of four.",
   "Two in four is 50%."],
  "**50%.** Half the boxes are Gg (green, because one G is enough) and half are gg, the only "
  "genotype that shows yellow. Crossing with a homozygous recessive parent always splits a "
  "heterozygote's alleles half and half.",
  "Hybrid × recessive: half and half.")

t, o, a, boxes, want = mono_q('guinea pigs', 'guinea pigs', 'black fur', 'B', 'white fur', 'b', 'is',
                              'Bb', 'Bb', 'white fur')
assert want == 25
q(Q, 2, t, o, a,
  "Two carriers: how many of the four boxes get b from both parents?",
  ["Each parent's gametes are B and b.",
   "The four boxes are %s." % ', '.join(boxes),
   "Only bb shows white fur, and it fills one box.",
   "One in four is 25%."],
  "**25%.** Both parents are carriers, so white fur appears only where both pass on b: one box in "
  "four. The other three boxes hold at least one B, so they show black. 75% would be the black "
  "guinea pigs, not the white ones.",
  "Bb × Bb: 3 dominant to 1 recessive.")

r = mono('Pp', 'Pp')
gr = ' : '.join('%d %s' % (r['geno'][g], g) for g in ('PP', 'Pp', 'pp'))
assert gr == '1 PP : 2 Pp : 1 pp'
q(Q, 2, "In pea plants, purple flowers (P) are dominant over white flowers (p). Two plants with the "
        "genotypes Pp × Pp are crossed. Which genotype ratio is expected among the offspring?",
  uniq([gr, '3 PP : 1 pp', '1 PP : 1 pp', '2 PP : 1 Pp : 1 pp']), 0,
  "The question asks for GENOTYPES, not colors. Count each pair of letters.",
  ["Each parent's gametes are P and p.",
   "The boxes are PP, Pp, pP and pp.",
   "Pp and pP are the same genotype, so there are two of them.",
   "So the ratio is 1 PP : 2 Pp : 1 pp."],
  "**1 PP : 2 Pp : 1 pp.** Each box is one genotype, and two boxes hold Pp. '3 PP : 1 pp' mixes up "
  "the 3 : 1 PHENOTYPE ratio (purple : white) with the genotype ratio.",
  "Genotypes 1 : 2 : 1; phenotypes 3 : 1.")

bd, bc = blood(['IA', 'IB'], ['i', 'i'])
assert bd['A'] == 50
o, a = pct_opts(bd['A'])
q(Q, 2, "Two parents with the blood genotypes %s × %s have children. What percentage of their "
        "children are expected to have type A blood?" % (bgeno(['IA', 'IB']), bgeno(['i', 'i'])),
  o, a,
  "One parent can only give i. What can the other give?",
  ["The IᴬIᴮ parent passes on either Iᴬ or Iᴮ.",
   "The ii parent always passes on i.",
   "So the boxes are Iᴬi, Iᴬi, Iᴮi and Iᴮi.",
   "Iᴬi is type A: two boxes of four, so 50%."],
  "**50%.** Half the children get Iᴬ and are Iᴬi, type A; the other half get Iᴮ and are Iᴮi, type "
  "B. No child can be AB or O: AB needs both from different parents, and O needs i from both.",
  "A type-AB parent never has a type-AB child with a type-O parent.")

bd, bc = blood(['IA', 'IA'], ['IB', 'i'])
br = blood_ratio(bc)
assert br == '2 type A : 2 type AB', br
br = '1 type A : 1 type AB'          # the same ratio in lowest terms
assert bc['A'] == bc['AB'] and not bc['B'] and not bc['O']
q(Q, 2, "Two parents with the blood genotypes %s × %s have children. Which blood types can their "
        "children have, and in what ratio?" % (bgeno(['IA', 'IA']), bgeno(['IB', 'i'])),
  uniq([br, '1 type A : 1 type B', '3 type A : 1 type AB', '1 type AB : 1 type O']), 0,
  "One parent can only give Iᴬ. Pair it with each of the other parent's alleles.",
  ["The IᴬIᴬ parent always passes on Iᴬ.",
   "The Iᴮi parent passes on Iᴮ or i.",
   "Iᴬ with Iᴮ makes IᴬIᴮ, type AB; Iᴬ with i makes Iᴬi, type A.",
   "Two boxes of each: 1 type A : 1 type AB."],
  "**1 type A : 1 type AB.** Every child gets Iᴬ, so none can be type B or type O. Whether the "
  "second allele is Iᴮ or i decides AB or A, and the two are equally likely.",
  "List the gametes first, then the types.")

h = het(['R', 'W'], ['R', 'W'])
assert h == 50
o, a = pct_opts(h)
q(Q, 2, "In cattle, red coat and white coat are codominant, and an animal with one of each allele is "
        "roan, with a mix of red and white hairs. Two cattle with the genotypes %s × %s are mated. "
        "What percentage of their calves are expected to be roan?" % (cgeno(['R', 'W']), cgeno(['R', 'W'])),
  o, a,
  "Roan is the heterozygote. How many boxes have one of each allele?",
  ["Each parent's gametes are Cᴿ and Cᵂ.",
   "The boxes are CᴿCᴿ, CᴿCᵂ, CᵂCᴿ and CᵂCᵂ.",
   "CᴿCᴿ is red, CᵂCᵂ is white, and the two mixed boxes are roan.",
   "Two in four is 50%."],
  "**50%.** With codominance the heterozygote has its own look, so the ratio is 1 red : 2 roan : 1 "
  "white instead of 3 : 1. 75% would be what you get if you wrongly treated red as dominant and "
  "counted every calf with a red allele.",
  "No allele hides here, so 1 : 2 : 1 is also the look.")

h = het(['R', 'W'], ['W', 'W'])
assert h == 50
o, a = pct_opts(h)
q(Q, 2, "In snapdragons, a red-flowered plant crossed with a white-flowered plant gives pink "
        "flowers. Two snapdragons with the genotypes %s × %s are crossed. What percentage of the "
        "offspring are expected to be pink?" % (cgeno(['R', 'W']), cgeno(['W', 'W'])),
  o, a,
  "Pink is the in-between, one red allele and one white. Count those boxes.",
  ["The pink parent's gametes are Cᴿ and Cᵂ; the white parent's are Cᵂ and Cᵂ.",
   "The boxes are CᴿCᵂ, CᴿCᵂ, CᵂCᵂ and CᵂCᵂ.",
   "CᴿCᵂ is pink and CᵂCᵂ is white.",
   "Two in four are pink: 50%."],
  "**50%.** Half the offspring get the red allele from the pink parent and are pink; the other half "
  "get white from both and are white. No offspring can be red, because the white parent never "
  "passes on Cᴿ.",
  "A blend in the middle: count the mixed boxes.")

q(Q, 2, "Which statement is true of every dominant allele?",
  uniq(["It can hide a recessive allele's trait in a heterozygote",
        "It is more common in a population than the recessive allele",
        "It gives the organism a better chance of surviving",
        "It is passed on to children more often than a recessive one"]), 0,
  "Dominant describes what happens inside one heterozygote. Does it say anything about a whole population?",
  ["Dominant means one copy is enough for the trait to show.",
   "So in a heterozygote it hides the recessive trait.",
   "It says nothing about how common or useful the allele is: polydactyly is dominant and rare.",
   "And each allele has the same 50% chance of being passed on.",
   "The one true statement is that it can hide the recessive trait."],
  "**It can hide a recessive allele's trait in a heterozygote.** That is what dominant means. A "
  "dominant allele can be rare (polydactyly, extra fingers or toes) or harmful, and the law of "
  "segregation gives either allele of a pair an equal chance of being passed on.",
  "Dominant ≠ common, and dominant ≠ better.")

q(Q, 2, "Human height shows a smooth range from short to tall, with most people near the middle. What "
        "best explains that pattern?",
  uniq(["Hundreds of genes each add a little to it",
        "One gene with a dominant allele for tall",
        "Two codominant alleles of a single gene",
        "A gene that is carried on the Y chromosome"]), 0,
  "How many different heights could ONE gene with two alleles give?",
  ["One gene with complete dominance gives only two phenotypes.",
   "Two codominant alleles give only three.",
   "A smooth bell curve needs many small steps between short and tall.",
   "Many genes, each adding a little, make that curve."],
  "**Hundreds of genes each add a little to it.** Height is polygenic. A single gene gives a few "
  "separate types, never a smooth range, and a Y-linked gene would affect only males.",
  "Smooth bell curve → many genes.")

r = xlinked(['XW', 'Xw'], ['Xw', 'Y'])
assert r == {'sons': 50, 'daughters': 50, 'all': 50}
o, a = pct_opts(r['sons'])
q(Q, 2, "In fruit flies, the eye-color gene is on the X chromosome, and red eyes (%s) are dominant "
        "over white eyes (%s). A female and a male with the genotypes %s × %s are mated. What "
        "percentage of their sons are expected to have white eyes?"
        % ('Xᵂ', 'Xʷ', xgeno(['XW', 'Xw']), xgeno(['Xw', 'Y'])),
  o, a,
  "Sons get their X from their mother. Which X can she give?",
  ["Every son gets the father's Y, so his eye color depends only on the mother's X.",
   "The mother is XᵂXʷ, so she gives Xᵂ or Xʷ equally often.",
   "Sons are XᵂY (red) or XʷY (white).",
   "Half the sons have white eyes: 50%."],
  "**50%.** A son's single X comes from his mother, and she has one of each. The father's Xʷ goes "
  "only to daughters, so it does not change the sons at all.",
  "For sons, look only at the mother.")

# --- level 3: reasoning
q(Q, 3, "Put the steps for using a Punnett square in order, from first to last.",
  ["Write down the genotypes of both parents",
   "Split each parent's two alleles along its own side of the square",
   "Fill each box with the allele from its row and the allele from its column",
   "Count how often each genotype appears in the boxes"], 0,
  "You cannot split alleles you have not written down yet.",
  ["Start with what you know: both parents' genotypes.",
   "Separate each parent's alleles onto the edges: these are the gametes.",
   "Combine one from each edge in every box: these are the zygotes.",
   "Finally count each genotype to get the proportions."],
  "**Genotypes, split, fill, count.** Each step needs the one before it: the edges come from the "
  "genotypes, the boxes come from the edges, and the proportions come from the boxes.",
  "Parents → gametes → zygotes → proportions.",
  kind='order')

q(Q, 3, "Red-green colorblindness is caused by a recessive allele on the X chromosome. Why do far "
        "more males than females have it?",
  uniq(["A male has one X, so no second X can mask the allele",
        "The allele for it is carried on the Y chromosome",
        "A male inherits his X chromosome from his father",
        "The allele is dominant in males and recessive in females"]), 0,
  "How many X chromosomes does a male have, and where does he get it?",
  ["A female is XX, so she needs the recessive allele on both X chromosomes to show it.",
   "A male is XY, and the Y carries no copy of this gene.",
   "So one recessive allele on his only X is enough.",
   "With no second X to hide it, males show it far more often."],
  "**A male has one X, so no second X can mask the allele.** The gene is on the X, not the Y, and a "
  "son's X comes from his MOTHER. An allele is not dominant in one sex and recessive in the other; "
  "males simply have no backup copy.",
  "One X, no backup.")

r = ylinked(['X', 'X'], ['X', 'Yt'])
assert r == {'sons': 100, 'daughters': 0}
q(Q, 3, "A gene found only on the Y chromosome causes a trait. A father who shows the trait has "
        "children with a mother. Which of their children are expected to show it?",
  uniq(["Every son, and no daughter",
        "Every daughter, and no son",
        "Half the sons and half the daughters",
        "No child, since it skips a generation"]), 0,
  "Which children get their father's Y chromosome?",
  ["The mother has no Y, so she cannot pass the trait on.",
   "Every son gets his father's Y, and with it the gene.",
   "Every daughter gets the father's X instead, which does not carry the gene.",
   "So every son shows it and no daughter does."],
  "**Every son, and no daughter.** A Y-linked gene goes wherever the father's Y goes, and that is "
  "into every son and never into a daughter. There is no second allele to hide it and nothing to "
  "skip a generation.",
  "Y-linked: father to every son.")

r = xlinked(['Xw', 'Xw'], ['XW', 'Y'])
assert r == {'sons': 100, 'daughters': 0, 'all': 50}
q(Q, 3, "In fruit flies, the eye-color gene is on the X chromosome, and red eyes (Xᵂ) are dominant "
        "over white eyes (Xʷ). A female and a male with the genotypes %s × %s are mated. Which "
        "describes their offspring?" % (xgeno(['Xw', 'Xw']), xgeno(['XW', 'Y'])),
  uniq(["Every son white-eyed; every daughter red-eyed",
        "Every daughter white-eyed; every son red-eyed",
        "Half of the sons and half of the daughters white",
        "No white-eyed offspring of either sex at all"]), 0,
  "Sons take their X from the mother, daughters take one X from each parent.",
  ["The mother is XʷXʷ, so every child gets Xʷ from her.",
   "Sons get the father's Y, so they are XʷY: white eyes.",
   "Daughters get the father's Xᵂ, so they are XᵂXʷ: red eyes, but carriers.",
   "So every son is white-eyed and every daughter red-eyed."],
  "**Every son white-eyed; every daughter red-eyed.** The father's dominant Xᵂ goes only to "
  "daughters and hides their Xʷ. Sons get nothing from him on the X, so their mother's Xʷ shows. "
  "This criss-cross pattern is a sign of an X-linked trait.",
  "Mother's X → son; father's X → daughter.")

q(Q, 3, "A person's karyotype shows the sex chromosomes XXY. Where in their body is the extra X "
        "found, and why?",
  uniq(["In every cell with a nucleus, as it was in the egg or sperm that made the first cell",
        "Only in the egg or sperm cells, as those are the only cells made by meiosis",
        "Only in cells made after birth, as an error in mitosis added it to them later",
        "Only in the reproductive organs, as those are the only places X genes are used"]), 0,
  "When did the extra chromosome arrive: in the first cell, or later?",
  ["During meiosis, a chromosome pair can fail to separate: nondisjunction.",
   "That leaves an egg or sperm with an extra sex chromosome.",
   "That gamete joins another to make the first cell, which already has XXY.",
   "Every later cell is copied from that one by mitosis, so the extra X is in every cell with a nucleus."],
  "**In every cell with a nucleus, as it was in the egg or sperm that made the first cell.** "
  "Nondisjunction in meiosis puts the extra X into a gamete, and every body cell descends from the "
  "zygote that gamete made. X genes are used all over the body, not only in reproductive organs.",
  "Error in the gamete → in every cell.")

q(Q, 3, "Crossing a red camellia with a white one gives flowers with red patches and white patches. "
        "Which pattern of inheritance is this, and why?",
  uniq(["Codominance, since both colors show in full",
        "Incomplete dominance, since the colors mix",
        "Complete dominance, since red hides white",
        "Polygenic, since many genes add up color"]), 0,
  "Did the colors blend into a new color, or did each show up as it is?",
  ["The offspring show red AND white, each in full, in separate patches.",
   "Incomplete dominance would give a blend in between, such as pink.",
   "Complete dominance would give all-red flowers.",
   "Both alleles showing side by side is codominance."],
  "**Codominance, since both colors show in full.** Red and white patches mean both alleles are "
  "expressed, like roan cattle or blood type AB. A blend such as pink would be incomplete "
  "dominance, and all-red flowers would be complete dominance.",
  "Patches = codominance; a blend = incomplete dominance.")

r = mono('SS', 'ss')
assert r['dom'] == 100 and set(r['geno']) == {'Ss'}
q(Q, 3, "A true-breeding plant with smooth seeds is crossed with a true-breeding plant with ridged "
        "seeds, and every offspring has smooth seeds. Which conclusion follows?",
  uniq(["Smooth is dominant, and every offspring is heterozygous",
        "Ridged is dominant, and every offspring is heterozygous",
        "Smooth is dominant, and every offspring is homozygous",
        "The two alleles are codominant in these seeds"]), 0,
  "True-breeding means homozygous. What genotype must every offspring have?",
  ["True-breeding parents are homozygous: SS for smooth and ss for ridged.",
   "Every offspring gets S from one parent and s from the other: Ss.",
   "Every offspring is smooth even though it carries s.",
   "So smooth is dominant, and every offspring is heterozygous."],
  "**Smooth is dominant, and every offspring is heterozygous.** Each offspring has one allele from "
  "each true-breeding parent, so all are Ss, and since they all look smooth, smooth must be the "
  "allele that hides the other. Codominance would show both traits at once.",
  "One parent's trait in every offspring → that trait is dominant.")

# ------------------------------------------------------------ the guards

DECK = re.compile(r"widow|\bbears?\b|\bears?\b|floppy|pointed|hemophilia|webbed|\bRr\b|\(R\)|"
                  r"Iᴬi × Iᴮi|Iᴮi × Iᴬi|Xᴿ|Xʳ", re.I)
for x in Q:
    blob = x['q'] + ' ' + ' '.join(x['opts'])
    assert not DECK.search(blob), ('reuses a deck example', x['id'], blob)
    # a heterozygous female × dominant male X-linked cross is the deck's colorblind/hemophilia shape
    assert 'XᵂXʷ × XᵂY' not in x['q'], x['id']
    assert not re.search(r'\b(all|none|both) of the above\b', blob, re.I), x['id']

NOTE = (
    "Built from her Biology Unit 7 folder: the class's Genetics lecture deck. Two copies are in Drive "
    "and the second is a superset of the first, so the second was used. It was read through Drive's "
    "text version, so the slide pictures were not seen: if a slide carries a fact only in a picture "
    "(a Punnett square drawn out, a karyotype image), it is not in this unit.\n\n"
    "Four places are taught more carefully than the deck words them. FIRST, knowledge-check question 2 "
    "prints 'All of the above' as option D, and that is not correct: a dominant allele is not "
    "'better to have' and not necessarily 'more common' (polydactyly, extra fingers or toes, is "
    "dominant and rare). The unit teaches option C, that a dominant allele can hide the recessive "
    "trait, and says the other two are false. If her class's answer key gives D, that is worth a "
    "word with her teacher. SECOND, question 1's 'every time unless told not to' is a classroom convention, not "
    "biology; the unit frames it as the class's default: assume complete dominance unless a problem "
    "names another pattern. THIRD, the deck names incomplete dominance but never defines it, so a "
    "card adds it (red × white snapdragon gives pink) and contrasts it with codominance, where both "
    "show in full (type AB blood, roan cattle). The deck's dog-ears problem calls floppy and pointed "
    "codominant, but semi-floppy as an in-between reads more like incomplete dominance; that problem "
    "is kept off every quiz question. FOURTH, the deck asks how extra sex chromosomes get there and "
    "which cells they are in; a card adds the answer, nondisjunction during meiosis, so the extra "
    "chromosome is in every cell, and links it back to Unit 5-1.\n\n"
    "Other cards are our additions, tagged as study suggestions: the worked answers to the "
    "widow's-peak and bear prompts, the six blood genotypes and four blood types, two heterozygous "
    "parents, why males show X-linked recessive traits more often, and Y-linked traits. The four "
    "sex-chromosome conditions are given only as names and karyotypes.\n\n"
    "Every percentage and ratio is computed by crossing the alleles in the builder. Quiz questions "
    "use fresh crosses (peas, guinea pigs, cattle, snapdragons, fruit flies, fresh blood crosses); "
    "the deck's widow's peak, bears, Iᴬi × Iᴮi, colorblindness, dog-ears and hemophilia problems "
    "appear on cards or not at all.")

build('ad-astra', C, Q, 'unit-bio-u7',
      'Biology 8 · Unit 7-1: Genetics', 'bio',

      "Your class's Unit 7 deck on genetics: genes, alleles, genotype and phenotype, dominant and "
      "recessive, Mendel and his three laws, Punnett squares, codominance and blood type, polygenic "
      "traits, sex-linked traits, karyotypes and the sex-chromosome conditions.",

      "Genetics explains why you look like your family and yet not exactly like anyone in it. A "
      "Punnett square turns that into numbers: the chance that a child shows a trait, carries it, "
      "or does neither. It builds directly on DNA (Unit 6-1) and meiosis (Unit 5-1).",

      [("Use the vocabulary: gene, allele, genotype, phenotype, dominant, recessive, heterozygous, "
        "homozygous.", 'source'),
       ("State Mendel's laws of dominance, segregation and independent assortment.", 'source'),
       ("Use a Punnett square to find the percentage of offspring with each genotype and phenotype.",
        'source'),
       ("Work out blood-type and sex-linked crosses.", 'source'),
       ("Tell codominance from incomplete dominance, and explain why males show X-linked recessive "
        "traits more often.", 'added')],

      NOTE,

      ("Start with the vocabulary cards, then draw a Punnett square on paper for each cross question "
       "before you choose. Say each answer out loud before you flip.", 30),
      'content/bio-unit-7-genetics.json',
      'Unit 7 Genetics lecture deck (Biology 8 · Unit 7, Drive)',
      'source', offset_hours=3, libv_=1)

# build() stamps quarter 1; this unit is taught in quarter 2.
path = os.path.join(REPO, 'content/bio-unit-7-genetics.json')
d = json.load(io.open(path, encoding='utf-8'))
d['records']['unit-bio-u7']['quarter'] = 2
io.open(path, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
