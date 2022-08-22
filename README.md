![OrcAttack Image](https://github.com/PaulWGraham/OrcAttack/blob/main/Screenshot%202022-08-21%2021-10-47.png)


# Orc Attack!
Orc Attack! is a simple program meant to demonstrate using the CLIPS expert system tool to make decisions. The premise is that an orc encounters a human. Does the orc Attack?

For a demonstration of Orc Attack! see [this video.](https://youtu.be/mGPh8Pol6hY)

## CLIPS rules:

Whether or not the orc attacks is determined by a number of [CLIPS rules](https://github.com/PaulWGraham/OrcAttack/blob/main/Text/orcattack.clp). The rules are triggered by facts that fall into three categories: environment, human, and orc. The following is the template used to assert facts about the orc:
```
	(deftemplate orc
		(slot health)
		(slot creed)
		(slot wealth)
		(slot attitude)
	)
```

This is one of the CLIPS rules:
```
(defrule tolzea-bad-orc-health
	(env (region ~"Tainmoun")) 
	(human (health ?human_health)) 
	(orc (creed "Tolzea") (health ?orc_health)) 
	(test (< ?orc_health (* ?human_health .10))) 
	=> 
	(println "attack:tolzea-bad-orc-health")
)
```

## GUI:

The GUI is managed by a [python script](https://github.com/PaulWGraham/OrcAttack/blob/main/orcattack.py). The way the script works is that it picks some random facts. The script then turns those facts into ASSERTs that CLIPSDOS can understand. A file is then created containing some previously prepared CLIPS rules and the generated ASSERTs. CLIPSDOS is then run using subprocess and the appropriate output is displayed. The output is the chosen random facts and the text of CLIPS rule triggered (if any).

## The Orcs

The following is a list of the types of orcs and their descriptions. These descriptions were used to guide to creation of the CLIPS rules.


### Tidban - bandit

Tidban orcs have no qualms attacking humans especially if they think there is money to be made. They might leave poor humans alone unless the orcs are in a bad mode or the humans are easy prey.


### Tuoved - devout

Tuoved orcs generally only attack humans if desperate or if the humans are aggressive. With rare exceptions Tuoved orcs don't attack humans they find in the holy lands of Tainmoun.


### Tolzea - zealot

Tolzea orcs tend to not attack humans unless they are in the holy land of Tainmoun. However, if they are in the holy land of Tainmoun Tolzea orcs will attack every human they find unless it's a holy holiday.


### Rageeva - average

Rageeva orcs tend to live around water and will likely attack humans they find near their homes.


### Narymerce - mercenary 

Narymerce orcs love to attack humans. However, they have been payed by a group of wealthy humans to leave rich humans alone.


