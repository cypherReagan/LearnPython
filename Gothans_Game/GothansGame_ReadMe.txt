Design:

	"Aliens have invaded a space ship and our hero has to go through a maze 
	of rooms defeating them so he can escape into an escape pod to the planet below. 
	The game will be more like a Zork or Adventure type game with text outputs and 
	funny ways to die. The game will involve an engine that runs a map full of rooms or scenes. 
	Each room will print its own description when the player enters it and then tell the engine 
	what room to run next out of the map."
	
	Death
		This is when the player dies and should be something funny.
		
	Central Corridor
		This is the starting point and has a Gothon already standing there they have to defeat with a joke before continuing.
		
	Laser Weapon Armory
		This is where the hero gets a neutron bomb to blow up the ship before getting to the escape pod. 
		It has a keypad the hero has to guess the number for.
		
	The Bridge
		Another battle scene with a Gothon where the hero places the bomb.
		
	Escape Pod
		Where the hero escapes but only after guessing the right escape pod.

		
	- Class Hierarchy:
		* Map
		  - next_scene
		  - opening_scene
		* Engine
		  - play
		* Scene
		  - enter
		  - run_attack
		  * Death
		  * Central Corridor
		  * Laser Weapon Armory
		  * The Bridge
		  * Escape Pod
		* Attack
		  - evalute_attack
		  - is_valid
		* Override
		  - run_override
		  - assign_wires
		* Inventory
		  - 
		  - 
		  *
		  
_______________________________________________________________________________________________

These are my notes:  

IDEA: After completing the Bridge scene, implement a global counter to expire in X minutes.
		
		
COMBAT IDEAS:
	- 	Rock-paper-scissor scenario? 
		I choose attack A, enemy (randomly!) chooses attack B. 
		A beats B so I win. As an extra bonus, with markov chains you cam make an AI for
		it if you want tougher opponents.
		
		Ex.
			Rock - beats scissors, loses to paper
			Paper - beats rock, loses to scissors
			Scissors - beats paper, loses to rock
			
			Leg Sweep - beats knife, loses to cloak
			Cloak - beats leg sweep, loses to knife
			Knife - beats cloak, loses to leg sweep
			
			
		
	-	Ranged attack?
		Type: snipe <direction> <target>
		Let's say that there is a jawa 5 rooms to the east, and the player is holding a rifle, they would type:
		Type: snipe east jawa
		The code would first look at the contents of the room directly to the east of this one if there is one. 
		If there are no targets named jawa, it continues by searching any room directly east of the one it just 
		checked until it reaches a certain distance (in number of rooms), finds the target, or there are no more 
		rooms to the east.
		
DEATH IDEAS:
	-	I could create a whole host of death descriptions (i.e. "The Gothan proceeds to dismember you.").
		I could then randomly select one on each death instance.
		
EXPANSION IDEAS:
	- 	Overrides:	At each keypad, allow user to override the door controls by cutting/splicing wires (red/green/black). 
					These wires would be connected to power/control/ect...
					
					Given 3 options:
						- Keypad output
						- Door input
						- Battery
						
					To win the user must cross the Battery wire with the Door input.
						
					Randomize the colors red/green/yellow.
					
	Inventory:	Weapons characterized by the following:
	
				  NAME			| TYPE		| AMMO			| DAMAGE %	| Range
				  ________________________________________________________________________
				- battery		| utility	| 1				| 			|
				- shield		| melee		| -1 (infinite)	| 100		|
				- net			| melee		| -1			| 100		|
				- knife			| melee		| -1			| 100		|
				- grenade		| ranged	| 1-5			| 100		|
				- blaster pistol| ranged	| 10			| 40		|
				- plasma rifle	| ranged	| 10			| 80		|
			
	