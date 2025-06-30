This repository contains code for the ABM project Peace within Chimps. 

The project aims at modelling different confrontation strategies between groups of chimpanzees. In particular, it introduces six types of strategies that chimpanzee-crews could follow: Anxious (passive), Aggressive (active, fighters), Show-offs (active, bluffing), Random, Resentful (a version of tit-for-tat), Flexible (using the knowledge about the scarcity of the resource to adjust their conflict engagement). The experiments are centered around two games: one-stage game that only involves fighting, and two-stage game that involves intimidation round first and gives a chance to win over the resource without engaging in costly fight. 

To reproduce two-stage game experiments, pull the branch two-stage-game. Locate yourself in the folder Type_experiment. Go to Type_plot.py. Adjust the variables in lines 8-14 for custom naming of the outputs and switching between experimental setups. Then run the Type_plot.py . If you want to produce a graph with a breakdown per energy level within each chimp agent type, adjust the similar lines in Type_plot_energies.py and run this script. 

The packages you will need: base Python 3, matplotlib, numpy, pathlib.
