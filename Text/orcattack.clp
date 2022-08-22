(deftemplate env
	(slot region)
	(slot terrain)
	(slot holiday)
)

(deftemplate orc
	(slot health)
	(slot creed)
	(slot wealth)
	(slot attitude)
)

(deftemplate human
	(slot health)
	(slot wealth)
	(slot attitude)
)

(defrule tidban-rich-human
	(orc (creed "Tidban") 
	(wealth ?orc_wealth) 
	(health ?orc_health) 
	(attitude ?orc_attitude)) 
	(human (health ?human_health) 
	(wealth ?human_wealth) 
	(attitude ?human_attitude)) 
	(test (> ?human_wealth ?orc_wealth))
	=>
	(println "attack:tidban-rich-human")
)

(defrule tidban-weak-human
	(orc (creed "Tidban") 
	(wealth ?orc_wealth) 
	(health ?orc_health) 
	(attitude ?orc_attitude)) 
	(human (health ?human_health) 
	(wealth ?human_wealth) 
	(attitude ?human_attitude)) 
	(test (> ?human_wealth 0)) 
	(test (< ?human_health (* ?orc_health .10)))
	=>
	(println "attack:tidban-weak-human")
)

(defrule tidban-orc-bad-attitude
	(orc (creed "Tidban") 
	(attitude "enraged" | "angry" | "belligerent"))
	=>
	(println "attack:tidban-orc-bad-attitude")
)

(defrule tidban-human-bad-attitude
	(orc (creed "Tidban")) 
	(human (attitude "belligerent"))
	=>
	(println "attack:tidban-human-bad-attitude")
)

(defrule tolzea-tainmoun-non-holiday
	(orc (creed "Tolzea")) 
	(env (region "Tainmoun") 
	(holiday ~TRUE))
	=>
	(println "attack:tolzea-tainmoun-non-holiday")
)

(defrule tolzea-bad-human-attitude
	(env (region ~"Tainmoun")) 
	(orc (creed "Tolzea")) 
	(human (attitude "belligerent")) 
	=> 
	(println "attack:tolzea-bad-human-attitude")
)

(defrule tolzea-bad-orc-health
	(env (region ~"Tainmoun")) 
	(human (health ?human_health)) 
	(orc (creed "Tolzea") (health ?orc_health)) 
	(test (< ?orc_health (* ?human_health .10))) 
	=> 
	(println "attack:tolzea-bad-orc-health")
)

(defrule rageeva-lake
	(orc (creed "Rageeva")) 
	(env (terrain "lake"))
	=>
	(println "attack:rageeva-lake")
)

(defrule rageeva-ork-attitude
	(orc (creed "Rageeva") 
	(attitude "enraged" | "angry" | "belligerent")) 
	=>
	(println "attack:rageeva-ork-attitude")
)

(defrule rageeva-human-attitude
	(human (attitude "belligerent")) 
	=>
	(println "attack:rageeva-human-attitude")
)

(defrule narymerce-rob-human
	(orc (creed "Narymerce") (health ?orc_health)) 
	(human (wealth ?human_wealth) (health ?human_health)) 
	(test (< ?human_wealth 70)) (test (> ?human_wealth 0)) 
	(test (< ?human_health (* ?orc_health .10)))
	=>
	(println "attack:"narymerce-rob-human)
)

(defrule narymerce-ork-attitude
	(orc (creed "Narymerce") (attitude "enraged" | "angry" | "belligerent")) 
	=>
	(println "attack:narymerce-ork-attitude")
)

(defrule narymerce-human-attitude
	(human (attitude "belligerent")) 
	=>
	(println "attack:narymerce-human-attitude")
)

(defrule tuoved-tainmoun-bad-health-and-attitude
	(env (region "Tainmoun")) 
	(human (attitude "belligerent") (health ?human_health)) 
	(orc (creed "Tuoved") (health ?orc_health)) 
	(test (< ?orc_health (* ?human_health .10))) 
	=> 
	(println "attack:tuoved-tainmoun-bad-health-and-attitude")
)

(defrule tuoved-bad-human-attitude
	(env (region ~"Tainmoun")) (orc (creed "Tuoved")) 
	(human (attitude "belligerent")) 
	=> 
	(println "attack:tuoved-bad-human-attitude")
)

(defrule tuoved-bad-orc-health
	(env (region ~"Tainmoun")) (human (health ?human_health)) 
	(orc (creed "Tuoved") (health ?orc_health)) 
	(test (< ?orc_health (* ?human_health .10))) 
	=> 
	(println "attack:tuoved-bad-orc-health")
)
