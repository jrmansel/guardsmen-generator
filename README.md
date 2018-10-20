# guardsmen-generator
Scripts for generating and processing unique Imperial Guardsmen for the Warhammer 40k tabletop game.
Author: Justin Mansell (2018)

Description:
These codes procedurally generate squads of characters for Astra Militarum units. The purpose is to add personality and quirks to the units and give a "band of brothers" feel to battles and their aftermath. Many players enjoy fleshing out backstories for their favourite characters in their army. This tool fills in the rest; adding a touch of life and story to the everyday men and women without whom no battle could be won.

Installation (Mac OS):
Download the program files (RandomGuardsman.py, PostBattle.py, and NewSquad.py) to a location of your choice. Open the terminal (Applications>Utilities>Terminal). Drag any file from the folder where you downloaded the files into the terminal. You should see the directory path appear on the command line. On the command line, delete the name of the file you dragged (the stuff after the last slash), then press control-a. This moves the cursor to the beginning of the command. Type cd and add a space. Hit enter to navigate to the folder directory. Then type: sudo pip install names and hit enter. The tool is then ready to use.

Usage:
1) Navigate to the directory using the method described in Installation above. You do not have to do this every time, just each time you restart the terminal.
2) To generate a new squad, type the following command into the terminal command line: python NewSquad.py N T, replacing N with the number of members in the squad and T for the type of squad. The tool currently supports the following types:
G - Standard guardsman squad. If T is neglected this is the default setting.
C - Conscripts (all are rank Cadet and there is no sergeant)
S - Scions (higher ranks and more skills)
V - Veterans (higher ranks and more skills)
Other - type other to generate a guardsman squad without the sergeant. This works well for generating heavy weapons platoons, special weapons squads, vehicle crews, etc.
3) To put the squad through a battle, run the command: python PostBattle.py squadName D C F P where:
squadName - the name of the squad file you wish to process (without .txt)
D - the number of guardsmen who are definitely dead
C - the number of guardsmen who may be either wounded or dead
F - the number of guardsmen who were lost due to failing morale tests
P - the number of victory points earned by the squad during the battle
The code will describe the events and aftermath of the battle and overwrite the squad file with the new squad. If you realize you made a mistake, the old file is copied to squadName_old.txt.

Limitations:
- Special equipment is not tracked. It is assumed that special weapons and equipment are distributed as appropriate.
- The squad leader is not tracked and is assumed to be highest ranking member of the squad. In many units the leader has a separate stat line, but for the purpose of this tool whether or not a particular guardsmen corresponds to the leader model on the board is ambiguous.
- You can modify the squad file by typing stuff in yourself provided: (i) you follow the correct format and (ii) you only type unicode UTF-8 characters. You may have to change the preferences on your text editor to make sure it isn't stylizing things like quotation marks by converting them to non UTF-8 characters.

Notes:
The ultimate fate for guardsmen is to end up in one of two places: the graveyard or the alumni. The graveyard stores all of the guardsmen killed so far. Alumni stores the guardsmen who left the regiment for other reasons, including: being invalided by an injury, being awarded an officer commission etc.

The 'definitely dead' parameter is used to represent the number of guardsmen who are unequivocally slain. Given the destructiveness of weapons in 40k it is tempting to treat all casualties this way, but doing so misses the point of the tool: to help create an interesting story of camaraderie. Keep in mind that humans are extremely weak relative to other combatants in the 40k universe. Even minor wounds (ricochets, glancing hits, single gunshot wounds, shrapnel from nearby blasts) are likely to put a guardsmen out of action. Therefore, while guardsmen are more likely to be killed in battle, they are also more likely to be wounded. It is recommended that the 'definitely dead' parameter be reserved for situations where a 'wounded' casualty result word be contradictory. For instance, summary executions or the Fire On My Position stratagem. It may also be appropriate to represent a certain amount of overkill such as being hit with titan-grade weapons.

Slightly less than 50% of the casualties specified by the 'casualties' parameter will be killed, the others are wounded. The percentage is 'slightly' less than 50% because certain traits (e.g. Die hard) can turn a lethal result into just a wound. Friends of the character can also attempt to intervene and save the character. In short, characters with many friends and a high skill-to-flaw ratio are less likely to be killed in battle.

Currently, when a guardsman survives 10 battles, they are allowed to retire. Depending on the guardsman's demeanour and ambitions they may refuse, but this is rare. Guardsmen who die add a 'legacy' entry to their profile representing how they will be remembered. The results range from anonymous sacrifice to becoming a local deity. The more friends and medals they have, the more likely they are to be remembered.
