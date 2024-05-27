from tkinter import *
from tkinter.messagebox import *
import  copy
root = Tk()
root.title(" 推箱子 ")

imgs= [PhotoImage(file='box_images\\Wall.gif'),
       PhotoImage(file='box_images\\Worker.png'),
       PhotoImage(file='box_images\\Box.gif'),
       PhotoImage(file='box_images\\Passageway.gif'),
       PhotoImage(file='box_images\\Destination.png'),
       PhotoImage(file='box_images\\WorkerInDest.png'),
       PhotoImage(file='box_images\\RedBox.png') ]

Wall = 0         # 0代表墙壁
Worker = 1       # 1代表工人
Box = 2          # 2代表箱子
Passageway = 3   # 3代表通道
Destination = 4  # 4代表目的地
WorkerInDest = 5 # 5代表工人位于目的地
RedBox = 6       # 6代表箱子位于目的地

# 游戏地图
myArray1 = [[0,0,3,3,3,4,0,0,0],
          [0,3,3,3,0,0,3,3,0],
          [3,3,2,3,3,3,3,2,0],
          [3,3,2,1,0,0,0,3,0],
          [4,0,3,2,0,4,0,3,0],
          [0,3,0,3,3,3,3,3,4],
          [3,3,3,3,3,3,0,3,3],
          [3,3,2,3,2,3,3,3,3],
          [4,0,3,3,0,0,0,0,4]]


#绘制整个游戏区域图形
def drawGameImage( ):
    global x,y
     
    for i in range(0,9) :   #0--8
       for j in range(0,9) :   #0--8
            if myArray[i][j] == Worker :
               x=i  #工人当前位置(x,y)
               y=j
               print("工人当前位置:",x,y)
            img1= imgs[myArray[i][j]]
            cv.create_image((i*32+20,j*32+20),image=img1)
            cv.pack()

def callback(event) :   #按键处理函数
    global x,y,myArray
    print ("按下键：", event.char)
    KeyCode = event.keysym
    #工人当前位置(x,y)，而(x1,y1)、(x2,y2)分别代表工人移动前方的两个方格的坐标
    if KeyCode=="Up":   #如果按了向上键
    #工人向上前进一步
            x1 = x;
            y1 = y - 1;
            x2 = x;
            y2 = y - 2;
            #将所有位置输入以判断并作地图更新
            MoveTo(x1, y1, x2, y2);
    #工人向下前进一步
    elif KeyCode=="Down":   #如果按了向下键
            x1 = x;
            y1 = y + 1;
            x2 = x;
            y2 = y + 2;
            MoveTo(x1, y1, x2, y2);
    #工人向左前进一步
    elif KeyCode=="Left":   #如果按了向左键
            x1 = x - 1;
            y1 = y;
            x2 = x - 2;
            y2 = y;
            MoveTo(x1, y1, x2, y2);
    #工人向右前进一步
    elif KeyCode=="Right":   #如果按了向右键
            x1 = x + 1;
            y1 = y;
            x2 = x + 2;
            y2 = y;
            MoveTo(x1, y1, x2, y2);
    elif KeyCode=="space":   #如果按了空格键
       print ("按下键：空格", event.char)
       myArray=copy.deepcopy(myArray1)  #恢复原始地图
       drawGameImage( )

#判断是否在游戏区域
def IsInGameArea(row, col) :
    return (row >= 0 and row < 9 and col >= 0 and col < 9)

def MoveTo(x1, y1, x2, y2) :        #定义移动工人和箱子的函数
        global x,y
        P1=None
        P2=None
        if IsInGameArea(x1, y1) :   #判断是否在游戏区域
            P1=myArray[x1][y1];
        if IsInGameArea(x2, y2) :
            P2 = myArray[x2][y2]
        if P1 ==  Passageway :      #如果P1处为通道
            MoveMan(x,y);
            x = x1; y = y1;
            myArray[x1][y1] =  Worker; 
        if P1 ==  Destination :     #如果P1处为目的地
            MoveMan(x, y);
            x = x1; y = y1;
            myArray[x1][y1] =  WorkerInDest;
        if P1 ==  Wall or  not IsInGameArea(x1, y1) : #如果P1处为墙壁或出界
            return;
        if P1 ==  Box  :            #如果P1处为箱子
           if P2 ==  Wall or  not IsInGameArea(x1, y1) or P2 ==  Box : #如果P2处为墙或出界
              return;
        if P1 ==  Box and P2 ==  Passageway :   #如果P1处为箱子,P2处为通道
            MoveMan(x, y);
            x = x1; y = y1;
            myArray[x2][y2]= Box;
            myArray[x1][y1] =  Worker;
        if P1 ==  Box and P2 ==  Destination :  #如果P1处为箱子,P2处为目的地
            MoveMan(x, y);
            x = x1; y = y1;
            myArray[x2][y2]= RedBox;
            myArray[x1][y1] =  Worker;
        if P1 ==  RedBox and P2 ==  Passageway :  #如果P1处为放到目的地的箱子,P2处为通道
            MoveMan(x, y);
            x = x1; y = y1;
            myArray[x2][y2] =  Box;
            myArray[x1][y1] =  WorkerInDest;
        if P1 ==  RedBox and P2 ==  Destination :  #P1处为放到目的地的箱子,P2处为目的地
            MoveMan(x, y);
            x = x1; y = y1;
            myArray[x2][y2] =  RedBox;
            myArray[x1][y1] =  WorkerInDest;
        drawGameImage()
        #这里要验证游戏是否过关
        if IsFinish() :
            showinfo(title="提示",message=" 恭喜你顺利过关" ) 

def  MoveMan(x, y) :
    if myArray[x][y] == Worker :
        myArray[x][y] = Passageway;
    elif myArray[x][y] == WorkerInDest :
        myArray[x][y] = Destination;

def IsFinish( ):      #验证是否过关
    bFinish = True;
    for i in range(0,9) :#0--9
       for j in range(0,9) :#0--9
            if  (myArray[i][j] == Destination
                   or myArray[i][j] == WorkerInDest) :
                bFinish = False;
    return bFinish;

def drawQiPan( ):      #画棋盘
    for i in range(0,15) :
        cv.create_line(20,20+40*i,580,20+40*i,width=2)
    for i in range(0,15) :
        cv.create_line(20+40*i,20,20+40*i,580,width=2)
    cv.pack()

def print_map( ) :#输出map地图
    for i in range(0,9) :     #0--9
       for j in range(0,9) :  #0--9
           print (map[i][j],end=' ')
       print ('w')

cv = Canvas(root, bg = 'green', width = 292, height = 292)
#drawQiPan( )
myArray=copy.deepcopy(myArray1) 
drawGameImage()
cv.bind("<KeyPress>", callback)
cv.pack()
cv.focus_set()    #将焦点设置到cv上
root.mainloop()
