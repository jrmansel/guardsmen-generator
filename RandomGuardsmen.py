import random as rd
import names as nm
import datetime

#Internal parameters
m2f = 0.5 #Fraction of men in regiment

#Guardsmen object
class Guardsman:
    sex = None
    name = None
    age = None
    rank = None
    squad = None
    personality = None
    background = None
    skill = []
    flaw = []
    ambition = None
    friends = []
    rivals = []
    confirmed_kills = 0
    awards = []
    battles = 0
    remarks = []

#Generate basics
def basics(g):
    g.sex = 'male' if rd.random() < m2f else 'female'
    g.name = nm.get_full_name(gender = g.sex)
    g.age = rd.randint(18,28)
    g.rank = 'Guardsman'
    g.remarks = ['Deployed '+str(datetime.date.today())]
    return g

#Generate demeanor
def demeanor(g):
    demeanors = [
    'Affable',
    'Backwater',
    'Heroic',
    'Spiteful',
    'Boisterous',
    'Braggart',
    'Condescending',
    'Cocky',
    'Pragmatic',
    'Dissenter',
    'Dreamer',
    'Gambler',
    'Naive',
    'Incompetent',
    'Jaded',
    'Joker',
    'Loner',
    'Loose cannon',
    'Loyal',
    'Mentor',
    'Leech',
    'Never bathes',
    'Nihilist',
    'Numb',
    'Awkward',
    'Obsessive',
    'Old',
    'Optimist',
    'Pessimist',
    'Pious',
    'Psychotic',
    'Quiet',
    'Reckless',
    'Sarcastic',
    'Sensible',
    'Slacker',
    'Smooth',
    'Steely',
    'Strict',
    'Superstitious',
    'Talkative',
    'Thief',
    'Edgy',
    'Narcissist',
    'Old',
    'Naive',
    'Drunkard'
    ]
    g.personality = rd.choice(demeanors)

    if g.personality == 'Old':
        g.age = rd.randint(29,65)
        g.personality = rd.choice(demeanors)
    elif g.personality == 'Naive':
        g.age = rd.randint(16,18)
        g.personality = rd.choice([rd.choice(demeanors), 'Naive'])
        g.rank = 'Cadet'

    return g

#Generate background
def gen_background(g, caste = 'low'):

    #These shouldn't be homeworld's per-se, but roles in society
    #that would exist on any world
    low_born_backgrounds = [
    'Ganger',
    'Scavenger',
    'Hiver',
    'Voidborn',
    'Administratum menial',
    'Outcast',
    'Forge worker',
    'Agri worker',
    'Planetary defence',
    'Slave'
    ]

    high_born_backgrounds = [
    'Child of the creed',
    'Savant',
    'Vaunted wealth',
    'Disgraced',
    'Merchant house',
    'Dilettante',
    'Arbiter',
    'Militarum',
    'Bastard child'
    ]

    if caste == 'low':
        bg = rd.choice(low_born_backgrounds)
    else:
        bg = rd.choice(high_born_backgrounds)
    g.background = bg

    #Token skills, flaws, and personalities
    token_skill_chance = 0.25
    token_flaw_chance = 0.25
    token_personality_chance = 0.25

    if bg == 'Ganger':
        token_skills = ['Street fighter','Lightning reflexes','Quick draw']
        token_flaws = ['Old wound','Addict','Poor discipline']
        token_personality = ['Thief','Dissenter','Gambler','Loyal']
    elif bg == 'Scavenger':
        token_skills = ['Survivalist','Handyman','Tough as nails']
        token_flaws = ['Tainted','Poor health','Illiterate']
        token_personality = ['Loner','Spiteful','Backwater']
    elif bg == 'Hiver':
        token_skills = ['Unremarkable','Technical knock','Cautious']
        token_flaws = ['Hive bound','Weak','Ignorant']
        token_personality = ['Dreamer','Affable','Talkative','Joker','Sarcastic']
    elif bg == 'Voidborn':
        token_skills = ['Lucky','Strong willed','Technical knock']
        token_flaws = ['Fragile','Tainted','Ship bound','Mistrusted']
        token_personality = ['Superstitious','Awkward','Steely']
    # elif bg == 'Ministorum servant':
    #     token_skills = ['Zealous','Unshakeable faith','Brave']
    #     token_flaws = ['Ignorant','Oblivious','Short temper']
    #     token_personality = ['Pious','Strict','Loose cannon']
    elif bg == 'Administratum menial':
        token_skills = ['Bookworm','Patient','Foresight']
        token_flaws = ['Bad eyesight','Bad back','Slow','Ugly']
        token_personality = ['Strict','Quiet','Awkward']
    elif bg == 'Outcast':
        token_skills = ['Silent move','Hardy','Survivalist','Quick draw']
        token_flaws = ['Tainted','Old wound','Mistrusted','Deranged']
        token_personality = ['Loner','Edgy','Psychotic','Jaded','Thief']
    elif bg == 'Forge worker':
        token_skills = ['Technical knock','Bionic arm','Bionic eye','Bionic leg','Tinkerer','Tireless']
        token_flaws = ['Hive bound','Ignorant','Flat footed']
        token_personality = ['Obsessive','Steely','Awkward']
    elif bg == 'Agri worker':
        token_skills = ['Tireless','Good sense of direction','Trustworthy']
        token_flaws = ['Oblivious','Ignorant','Illiterate']
        token_personality = ['Naive','Dreamer','Sensible']
    elif bg == 'Planetary defence':
        token_skills = ['Rapid reload','Crack shot','Combat master','Nerves of steel']
        token_flaws = ['Poor initiative','Flashbacks']
        token_personality = ['Loyal','Mentor','Strict','Cocky']
        if g.rank is not 'Cadet' and rd.random() < 0.5:
            g.rank = 'Corporal'
    # elif bg == 'Enforcer':
    #     token_skills = ['Observant','Unarmed warrior']
    #     token_flaws = ['']
    #     token_personality = ['Steely','Strict','']
    elif bg == 'Slave':
        token_skills = ['Unremarkable','Tireless','Hardy']
        token_flaws = ['Illiterate','Unlucky','Mistrusted']
        token_personality = ['Dreamer','Thief','Spiteful']

    #Highborn backgrounds
    elif bg == 'Child of the creed':
        token_skills = ['Zealous','Unshakeable faith','Brave']
        token_flaws = ['Ignorant','Oblivious','Short temper']
        token_personality = ['Pious','Strict','Loose cannon']
    elif bg == 'Savant':
        token_skills = ['Bookworm','Foresight','Lateral thinker']
        token_flaws = ['Hesistant','Pacifist','Absent minded','Gullible']
        token_personality = ['Sensible','Curious','Quiet','Awkward']
    elif bg == 'Vaunted wealth':
        token_skills = ['Duelist','Good looking','Unshakeable pride']
        token_flaws = ['Coward','Addict','Tainted','Fragile','Weak','Gluttonous']
        token_personality = ['Slacker','Condescending','Narcissist','Smooth','Naive','Incompetent']
    elif bg == 'Disgraced':
        token_skills = ['Cautious','Die hard','Lightning reflexes']
        token_flaws = ['Unlucky','Flashbacks','Unbearable guilt']
        token_personality = ['Spiteful','Loner','Jaded']
    elif bg == 'Merchant house':
        token_skills = ['Sound judgement','Foresight','Cautious']
        token_flaws = ['Pacifist','Dishonest','Gluttonous']
        token_personality = ['Affable','Gambler','Optimist']
    elif bg == 'Dilettante':
        token_skills = ['Musician','Lateral thinker','Observant']
        token_flaws = ['Poor discipline','Careless','Clumsy','Smart-ass']
        token_personality = ['Smooth','Cocky','Naive','Slacker','Dissenter','Reckless']
    elif bg == 'Arbiter':
        token_skills = ['Observant','Sound judgement','Trustworthy']
        token_flaws = ['Poor initiative','Slow','Cruel']
        token_personality = ['Strict','Sensible','Steely']
    elif bg == 'Militarum':
        token_skills = ['Zealous','Tactical genius','Born leader','Unshakeable pride']
        token_flaws = ['Overconfident','Short temper','Self-righteous']
        token_personality = ['Loyal','Strict','Heroic','Mentor']
    elif bg == 'Bastard child':
        token_skills = ['Lucky','Brave','Unremarkable','Good looking']
        token_flaws = ['Mistrusted','Unlucky','Oblivious','Ignorant']
        token_personality = ['Backwater','Loyal','Loose cannon','Mentor','Loner','Dreamer']

    if rd.random() < token_skill_chance:
        g.skill.append(rd.choice(token_skills))
    if rd.random() < token_flaw_chance:
        g.flaw.append(rd.choice(token_flaws))
    if rd.random() < token_personality_chance:
        g.personality = rd.choice(token_personality)
    return g

#Generate ambition
def ambition(g):
    ambitions = [
    'marry a distant paramour',
    'start a business',
    'get promoted',
    'travel the galaxy',
    'earn the respect of their comrades',
    'earn the respect of their superiors',
    'make a difference',
    'bring honor to their family',
    'make it home',
    'start a family',
    'become rich',
    'become famous',
    'acquire knowledge',
    'meet someone famous',
    'learn to fly',
    'redeem themselves',
    'transfer to a different regiment',
    'protect a friend',
    'get laid',
    'write a book',
    'own their own house',
    'set a record',
    'serve up a cold plate of vengeance',
    'kill heretics',
    'kill xenos',
    'impress the commissar',
    'sleep in',
    'set foot on Terra',
    'eat like a king',
    'be remembered',
    'die for the Emperor',
    'get back to the good old days',
    'desert at the first opportunity'
    ]

    if rd.random() < 0.1:
        g.ambition = 'survive'
    else:
        g.ambition = rd.choice(ambitions)

    return g

#Generate flaws and boons
def traits(g):
    nflaws = rd.randint(0,2)
    nskills = rd.randint(0,2)
    if g.personality == 'Incompetent':
        nflaws = nflaws + 1
    elif g.personality == 'Heroic':
        nskills = nskills + 1

    skills = [
    'Nerves of steel',
    'Tinkerer',
    'Lucky',
    'Cook',
    'Crack shot',
    'Combat master',
    'Street fighter',
    'Lateral thinker',
    'Lightning reflexes',
    'Rapid reload',
    'Bulging biceps',
    'Heightened senses',
    'Tough as nails',
    'Unshakeable faith',
    'Foresight',
    'Ambidextrous',
    'Duelist',
    'Tireless',
    'Bookworm',
    'Observant',
    'Handyman',
    'Bionic arm',
    'Bionic leg',
    'Bionic eye',
    'Quick draw',
    'Hardy',
    'Born leader',
    'Unarmed warrior',
    'Unremarkable',
    'Silent move',
    'Good sense of direction',
    'Sound judgement',
    'Survivalist',
    'Athlete',
    'Good looking',
    'Unshakeable pride',
    'Patient',
    'Musician',
    'Awesome scar',
    'Trustworthy',
    'Hard target',
    'Die hard',
    'Cautious',
    'Zealous',
    'Mustache',
    'Beard',
    'Bald',
    'Brave'
    ]

    flaws = [
    'Clumsy',
    'Unlucky',
    'Fragile',
    'Hesitant',
    'Careless',
    'Pacifist',
    'Death-wish',
    'Coward',
    'Paranoid',
    'Addict',
    'Slow',
    'Gullible',
    'Oblivious',
    'Poor discipline',
    'Bad back',
    'Allergies',
    'Ugly',
    'Poor health',
    'Weak',
    'Overweight',
    'Unbearable guilt',
    'Tainted',
    'Poor aim',
    'Insomniac',
    'Old wound',
    'Bad eyesight',
    'Dyslexic',
    'Short temper',
    'Asthma',
    'Absent minded',
    'Flat footed',
    'Cruel',
    'Dishonest',
    'Ignorant',
    'Twitchy',
    'Impulsive',
    ]

    for s in range(0,nskills):
        g.skill.append(rd.choice(skills))

    for s in range(0,nflaws):
        g.flaw.append(rd.choice(flaws))

    return g
