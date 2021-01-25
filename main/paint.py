try:
    import pygame
except:
    import install_requirements
    import pygame
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from gridModule import colorPallet
from gridModule import pixelArt
from gridModule import menu

import sys

sys.setrecursionlimit(1000000)

pygame.init()  
paintBrush = pygame.image.load("Paintbrush.png")
currentVersion = 1.1

# Set defaults for our screen size and rows and columns
rows = 50
cols = 50
wid = 600
heigh = 600

checked = []


def fill(spot, grid, color, c):
    if spot.color != c:
        pass
    else:
        spot.click(grid.screen, color)
        pygame.display.update()

        i = spot.col  
        j = spot.row  

        # Horizontal and vertical neighbors
        if i < cols - 1:  # Right
            fill(grid.getGrid()[i + 1][j], grid, color, c)
        if i > 0:  # Left
            fill(grid.getGrid()[i - 1][j], grid, color, c)
        if j < rows - 1:  # Up
            fill(grid.getGrid()[i][j + 1], grid, color, c)
        if j > 0:  # Down
            fill(grid.getGrid()[i][j - 1], grid, color, c)


def save(cols, rows, show, grid, path):
    if len(path) >= 4:  # This just makes sure we have .txt at the end of our file selection
        if path[-4:] != '.txt':
            path = path + '.txt'
    else:
        path = path + '.txt'

    # Overwrite the current file, or if it doesn't exist create a new one
    file = open(path, 'w')
    file.write(str(cols) + ' ' + str(rows) + ' ' + str(show) + '\n')

    for pixel in grid:
        for p in pixel:  
            wr = str(p.color[0]) + ',' + str(p.color[1]) + ',' + str(p.color[2])
            file.write(wr + '\n')
    file.write(str(currentVersion))

    file.close()
    name = path.split("/")
    changeCaption(name[-1])

def openFile(path):
    global grid

    file = open(path, 'r')
    f = file.readlines()
    if f[-1] == str(currentVersion):

        dimensions = f[0].split()  
        columns = int(dimensions[0])
        rows = int(dimensions[1])

        if dimensions[
            2] == '0':  
            v = False
        else:
            v = True
        initalize(columns, rows, v)  
        name = path.split("/")
        changeCaption(name[-1])

        line = 0
        for i in range(columns):  
            for j in range(rows):
                line += 1
                nColor = []
                for char in f[line].strip().split(','):
                    nColor.append(int(char))

                grid.getGrid()[i][j].show(win, tuple(nColor), 0)  
    else:
        window = Tk()
        window.withdraw()
        messagebox.showerror("Unsupported Version",
                             "The file you have opened is created using a previous version of this program. Please open it in that version.")


# Change pygame caption
def changeCaption(txt):
    pygame.display.set_caption(txt)

    
def showFileNav(op=False):
    
    window = Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    myFormats = [('Windows Text File', '*.txt')]
    if op:
        filename = askopenfilename(title="Open File", filetypes=myFormats)  
    else:
        filename = asksaveasfilename(title="Save File",
                                     filetypes=myFormats)  

    if filename:  
        x = filename[:]  
        return x


def onsubmit(x=0):
    global cols, rows, wid, heigh

    st = rowsCols.get().split(',')  
    window.quit()
    window.destroy()
    try:  
        if st[0].isdigit():
            cols = int(st[0])
            while 600 // cols != 600 / cols:
                if cols < 300:
                    cols += 1
                else:
                    cols -= 1
        if st[1].isdigit():
            rows = int(st[1])
            while 600 // rows != 600 / rows:
                if rows < 300:
                    rows += 1
                else:
                    rows -= 1
        if cols > 300:
            cols = 300
        if rows > 300:
            rows = 300

    except:
        pass


def updateLabel(a, b, c):
    sizePixel = rowsCols.get().split(',')  
    l = 12
    w = 12

    try:
        l = 600 / int(sizePixel[0])
    except:
        pass

    try:
        w = 600 / (int(sizePixel[1]))
    except:
        pass

    label1.config(text='Pixel Size: ' + str(l) + ', ' + str(w))  # Change label to show pixel size


# CREATE SCREEN
def initalize(cols, rows, showGrid=False):
    global pallet, grid, win, tools, lineThickness, saveMenu

    
    try:
        del grid
    except:
        pass

    pygame.display.set_icon(paintBrush)
    win = pygame.display.set_mode((int(wid), int(heigh) + 100))
    pygame.display.set_caption('By Rizwan.AR')
    win.fill((255, 255, 255))

    # CREATION OF OBJECTS
    grid = pixelArt(win, int(wid), int(heigh), cols, rows, showGrid)
    grid.drawGrid()

    pallet = colorPallet(win, 90, 90, 3, 3, True, 10, grid.height + 2)
    pallet.drawGrid()

    colorList = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 168, 0),
                 (244, 66, 173), (65, 244, 226)]
    pallet.setColor(colorList)

    tools = menu(win, 200, 40, 5, 1, True, grid.width - 210, grid.height + 50)
    tools.drawGrid()

    buttons = ['D', 'E', 'F', 'R', 'C']
    tools.setText(buttons)
    tools.drawGrid()

    l = tools.getGrid()
    l[0][0].show(grid.screen, (255, 0, 0), 1, True)

    lineThickness = menu(win, 180, 40, 4, 1, True, grid.width - 200, grid.height + 10)
    lineThickness.drawGrid()

    buttons = ['1', '2', '3', '4']
    lineThickness.setText(buttons)

    saveMenu = menu(win, 140, 40, 2, 1, True, grid.width - 400, grid.height + 25)
    saveMenu.drawGrid()

    buttons = ['Save', 'Open']
    saveMenu.setText(buttons)

    pygame.display.update()

window = Tk()
window.title('Draw')

t_var = StringVar()
t_var.trace('w', updateLabel)

label = Label(window, text='# Of Rows and Columns (25,50): ')
rowsCols = Entry(window, textvariable=t_var)

label1 = Label(window, text="Pixel Size: 12.0, 12.0")
var = IntVar()
c = Checkbutton(window, text="View Grid", variable=var)
submit = Button(window, text='Submit', command=onsubmit)
window.bind('<Return>', onsubmit)

submit.grid(columnspan=1, row=3, column=1, pady=2)
c.grid(column=0, row=3)
label1.grid(row=2)
rowsCols.grid(row=0, column=1, pady=3, padx=8)
label.grid(row=0, pady=3)

window.update()
mainloop()


initalize(cols, rows, var.get())
pygame.display.update()
color = (0, 0, 0)  
thickness = 1
replace = False
doFill = False
savedPath = ''  

run = True
while run:
    
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            window = Tk()
            window.withdraw()
            
            if pygame.display.get_caption()[0].count('*') > 0:
                if messagebox.askyesno("Save Work?", "Would you like to save before closing?"):
                    
                    if savedPath != "":
                        save(cols, rows, grid.showGrid, grid.getGrid(), savedPath)
                    else:
                        path = showFileNav()
                        if path:
                            savedPath = path
                            save(cols, rows, grid.showGrid, grid.getGrid(), savedPath)
            run = False

        if pygame.mouse.get_pressed()[0]:  
            try:
                pos = pygame.mouse.get_pos()
                if pos[1] >= grid.height:  
                    if pos[0] >= tools.startx and pos[0] <= tools.startx + tools.width and pos[1] >= tools.starty and \
                            pos[1] < + tools.starty + tools.height:  
                        replace = False
                        doFill = False
                        tools.drawGrid()  
                        buttons = ['D', 'E', 'F', 'R', 'C']
                        tools.setText(buttons)

                        clicked = tools.clicked(pos)
                        clicked.show(grid.screen, (255, 0, 0), 1, True)

                        # Depending what tool they click
                        if clicked.text == 'D':  # Draw tool
                            color = (0, 0, 0)
                        elif clicked.text == 'E':  # Erase tool
                            color = (255, 255, 255)
                        elif clicked.text == 'F':  # Fill tool
                            doFill = True
                        elif clicked.text == 'R':  # Replace tool
                            replace = True
                        elif clicked.text == 'C':  # Clear grid tool
                            grid.clearGrid()
                            tools.drawGrid()  
                            buttons = ['D', 'E', 'F', 'R', 'C']
                            tools.setText(buttons)
                            l = tools.getGrid()
                            l[0][0].show(grid.screen, (255, 0, 0), 1, True)

                   
                    elif pos[0] >= pallet.startx and pos[0] <= pallet.startx + pallet.width and pos[
                        1] >= pallet.starty and pos[1] <= pallet.starty + pallet.height:
                        clicked = pallet.clicked(pos)
                        color = clicked.getColor()  

                        pallet = colorPallet(win, 90, 90, 3, 3, True, 10, grid.height + 2)
                        pallet.drawGrid()

                        colorList = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                                     (255, 168, 0), (244, 66, 173), (65, 244, 226)]
                        pallet.setColor(colorList)
                        clicked.show(grid.screen, (255, 0, 0), 3, True)

                    elif pos[0] >= lineThickness.startx and pos[0] <= lineThickness.startx + lineThickness.width and \
                            pos[1] >= lineThickness.starty and pos[1] <= lineThickness.starty + lineThickness.height:
                        lineThickness.drawGrid()  
                        buttons = ['1', '2', '3', '4']
                        lineThickness.setText(buttons)

                        clicked = lineThickness.clicked(pos)
                        clicked.show(grid.screen, (255, 0, 0), 1, True)

                        thickness = int(clicked.text)  

                    # If they click on the save menu
                    elif pos[0] >= saveMenu.startx and pos[0] <= saveMenu.startx + saveMenu.width and pos[
                        1] >= saveMenu.starty and pos[1] <= saveMenu.starty + saveMenu.height:
                        clicked = saveMenu.clicked(pos)

                        if clicked.text == 'Save':  
                            path = showFileNav()
                            if path:
                                savedPath = path
                                save(cols, rows, grid.showGrid, grid.getGrid(), savedPath)
                        else:  
                            path = showFileNav(True)
                            if path:
                                openFile(path)
                                savedPath = path
                          
                else:
                    if replace:  
                        tools.drawGrid()  
                        buttons = ['D', 'E', 'F', 'R', 'C']
                        tools.setText(buttons)

                        tools.getGrid()[0][0].show(grid.screen, (255, 0, 0), 1, True)

                        clicked = grid.clicked(pos)
                        c = clicked.color
                        replace = False

                        for x in grid.getGrid():
                            for y in x:
                                if y.color == c:
                                    y.click(grid.screen, color)
                    elif doFill:
                        clicked = grid.clicked(pos)
                        if clicked.color != color:
                            fill(clicked, grid, color, clicked.color)
                            pygame.display.update()

                    else:  
                        name = pygame.display.get_caption()[0]
                        if name.find("*") < 1:
                            changeCaption(name + '*')

                        clicked = grid.clicked(pos)
                        clicked.click(grid.screen, color)
                        if thickness == 2:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                        elif thickness == 3:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                        elif thickness == 4:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                                    for x in p.neighbors:
                                        x.click(grid.screen, color)

                pygame.display.update()
            except AttributeError:
                pass

pygame.quit()
