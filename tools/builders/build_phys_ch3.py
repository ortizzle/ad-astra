# Kinematics 1 · Describing Motion — from the textbook chapter the teacher
# shared ("03_Kinematics.pdf", Glencoe Physics ch. 3, in her Drive folder).
# Deliberately the VOCABULARY chapter: the homework-derived units already
# cover motion graphs and the four equations, so this fills the gap they
# leave — what the words mean and why the definitions are built that way.
import json, io, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, _balance

C, Q = [], []

# ------------------------------------------------------------- 3.1 diagrams
card(C, 'Motion diagram',
     "**A series of images of a moving object taken at regular time intervals, showing where it was at each moment.**\n"
     "• Because the frames are evenly spaced in TIME, the spacing of the object tells you about speed.\n"
     "• Even spacing = constant speed. Spreading out = speeding up. Bunching together = slowing down.",
     "Same time between frames, so spacing IS speed.")
card(C, 'Particle model',
     "**Replacing an object by a single point, treating all of its mass as concentrated there.**\n"
     "• You track one point — the knot on a runner's belt — and ignore swinging arms and legs.\n"
     "• Two conditions before you may use it: the object must be much SMALLER than the distance it moves, and you must ignore its internal motions.",
     "Shrink the runner to a dot, but only if the dot travels much further than the runner is wide.")
card(C, 'Operational definition',
     "**A definition that describes a concept in terms of the process or operation used to find it.**\n"
     "• The textbook defines velocity and acceleration this way on purpose: not 'how fast it feels' but 'what you measure and divide'.\n"
     "• It is why every definition in this chapter is really a recipe.",
     "Defined by how you measure it, not by what it feels like.")

# ------------------------------------------------------------- 3.2 where/when
card(C, 'Coordinate system',
     "**What tells you where the zero point of the quantity you are studying is, and which direction counts as increasing.**\n"
     "• Deciding where to lay the measuring tape and when to start the stopwatch IS choosing a coordinate system.\n"
     "• You may define any coordinate system you like — some are just more convenient than others.",
     "Where zero is, and which way is up.")
card(C, 'Origin',
     "**The point at which the variables have the value zero.**\n"
     "• For a sprinter it could be the starting line — or anywhere else you choose.\n"
     "• Two people can pick different origins for the same race and both be right.",
     "Zero lives wherever you decide to put it.")
card(C, 'Position vector',
     "**An arrow drawn from the origin to the object, whose length is proportional to how far the object is from the origin.**\n"
     "• It points from the origin to where the object is at that particular moment.\n"
     "• Change the origin and every position vector changes with it.",
     "From zero, out to the thing.")
card(C, 'Negative positions and negative times are real',
     "**A negative position simply means a position on the other side of the origin; a negative time means before the clock was started.**\n"
     "• If the x-axis increases to the right, anything left of the origin has a negative position.\n"
     "• Both are perfectly acceptable — the minus sign is information about direction, not a mistake.",
     "A minus sign here means 'the other way', not 'wrong'.")
card(C, 'Scalar quantity',
     "**A quantity that tells you only the magnitude of something — a number with units, and nothing about direction.**\n"
     "• Time, temperature, mass and distance are all scalars.\n"
     "• Written with plain letters: m for mass, t for time, T for temperature.",
     "Just how much. No arrow.")
card(C, 'Vector quantity',
     "**A quantity that tells you the magnitude AND the direction.**\n"
     "• 'Kansas City is 192 miles northeast of Wichita' is a vector; '192 miles' on its own is a scalar.\n"
     "• Written with an arrow above the letter, or in bold in the textbook: v for velocity, a for acceleration.",
     "How much, and which way.")
card(C, 'Displacement',
     "**The distance AND direction between two positions — a vector, found by subtracting the earlier position from the later one.**\n"
     "• Drawn with its tail at the earlier position and its head at the later one.\n"
     "• It is a change in position, not a total of ground covered.",
     "Where you ended up, measured from where you began.",
     eq='Δd = d₁ − d₀')
card(C, 'Distance',
     "**The length, or size, of the displacement vector — and therefore a scalar.**\n"
     "• If a sprinter's displacement is 50 m down the track, the distance between those two positions is 50 m.\n"
     "• Distance has no direction attached, which is exactly what makes it a scalar.",
     "Distance is displacement with the direction stripped off.")
card(C, 'Why displacement beats position',
     "**Move the origin and every position changes — but the displacement between two points does not.**\n"
     "• That is why physics problems are built around displacement rather than raw position.\n"
     "• Two students who chose different origins will disagree about d₀ and d₁ and still agree about Δd.",
     "The one thing everybody agrees on, whatever they called zero.")
card(C, 'Time interval',
     "**The change in clock reading between two moments — the later time minus the earlier one.**\n"
     "• The Greek letter delta, Δ, always means 'a change in'.\n"
     "• Time interval is a scalar: it has a size but no direction.",
     "Δ means change. Always later minus earlier.",
     eq='Δt = t₁ − t₀')

# ------------------------------------------------------------- 3.3 v and a
card(C, 'Average velocity',
     "**The displacement divided by the time interval over which it happened — a vector, pointing the same way as the displacement.**\n"
     "• It gets bigger when the displacement gets bigger, and bigger when the time gets smaller, which is exactly what 'faster' should mean.\n"
     "• In this course the usual unit is metres per second, m/s.",
     "Change in position, per second.",
     eq='v = Δd/Δt = (d₁ − d₀)/(t₁ − t₀)')
card(C, 'Average speed',
     "**The ratio of the TOTAL DISTANCE travelled to the time interval — a scalar.**\n"
     "• Not the same thing as average velocity: velocity uses displacement, speed uses total ground covered.\n"
     "• Run a full lap of a track and you have a large average speed and a displacement of zero.",
     "Speed counts every metre you covered; velocity only counts the net move.")
card(C, 'Instantaneous velocity',
     "**The speed and direction of an object at one particular moment, rather than averaged over an interval.**\n"
     "• A motion diagram can only give you an AVERAGE — inside the interval the object might have sped up, slowed down or turned round.\n"
     "• When the textbook says just 'velocity', it means the instantaneous one, written v.",
     "What the speedometer reads right now.")
card(C, 'Average acceleration',
     "**The change in velocity divided by the time interval in which it happened.**\n"
     "• Velocity is measured in m/s, so acceleration is m/s per second — abbreviated m/s².\n"
     "• An object accelerates whenever the magnitude OR the direction of its velocity changes.",
     "Change in velocity, per second.",
     eq='a = Δv/Δt = (v₁ − v₀)/(t₁ − t₀)')
card(C, 'What the sign of acceleration means',
     "**Speeding up: acceleration points the SAME way as velocity. Slowing down: acceleration points the OPPOSITE way. Constant velocity: acceleration is zero.**\n"
     "• With the origin on the left and motion to the right, a car speeding up has positive acceleration and a car braking has negative acceleration.\n"
     "• So a negative acceleration does not mean 'moving backwards' — it means 'velocity is being reduced'.",
     "Compare the two arrows. Same way = speeding up.")
card(C, 'The coordinate system decides the signs',
     "**Choose the origin at one end and the velocity is positive; choose it at the other and the very same motion has negative velocity.**\n"
     "• Both choices are equally correct, as long as you stay consistent.\n"
     "• What never changes is the displacement and the physics — only the labels move.",
     "The minus signs belong to your choice of axes, not to the motion.")

# ------------------------------------------------------------- ponder
card(C, 'Ponder: when does the particle model break?',
     "**The rule is that the object must be much smaller than the distance it travels.**\n"
     "• A car crossing a city, fine. A car rolling forward 30 cm in a car park — is it still fine?\n"
     "• Where would you draw the line, and what would go wrong if you crossed it?",
     "No wrong answers. Try to name what the model would start hiding.",
     frm='added')

# ------------------------------------------------------------- questions
q(Q, 1, "A motion diagram shows an object's position in frames taken at equal time intervals. The dots get further and further apart. What is the object doing?",
  ["Speeding up", "Slowing down", "Moving at a constant speed", "Standing still"],
  0,
  "The time between frames never changes.",
  ["Every frame is separated by the same amount of time.",
   "So the gap between two dots shows how far the object moved in that fixed time.",
   "Gaps that grow mean it covered more ground in each successive interval.",
   "Covering more ground per unit time is exactly what speeding up means."],
  "**Speeding up.** Because the frames are evenly spaced in time, the spacing of the dots is a direct picture of speed — that is the whole reason a motion diagram is useful.",
  "Even spacing is constant speed; bunching up is slowing down.")

q(Q, 2, "A physics class treats a sprinter as a single point at the knot on her belt. What must be true for this particle model to be allowed?",
  ["She must be much smaller than the distance she runs",
   "She must be running at a constant speed throughout",
   "She must be moving in a straight line only",
   "Her arms and legs must actually be still"],
  0,
  "Two conditions attach to the model; one is about size.",
  ["The particle model replaces an object with one point holding all its mass.",
   "The textbook attaches two conditions to using it.",
   "First, the size of the object must be much less than the distance it moves.",
   "Second, you must IGNORE internal motions like swinging arms — not require that they stop."],
  "**She must be much smaller than the distance she runs.** The arms keep swinging; the model just chooses to disregard them. The size condition is the one that can actually fail.",
  "Model a runner crossing a track, yes. Model her taking half a step, and the point stops standing for the whole runner.")

q(Q, 2, "Which of these is a vector quantity?",
  ["A displacement of 50 m down the track",
   "A mass of 125.00 g measured on a balance",
   "A time interval of 15 s on a stopwatch",
   "A temperature of 25 °C on a thermometer"],
  0,
  "One of them cannot be stated without saying which way.",
  ["A scalar gives you only a magnitude — a number with units.",
   "Mass, time and temperature are each fully described by a number and a unit.",
   "Displacement is not: it is the distance AND the direction between two positions.",
   "Needing a direction to be complete is what makes a quantity a vector."],
  "**The displacement.** Vectors carry a direction as well as a size — which is why the book writes them in bold, or with a little arrow on top.",
  "Distance is the sneaky one: '50 m' alone is a scalar, even though it is the length of a vector.")

q(Q, 3, "Two students draw position vectors for the same object at the same instant and get vectors pointing different ways. What went wrong?",
  ["Nothing — they chose different origins, and both are correct",
   "One of them measured the distance incorrectly",
   "One of them drew the vector from the object to the origin",
   "Position vectors cannot point in different directions"],
  0,
  "A position vector is drawn from something you get to choose.",
  ["A position vector runs from the ORIGIN to the object.",
   "You may put the origin wherever you like — it is a choice, not a fact about the world.",
   "Put the origin on the far side of the object and the arrow points the other way.",
   "So two different origins give two different position vectors for the same object at the same moment."],
  "**Nothing went wrong.** This is the chapter's real lesson: position depends on your coordinate system. It is exactly why physics leans on displacement, which does not.",
  "Ask them for the DISPLACEMENT between two moments instead, and they will agree.")

q(Q, 3, "A runner does one complete lap of a 400-m track in 80 s, finishing where she started. What are her average speed and her average velocity?",
  ["Average speed 5 m/s; average velocity zero",
   "Average speed zero; average velocity 5 m/s",
   "Both are 5 m/s",
   "Both are zero"],
  0,
  "The two definitions use different quantities on top.",
  ["Average speed is total DISTANCE travelled divided by time: 400 m ÷ 80 s = 5 m/s.",
   "Average velocity is DISPLACEMENT divided by time.",
   "She finished where she started, so her displacement is zero.",
   "Zero divided by 80 s is zero, so her average velocity is zero."],
  "**5 m/s and zero.** This is the cleanest demonstration that speed and velocity are genuinely different quantities rather than two words for one idea.",
  "Any closed loop does this: real effort, real distance, zero displacement.")

q(Q, 2, "Why does the textbook build physics problems around displacement rather than position?",
  ["Displacement is the same whichever origin you choose",
   "Displacement is a scalar and so is easier to work with",
   "Position cannot be measured accurately in a laboratory",
   "Displacement is always positive, so signs never cause trouble"],
  0,
  "Think about what changes when you move the measuring tape.",
  ["Move the origin and every position value changes.",
   "But displacement is the difference between two positions.",
   "Shifting the origin shifts both positions by the same amount, so the difference is unaffected.",
   "That makes displacement something everyone agrees on, whatever coordinate system they picked."],
  "**It does not depend on where you put the origin.** Displacement is a vector and it can certainly be negative — its virtue is that it survives a change of coordinate system unchanged.",
  "Distance — the length of that vector — is the scalar in this family.")

q(Q, 2, "A car moving in the positive direction is braking. What are the signs of its velocity and its acceleration?",
  ["Velocity positive, acceleration negative",
   "Velocity negative, acceleration negative",
   "Velocity positive, acceleration positive",
   "Velocity negative, acceleration positive"],
  0,
  "Acceleration's sign compares its direction with the velocity's.",
  ["The car is moving in the positive direction, so its velocity is positive.",
   "Braking means the velocity is being reduced.",
   "When an object slows down, the acceleration vector points OPPOSITE to the velocity.",
   "Velocity positive and acceleration opposite to it means the acceleration is negative."],
  "**Positive velocity, negative acceleration.** A negative acceleration does not mean the car is reversing — it means the velocity is shrinking. Direction of travel and direction of acceleration are two separate questions.",
  "Same motion, origin moved to the other end: now velocity is negative and acceleration positive. The braking hasn't changed.")

q(Q, 1, "What does the symbol Δ mean in Δt and Δd?",
  ["A change in the quantity",
   "The average value of the quantity",
   "The total of the quantity",
   "The direction of the quantity"],
  0,
  "It is a Greek letter with one fixed job.",
  ["Δ is the Greek capital letter delta.",
   "In this book it always signals a change in whatever follows it.",
   "So Δt is the time interval, t₁ − t₀.",
   "And Δd is the displacement, d₁ − d₀."],
  "**A change in the quantity.** Always the later value minus the earlier one — get that order backwards and every sign in the problem flips.",
  "The subscript 0 goes with the starting value; subscript 1 with the later one.")

q(Q, 2, "Why can a motion diagram give you only an AVERAGE velocity, never an instantaneous one?",
  ["It shows positions at the ends of an interval, not what happened inside it",
   "The camera cannot record fast enough to see one instant",
   "Average velocity is a vector and instantaneous velocity is a scalar",
   "The frames are not separated by equal amounts of time"],
  0,
  "Think about what the diagram leaves out.",
  ["A motion diagram gives the object's position at the start and end of each time interval.",
   "Between two frames, anything could have happened.",
   "The object might have sped up, slowed down, stopped or reversed and come back.",
   "So all you can honestly calculate is the total displacement divided by the total time — an average."],
  "**It says nothing about what happened between the frames.** Instantaneous velocity is the value at one particular moment, and that is more than a sequence of snapshots can tell you.",
  "When the textbook says plain 'velocity' from here on, it means the instantaneous one.")

q(Q, 1, "The textbook defines velocity and acceleration operationally. What does that mean?",
  ["They are defined by the process used to measure them",
   "They are defined only for objects that are actually operating",
   "They are defined by a formula that cannot be derived",
   "They are defined differently in each chapter of the book"],
  0,
  "The word comes from 'operation' in the sense of a procedure.",
  ["An operational definition describes a concept in terms of the process used to find it.",
   "Velocity is not defined as 'how fast something feels'.",
   "It is defined as a specific measurement: displacement divided by time interval.",
   "Follow the procedure and you get the quantity — that is what makes the definition operational."],
  "**By the process used to measure them.** It is why every definition in this chapter reads like a recipe: measure this, measure that, divide. It keeps physics arguments about numbers rather than about words.",
  "It also means two people following the same procedure must get the same answer.")

q(Q, 2, "An object's velocity is described as changing. Which of these counts as a change in velocity?",
  ["Turning a corner at a steady 20 km/h",
   "Sitting parked with the engine running",
   "Driving straight down a motorway at a steady 100 km/h",
   "Being pushed but not moving because the brake is on"],
  0,
  "Velocity has two parts, and either one changing is enough.",
  ["Velocity is a vector: it has a magnitude and a direction.",
   "An object accelerates when EITHER the magnitude or the direction of its velocity changes.",
   "Driving straight at a steady speed changes neither, and the parked cases have no velocity at all.",
   "Turning a corner changes the direction, even though the speed stays at 20 km/h."],
  "**Turning a corner.** This catches almost everyone, because in ordinary speech 'accelerating' means going faster. In physics, changing direction is accelerating too.",
  "It is the reason anything moving in a circle is accelerating, even at a perfectly steady speed.")

q(Q, 2, "A sprinter has just crossed the finish line and is slowing down, still moving forwards. Taking the starting block as the origin and forwards as positive, describe her average velocity and average acceleration.",
  ["Velocity still positive, acceleration now negative",
   "Both velocity and acceleration are now negative",
   "Velocity now negative, acceleration still positive",
   "Both are zero, because the race has finished"],
  0,
  "She has not started moving backwards.",
  ["Forwards is positive and she is still moving forwards, so velocity is positive.",
   "It is decreasing, but a decreasing positive number is still positive.",
   "Slowing down means the acceleration opposes the velocity.",
   "So the acceleration is negative while the velocity is still positive."],
  "**Positive velocity, negative acceleration.** During the race both were positive; after the line the velocity keeps its sign and the acceleration flips. Only one of the two changed.",
  "She is only moving backwards once the velocity itself turns negative — which never happens here.")

q(Q, 3, "Kinematics 1 · Describing Motion. Put these steps of setting up a motion problem in the order the textbook uses.",
  ["Choose a coordinate system and mark the origin",
   "Draw the position vectors to the object at each time",
   "Subtract to get the displacement between those positions",
   "Divide the displacement by the time interval to get average velocity"],
  0,
  "Nothing can be measured until zero has been chosen.",
  ["First you must decide where zero is and which direction is positive — the coordinate system.",
   "Only then can you draw a position vector from that origin to the object.",
   "Two position vectors give a displacement when you subtract the earlier from the later.",
   "And displacement over time interval is the definition of average velocity."],
  "**Coordinate system, positions, displacement, velocity.** Each step needs the one before it, which is why choosing the coordinate system is not a formality — nothing has a value until it is done.",
  "It also explains why two people can get different-looking answers and both be right.",
  kind='order')

q(Q, 2, "Which statement about scalars and vectors is NOT true?",
  ["Distance is a vector, since it comes from a displacement vector",
   "A time interval has size but no direction, so it is a scalar",
   "Displacement carries a direction, so it is a vector",
   "Average acceleration carries a direction, so it is a vector"],
  0,
  "Three of these match the textbook exactly. One promotes a scalar.",
  ["Displacement carries a direction, so it is a vector.",
   "Average acceleration carries a direction too, so it is also a vector.",
   "A time interval has a size but no direction, making it a scalar.",
   "Distance is the LENGTH of the displacement vector — a magnitude with no direction, so it is a scalar."],
  "**Distance is not a vector.** It is the size of a vector, which is a different thing: taking the length of an arrow throws the direction away.",
  "With a NOT-true question, check each option against the definition rather than picking the one that sounds odd.")

q(Q, 1, "In the symbols d₀ and t₀, what does the subscript zero mean?",
  ["The initial value, at the moment the clock starts",
   "A value that has been measured to be zero",
   "The value at the origin of the coordinate system",
   "The average value over the whole interval"],
  0,
  "It marks a moment in time, not a place.",
  ["Subscripts are used to say WHICH moment a quantity belongs to.",
   "Subscript 0 marks the earlier of the two: the initial value.",
   "Subscript 1 marks the later one.",
   "So d₀ is where the object started and t₀ is when the timing began — neither is necessarily zero itself."],
  "**The initial value.** d₀ is not required to be zero; it is simply the position at the start. Choosing an origin so that d₀ happens to equal zero is convenient, not compulsory.",
  "The equations of motion on your formula sheet are full of these — v₀ is the starting velocity.")

_balance(Q)

unit = {
    'id': 'unit-phys-ch3', 'type': 'unit',
    'updatedAt': int(time.time() * 1000) - 4 * 3600 * 1000,
    'classId': 'physics', 'quarter': 1, 'status': 'draft',
    'title': 'Kinematics 1 · Describing Motion',
    'srcName': 'Physics textbook, chapter 3: Describing Motion (Drive)',
    'source': 'The textbook chapter shared by her physics teacher — sections 3.1 Picturing Motion, 3.2 Where and When?, 3.3 Velocity and Acceleration',
    'summary': {'text':
        "Chapter 3 of the physics textbook — the vocabulary the rest of kinematics is built on. Motion "
        "diagrams and the particle model; coordinate systems, origins and position vectors; the "
        "difference between a scalar and a vector; displacement, distance and the time interval; and "
        "then the operational definitions of average velocity, average speed, instantaneous velocity "
        "and average acceleration, including what the sign of an acceleration actually tells you.",
        'from': 'source'},
    'why': {'text':
        "Your other physics units drill the graphs and the four equations. This one is the layer "
        "underneath them: what the words in those equations mean, and why they are defined the way "
        "they are. It is also where most marks quietly go missing — distance mistaken for "
        "displacement, average speed mistaken for average velocity, and a negative acceleration read "
        "as 'going backwards' when it only means 'slowing down'.",
        'from': 'added'},
    'objectives': [
        {'text': "Draw and read a motion diagram, and say when the particle model may be used.", 'from': 'source'},
        {'text': "Choose a coordinate system, and recognise how that choice affects the signs of vector quantities.", 'from': 'source'},
        {'text': "Differentiate between scalar and vector quantities.", 'from': 'source'},
        {'text': "Define a displacement vector and determine a time interval.", 'from': 'source'},
        {'text': "Define velocity and acceleration operationally, and relate their directions to the motion.", 'from': 'source'},
        {'text': "Tell average speed and average velocity apart, and say when they disagree.", 'from': 'added'},
    ],
    'parentNote': {'text':
        "Built from the textbook chapter her physics teacher shared (\"03_Kinematics.pdf\"), which is the "
        "definitions chapter — motion diagrams, coordinate systems, scalars and vectors, displacement, "
        "and the definitions of velocity and acceleration. It is deliberately NOT another unit on graphs "
        "or on the four equations: her existing units already cover both, and duplicating them would "
        "just re-ask questions she has already met. What this fills in is the vocabulary underneath "
        "them. Three ideas here are the ones that reliably cost marks and are each targeted directly: "
        "distance is a scalar and displacement is a vector (a full lap of a track has a large distance "
        "and zero displacement); average speed uses total distance while average velocity uses "
        "displacement, so they can differ wildly; and a negative acceleration means the velocity is "
        "being reduced, NOT that the object is travelling backwards. The chapter also makes a point "
        "worth reinforcing out loud — that choosing where to put the origin is a free choice, and two "
        "people who choose differently will get different signs and both be right.",
        'from': 'added'},
    'nextUp': {'text': "Cards first — this one is mostly definitions, so say each meaning out loud before flipping. Then a couple of quiz rounds.",
               'minutes': 20, 'from': 'added'},
    'cards': C, 'questions': Q,
}

path = '/home/user/ad-astra/content/phys-ch3-describing-motion.json'
io.open(path, 'w', encoding='utf-8').write(
    json.dumps({'v': 4, 'records': {'unit-phys-ch3': unit}}, ensure_ascii=False, indent=1))
lv = {1: 0, 2: 0, 3: 0}
for x in Q: lv[x['lv']] += 1
print('phys-ch3-describing-motion.json  %2d cards · %2d questions  %s' % (len(C), len(Q), lv))
