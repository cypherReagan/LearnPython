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
		  * Death
		  * Central Corridor
		  * Laser Weapon Armory
		  * The Bridge
		  * Escape Pod
		  
_______________________________________________________________________________________________

These are my notes:  

IDEA: After completing the Bridge scene, implement a global counter to expire in X minutes.
		