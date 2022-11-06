add_library('minim')
import random

minim=Minim(this)
screen=1 #first screen
canvasSize = [1024,600] #x,y window size 
page1Size = [281, 411] #x,y first screen background size 
buttonStart = [25, 372, 281, 411] #x1,y1,x2,y2 start button
playerSpeed = 7
player = [50, (canvasSize[1]-54)/2, 43, 58] #player position x,y,w,h
bricks = [] #list of bricks, each is [x,y,w,h]
brickOffset = [0,0] #offset for bricks, each is draw at brick[0]-offset[0], brick[1]-offset[1]
level = 50
paused = False
finished = False
highScore = 0
keysDict = dict() 

def setup():
    global canvasSize, backImage, playerImage, backImage2, bricks, minim, music, keysDict
    
    size(canvasSize[0], canvasSize[1])#canvas size
    add_library('minim')
    music = minim.loadFile("Street Fighter II Arcade Music - Ryu Stage - CPS1.mp3")
    minim=Minim(this)
    music.play()
    music.loop

    #load images
    backImage = loadImage("page1.png")
    backImage2 = loadImage("page2.jpg")
    playerImage = loadImage("plane.gif")
    #text size
    textSize(20)

    #show page1 image
    image(backImage, (canvasSize[0]-page1Size[0])/2, (canvasSize[1]-page1Size[1])/2)
    
    #create bricks
    createBricks()
    #create dictionary
    createKeysDict()
    
    #display legend
    y = 20;
    fill(0,0,0)
    text("Press Start button to start playing", 10, y)
    y = y + 20
    text("Keys during play", 10, y)
    y = y + 20
    
    for k in keysDict:
        text(k + " : " + keysDict[k], 10, y)
        y = y + 20
        
def createKeysDict():
    global keysDict;
    keysDict["UP"] = "Move Up"
    keysDict["DOWN"] = "Move Down"
    keysDict["Left"] = "Move Left"
    keysDict["Right"] = "Move Right"
    keysDict["C"] = "Pause game"
    keysDict["Space"] = "Continue playing"
    keysDict["Mouse Drag"] = "Move"
    


def createBricks():
    global canvasSize, bricks 
    random.random()
    brickWidth = 40 #width of a brick
    brickHSpacing = player[2]*4 #horizontal space between bricks 
    brickVSpacing = player[3]*1.5 #vertical space between bricks 
    for i in range(level):
         r = random.randint(0, canvasSize[1]-player[3]-5) #max canvas height - player height - 5
         brick = [200+2*player[2]+i*(brickWidth+brickHSpacing), 0, brickWidth, int(r)] #top brick x,y,w,h 
         bricks.append(brick)
         brick = [200+2*player[2]+i*(brickWidth+brickHSpacing), int(r)+brickVSpacing, brickWidth, canvasSize[1]-(int(r)+brickVSpacing)] #bottom brick x,y,w,h 
         bricks.append(brick)
    
def draw():
    global screen, canvasSize, playerImage, backImage2, player, paused, finished, highScore
    if screen == 1:
        return
    if paused:
        return
    if finished:
        return
    
    #clear screen
    #background(0,0,153)
    image(backImage2, 0,0)
    
    #draw bricks
    fill(200,200,200)
    #move bricks by increment offset
    brickOffset[0] += 1 
    #brickOffset[1] += 1
    
    #check if win 
    if brickOffset[0]>bricks[len(bricks)-1][0]:#offset greater than last brick, all displayed
        finished = True;
        # show results
        showFinished(True, len(bricks))
        brickOffset[0] = 0;
        return
        
    # draw bricks
    for i in range(len(bricks)):
        x = brickLeft(bricks[i])
        y = brickTop(bricks[i])
        if x+bricks[i][2]>0 and x<canvasSize[0]:
            rect(x,y,bricks[i][2],bricks[i][3])
            
    # draw imageplayer 
    image(playerImage, player[0], player[1])

    #check if hit, returns brick number
    hit = playerHit()
    #if hit finished
    if hit >= 0:
        finished = True
        brickOffset[0] = 0;
        #show results
        showFinished(False, hit)

                
#return x coordinate of brick                
def brickLeft(brick):
    return brick[0]-brickOffset[0]
        
#return right coordinate of brick (x+width)        
def brickRight(brick):
    return brick[0]-brickOffset[0]+brick[2]

#return top coordinate of brick 
def brickTop(brick):
    return brick[1]-brickOffset[1]
        
#return bottom coordinate of brick(top + height)                
def brickBottom(brick):
    return brick[1]-brickOffset[1]+brick[3]

#return True when point intersects the brick
def pointIntersect(x,y, brick):
    return x < brickRight(brick) and x > brickLeft(brick) and y < brickBottom(brick) and y > brickTop(brick);
    
#return True when player intersects the brick
def playerIntersect(brick):
    global player, paused
    topleftIn = pointIntersect(player[0],player[1], brick)
    toprightIn = pointIntersect(player[0]+player[2],player[1], brick)
    bottomleftIn = pointIntersect(player[0],player[1]+player[3], brick)
    bottomrightIn = pointIntersect(player[0]+player[2],player[1]+player[3], brick)
    hit = topleftIn or toprightIn or bottomleftIn or bottomrightIn

    return hit

#return brick hit, -1 if no hit 
def playerHit():
    global bricks  
    
    hit = False
    counter = 0 #brick number 
    #iterate bricks and check if hit 
    brickLen = len(bricks) 
    while not hit and counter < brickLen:
        # check intersect 
        hit =  playerIntersect(bricks[counter])
        counter = counter+1
        
    if hit:
       return int(counter/2) #each line has 2 bricks, divide  
       
    #no hit
    return -1

# show results
def showFinished(won, hit):
    global canvasSize, finished, player, highScore
    #load and display sticker image
    img = loadImage("sticker.jpg")
    x = canvasSize[0]/2-100#middle
    y = canvasSize[1]/2-100#middle
    image(img, x, y)
    #move below image 
    y = y + 220 
    if not won:
        fill(255,0,0)#lost in red
        #show line hit 
        text("Line "+str(hit)+" was hit!", x, y)
        y = y + 20 
        #show result
        text("You LOST!", x, y)
        y = y + 20 
    else:
        fill(0,255,0)#won green
        text("You WON!", x, y)
        y = y + 20
    #calculate score 
    score = hit*7
    #calculate high high score
    if score > highScore:
        highScore = score
    
    #show score and high score 
    text("Points: " +  str(score) + ". High Score: " +  str(highScore), x, y)
    y = y + 20
    y = y + 20
    #show continue 
    text("Press SPACE key to play again", x, y)
    player = [50, (canvasSize[1]-54)/2, 43, 58] #player position x,y,w,h
    
         
#when mouse button pressed
def mousePressed():
    global screen, buttonStart, canvasSize, page1Size
    
    #only for screen 1
    if screen != 1:
        return
    #offset page 1 image to canvas
    x = mouseX-(canvasSize[0]-page1Size[0])/2
    y = mouseY-(canvasSize[1]-page1Size[1])/2
    #if click in Start button 
    if x >= buttonStart[0] and y >= buttonStart[1] and x <= buttonStart[2] and y <= buttonStart[3]:
        screen = 2 #change screen

#when key is pressed
def keyPressed():
    global playerSpeed, player, canvasSize, paused, finished
    #increment/decrement player coordinates 
    if keyCode == UP:
        player[1] -= playerSpeed
    if keyCode == DOWN:
        player[1] += playerSpeed
    if keyCode == LEFT:
        player[0] -= playerSpeed
    if keyCode == RIGHT:
        player[0] += playerSpeed
    
    #check boundaries
    if player[0] < 0:
        player[0] = 0
    if player[0] > canvasSize[0]-player[2]:
        player[0] = canvasSize[0]-player[2]
    if player[1] < 0:
        player[1] = 0
    if player[1] > canvasSize[1]-player[3]:
        player[1] = canvasSize[1]-player[3]
    #pause game
    if key == 'c' or key == 'C': 
        paused = True
    #continue or restart game
    if key == ' ':
        paused = False
        finished = False
 
#when mouse is dragged
def mouseDragged():
    global playerSpeed, player, canvasSize, paused, finished
    #do not move horizontal, player can jup at end
    #player[0] = mouseX
    #move vertical
    player[1] = mouseY 
 