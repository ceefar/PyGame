# PyGame - Winner Winner Zombie Dinner   

### Project Status
This version has seen a large overhaul since its inception, currently in a private repo which I will be moving to public shortly. Drastically improved new version includes some advanced pathfinding algorithms (which I'm currently finishing up), Breadth First Search, Dijkstra's, & A*.   
  
Check out the small image showcase below for a preview of the improved UI and upcoming functionality! v2 version expected live at the start of November, & I will create a .exe of the project shortly after.  
  
### Notable Features  
Please note that lots of functionality is missing or not shown in the below screenshots which are taken from test versions, as such UI and final v2 functionality has improved substantially on what is being previewed below :D   
*(please excuse low image quality, this repo is massively temporary, I just wanted to lay down something quick for now)*  

**Pathfinder, Pathfinder, Find Me A Path**     
Currently in development, implementation of advanced algorithms & data structures - Version in the image showing BFS (Breadth First Search) & Graph/Nodes working as expected, plus zombie path being rendered to screen for debugging     
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/pathfinding2.png" width="800">   

**Winner Winner ~~Chicken~~ Zombie Dinner**    
Casino roller triggers on player level up, granting items or bonuses if the reels land on a winner, this level up gambling mechanic will be a large part of the game loop. We can also see the initial implementation of character conversations here too
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/casinoAndConvo2.png" width="800">  
    
**Day & Night (wut wut)**  
Implementation of a basic day and night cycle... and yes that is a kid cudi reference  
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/daynight1.png" width="800">  

**There's A Bug Here Somewhere... I Can Feel It**     
Effectively coding collisions can be tough, particularly in pygame, handy debug mode helps by drawing hitboxes and constraints for all sprites on screen. I'm considering moving to pixel perfect collisions at some point in the future, for now these are just basic sprite collisions.    
*Please note title is just a joke, project is surprisingly error free and incredibly stable except for ongoing pathfinding work*  
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/debugmode1.png" width="800">    
    
**Clumping, Basic Pathfinding, UI's, Efficiencies**  
Added avoid radius where zombies inside the radius of another will 'push' slightly in the opposite direction, can also see some basic pathfinding, level and hp UI, and effeciencies for notable amount of enemies on screen (Pygame runs off the CPU so it can get taxing)
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/clumping.png" width="800">   
     
**Say Cheese**  
For fun selfie functionaliity, grants player temporary bonus gold/stats, note that the lego man polaroid is because the player sprite will be a lego character, have done a basic animated custom sprite already but don't use animations (except for basic item tweening) during development. Dynamic image gen coming at some point.
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/selfie1.png" width="800">  
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/selfie2.png" width="800">  

**Guns... Lots of Guns**  
Weapons, pickups, ammo, weapon constraints, critical hits, reloading and ammo count ui   
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/reloading1.png" width="800">   

**Ouch... Ouch... Ouch**    
Breaking a leg will cause the player to become injured, reducing accuracy and movement speed while also causing the player to walk with a limp, making shooting and escaping much harder, the player will need to find a health pack (or 3) to heal to the required threshold to remove this debuff.  
<img src="https://github.com/ceefar/PyGame/blob/master/RepoImages/injury2.png" width="800">    

  
  
### Why This Project?  
Taking a break from quite a gruelling period on my NHS Waiting Times Web App to work on something to showcase both front end skills, mathematical ability, and OOP concepts. 
  
### Learning Objectives  
Primary aim is to really deep dive into OOP and class based structure, and arguably the best enviornment for OOP is a game environment (lots of reapeated objects, lots of complex relationships between classes).   
Secondary aim is to explore some of the more intermediate and advanced concepts in python and relearn some of the things I knew once from mathematics for graphics and rendering, and algorithms like Breadth First Search.    
   
#### Initial v0.1 Basic Functionality *(outdated)*
- Basic tile based interaction laid down, moving, walls, tilemap, etc    
- Super basic sprint functionality  
- Super basic breakable walls and upgradable walls  
- Added wall collisions  
- Implementing dynamic camera  
- Upgraded sprites to vectors 
- Upgraded is_near to use pythagoras for distances  
- Proper breakable wall collisions  
- Improved breakable walls with highlighting and building indicators  
- Removed upgradable walls for now  
