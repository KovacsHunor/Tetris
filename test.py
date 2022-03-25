import random, time, keyboard, serial, copy


table = [[False for i in range(24)] for j in range(7)]
shape = [[[[False for i in range(4)] for j in range(4)] for k in range(4)] for l in range(7)]
shapetable = "0000111100000000001000100010001000000000111100000100010001000100100011100000000001100100010000000000111000100000010001001100000000101110000000000100010001100000000011101000000011000100010000000110011000000000011001100000000001100110000000000110011000000000011011000000000001000110001000000000011011000000100011000100000001001110000000000100011001000000000011100100000001001100010000001100011000000000001001100100000000001100011000000100110010000000"

uptable = [[[1,1,1,1],[0,0,0,0]], [[1,1,1,0],[0,0,1,0]], [[1,1,1,0],[1,0,0,0]], [[1,1,0,0],[1,1,0,0]], [[0,1,1,0],[1,1,0,0]], [[1,1,1,0],[0,1,0,0]], [[1,1,0,0],[0,1,1,0]]]
 
game = True
ystart = 4
class Shapes:
    
    def __init__(self):
        self.x, self.y, self.object, self.rotation, self.former = (2, 4, 0, 0, [[0,0,0,0],[0,0,0,0]])

    def PosDown(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if self.y + j == 23 and shape[self.object][self.rotation][i][j]:
                    return 1
                elif i + self.x < 7 and j + self.y + 1 < 24:
                    if (table[i + self.x][j + self.y + 1] and shape[self.object][self.rotation][i][j]):
                        return 1
        return 0
    
    def Down(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if i + self.x < 7 and j + self.y < 24:
                    if (table[i + self.x][j + self.y] and shape[self.object][self.rotation][i][j]):
                        return 1
        return 0 
    
    def PosRight(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if self.x + i + 1 > 6 :
                    if shape[self.object][self.rotation][i][j]:
                        return 1
                elif j + self.y < 24:
                    if table[i + self.x + 1][j + self.y] and shape[self.object][self.rotation][i][j]:
                        return 1
        return 0
    
    def PosLeft(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if self.x + i - 1 > 6 :
                    if shape[self.object][self.rotation][i][j]:
                        return 1
                elif j + self.y < 24:    
                    if table[i + self.x - 1][j + self.y] and shape[self.object][self.rotation][i][j]:
                        return 1
        return 0
    
    def Right(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if self.x + i > 6 :
                    if shape[self.object][self.rotation][i][j]:
                        return 1
                elif self.x + i < 7 and j + self.y < 24:
                    if table[i + self.x][j + self.y] and shape[self.object][self.rotation][i][j]:
                        return 1
        return 0
    
    def Left(self):
        for i in range (3, -1, -1):
            for j in range (3, -1, -1):
                if self.x + i < 0:
                    if shape[self.object][self.rotation][i][j]:
                        return 1
                elif self.x + i < 7 and self.y + j < 24:
                    if table[i + self.x][j + self.y] and shape[self.object][self.rotation][i][j]:
                        return 1
        return 0
    
    def Next(self, n):
        global ystart
        self.object = n
        self.rotation = 0
        self.x = 2
        self.y = ystart
        for i in range(0, 2):
            for j in range(0, 4):
                self.former[i][j] = 0
        if(self.Down()):
            if(self.Down()):
                ystart = 0
                self = copy.deepcopy(nexta)
                nexta.Next(Random())
        return 0

ran = [i for i in range(7)]
pt = 0
def Random():
    global pt
    pt -= 1
    if (pt == -1):
        bag = [0, 1, 2, 3, 4, 5, 6] 
        for i in range(6):
            n = random.randint(0, 6-i)
            ran[6-i] = bag[n]
            bag[n] = bag[6-i]
        pt = 6
    return ran[pt]
        
    
    

nexta = Shapes()
hold = Shapes()
tetrimino = Shapes()

first = True
canhold = True

verlim = 0
horlim = 0
rotlim = 0
rottime = 0
rotbool = False
rothelp = False
anim = 1

fokgyem = [0 for i in range(21)]
out = [[0 for i in range(24)] for j in range(7)]
arduino = serial.Serial("COM6", 19200, timeout = 3)

def send():
    for i in range(3):
        for j in range(7):
            if (j >= 0 and j < 4 and i >= 0 and i < 2):
                out[j][i] = uptable[nexta.object][i][j]
            else:
                out[j][i] = table[j][i]
    if not first:
        for i in range(3):
            for j in range(7):
                if (6-j >= 0 and 6-j < 4 and 2-i >= 0 and 2-i < 2):
                    out[j][i] = uptable[hold.object][2-i][6-j]
    for i in range(7):
        out[i][3] = True
    for i in range(4, 24):
        for j in range(7):
            if (j >= tetrimino.x and j < tetrimino.x + 4 and i >= tetrimino.y and i < tetrimino.y + 4):
                out[j][i] = (table[j][i] or shape[tetrimino.object][tetrimino.rotation][j - tetrimino.x][i - tetrimino.y])
            else:
                out[j][i] = table[j][i]
    for i in range(0, 7):
        for j in range(0, 3):
            n = 0
            for k in range(0, 8):
                if out[i][24-(j+1)*8+k]:
                    n += 2**k
            fokgyem[i*3+j] = n
    
    arduino.write(fokgyem)
    
def end():
    for i in range(0, 7):
        for j in range(0, 3):
            n = 0
            for k in range(0, 8):
                if out[i][24-(j+1)*8+k]:
                    n += 2**k
            fokgyem[i*3+j] = n
    
    arduino.write(fokgyem)
    

speed = 0
acceleration = 0.0
drop = False
dropb = False
tetrimino.Next(Random())
nexta.Next(Random())
for g in range(0, 7):
    for b in range(0, 4):
        for c in range(0, 4):
            for d in range(0, 4):
                if shapetable[64 * g + 16 * b + 4 * c + d] == '1':
                    shape[g][b][d][c] = True
                else:
                    shape[g][b][d][c] = False
               
     
lastframe = int(time.process_time() * 55)
l = 1
enddelay = 0
while (game):
    if tetrimino.PosDown() == 1:
        if not rothelp:
            rottime = 1
            rothelp = True
        if rottime == 0 or rotbool:
            for c in range(0, 4):
                for b in range(0, 4):
                    if tetrimino.x + c < 7 and tetrimino.y + b < 24:
                        table[tetrimino.x + c][tetrimino.y + b] = table[tetrimino.x + c][tetrimino.y + b] or shape[tetrimino.object][tetrimino.rotation][c][b]
            drop = False
            tetrimino = copy.deepcopy(nexta)
            nexta.Next(Random()) 
            canhold = True
            rotbool = False
            rottime = 0
            rothelp = False
        if ystart == 0:
            enddelay = (enddelay+1)%80
            if enddelay == 0:
                game = False
    frame = int(time.process_time() * 55)
    if lastframe != frame:
        if (horlim != 0):
            horlim = (horlim + 1) % 10
        if rotlim != 0:
            rotlim = (rotlim + 1) % 10
        if anim == 0:
            send()
        if rottime != 0:
            rottime = (rottime + 1) % 200
        anim = (anim + 1) % 10
        #input logic:
        if horlim == 0:
            if keyboard.is_pressed('a'):
                if tetrimino.PosLeft() == 0:
                    tetrimino.x -= 1
                    horlim = 1
            if keyboard.is_pressed('d'):
                if tetrimino.PosRight() == 0:     
                    tetrimino.x += 1
                    horlim = 1
        if keyboard.is_pressed('s'):
            speed = 56
        elif acceleration < 52:
            speed = int(acceleration)
                
        if keyboard.is_pressed('space'):
            if not dropb:
                rotbool = True
                drop = True
                dropb = True
        else:
            dropb = False
        
        if keyboard.is_pressed('up') and canhold:
            if first:
                hold = copy.deepcopy(tetrimino)
                hold.Next(hold.object)
                tetrimino = copy.deepcopy(nexta)
                nexta.Next(Random())
                first = False
            else:
                swap = copy.deepcopy(hold)
                hold = copy.deepcopy(tetrimino)
                tetrimino = copy.deepcopy(swap)
                hold.Next(hold.object)
            canhold = False
                
        if rotlim == 0:
            prerot = tetrimino.rotation
            prelim = rotlim
            prex = tetrimino.x
            if keyboard.is_pressed('left'):
                tetrimino.rotation = (tetrimino.rotation + 3) % 4
                rotlim += 1
                rottime -= 2
            if keyboard.is_pressed('right'):
                tetrimino.rotation = (tetrimino.rotation + 1) % 4
                rotlim += 1
                rottime -= 2
            i = 0
            while tetrimino.Left() == 1 and i < 4:
                tetrimino.x+=1
                i+=1
            i = 0
            while tetrimino.Right() == 1 and i < 8:
                tetrimino.x-=1
                i+=1
            i = 0
            while (tetrimino.Down() == 1):
                tetrimino.y-=1
            if tetrimino.Left() == 1 or tetrimino.Right() == 1:
                tetrimino.x = prex
                tetrimino.rotation = prerot
                rotlim = prelim
        for i in range(4,24):
            full = True
            for j in range(0, 7):
                if table[j][i] == False:
                    full = False
            if (full):
                acceleration += 2
                for j in range(0, 7):
                    table[j][i] = False
                for j in range(i, 0, -1):
                    for a in range(0, 7):
                        table[a][j] = table[a][j - 1]
                for j in range(0, 7): 
                
                    table[j][0] = False
        #move logic:
        if ((l == 0 or drop)):
            if (rottime == 0 or tetrimino.PosDown() == 0):
                tetrimino.y+=1
        lastframe = frame
        l = (l + 1) % (60 - speed)
out = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]               
if False:
    out = [[0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0]]
table = out
end()