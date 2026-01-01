# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 02:44:31 2023

@author: MOHAMED
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton,QLineEdit,QMessageBox, QRadioButton
from PyQt5.QtGui import QFont, QColor,QIcon
from PyQt5.QtCore import Qt
import heapq, time




class PuzzleWindow(QWidget):
    grid_values=[]
    text_box=None
    stop_flag=False
    stop_running_in_terminal= False
    dynamic_colors=[]
    optimal_path=[]
    def __init__(self):
        super().__init__()

        # Set up the grid layout for the buttons
        self.grid_layout = QGridLayout()# A new QGridLayout is created
        self.setLayout(self.grid_layout)# This means that any child widgets added to the PuzzleWindow will be arranged according to this grid layout.

        # Set up the font and color for the tiles defined in current method
        self.font_size = 20
        self.font = QFont('Arial', self.font_size)
        self.colors = [QColor('#FF6B6B'), QColor('#FFE66D'), QColor('#6ECB63'),QColor('#6ECB9F'), QColor('#6ED1CB'), QColor('#7C6ED1'),QColor('#D16EAD'), QColor('#D16E6E'), QColor('#D1A86E')]
        
        self.create_tiles()
        
        self.text_box = QLineEdit()
        self.grid_layout.addWidget(self.text_box, 3, 0,1,3)  # Add text2 to row 3, column 0
        # addWidget(object, row, column, rowSpan, columnSpan)
     
        
        self.read_button = QPushButton("Read Input")
        self.read_button.clicked.connect(self.read_input)
        self.grid_layout.addWidget(self.read_button, 4, 0, 1, 3)
        
        
        self.radioBFS = QRadioButton("BFS")
        self.radioDFS = QRadioButton("DFS")
        self.radioAStar = QRadioButton("A*")
        
        self.radioAStar.setChecked(True)

        self.grid_layout.addWidget(self.radioBFS, 5, 0, alignment=Qt.AlignHCenter)
        self.grid_layout.addWidget(self.radioDFS, 5, 1, alignment=Qt.AlignHCenter)
        self.grid_layout.addWidget(self.radioAStar, 5, 2, alignment=Qt.AlignHCenter)
  
        self.solving_button = QPushButton("Start")
        #self.solving_button.setEnabled(False)
        self.solving_button.clicked.connect(self.start_solving)
        self.grid_layout.addWidget(self.solving_button, 6, 0, 1, 3)# Add the "Start" button to the grid layout at row 3, column 0 and specify a row span of 1 and a column span of 3.

        # Add a "Stop" button to stop solving
        self.stop_button = QPushButton("Stop")
       # self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_solving)
        self.grid_layout.addWidget(self.stop_button, 7, 0, 1, 3)

        # Add a "Replay" button to replay solving
        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.replay_solving)
        self.grid_layout.addWidget(self.replay_button, 8, 0, 1, 3)

        # Set the window properties
        self.setWindowTitle("8-Puzzle-Solver")
        self.setWindowIcon(QIcon('IdlibIcon.png'))
        self.setGeometry(600, 300, 300, 300)
        self.show()

         
    def create_tiles(self):
        # Create the buttons and add them to the layout
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = QPushButton()
                button.setFixedSize(80, 80)
                button.setFont(self.font)
                index = i * 3 + j
                button.setStyleSheet("background-color: %s; color: black;" % self.colors[index].name())
                self.grid_layout.addWidget(button, i, j)
                self.buttons.append(button)
                
    
        
    def read_input(self):
        # Get the text from the text box and split it by spaces
        self.stop_flag = False
        self.grid_values=[]
        self.dynamic_colors= [QColor('#FFFFFF') for i in range(9)]
        
        for i in range(3):
            for j in range(3):
                button_in_grid = self.grid_layout.itemAtPosition(i, j).widget()
                button_in_grid.setText('')
                
        text = self.text_box.text()
        values = text.split()
        values = [values[i:i+3] for i in range(0, len(values), 3)] # reshape the list to 3 by 3   
        for i in range(3):
            self.grid_values.append(values[i])
            for j in range(3):
                button_in_grid = self.grid_layout.itemAtPosition(i, j).widget()
                if self.grid_values[i][j]!='0':
                    button_in_grid.setText(self.grid_values[i][j])
                    self.dynamic_colors[int(self.grid_values[i][j])]= self.colors[i * 3 + j]
                else:
                    button_in_grid.setStyleSheet("background-color: %s; color: black;" % self.dynamic_colors[0].name())
                    
        self.stop_running_in_terminal=False
        print (self.grid_values)
    
    
    def update_tiles(self):
        for i in range(3):
             for j in range(3):
                 button_in_grid = self.grid_layout.itemAtPosition(i, j).widget() 
                 if self.grid_values[i][j]=='0':
                     button_in_grid.setText('')
                     button_in_grid.setStyleSheet("background-color: %s; color: black;" % self.dynamic_colors[0].name())
                 else:
                     button_in_grid.setText(self.grid_values[i][j]) 
                     index = int (self.grid_values[i][j])
                     button_in_grid.setStyleSheet("background-color: %s; color: black;" % self.dynamic_colors[index].name())
                     button_in_grid.update()
                 QApplication.processEvents()
       
    def start_solving(self):
        
        flat_grid_values = [elem for row in self.grid_values for elem in row]
        
        flat_grid_values=[]
        for row in self.grid_values:
            for item in row:
                flat_grid_values.append(item)
                
        inversion_count = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if flat_grid_values[i] != '0' and flat_grid_values[j] != '0' and flat_grid_values[i] > flat_grid_values[j]:
                    inversion_count += 1
        if (inversion_count % 2 == 0):
            intial_state=list(map(lambda x: list(map(int, x)), self.grid_values))
            puz = puzzle(intial_state) # create an instance of the Node class and assigns it to the variable puz
            if self.radioBFS.isChecked():
                self.optimal_path=puz.solve_BFS()
            if self.radioDFS.isChecked():
                self.optimal_path=puz.solve_DFS()
            if self.radioAStar.isChecked():
                self.optimal_path=puz.solve_Astar()
                
            self.stop_running_in_terminal= False 
            
        else :
           QMessageBox.information(None, 'AI-Lab', 'The state is not solvable')
   

    def stop_solving(self):
        self.stop_flag = True
        self.stop_running_in_terminal= True 
    
 

    def closeEvent(self, event):
        self.stop_running_in_terminal= True 
        print("Goodbye!")
        event.accept()
        
    def replay_solving(self):   
        for state in self.optimal_path:
            self.grid_values=list(map(lambda row: list(map(str, row)), state))
            time.sleep(1)
            self.update_tiles()
        QMessageBox.information(None, 'AI-Lab', f'The path length is {len(self.optimal_path)-1}')
            
     

##################################################################################################################

class Node:
    def __init__(self, state, parent=None, move=0, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.heuristic = self.manhattan_distance()
        self.score = self.depth + self.heuristic
        

    def __lt__(self, other):
        return self.score < other.score

    def manhattan_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    row = (self.state[i][j] - 1) // 3
                    col = (self.state[i][j] - 1) % 3
                    distance += abs(i - row) + abs(j - col)
        return distance

    def get_moves(self):
        moves = []
        i, j = self.get_blank_position()
        if i > 0:
            moves.append('up')
        if i < 2:
            moves.append('down')
        if j > 0:
            moves.append('left')
        if j < 2:
            moves.append('right')
        return moves

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def move_blank(self, direction):
        i, j = self.get_blank_position()
        new_state = [row[:] for row in self.state]  # create a new copy of the state
        if direction == 'up':
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down':
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left':
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right':
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        return Node(new_state, self, direction, self.depth + 1)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))
    
class puzzle:
    
    def __init__(self,iput_state):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.initial_state = iput_state
      
    def solve_BFS(self):
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        queue = []
        visited = set()
        queue.append(start_node)
        while queue:
            QApplication.processEvents()
            if window.stop_flag:
                return
            if  window.stop_running_in_terminal:
                        return
            current_node = queue.pop(0)
            window.grid_values= list(map(lambda row: list(map(str, row)), current_node.state))
            window.update_tiles()
            visited.add(current_node)
            if current_node.heuristic == 0:
                path = []
                node = current_node
                while node:
                    path.append(node.state)
                    node = node.parent
                path.reverse()
                return path
            #print (current_node.state)
            #time.sleep(2)
            for move in current_node.get_moves():
                child_node = current_node.move_blank(move)

                if child_node not in visited:
                    queue.append(child_node)
        else:
            path = []
            node = current_node
            # for row in node.state: print(row)
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.reverse()
            # print(path)
            return path  
    
    def solve_DFS(self):
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        stack = []
        visited = set()
        stack.append(start_node)
        while stack:
            QApplication.processEvents()
            if window.stop_flag:
                return
            if  window.stop_running_in_terminal:
                        return
            current_node = stack.pop()
            window.grid_values= list(map(lambda row: list(map(str, row)), current_node.state))
            window.update_tiles()
            visited.add(current_node)
            if current_node.heuristic == 0:
                path = []
                node = current_node
                while node:
                    path.append(node.state)
                    node = node.parent
                path.reverse()
                return path
            #print (current_node.state)
            #time.sleep(2)
            for move in current_node.get_moves():
                child_node = current_node.move_blank(move)

                if child_node not in visited:
                    stack.append(child_node)
        else:
            path = []
            node = current_node
            # for row in node.state: print(row)
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.reverse()
            # print(path)
            return path  
    
    def solve_Astar(self):
        
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        heap = []
        visited = set()
        heapq.heappush(heap, start_node)
        while heap:
            QApplication.processEvents()
            if window.stop_flag:
                return
            if  window.stop_running_in_terminal:
                        return
            current_node = heapq.heappop(heap)
            window.grid_values= list(map(lambda row: list(map(str, row)), current_node.state))
            window.update_tiles()
            visited.add(current_node)
            if current_node.heuristic == 0:
                path = []
                node = current_node
                while node:
                    path.append(node.state)
                    node = node.parent
                path.reverse()
                return path
            #print (current_node.state)
            #time.sleep(2)
            for move in current_node.get_moves():
                child_node = current_node.move_blank(move)

                if child_node not in visited:
                    heapq.heappush(heap, child_node)
        else:
            path = []
            node = current_node
            # for row in node.state: print(row)
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.reverse()
            # print(path)
            return path  
      
    

##################################################################################################################
app = QApplication(sys.argv)
window = PuzzleWindow()
sys.exit(app.exec_())
