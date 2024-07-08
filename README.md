# coffee-go-drone

## Things to note

Character Description of tile 
X Building Tile (drone can’t go here) 
. Road Tile (drone can fly here) 
s The start location of the drone 
e The end location to deliver the coffee 

get up to 50 X 50 dimensions for city map

drone is red triangle


## Flow

- Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)
    - when f is pressed, calculate path and display shortest path in yellow circles

- Automatic Pilot: Press ‘g’ to follow pre-calculated path.
    - When g is pressed, the drone follows the path slowly 

- Automatic Pilot: Following pre-calculated path. Press ‘p’ to toggle pause/resume.
    - pressing p will pause the drone and pressing it again will unpause it