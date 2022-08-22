# orcattack.py
# This is quick and dirty script put together to demonstrate 
# using CLIPS expert system tool to make decisions. The clips
# rules used to make the decisions can be found in orcattack.clp

# Generally the way this script works is that it picks some
# random facts. The script then turns those facts into ASSERTs
# that CLIPSDOS can understand. A file is then created containing
# some previously prepared CLIPS rules and the generated ASSERTs.
# CLIPSDOS is then run using subprocess and the appropriate
# output is displayed. The output is the chosen random facts and
# the text of CLIPS rule triggered (if any).

import random
import subprocess
import tkinter
import tkinter.ttk

# Constants and globals
CLIPSDOS_PATH = "D:\\Program Files\\CLIPS 6.4\\CLIPSDOS.exe"
CLIPSDOS_FLAGS = "-f"
CLIPS_RULES_HEADER_PATH = "D:\\Development\\Misc\\WOTC Job Application\\Ork Attack\\Text\\orcattack.clp"
CLIPS_RULES_FOOTER_PATH = "D:\\Development\\Misc\\WOTC Job Application\\Ork Attack\\Text\\footer.clp"
CLIPS_RULES_PATH = "D:\\Development\\Misc\\WOTC Job Application\\Ork Attack\\Text\\target.clp"

CLIPS_OUTPUT_LINE_SEPARATOR = '\n'
ATTACK_MESSAGE_LOCATION = -3
ATTACK_MESSAGE_SEPARATOR = ':'
ATTACK_MESSAGE = "attack"
NO_ATTACK_MESSAGE = "No Attack"

ENV_TEMPLATE = """(assert (env
	(region \"{}\")
	(terrain \"{}\")
	(holiday {})
))
"""

ORC_TEMPLATE = """(assert (orc
	(health {})
	(creed \"{}\")
	(wealth {})
	(attitude \"{}\")
))
"""

HUMAN_TEMPLATE = """(assert (human
	(health {})
	(wealth {})
	(attitude \"{}\")
))
"""

ENV_REGION_POSSIBILITIES = ("Tainmoun", "Landlow", "Nonside")
ENV_TERRAIN_POSSIBILITIES =("lake", "hill", "valley")
ENV_HOLIDAY_POSSIBILITIES =("TRUE", "FALSE")
ORC_HEALTH_MIN_MAX = (1, 200)
ORC_WEALTH_MIN_MAX = (0, 500)
ORC_CREED_POSSIBILITIES = ("Tidban", "Tolzea", "Rageeva", "Narymerce", "Tuoved")
ORC_ATTITUDE_POSSIBILITIES = ("happy", "scared", "enraged", "angry", "belligerent")
HUMAN_HEALTH_MIN_MAX = (1, 1000)
HUMAN_WEALTH_MIN_MAX = (0, 1000)
HUMAN_ATTITUDE_POSSIBILITIES = ("happy", "scared", "enraged", "angry", "belligerent")

FONT = ("Arial", 25)

ORC_CREED_LABEL = None
ORC_HEALTH_LABEL = None
ORC_WEALTH_LABEL = None
ORC_ATTITUDE_LABEL = None
HUMAN_CREED_LABEL = None
HUMAN_HEALTH_LABEL = None
HUMAN_WEALTH_LABEL = None
HUMAN_ATTITUDE_LABEL = None
ENV_REGION_LABEL = None
ENV_TERRAIN_LABEL = None
ENV_HOLIDAY_LABEL = None
ATTACK_LABEL = None
CLIPS_TEXT = None

CLIPS_RULES = None

def pick_attributes():
	attributes = {}
	attributes['env_region'] = random.choice(ENV_REGION_POSSIBILITIES)
	attributes['env_terrain'] = random.choice(ENV_TERRAIN_POSSIBILITIES)
	attributes['env_holiday'] = random.choice(ENV_HOLIDAY_POSSIBILITIES)

	attributes['orc_health'] = random.randrange(*ORC_HEALTH_MIN_MAX)
	attributes['orc_creed'] = random.choice(ORC_CREED_POSSIBILITIES)
	attributes['orc_wealth'] = random.randrange(*ORC_WEALTH_MIN_MAX)
	attributes['orc_attitude'] =  random.choice(ORC_ATTITUDE_POSSIBILITIES)

	attributes['human_health'] = random.randrange(*HUMAN_HEALTH_MIN_MAX)
	attributes['human_wealth'] = random.randrange(*HUMAN_WEALTH_MIN_MAX)
	attributes['human_attitude'] = random.choice(HUMAN_ATTITUDE_POSSIBILITIES)
	
	return attributes

def write_clips_rules(attributes):
	env = ENV_TEMPLATE.format(	attributes['env_region'], 
								attributes['env_terrain'], 
								attributes['env_holiday'])
	
	orc = ORC_TEMPLATE.format(	attributes['orc_health'],
								attributes['orc_creed'],
								attributes['orc_wealth'],
								attributes['orc_attitude']) 
			
	human = HUMAN_TEMPLATE.format(	attributes['human_health'],
									attributes['human_wealth'],
									attributes['human_attitude'])

	with open(CLIPS_RULES_HEADER_PATH) as clips_header:
		header = clips_header.read()

	with open(CLIPS_RULES_FOOTER_PATH) as clips_footer:
		footer = clips_footer.read()

	with open(CLIPS_RULES_PATH, 'w') as clips_rules:
		clips_rules.write(
			header +
			env +
			orc +
			human +
			footer
		)

def run_clips_rules():
	clips_output = subprocess.run([CLIPSDOS_PATH, CLIPSDOS_FLAGS, CLIPS_RULES_PATH], stdout = subprocess.PIPE, text = True).stdout
	attack_message = clips_output.split(CLIPS_OUTPUT_LINE_SEPARATOR)[ATTACK_MESSAGE_LOCATION]
	if attack_message.startswith(ATTACK_MESSAGE):
		attack = attack_message.split(ATTACK_MESSAGE_SEPARATOR)[1]
	else:
		attack = None

	return attack

def new_encounter():
	attributes = pick_attributes()
	write_clips_rules(attributes)
	attack = run_clips_rules()

	ENV_REGION_LABEL.config(text = "REGION: " + attributes["env_region"])
	ENV_TERRAIN_LABEL.config(text = "TERRAIN: " + attributes["env_terrain"])
	ENV_HOLIDAY_LABEL.config(text = "HOLIDAY: " + attributes["env_holiday"])
	ORC_CREED_LABEL.config(text = "CREED: " + attributes["orc_creed"])
	ORC_HEALTH_LABEL.config(text = "HEALTH: " + str(attributes["orc_health"]))
	ORC_WEALTH_LABEL.config(text = "WEALTH: " + str(attributes["orc_wealth"]))
	ORC_ATTITUDE_LABEL.config(text = "ATTITUDE: " + attributes["orc_attitude"])
	HUMAN_HEALTH_LABEL.config(text = "HEALTH: " + str(attributes["human_health"]))
	HUMAN_WEALTH_LABEL.config(text = "WEALTH: " + str(attributes["human_wealth"]))
	HUMAN_ATTITUDE_LABEL.config(text = "ATTITUDE: " + attributes["human_attitude"])

	attack_font = (FONT[0], FONT[1] * 2)
	if attack:
		CLIPS_TEXT.delete(1.0, "end")
		CLIPS_TEXT.insert("end", CLIPS_RULES[attack])
		ATTACK_LABEL.config(text = "ATTACK!", background = "red", font = attack_font)
	else:
		CLIPS_TEXT.delete(1.0, "end")
		ATTACK_LABEL.config(text = "No attack.", background = "", font = attack_font)

if __name__ == '__main__':

	with open(CLIPS_RULES_HEADER_PATH) as clips_header:
		header = clips_header.read()
	
	# Parse the prepared CLIPS file and extract the DEFRULEs.
	# This will break if an unmatched parentheses is present
	# anywhere in the file. 
	parentheses_count = 0
	CLIPS_RULES = {}
	current_block = []
	for c in header:
		current_block.append(c)
		if c == '(':
			parentheses_count += 1
		elif c == ')':
			parentheses_count -= 1
			if parentheses_count == 0:
				block = ''.join(current_block).strip()
				current_block = []
				if block.startswith('(defrule'):
					CLIPS_RULES[block.split()[1]] = block
	
	# Setup the GUI
	root = tkinter.Tk()
	root.title("Orc Attack!")
	frm = tkinter.ttk.Frame(root, padding = 20)
	frm.pack(fill = "both", expand = "yes")
	info_frame = tkinter.ttk.Frame(frm, padding = 20)
	info_frame.pack(side = 'top')
	orc_frame = tkinter.ttk.Frame(info_frame, padding = 20)
	orc_frame.pack(side = 'left')
	orc_label = tkinter.ttk.Label(orc_frame, text = "ORC", font = FONT)
	orc_label.pack(side = 'top')
	ORC_CREED_LABEL = tkinter.ttk.Label(orc_frame, font = FONT)
	ORC_CREED_LABEL.pack(side = 'top')
	ORC_HEALTH_LABEL =  tkinter.ttk.Label(orc_frame, font = FONT)
	ORC_HEALTH_LABEL.pack(side = 'top')
	ORC_WEALTH_LABEL =  tkinter.ttk.Label(orc_frame, font = FONT)
	ORC_WEALTH_LABEL.pack(side = 'top')
	ORC_ATTITUDE_LABEL =  tkinter.ttk.Label(orc_frame, font = FONT)
	ORC_ATTITUDE_LABEL.pack(side = 'top')

	human_frame = tkinter.ttk.Frame(info_frame, padding = 20)
	human_frame.pack(side = 'left')
	human_label = tkinter.ttk.Label(human_frame, text = "HUMAN", font = FONT)
	human_label.pack(side = 'top')
	human_blank_label = tkinter.ttk.Label(human_frame, font = FONT)
	human_blank_label.pack(side = 'top')
	HUMAN_HEALTH_LABEL = tkinter.ttk.Label(human_frame, font = FONT)
	HUMAN_HEALTH_LABEL.pack(side = 'top')
	HUMAN_WEALTH_LABEL = tkinter.ttk.Label(human_frame, font = FONT)
	HUMAN_WEALTH_LABEL.pack(side = 'top')
	HUMAN_ATTITUDE_LABEL = tkinter.ttk.Label(human_frame, font = FONT)
	HUMAN_ATTITUDE_LABEL.pack(side = 'top')

	env_frame = tkinter.ttk.Frame(info_frame, padding = 20)
	env_frame.pack(side = 'left')
	env_label = tkinter.ttk.Label(env_frame, text = "ENV", font = FONT)
	env_label.pack(side = 'top')
	env_blank_label = tkinter.ttk.Label(env_frame, font = FONT)
	env_blank_label.pack(side = 'top')
	ENV_REGION_LABEL = tkinter.ttk.Label(env_frame, font = FONT)
	ENV_REGION_LABEL.pack(side = 'top')
	ENV_TERRAIN_LABEL = tkinter.ttk.Label(env_frame, font = FONT)
	ENV_TERRAIN_LABEL.pack(side = 'top')
	ENV_HOLIDAY_LABEL = tkinter.ttk.Label(env_frame, font = FONT)
	ENV_HOLIDAY_LABEL.pack(side = 'top')
	attack_frame = tkinter.ttk.Frame(frm, padding = 20)
	attack_frame.pack(side = 'top')
	ATTACK_LABEL = tkinter.ttk.Label(attack_frame, text = ' ', font = FONT)
	ATTACK_LABEL.pack(side = 'top')
	clips_frame = tkinter.ttk.Frame(frm, padding = 20)
	clips_frame.pack(side = 'top')
	CLIPS_TEXT = tkinter.Text(clips_frame, font = FONT, height = 13)
	CLIPS_TEXT.pack(side = 'top')
	
	tkinter.ttk.Button(frm, text = "Next", command = new_encounter).pack(side = 'top')
	root.mainloop()