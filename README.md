# coffee-go-drone

## Things to note

Character Description of tile 
X Building Tile (drone can’t go here) 
. Road Tile (drone can fly here) 
s The start location of the drone 
e The end location to deliver the coffee 

## Flow

- Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)
    - when f is pressed, calculate path and display shortest path in yellow circles

- Automatic Pilot: Press ‘g’ to follow pre-calculated path.
    - When g is pressed, the drone follows the path slowly 

- Automatic Pilot: Following pre-calculated path. Press ‘p’ to toggle pause/resume.
    - pressing p will pause the drone and pressing it again will unpause it


| Key          | Action        | Description                                                                                   |
|--------------|---------------|-----------------------------------------------------------------------------------------------|
| `f`          | find          | Will calculate, and display, the shortest path from current drone location to coffee delivery location. |
| `g`          | go            | Will let the drone follow the current path.                                                   |
| `c`          | continue      | Will bring the drone back to manual operation after it has completed following a path.        |
| `r`          | reset         | Resets the drone to the original start location, as when the application started. If there is any path set, it will be cleared. |
| `p`          | pause/resume  | Will toggle pause/resume a drone that is following a path.                                    |
| `h`          | show/hide     | Will toggle show/hide of a path.                                                              |
| `left arrow` | move left     | Will move the drone to the tile at left (if free) and only if drone is in manual operation.   |
| `right arrow`| move right    | Will move the drone to the tile at right (if free) and only if drone is in manual operation.  |
| `up arrow`   | move up       | Will move the drone to the tile at top (if free) and only if drone is in manual operation.    |
| `down arrow` | move down     | Will move the drone to the tile at bottom (if free) and only if drone is in manual operation. |
| `q`          | quit          | Will quit the application                                                                     |
