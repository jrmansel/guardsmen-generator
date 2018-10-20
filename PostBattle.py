#=============================================================================#
# PROGRAM: PostBattle.py
# AUTHOR: Justin Mansell (2018)
# DESCRIPTION: processes changes to a guardsmen squad following a battle
#=============================================================================#
from RandomGuardsmen import *
from shutil import copyfile
import random as rd
import ast
import datetime
import sys
from collections import OrderedDict

#Read squad file
squadname = str(sys.argv[1])
Ndeaddead =  int(sys.argv[2]) #Number who are definitely dead
Ncasualties = int(sys.argv[3]) #Number of casualties
Nmorale = int(sys.argv[4]) #Number of losses to Morale
VP = int(sys.argv[5]) #Number of victory points earned by the squad

#Copy the squad file in case it gets screwed up
copyfile(squadname+'.txt',squadname+'_old.txt')

new_skills = ['Brave',
'Nerves of steel',
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
'Tactical genius',
'Foresight',
'Ambidextrous',
'Observant',
'Handyman',
'Hardy',
'Good sense of direction',
'Sound judgement',
'Survivalist',
'Athlete',
'Tireless',
'Duelist',
'Silent move',
'Unshakeable pride',
'Patient',
'Trustworthy',
'Hard target',
'Die hard',
'Cautious',
'Beard',
'Mustache'
]

new_flaws = [
'Hesitant',
'Coward',
'Paranoid',
'Shell-shock',
'Unbearable guilt',
'Nightmares',
'Death-wish',
'Flashbacks',
]

ranks = [
'Cadet',
'Guardsman',
'Corporal',
'Lance Corporal',
'Sergeant',
'Lance Sergeant'
]

legacy = [
'Anonymous sacrifice',
'Inscription on a nearby ruin',
'Rifle with helmet and tags hung on it',
'Fond memories in the minds of his friends',
"Inscription on a comrade's weapon",
'Cross with oath tag draped over it',
'Vengeful relative',
'A tombstone amongst thousands',
'Inscription on an overgrown memorial plaque',
'A cautionary tale',
'Inscription on a vehicle',
'Equipment becomes a family heirloom',
'Service in death as a servo skull',
'Official commendation in the dispatches',
'Inscription on the regimental standard',
'Statue bust',
'Local deity'
]

def load_squad(fname, newline = '\n'):
    f = open(fname+'.txt','r')
    squad = []
    stats = {}
    for line in f:
        if  line.strip():
            stats[line.split(': ')[0]] = line.split(': ')[1].split('\n')[0]
        else:
            g = Guardsman()
            g.name = stats['Name']
            g.age = int(stats['Age'])
            g.rank = stats['Rank']
            g.personality = stats['Personality']
            g.skill = ast.literal_eval(stats['Skills'])
            g.flaw = ast.literal_eval(stats['Flaws'])
            g.ambition = stats['Wants to']
            g.friends = ast.literal_eval(stats['Liked by'])
            g.rivals = ast.literal_eval(stats['Disliked by'])
            g.battles = int(stats['Battles'])
            if 'Confirmed kills' in stats.keys():
                g.confirmed_kills = ast.literal_eval(stats['Confirmed kills'])
            else: g.confirmed_kills = 0
            if 'Background' in stats.keys():
                g.background = stats['Background']
            else: g.background = None
            if 'Awards' in stats.keys():
                g.awards = ast.literal_eval(stats['Awards'])
            else: g.awards = []
            if 'Remarks' in stats.keys():
                g.remarks = ast.literal_eval(stats['Remarks'])
            else: g.remarks = []
            squad.append(g)
            stats = {}

    if len(squad) < Ndeaddead + Ncasualties + Nmorale:
        print('Error: casualties and morale losses exceed squad size')
        quit()
    return squad

def battle(squad,casualties,morale_losses,deadly_casualties):
#Allocates casualties from the battle
#squad = the list of guardsmen objects in the squad
#casualties = no. guardsmen removed as casualties that may or may not be dead
#morale_losses = no. guardsmen removed due to morale
#deadly_casualties = no. guardsmen who are definitely dead

    print('------------------BATTLE RESULTS----------------------')
    rd.shuffle(squad)


    #First off...everyone increases the number of battles by 1
    for g in squad: g.battles += 1

    #Allocate deadly casualties
    dead = []
    for i in range(0,1000):
        if len(dead) >= deadly_casualties: break
        g = rd.choice(squad)
        #No, not me! Make a saving throw
        savethr = min([(len(g.skill) - len(g.flaw) + g.battles)/10.0,0.5])
        if rd.random() < savethr:
            print(g.name+' narrowly escaped death!')
            continue
        else:
            print(g.name+' was killed in action.')
            g.remarks.append('Killed in action '+str(datetime.date.today()))
            squad.remove(g)
            dead.append(g)


    #Allocate normal casualties
    wounded = []
    for i in range(0,1000):
        if len(dead)+len(wounded) >= deadly_casualties + casualties: break
        g = rd.choice(squad)

        #Basic saving throw
        savethr = min([(len(g.skill) - len(g.flaw) + g.battles)/10.0,0.75])
        if rd.random() < savethr:
            continue #Phew, that was close!

        #Save failed...
        fate = rd.choice(['Killed','Injured'])

        #Saving throw due to traits
        if ('Tough as nails' in g.skill or 'Hardy' in g.skill) and fate == 'Injured' and rd.random() < 0.5:
            print(g.name+' took a hit, but it was just a flesh wound!')
            continue
        if ('Unshakeable faith' in g.skill or 'Die hard' in g.skill) and fate == 'Killed' and rd.random() < 0.5:
            print(g.name+' was hit bad but they simply refused to die.')
            fate = 'Injured'
            squad.remove(g)
            wounded.append(g)
            continue

        #Saving throw due to comrades
        unharmed = 0
        for s in squad:
            chance = 0.01
            if s.name == g.name: continue
            if s.name in g.friends:
                chance = chance + 0.1
            if s.personality in ['Heroic','Loyal','Mentor']:
                chance = chance + 0.1
            if 'Observant' in s.skill or 'Cautious' in s.skill or 'Trustworthy' in s.skill:
                chance = chance + 0.1
            if rd.random() < chance:
                print(s.name+' saved '+g.name)
                if fate == 'Killed': fate = 'Injured'
                if fate == 'Injured': unharmed = 1
                if g.name in s.rivals and rd.random() < 0.5:
                    s.rivals.remove(g.name) #Maybe you aren't so bad after all
                    print(g.name+' no longer dislikes ',s.name)
                elif g.name not in s.friends:
                    s.friends.append(g.name)
                    print(g.name+' admires ',s.name)

        if unharmed == 1: continue

        #Saving throw due to extraordinary circumstances
        if rd.random() <= 0.01:
            print(g.name+' was left for dead but survived against the odds')
            fate = 'Injured'
            g.skill.append(rd.choice(new_skills))

        #No more saving throws. Sorry, friend.
        if fate == 'Injured':
            print(g.name+' was wounded.')
            g.remarks.append('Wounded in combat '+str(datetime.date.today()))
            squad.remove(g)
            wounded.append(g)
        else:
            print(g.name+' was killed in action.')
            g.remarks.append('Killed in action '+str(datetime.date.today()))
            squad.remove(g)
            dead.append(g)



    #Allocate fled soldiers
    fled = []
    deserters = 0
    for i in range(0,1000):
        if morale_losses < 1: break
        g = rd.choice(squad)


        #Saving throws due to positive traits
        if bool(set(['Brave','Zealous','Nerves of steel','Unshakeable faith']) & set(g.skill)) \
            or (g.personality in ['Heroic','Numb','Jaded','Reckless',\
            'Nihilist','Pious','Loyal','Psychotic']) or (g.flaw == 'Death-wish') \
            or g.ambition == 'die for the Emperor':
            morale_save = max([0.75,g.battles/10.0])

        #Saving throw due to negiatve traits
        elif bool(set(['Coward','Hesitant','Flashbacks','Poor discipline','Pacifist']) & set(g.flaw)) or \
            g.personality in ['Pessimist','Green','Sympathizer']:
            morale_save = min([0.25,g.battles/10.0])
        elif g.rank in ['Lance Sergeant','Sergeant','Lance Corporal']:
            morale_save = max([g.battles/10.0,0.5])
        else:
            morale_save = max([g.battles/10.0,0.25])


        if g.ambition == 'desert at the first opportunity' and rd.random() < 0.5:
            fate_options = ['but was caught and executed',
            'but was slain by the enemy',
            'and was never seen again']
            fate = rd.choice(fate_options)
            print(g.name+' attempted to desert '+fate)
            if fate in fate_options[0:2]:
                dead.append(g)
                g.remarks.append('Killed in action '+str(datetime.date.today()))
            squad.remove(g)
            deserters = deserters+1
            morale_losses = morale_losses - 1
            continue

        if len(fled)+deserters >= morale_losses: break #Need to have this here
        #in case the deserter was the last morale loss to account for


        if rd.random() < morale_save:
            continue

        act = [
        'hid in a hole for most of the battle',
        'succumbed to panic',
        'was paralyzed by fear',
        'sobbed uncontrollably',
        'fainted',
        'began hyperventilating',
        'shivered uncontrollably',
        'vomited',
        'played dead',
        'prayed fervently for salvation'
        ]

        print(g.name+' '+rd.choice(act))

        snapped_out = 0
        for s in squad:
            chance = 0.01
            if s in fled: continue
            if s.name == g.name: continue
            if s.name in g.friends:
                chance = chance + 0.1
            if s.personality in ['Heroic','Loyal','Mentor','Strict']:
                chance = chance + 0.1
            if 'Born leader' in s.skill:
                chance = chance + 0.1
            if rd.random() < chance:
                print(s.name+' snapped '+g.name+' out of it!')
                snapped_out = 1
                break
        if snapped_out == 1:
            continue
        else:
            squad.remove(g)
            fled.append(g)
            print(g.name+' fled the battle. Disgraceful!')
            for s in squad:
                if s.name in g.friends and rd.random() < 0.25:
                    g.friends.remove(s.name)
                    print(s.name,' no longer likes ',g.name)
                elif (s.name not in g.rivals) and rd.random() < 0.25:
                    g.rivals.append(s.name)
                    print(s.name,' dislikes ',g.name)

        if len(fled)+deserters >= morale_losses: break


    print('------------------------------------------------------')
    return squad,dead,wounded,fled


def effects(squad,dead,wounded,fled,VP,special=None):
    #Lasting effects of the battle
    #special = award to give to all members of the squad
    #Squad are those who survived intact. Does not include wounded and fled

    print('-------------------AFTER EFFECTS----------------------')

    #Remove dead friends and rivals
    for g in squad:
        for f in g.friends:
            if f in [s.name for s in dead]: g.friends.remove(f)
        for r in g.rivals:
            if r in [s.name for s in dead]: g.rivals.remove(r)

    for g in wounded:
        for f in g.friends:
            if f in [s.name for s in dead]: g.friends.remove(f)
        for r in g.rivals:
            if r in [s.name for s in dead]: g.rivals.remove(r)

    for g in fled:
        for f in g.friends:
            if f in [s.name for s in dead]: g.friends.remove(f)
        for r in g.rivals:
            if r in [s.name for s in dead]: g.rivals.remove(r)


    #Distribute wounds
    critical_wounds = [
    'Missing eye',
    'Disfigurement',
    'Missing leg',
    'Old wound',
    'Missing arm',
    'Concussion',
    'Mostly deaf'
    ]

    discharged = []
    for g in wounded:

        #Minor wound by default
        if rd.random() < 0.1:
            g.skill.append('Awesome scar')
        elif rd.random() < 0.5: #Major wound
            wound = rd.choice(critical_wounds)
            print(g.name+' gained a critical wound: '+wound)

            #Award the medallion crimson
            if wound in ['Missing leg','Missing arm','Disfigurement','Missing Eye'] and \
            'Medallion Crimson' not in g.awards:
                print(g.name+' was awarded the Medallion Crimson for their injury')
                g.remarks.append('Awarded the Medallion Crimson '+str(datetime.date.today()))
                g.awards.append('Medallion Crimson')

            #Check if they are elligibe for a bionic
            if ((int(g.battles) + len(g.skill) - len(g.flaw) + len(g.awards) > 3) or \
                g.rank in ['Lance Sergeant','Sergeant','Lance Corporal']) and \
                wound in ['Missing eye','Missing leg','Missing arm']:
                if wound == 'Missing eye': bionic = 'Bionic eye'
                if wound == 'Missing leg': bionic = 'Bionic leg'
                if wound == 'Missing arm': bionic = 'Bionic arm'
                print(g.name+' qualified for a bionic: '+bionic)
                g.skill.append(bionic)
            else:
                g.flaw.append(wound)


        #Check for invalids
        if ('Missing leg' in g.flaw) or ('Missing arm' in g.flaw) or \
            (g.flaw.count('Missing eye') > 1):
            print(g.name+' became an invalid due to their injuries.')
            print(g.name+' was granted an honorable discharge to a non-combat unit.')
            wounded.remove(g)
            discharged.append(g)
            g.remarks.append('Discharged to a non-combat unit '+str(datetime.date.today()))

    #Pychological effects
    for g in dead:
        for fr in g.friends:
            #Lost a friend, chance to gain a personality change or flaw
            #Note that f is just a string with the name...not an object

            friend_found = 0
            guilt_prob = 0.1
            for g2 in squad:
                if g2.name == fr:
                    f = g2
                    friend_found = 1
            for g2 in wounded:
                if g2.name == fr:
                    f = g2
                    friend_found = 1
            for g2 in fled:
                if g2.name == fr:
                    f = g2
                    friend_found = 1
                    guilt_prob = 0.5
            if friend_found == 0: continue

            if rd.random() < guilt_prob:
                f.flaw.append(rd.choice(new_flaws))
                print(f.name+' lost a comrade and gained a new flaw: ',f.flaw[-1])
            elif rd.random() < 0.25:
                f.personality = rd.choice(['Numb','Jaded','Quiet','Loner','Nihilist'])
                print(f.name+' lost a comrade and changed personality to: ',f.personality)
            elif rd.random() < 0.25:
                f.ambition = rd.choice(['kill xenos','kill heretics','get back to the good old days',
                'serve up a cold plate of vengeance','protect a friend'])
                print(f.name+' lost a comrade and changed ambition to: ',f.ambition)


    for g in fled:
        if (rd.random() > g.battles/10.0):
            g.flaw.append(rd.choice(new_flaws))
            print(g.name+' suffered lingering psychological damage: ',g.flaw[-1])

    #Promotions
    nprom = rd.randint(0,1) + 2*VP #Number of promotions to give
    rd.shuffle(squad)
    nominations = squad[0:min([len(squad),nprom])]
    proms_sofar = 0
    for g in nominations:
        if g.rank not in ranks: continue
        current_rank_index = ranks.index(g.rank)
        if current_rank_index > len(ranks)-2:
            print(g.name+' was nominated for an officer commission.')
            if rd.random() < 0.5:
                print(g.name+"'s commission was approved by high command.")
                print(g.name+' was promoted to Warrant Officer and joined the officer corps.')
                g.rank = 'Warrant Officer 2nd Class'
                g.remarks.append('Earned officer commission '+str(datetime.date.today()))
                squad.remove(g)
                discharged.append(g)
            else:
                print(g.name+"'s commission is pending approval.")
        else:
            new_rank_index = current_rank_index+1
            g.rank = ranks[new_rank_index]
            g.remarks.append('Promoted to '+g.rank+' '+str(datetime.date.today()))
            print(g.name+' was promoted to: ',g.rank)

        proms_sofar += 1
        if proms_sofar >= nprom: break

    if proms_sofar < nprom:
        for g in wounded:
            if g.rank not in ranks: continue
            current_rank_index = ranks.index(g.rank)
            if current_rank_index > len(ranks)-2:
                print(g.name+' was nominated for an officer commission.')
                if rd.random() < 0.5:
                    print(g.name+"'s commission was approved by high command.")
                    print(g.name+' was promoted to Warrant Officer and joined the officer corps.')
                    g.rank = 'Warrant Officer 2nd Class'
                    g.remarks.append('Earned officer commission '+str(datetime.date.today()))
                    wounded.remove(g)
                    discharged.append(g)
                else:
                    print(g.name+"'s commission is pending approval.")
            else:
                new_rank_index = current_rank_index+1
                g.rank = ranks[new_rank_index]
                g.remarks.append('Promoted to '+g.rank+' '+str(datetime.date.today()))
                print(g.name+' was promoted to: ',g.rank)
            proms_sofar += 1
            if proms_sofar >= nprom: break

    #Demotions
    for g in fled:
        current_rank_index = ranks.index(g.rank)
        if rd.random() < 0.5:
            if current_rank_index == 0 or rd.random() < 0.2:
                fates = ['Executed for desertion',
                'Executed for desertion',
                'Executed for desertion',
                'Sent to a penal legion',
                'Converted to a servitor'
                ]
                fate = rd.choice(fates)
                print(g.name+' was '+fate)
                g.remarks.append(fate+' '+str(datetime.date.today()))
                dead.append(g)
                fled.remove(g)
            else:
                new_rank_index = current_rank_index-1
                g.rank = ranks[new_rank_index]
                g.remarks.append('Demoted to '+g.rank+' '+str(datetime.date.today()))
                print(g.name+' was demoted to: ',g.rank)

    #New skills and flaws
    for g in squad:
        if rd.random() < 1.0/(len(g.skill)+1.0):
            newskill = rd.choice(new_skills)
            if newskill in g.skill: newskill = rd.choice(new_skills)
            print(g.name+' gained a new skill: '+newskill)
            g.skill.append(newskill)
        if rd.random() < float(len(dead) - g.battles)/float(squad_size):
            newflaw = rd.choice(new_flaws)
            if newflaw in g.flaw: newflaw = rd.choice(new_flaws)
            print(g.name+' gained a new flaw: '+newflaw)
            g.flaw.append(newflaw)

    for g in wounded:
        if rd.random() < 1/(len(g.skill)+1):
            newskill = rd.choice(new_skills)
            if newskill in g.skill: newskill = rd.choice(new_skills)
            print(g.name+' gained a new skill: '+newskill)
            g.skill.append(newskill)
        if rd.random() < float(len(dead) - g.battles)/float(squad_size):
            newflaw = rd.choice(new_flaws)
            if newflaw in g.flaw: newflaw = rd.choice(new_flaws)
            print(g.name+' gained a new flaw: '+newflaw)
            g.flaw.append(newflaw)

    #Medals
    heroicness = VP*len(dead)/float(squad_size) #Heroicness of the battle

    #Eagle Ordinary
    if heroicness > 0.6:
        for g in squad:
            if bool(set(['Brave','Zealous','Nerves of steel','Unshakeable faith','Born leader']) & set(g.skill)) \
                or (g.personality in ['Heroic','Numb','Jaded','Reckless','Mentor','Optimistic',\
                'Nihilist','Pious','Loyal','Psychotic']) or ('Death-wish' in g.flaw) \
                or g.ambition == 'die for the Emperor':
                hero_chance1 = 0.5
            else:
                hero_chance1 = 0.1
            hero_chance = max([(len(g.skill) - len(g.flaw) + g.battles)/100.0,hero_chance1])
            if rd.random() < hero_chance:
                print(g.name+' was awarded the Eagle Ordinary')
                g.remarks.append('Awarded the Eagle Ordinary '+str(datetime.date.today()))
                g.awards.append('Eagle Ordinary')
        for g in wounded:
            if bool(set(['Brave','Zealous','Nerves of steel','Unshakeable faith','Born leader']) & set(g.skill)) \
                or (g.personality in ['Heroic','Numb','Jaded','Reckless','Mentor','Optimistic',\
                'Nihilist','Pious','Loyal','Psychotic']) or (g.flaw == 'Death-wish') \
                or g.ambition == 'die for the Emperor':
                hero_chance1 = 0.5
            else:
                hero_chance1 = 0.1
            hero_chance = max([(len(g.skill) - len(g.flaw) + g.battles)/100.0,hero_chance1])
            if rd.random() < hero_chance:
                print(g.name+' was awarded the Eagle Ordinary')
                g.remarks.append('Awarded the Eagle Ordinary '+str(datetime.date.today()))
                g.awards.append('Eagle Ordinary')

    #Macharian Cross
    tacticalness = VP*(squad_size - len(dead))/float(squad_size)
    if tacticalness > 0.99:
        for g in squad:
            hero_chance1 = 0
            if bool(set(['Foresight','Tactical genius','Observant','Patient','Born leader','Sound judgement',\
            'Lateral thinker','Bookworm','Survivalist']) & set(g.skill)):
                hero_chance1 = hero_chance1 + 0.1
            elif g.rank in ['Lance Corporal','Sergeant','Lance Sergeant']:
                hero_chance1 = hero_chance1 + 0.1
            else:
                hero_chance1 = hero_chance1 + 0.01
            hero_chance = max([(g.battles)/100.0,hero_chance1])
            if rd.random() < hero_chance:
                print(g.name+' was awarded the Macharian Cross')
                g.remarks.append('Awarded the Macharian Cross '+str(datetime.date.today()))
                g.awards.append('Macharian Cross')

    #Ribbon Intrinsic
    if VP > 2:
        print('The Guardsmen of '+squadname+' were awarded the Ribbon Intrinsic for playing a pivotal role in the battle')
        for g in squad:
            g.awards.append('Ribbon Intrinsic')
            g.remarks.append('Awarded the Ribbon Intrinsic '+str(datetime.date.today()))
        for g in wounded:
            g.awards.append('Ribbon Intrinsic')
            g.remarks.append('Awarded the Ribbon Intrinsic '+str(datetime.date.today()))

    #Triple Skull
    if len(dead) > 0.66*squad_size:
        print('The Guardsmen of '+squadname+' were awarded the Triple Skull for sustaining massive casualties')
        for g in squad:
            g.awards.append('Triple Skull')
            g.remarks.append('Awarded the Triple Skull '+str(datetime.date.today()))
        for g in wounded:
            g.awards.append('Triple Skull')
            g.remarks.append('Awarded the Triple Skull '+str(datetime.date.today()))

    #Long Service Badge
    for g in squad:
        if g.battles >= 5:
            if 'Service Badge' not in g.awards:
                g.awards.append('Service Badge')
                g.remarks.append('Awarded the Service Badge '+str(datetime.date.today()))
                print(g.name+' was awarded the Guardsman Long Service Badge')
    for g in wounded:
        if g.battles >= 5:
            if 'Service Badge' not in g.awards:
                g.awards.append('Service Badge')
                g.remarks.append('Awarded the Service Badge '+str(datetime.date.today()))
                print(g.name+' was awarded the Guardsman Long Service Badge')


    #Finally if guardsman has served in 10 battles they can retire
    decline_options = [
    'serve up a cold plate of vengeance',
    'kill heretics',
    'kill xenos',
    'impress the commissar',
    'die for the Emperor',
    ]
    for g in squad:
        if g.battles > 9 and 'Merit of Terra' not in g.awards:
            if g.ambition in decline_options:
                print(g.name+' was offered an honorable discharge but declined')
                g.awards.append('Merit of Terra')
                g.remarks.append('Awarded the Merit of Terra '+str(datetime.date.today()))
                print(g.name+' was awarded the Merit of Terra for their continued service')
            else:
                print(g.name+' was granted an honorable discharge. Their tour of duty is complete.')
                g.remarks.append('Granted honorable discharge '+str(datetime.date.today()))
                discharged.append(g)
                squad.remove(g)

    for g in wounded:
        if g.battles > 9 and 'Merit of Terra' not in g.awards:
            if g.ambition in decline_options:
                print(g.name+' was offered an honorable discharge but declined')
                g.awards.append('Merit of Terra')
                g.remarks.append('Awarded the Merit of Terra '+str(datetime.date.today()))
                print(g.name+' was awarded the Merit of Terra for their continued service')
            else:
                print(g.name+' was granted an honorable discharge. Their tour of duty is complete.')
                g.remarks.append('Granted honorable discharge '+str(datetime.date.today()))
                discharged.append(g)
                wounded.remove(g)

    print('------------------------------------------------------')
    return squad,dead,wounded,discharged


def downtime(squad):

    print('--------------------Downtime--------------------------')

    #Replenish squad
    nfill = squad_size - len(squad) #Number to replenish
    for i in range(0,nfill):
        gi = None
        gi = Guardsman()
        gi = basics(gi)
        gi = demeanor(gi)
        gi = ambition(gi)
        gi.skill = []
        gi.flaw = []
        gi.friends = [] #No idea why I need this
        gi.rivals = []
        gi = traits(gi)
        if squadname[0:6] == 'Scions' or rd.random() < 0.01:
            gi = gen_background(gi, 'high')
        else:
            gi = gen_background(gi, 'low')
        if squadname[0:6] == 'Scions':
            gi.rank = 'Corporal'
            gi = traits(gi) #Add extra skills/flaws
            if len(gi.flaw) > 2: #Maximum of 2 flaws
                gi.flaw = gi.flaw[0:2]
        elif 'conscripts' in squadname:
            gi.rank = 'Cadet'
        print(gi.name+' joined the squad.')
        squad.append(gi)

    #Socializing
    for gi in squad:
        p_newfriend = 0.33
        p_newrival = 0.1
        if gi.personality in ['Quiet','Loner','Backwater','Psychotic','Awkward']:
            p_newfriend = 0.1
        if gi.personality in ['Spiteful','Sympathizer','Slacker','Thief','Condescending'\
        'Narcissist','Strict','Leech','Never bathes','Incompetent','Braggart','Dissenter','Drunkard']:
            p_newfriend= 0.1
            p_newrival = 0.5
        if gi.personality in ['Affable','Mentor','Heroic'] or 'Born leader' in gi.skill or \
        'Cook' in gi.skill or 'Trustworthy' in gi.skill:
            p_newfriend = 0.5

        if rd.random() < p_newfriend: #Gain a new friend
            for i in range(0,1000):
                f = rd.choice(squad)
                if f.name == gi.name: continue
                if f.name in gi.friends: continue
                if f.name in gi.rivals: continue
                gi.friends.append(f.name)
                print(f.name+' became friends with '+gi.name)
                break

        if rd.random() < p_newrival: #Gain a new rival
            for i in range(0,1000):
                f = rd.choice(squad)
                if f.name == gi.name: continue
                if f.name in gi.friends: continue
                if f.name in gi.rivals: continue
                gi.rivals.append(f.name)
                print(f.name+' became rivals with '+gi.name)
                break

        #TODO: figure out why names are appearing unexpectedly in friends/rivals
        if gi.name in gi.friends: gi.friends.remove(gi.name)
        if gi.name in gi.rivals: gi.rivals.remove(gi.name)
        for f in gi.friends:
            if f in gi.rivals:
                gi.friends.remove(f)
                gi.rivals.remove(f)
            if f in [d.name for d in dead]: gi.friends.remove(f)
        for f in gi.rivals:
            if f in gi.friends:
                gi.friends.remove(f)
                gi.rivals.remove(f)
            if f in [d.name for d in dead]: gi.rivals.remove(f)


    print('------------------------------------------------------')
    return squad


#Do the stuff
squad = load_squad(squadname)
squad_size = len(squad)
squad,dead,wounded,fled = battle(squad,Ncasualties,Nmorale,Ndeaddead)
squad,dead,wounded,discharged = effects(squad,dead,wounded,fled,VP)

#Reform the squad
for g in wounded:
    squad.append(g)
for g in fled:
    squad.append(g)

#Process Downtime
squad = downtime(squad)


#Append to the graveyard
f = open('Graveyard.txt','a',newline='\n')
for g in dead:
    #Determine their legacy:
    legacy_ind = rd.randint(0,6)
    legacy_ind = legacy_ind + 2*len(g.awards) + len(g.friends)
    legacy_ind = min([legacy_ind,len(legacy)-1])
    leg = legacy[legacy_ind]


    f.write('Name: '+g.name+'\n')
    f.write('Age: '+str(g.age)+'\n')
    f.write('Rank: '+g.rank+'\n')
    f.write('Squad: '+str(squadname)+'\n')
    f.write('Battles: '+str(g.battles)+'\n')
    f.write('Personality: '+g.personality+'\n')
    if g.background is not None:
        f.write('Background: '+g.background+'\n')
    f.write('Wants to: '+str(g.ambition)+'\n')
    f.write('Skills: '+str(g.skill)+'\n')
    f.write('Flaws: '+str(g.flaw)+'\n')
    f.write('Liked by: '+str(g.friends)+'\n')
    f.write('Disliked by: '+str(g.rivals)+'\n')
    f.write('Confirmed kills: '+str(g.confirmed_kills)+'\n')
    f.write('Awards: '+str(g.awards)+'\n')
    f.write('Remarks: '+str(g.remarks)+'\n')
    f.write('Legacy: '+str(leg)+'\n')
    f.write('\n')
f.close()

#Append to the alumni
f = open('Alumni.txt','a',newline='\n')
for g in discharged:
    f.write('Name: '+g.name+'\n')
    f.write('Age: '+str(g.age)+'\n')
    f.write('Rank: '+g.rank+'\n')
    f.write('Squad: '+str(squadname)+'\n')
    f.write('Battles: '+str(g.battles)+'\n')
    f.write('Personality: '+g.personality+'\n')
    if g.background is not None:
        f.write('Background: '+g.background+'\n')
    f.write('Wants to: '+str(g.ambition)+'\n')
    f.write('Skills: '+str(g.skill)+'\n')
    f.write('Flaws: '+str(g.flaw)+'\n')
    f.write('Liked by: '+str(g.friends)+'\n')
    f.write('Disliked by: '+str(g.rivals)+'\n')
    f.write('Confirmed kills: '+str(g.confirmed_kills)+'\n')
    f.write('Awards: '+str(g.awards)+'\n')
    f.write('Remarks: '+str(g.remarks)+'\n')
    f.write('\n')
f.close()

#Save the squad
fname = squadname + '.txt'
f = open(fname,'w',newline='\n')
for gi in squad:
    f.write('Name: '+gi.name+'\n')
    f.write('Age: '+str(gi.age)+'\n')
    f.write('Rank: '+gi.rank+'\n')
    f.write('Battles: '+str(gi.battles)+'\n')
    f.write('Personality: '+gi.personality+'\n')
    if gi.background is not None:
        f.write('Background: '+gi.background+'\n')
    f.write('Wants to: '+str(gi.ambition)+'\n')
    f.write('Skills: '+str(list(OrderedDict.fromkeys(gi.skill)))+'\n')
    f.write('Flaws: '+str(list(OrderedDict.fromkeys(gi.flaw)))+'\n')
    f.write('Confirmed kills: '+str(gi.confirmed_kills)+'\n')
    f.write('Awards: '+str(gi.awards)+'\n')
    f.write('Liked by: '+str(gi.friends)+'\n')
    f.write('Disliked by: '+str(gi.rivals)+'\n')
    f.write('Remarks: '+str(gi.remarks)+'\n')
    f.write('\n')
f.close()

# END
