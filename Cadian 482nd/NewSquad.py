#=============================================================================#
# PROGRAM: NewSquad.py
# AUTHOR: Justin Mansell (2018)
# DESCRIPTION: Generates a list of random guardsmen complete with personalities
# so you can make your opponent feel bad when he inevitably slaughters them.
#=============================================================================#
import names as nm #May have to install: sudo pip install names
import random as rd
import sys
import os
from RandomGuardsmen import *
from collections import OrderedDict

#Settings
Ng = int(sys.argv[1]) #Number of guardsmen in the squad (read from console)
try:
    squad_type = str(sys.argv[2])
except:
    squad_type = 'G'
rd.seed()

#Put the squad together
squad = []
for i in range(0,Ng):
    gi = Guardsman()
    gi = basics(gi)
    gi = demeanor(gi)
    gi = ambition(gi)
    gi.skill = []
    gi.flaw = []
    gi.friends = []
    gi.rivals = []
    gi = traits(gi)
    if squad_type == 'S' or rd.random() < 0.01:
        gi = gen_background(gi, 'high')
    else:
        gi = gen_background(gi, 'low')
    squad.append(gi)

#Conscript squad
if squad_type == 'C':
    for g in squad:
        g.rank = 'Cadet'

#Scions or veterans
if squad_type == 'S' or squad_type == 'V':
    for g in squad:
        g.rank = 'Corporal'
        g = traits(g) #Add extra skills/flaws
        if len(g.flaw) > 2: #Maximum of 2 flaws
            g.flaw = g.flaw[0:2]

#Generate friends/rivals
for gi in squad:
    Nfriends = rd.randint(0,2)
    Nrivals = rd.randint(0,2)
    if gi.personality in ['Quiet','Loner','Backwater','Psychotic']:
        Nfriends = rd.randint(0,1)
    if gi.personality in ['Spiteful','Sympathizer','Slacker','Thief',\
    'Narcissist','Strict','Leech','Never bathes','Incompetent','Braggart']:
        Nfriends = rd.randint(0,1)
        Nrivals = Nrivals + rd.randint(0,2)
    if gi.personality in ['Affable','Mentor','Heroic'] or 'Cook' in gi.skill:
        Nfriends = Nfriends + rd.randint(0,2)


    gi.friends = []
    gi.rivals = []
    j = 0
    while len(gi.friends) < Nfriends and j < 10:
        f = rd.choice(squad)
        if f.name in gi.friends or f.name == gi.name:
            j = j+1
            continue
        else:
            gi.friends.append(f.name)
    j = 0
    while len(gi.rivals) < Nrivals and j < 10:
        f = rd.choice(squad)
        if f.name in gi.friends or f.name in gi.rivals or f.name == gi.name:
            j = j+1
            continue
        else:
            gi.rivals.append(f.name)

#Appoint the sergeant
if squad_type in ['S','G','V']:
    serg = 0 #No sergeant yet
    for i in range(0,Ng):
        gi = squad[i]
        if gi.age > 18 and rd.random() < 0.2:
            # specialists = [
            # 'Weapon specialist',
            # 'Weapon specialist',
            # 'Medic',
            # 'Combat engineer',
            # 'Vox operator',
            # 'Standard bearer'
            # ]
            specialists = ['Corporal']
            gi.rank = rd.choice(specialists)
        if gi.age < 21 or len(gi.skill) < 1:
            continue
        if serg == 0:
            gi.rank = 'Sergeant'
            serg = 1

#Save the squad
for i in range(0,1000):
    if squad_type == 'S':
        prefix = 'Scions'
    else:
        prefix = 'squad'
    fname = prefix + str(rd.randint(1,999)) + '.txt'
    if not os.path.isfile(fname): break

f = open(fname,'w', newline='\n')
for i in range(0,Ng):
    gi = squad[i]
    f.write('Name: '+gi.name+'\n')
    f.write('Age: '+str(gi.age)+'\n')
    f.write('Rank: '+gi.rank+'\n')
    f.write('Battles: '+str(gi.battles)+'\n')
    f.write('Personality: '+gi.personality+'\n')
    f.write('Background: '+gi.background+'\n')
    f.write('Wants to: '+str(gi.ambition)+'\n')
    f.write('Skills: '+str(list(OrderedDict.fromkeys(gi.skill)))+'\n')
    f.write('Flaws: '+str(list(OrderedDict.fromkeys(gi.flaw)))+'\n')
    f.write('Liked by: '+str(gi.friends)+'\n')
    f.write('Disliked by: '+str(gi.rivals)+'\n')
    f.write('Confirmed kills: '+str(gi.confirmed_kills)+'\n')
    f.write('Awards: '+str(gi.awards)+'\n')
    f.write('Remarks: '+str(gi.remarks)+'\n')
    f.write('\n')
f.close()

#END
