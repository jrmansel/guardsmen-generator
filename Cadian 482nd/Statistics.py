#=============================================================================#
# PROGRAM: Statistics.py
# AUTHOR: Justin Mansell (2018)
# DESCRIPTION: analyzes guardsmen statistics
#=============================================================================#
import matplotlib.pyplot as plt
from RandomGuardsmen import *
import numpy as np
import ast

#Enter the squads to be analyzed here:
squads = ['chimera898','command974','HWP281','RussB185','RussD284','RussE592',
'squad68','squad650','squad705','SuperHeavy789', 'Scions475', 'Basilisk969',
'Basilisk716','Basilisk130','HWP84','HWP305','squad223']
Nbattles = 21 #Number of battles

#Load guardsmen
active_roster = []
dead_roster = []
alumni_roster = []
for file in squads:
    f = open(file+'.txt','r')
    stats = {}
    print(file)
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
            if 'Squad' in stats.keys():
                g.squad = ast.literal_eval(stats['Squad'])
            else: g.squad = file
            if 'Background' in stats.keys():
                g.background = stats['Background']
            else: g.background = 0
            if 'Awards' in stats.keys():
                g.awards = ast.literal_eval(stats['Awards'])
            else: g.awards = []
            if 'Remarks' in stats.keys():
                g.remarks = ast.literal_eval(stats['Remarks'])
            else: g.remarks = []
            active_roster.append(g)
            stats = {}
    f.close()

f = open('Graveyard.txt','r')
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
        if 'Squad' in stats.keys():
            g.squad = stats['Squad']
        else: g.squad = None
        if 'Background' in stats.keys():
            g.background = stats['Background']
        else: g.background = 0
        if 'Awards' in stats.keys():
            g.awards = ast.literal_eval(stats['Awards'])
        else: g.awards = []
        if 'Remarks' in stats.keys():
            g.remarks = ast.literal_eval(stats['Remarks'])
        else: g.remarks = []
        dead_roster.append(g)
        stats = {}
f.close()

f = open('Alumni.txt','r')
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
        if 'Squad' in stats.keys():
            g.squad = stats['Squad']
        else: g.squad = None
        if 'Background' in stats.keys():
            g.background = stats['Background']
        else: g.background = 0
        if 'Awards' in stats.keys():
            g.awards = ast.literal_eval(stats['Awards'])
        else: g.awards = []
        if 'Remarks' in stats.keys():
            g.remarks = ast.literal_eval(stats['Remarks'])
        else: g.remarks = []
        alumni_roster.append(g)
        stats = {}
f.close()

#Medals
medals_fig = plt.figure(figsize=(10, 6))
medals = ['Medallion Crimson','Triple Skull','Service Badge',
'Ribbon Intrinsic','Macharian Cross','Eagle Ordinary','Honorifica Imperialis','Merit of Terra','Other']
active_awardees = [0,0,0,0,0,0,0,0,0]
dead_awardees = [0,0,0,0,0,0,0,0,0]
alumni_awardees = [0,0,0,0,0,0,0,0,0]
for i,medal in enumerate(medals):
    for g in active_roster:
        if medal in g.awards:
            active_awardees[i]+=1
        elif medal == 'Other' and list(set(g.awards) - set(medals)):
            active_awardees[-1]+=len(list(set(g.awards) - set(medals)))
    for g in dead_roster:
        if medal in g.awards:
            dead_awardees[i]+=1
        elif medal == 'Other' and list(set(g.awards) - set(medals)):
            dead_awardees[-1]+=len(list(set(g.awards) - set(medals)))
    for g in alumni_roster:
        if medal in g.awards:
            alumni_awardees[i]+=1
        elif medal == 'Other' and list(set(g.awards) - set(medals)):
            alumni_awardees[-1]+=len(list(set(g.awards) - set(medals)))
alive_awardees = [sum(x) for x in zip(active_awardees, alumni_awardees)]

ind = np.arange(9)
width = 0.35
p1 = plt.bar(ind, active_awardees, width, color='b')
p2 = plt.bar(ind, alumni_awardees, width, bottom=active_awardees,color='g')
p3 = plt.bar(ind, dead_awardees, width, bottom=alive_awardees,color='r')
plt.ylabel('Awards')
plt.title('Company Medals')
plt.xticks(ind, medals, rotation = 45)
plt.subplots_adjust(bottom=0.20)
plt.legend((p1[0], p2[0], p3[0]), ('Active', 'Discharged', 'Dead'))
plt.show()
medals_fig.savefig('Medals.png', dpi=200)

#Battles survived
battles_fig = plt.figure()
battles = ['0','1','2','3','4','5','6','7','8','9','10','11+']
active_n = np.zeros(len(battles))
dead_n = np.zeros(len(battles))
alumni_n = np.zeros(len(battles))
for i,n in enumerate(battles):
    if i == 11:
        for g in active_roster:
            if int(g.battles) > 10: active_n[i]+=1
        for g in dead_roster:
            if int(g.battles) > 10: dead_n[i]+=1
        for g in alumni_roster:
            if int(g.battles) > 10: alumni_n[i]+=1
    else:
        for g in active_roster:
            if n == str(g.battles): active_n[i]+=1
        for g in dead_roster:
            if n == str(g.battles-1): dead_n[i]+=1
        for g in alumni_roster:
            if n == str(g.battles): alumni_n[i]+=1
alive_n = [sum(x) for x in zip(active_n, alumni_n)]

ind = np.arange(len(battles))
width = 0.35
p1 = plt.bar(ind, active_n, width, color='b')
p2 = plt.bar(ind, alumni_n, width, bottom=active_n, color='g')
p3 = plt.bar(ind, dead_n, width, bottom = alive_n, color='r')
plt.ylabel('Number')
plt.xlabel('Battles')
plt.title('Battles Survived')
plt.xticks(ind, battles)
plt.legend((p1[0], p2[0], p3[0]), ('Active', 'Discharged', 'Dead'))
plt.show()
battles_fig.savefig('Battles.png', dpi=200)

#Ranks
ranks_fig = plt.figure(figsize=(10, 6))
ranks = [
'Cadet',
'Guardsman',
'Corporal',
'Lance Corporal',
'Sergeant',
'Lance Sergeant'
]
active_ranks = [0,0,0,0,0,0]
dead_ranks = [0,0,0,0,0,0]
alumni_ranks = [0,0,0,0,0,0]
for i,rank in enumerate(ranks):
    for g in active_roster:
        if rank == g.rank: active_ranks[i]+=1
    for g in dead_roster:
        if rank == g.rank: dead_ranks[i]+=1
    for g in alumni_roster:
        if rank == g.rank: alumni_ranks[i]+=1
alive_ranks = [sum(x) for x in zip(active_ranks, alumni_ranks)]

ind = np.arange(6)
width = 0.35
p1 = plt.bar(ind, active_ranks, width, color='b')
p2 = plt.bar(ind, alumni_ranks, width,bottom=active_ranks,color='g')
p3 = plt.bar(ind, dead_ranks, width,bottom=alive_ranks,color='r')
plt.ylabel('Number')
plt.title('Company Ranks')
plt.xticks(ind, ranks)
plt.xlabel('Rank')
plt.legend((p1[0], p2[0], p3[0]), ('Active', 'Discharged', 'Dead'))
plt.show()
ranks_fig.savefig('Ranks.png', dpi=200)

#Squad turn over rates
# squads_fig = plt.figure()
# some_squads = ['command679','HWP84','HWP281','RussB692','RussD668','RussE440','Scions738',
# 'squad68','squad137','squad382','SWT590','SWT291']
# squad_active = np.zeros(len(some_squads))
# squad_dead = np.zeros(len(some_squads))
# squad_alumni = np.zeros(len(some_squads))
# for i,squad in enumerate(some_squads):
#     for g in active_roster:
#         if not g.squad: continue
#         if squad in g.squad: squad_active[i]+=1
#     for g in dead_roster:
#         if not g.squad: continue
#         if squad in g.squad: squad_dead[i]+=1
#     for g in alumni_roster:
#         if not g.squad: continue
#         if squad in g.squad: squad_alumni[i]+=1
# squad_alive = [sum(x) for x in zip(squad_active, squad_alumni)]
# ind = np.arange(len(some_squads))
# width = 0.35
# p1 = plt.bar(ind, squad_active, width, color='b')
# p2 = plt.bar(ind, squad_alumni, width,bottom=squad_active,color='g')
# p3 = plt.bar(ind, squad_dead, width,bottom=squad_alive,color='r')
# plt.ylabel('Number')
# plt.title('Company Squads')
# plt.xticks(ind, some_squads, rotation = 45)
# plt.subplots_adjust(bottom=0.18)
# plt.xlabel('Squad')
# plt.legend((p1[0], p2[0], p3[0]), ('Active', 'Discharged', 'Dead'))
# plt.show()
# squads_fig.savefig('Rates.png', dpi=200)

#Basic stats
print('*****************COMPANY STATS*********************')
everybody = active_roster+alumni_roster+dead_roster
print('Number of active soldiers:',len(active_roster))
print('Number of discharged soldiers:',len(alumni_roster))
print('Number of fallen soldiers:',len(dead_roster))
print('Company turn over rate per battle (%)',float(len(dead_roster+alumni_roster))/len(active_roster)*100.0/(Nbattles))

#Other random stats

#Skill deficit
active_def = []
dead_def = []
for g in active_roster:
    active_def.append(len(g.skill)-len(g.flaw))
for g in dead_roster:
    dead_def.append(len(g.skill)-len(g.flaw))
print('Mean skill deficit for active troops:',np.mean(active_def))
print('Mean skill deficit for dead troops:',np.mean(dead_def))

#Average number of battles survived
survived = []
for g in dead_roster:
    survived.append(g.battles-1)
print('Average number of battles survived:',np.mean(survived))
print('Survival rate (%):',float(len(alumni_roster))/(len(dead_roster)+len(alumni_roster))*100.0)

#Percentage of guardsmen who survive their first battle
survived_first_battle = 0.0
died_first_battle = 0.0
for g in active_roster:
    if g.battles > 0: survived_first_battle+=1
for g in alumni_roster:
    if g.battles > 0: survived_first_battle+=1
for g in dead_roster:
    if g.battles > 1: survived_first_battle+=1
    if g.battles <= 1: died_first_battle+=1
print('Percentage of soldiers who survive their first battle:',survived_first_battle/(survived_first_battle+died_first_battle)*100)

#Percentage of guardsmen who survive at least 3 battles
survived_three_battles = 0.0
died_before3_battle = 0.0
for g in active_roster:
    if g.battles > 2: survived_three_battles+=1
for g in alumni_roster:
    if g.battles > 2: survived_three_battles+=1
for g in dead_roster:
    if g.battles > 3: survived_three_battles+=1
    if g.battles <= 3: died_before3_battle+=1
print('Percentage of soldiers who survive 3 battles:',survived_three_battles/(survived_three_battles+died_before3_battle)*100)

#Percentage of guardsmen who survive at least 5 battles
survived_five_battles = 0.0
died_before5_battle = 0.0
for g in active_roster:
    if g.battles > 4: survived_five_battles+=1
for g in alumni_roster:
    if g.battles > 4: survived_five_battles+=1
for g in dead_roster:
    if g.battles > 5: survived_five_battles+=1
    if g.battles <= 5: died_before5_battle+=1
print('Percentage of soldiers who survive 5 battles:',survived_five_battles/(survived_five_battles+died_before5_battle)*100)

#Average number of medals
print('Average number of medals:',np.mean([len(g.awards) for g in everybody]))

#Percentage of guardsmen with at least one medal
have_medals = 0.0
for g in everybody:
    if g.awards: have_medals+=1
print('Percentage of soldiers with at least one medal:',have_medals/len(everybody)*100)

#Most popular soldier
popularity = [len(g.friends)-len(g.rivals) for g in active_roster]
ii = np.argmax(popularity)
names = [g.name for g in active_roster]
squads_list = [g.squad for g in active_roster]
print('The most popular soldier is',names[ii],'from squad:',squads_list[ii])

#Least popular soldier
ii = np.argmin(popularity)
print('The least popular soldier is',names[ii],'from squad:',squads_list[ii])

#Most badass soldier
bad_ass_score = [len(g.skill)-len(g.flaw)+g.battles+len(g.awards) for g in active_roster]
ii = np.argmax(bad_ass_score)
print('The most bad-ass soldier is',names[ii],'from squad:',squads_list[ii])

#Least badass soldier
ii = np.argmin(bad_ass_score)
print('The least bad-ass soldier is',names[ii],'from squad: ',squads_list[ii])

#Oldest guardsman
ages = [g.age for g in active_roster]
ii = np.argmax(ages)
print('The oldest soldier in the regiment is',names[ii],'(age',ages[ii],') from squad',squads_list[ii])

#Saddest guardsmen
friends_lost = np.zeros(len(active_roster))
for j,g in enumerate(active_roster):
    for f in dead_roster:
        if g.name in f.friends: friends_lost[j]+=1
ii = np.argmax(friends_lost)
print('The saddest soldier in the regiment is:',names[ii],'from squad',squads_list[ii],'who has lost',int(friends_lost[ii]),'friends')
