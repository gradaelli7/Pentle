import tkinter as tk
from tkinter import ttk
import random
import math

class Pentle:
    def __init__(self):
        #read words file
        f = open('words.txt')

        #create word list
        self.word_list = []
        for line in f:
            line = line.strip().upper()
            self.word_list.append(line)
        
        self.window = tk.Tk() # Create a window
        self.window.title("Pentle") # Set a title

        self.size = 790 #set a self.size for the canvas height/width
        self.center_y = self.size//2 + 20
        self.factor = 15
        self.canvas_width = self.size
        self.canvas_height = self.size
        self.count = 0
        self.num_correct = 0

        self.display()

    def display(self):

        #get random word
        self.random_word = self.get_random_word()
        print(self.random_word)
        
        # Place canvas in window
        self.canvas = tk.Canvas(self.window, 
                width = self.canvas_width,
                height = self.canvas_height,
                bg = 'white') 
        self.canvas.grid(row = 1, column = 1)

        #calculate coordinates for each letter A
        self.A1 = (self.size//2,self.center_y-self.factor)
        self.A2 = (self.size//2 + self.factor*(1/4*(math.sqrt(10+2*math.sqrt(5)))), self.center_y - self.factor*(1/4*(math.sqrt(5)-1)))
        self.A3 = (self.size//2 + self.factor*(1/4*(math.sqrt(10-2*math.sqrt(5)))), self.center_y + self.factor*(1/4*(math.sqrt(5)+1)))
        self.A4 = (self.size//2 - self.factor*(1/4*(math.sqrt(10-2*math.sqrt(5)))), self.center_y + self.factor*(1/4*(math.sqrt(5)+1)))
        self.A5 = (self.size//2 - self.factor*(1/4*(math.sqrt(10+2*math.sqrt(5)))), self.center_y - self.factor*(1/4*(math.sqrt(5)-1)))

        #create dictionary to hold each alphabet (convert ASCII value to corresponding character, in this case 65 -> A)
        self.dict_of_dicts = {0:{chr(65):self.A1},1:{chr(65):self.A2},2:{chr(65):self.A3},3:{chr(65):self.A4},4:{chr(65):self.A5}}

        #create 5 letters 'A' (conversion from ASCII)
        self.canvas.create_text(self.A1[0],self.A1[1], text = chr(65))
        self.canvas.create_text(self.A2[0],self.A2[1], text = chr(65))
        self.canvas.create_text(self.A3[0],self.A3[1], text = chr(65))
        self.canvas.create_text(self.A4[0],self.A4[1], text = chr(65))
        self.canvas.create_text(self.A5[0],self.A5[1], text = chr(65))

        self.text_box = self.canvas.create_text(self.size//2,700,text="")
        self.correct_guesses = []
        self.a_bank = self.canvas.create_text(140,45,text = 'Alphabet Bank')
        self.list_f = []
        self.list_s = []
        for i in range(13):
            self.tag_f = chr(65+i)
            self.tag_s = chr(78+i)
            self.list_f.append(self.tag_f)
            self.list_s.append(self.tag_s)
            self.canvas.create_text(50 + 15*i,65,text = chr(65+i),tag=self.tag_f)
            self.canvas.create_text(50 + 15*i,80,text = chr(78+i),tag=self.tag_s)

        #procedurally loop through rest of alphabet
        for i in range(25):
            self.cur_chr = chr(65+(i+1))

            self.a1_let = (self.size//2,self.center_y-(self.factor*(i+2)))
            self.a2_let = (self.size//2 + self.factor*(i+2)*(1/4*(math.sqrt(10+2*math.sqrt(5)))), self.center_y - self.factor*(i+2)*(1/4*(math.sqrt(5)-1)))
            self.a3_let = (self.size//2 + self.factor*(i+2)*(1/4*(math.sqrt(10-2*math.sqrt(5)))), self.center_y + self.factor*(i+2)*(1/4*(math.sqrt(5)+1)))
            self.a4_let = (self.size//2 - self.factor*(i+2)*(1/4*(math.sqrt(10-2*math.sqrt(5)))), self.center_y + self.factor*(i+2)*(1/4*(math.sqrt(5)+1)))
            self.a5_let = (self.size//2 - self.factor*(i+2)*(1/4*(math.sqrt(10+2*math.sqrt(5)))), self.center_y - self.factor*(i+2)*(1/4*(math.sqrt(5)-1)))

            #append letter:coordinate pair to each dictionary of corresponding alphabet
            #create letters in display (conversion from ASCII)
            lst_a = [self.a1_let,self.a2_let,self.a3_let,self.a4_let,self.a5_let]
            for j in range(len(lst_a)):
                self.dict_of_dicts[j].update({self.cur_chr:lst_a[j]})
                self.canvas.create_text(lst_a[j][0], lst_a[j][1], text = self.cur_chr)

        # Input frame in window
        self.input_frame = ttk.Frame(self.window)
        self.input_frame.grid(row = 2, column = 1)

        # create guess label
        self.guess_label = ttk.Label(self.input_frame, text="Guess:")
        self.guess_label.grid(row=1,column=1)

        # create entry guess
        self.guess = tk.StringVar()
        self.guess_entry = ttk.Entry(self.input_frame, textvariable=self.guess)
        self.guess_entry.grid(row=1,column=2)
        
        #create button enter
        self.enter_button = ttk.Button(self.input_frame,
                text = "Enter", command = self.enter)
        self.enter_button.grid(row = 1, column = 3)

        # Button frame in window
        self.button_frame = ttk.Frame(self.window)
        self.button_frame.grid(row = 3, column = 1)

        #create button new game
        self.new_game_button = ttk.Button(self.button_frame,
                text = "New Game", command = self.new_game)
        self.new_game_button.grid(row = 1, column = 1)

        #create button quit
        self.quit_button = ttk.Button(self.button_frame,
                text = "Quit", command = self.window.destroy)
        self.quit_button.grid(row = 1, column = 2)
            
        # Start event loop
        self.window.mainloop()

    def get_random_word(self):
        #return random word
        length = len(self.word_list)
        number = random.randint(0, length-1)
        return self.word_list[number]

    def enter(self):
        """Enter guess."""

        self.canvas.itemconfig(self.text_box,text="")

        #convert entered value to string, delete from entry box
        self.guess_str = str(self.guess.get())
        self.guess_entry.delete(0,tk.END)

        #scan string
        entered_guess = self.guess_str.upper()

        status_code = 0
        if entered_guess in self.correct_guesses:
            status_code = 3

        #convert r_word into list of its characters
        r_word_list = []
        for i in range(len(self.random_word)):
            r_word_list.append(self.random_word[i])

        if len(entered_guess) != 5 or entered_guess not in self.word_list:
            status_code = 1

        if (self.count < 6):
            #check if 5 characters long and string is in random word list
            if (len(entered_guess) == 5) and (entered_guess in self.word_list) and (status_code != 3):
                self.correct_guesses.append(entered_guess)
                
                self.count += 1
                color_list = []
                coordinates_list = []

                #check each character, make upper, and extract coordinate from dict, save coordinates
                #check each character with random word, decide if green, yellow, none
                #need to remember what is already checked, so "cross out" letters already taken from random word
                for j in range(5):
                    coordinates = self.dict_of_dicts[j][entered_guess[j]]
                    coordinates_list.append(coordinates)
                    if entered_guess[j] == r_word_list[j]:
                        color_list.append("green")
                        r_word_list[j] = "crossed out"
                        self.num_correct += 1

                        if entered_guess[j] in self.list_f:
                            self.canvas.itemconfig(entered_guess[j],text=entered_guess[j],fill="green")
                            self.list_f.remove(entered_guess[j])
                        elif entered_guess[j] in self.list_s:
                            self.canvas.itemconfig(entered_guess[j],text=entered_guess[j],fill="green")
                            self.list_s.remove(entered_guess[j])

                    elif entered_guess[j] in r_word_list:
                        color_list.append("yellow")
                        index = r_word_list.index(entered_guess[j])
                        r_word_list[index] = "crossed out"

                        if entered_guess[j] in self.list_f:
                            self.canvas.itemconfig(entered_guess[j],text=entered_guess[j],fill="yellow")
                            self.list_f.remove(entered_guess[j])
                        elif entered_guess[j] in self.list_s:
                            self.canvas.itemconfig(entered_guess[j],text=entered_guess[j],fill="yellow")
                            self.list_s.remove(entered_guess[j])

                    else:
                        color_list.append("white")
                        
                        if entered_guess[j] in self.list_f:
                            self.canvas.itemconfig(entered_guess[j],text="")
                            self.list_f.remove(entered_guess[j])
                        elif entered_guess[j] in self.list_s:
                            self.canvas.itemconfig(entered_guess[j],text="")
                            self.list_s.remove(entered_guess[j])

                #create lines between 0-1,1-2,2-3,3-4,4-0
                self.canvas.create_line(coordinates_list[0][0],coordinates_list[0][1],coordinates_list[1][0],coordinates_list[1][1])
                self.canvas.create_line(coordinates_list[1][0],coordinates_list[1][1],coordinates_list[2][0],coordinates_list[2][1])
                self.canvas.create_line(coordinates_list[2][0],coordinates_list[2][1],coordinates_list[3][0],coordinates_list[3][1])
                self.canvas.create_line(coordinates_list[3][0],coordinates_list[3][1],coordinates_list[4][0],coordinates_list[4][1])
                self.canvas.create_line(coordinates_list[4][0],coordinates_list[4][1],coordinates_list[0][0],coordinates_list[0][1])
                
                #draw circle around each vertex, color (green,yellow,n/a) in depending on in word or not.
                radius = 7
                for j in range(5):
                    self.canvas.create_oval(coordinates_list[j][0]-radius,coordinates_list[j][1]-radius,
                        coordinates_list[j][0]+radius,coordinates_list[j][1]+radius,fill=color_list[j])
            
                    #recreate letter text over color
                    self.canvas.create_text(coordinates_list[j][0],coordinates_list[j][1],text=entered_guess[j])
                if self.num_correct == 5:
                    self.canvas.itemconfig(self.text_box, text="You genius! You did it!")
                    self.enter_button.destroy()
                else:
                    self.num_correct = 0

            if status_code == 1:
                self.canvas.itemconfig(self.text_box, text="Not a valid word silly! Try again please :)")
            elif status_code == 3:
                self.canvas.itemconfig(self.text_box, text="You already guessed that word!")

        else:
            self.canvas.itemconfig(self.text_box,text="You lose!! The correct word was " + self.random_word)
            self.enter_button.destroy()
        
            

    def new_game(self):
        """Create new game."""
        self.count=0
        self.num_correct=0
        self.canvas.delete('all')
        self.display()
        
if __name__ == "__main__":
    Pentle()