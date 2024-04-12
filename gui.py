from tkinter import*
import customtkinter


root = customtkinter.CTk()
root.geometry('1600x1200')
root.title('Fruit Guesser')

def start_game():
    # Function to transition to the game page
    start_frame.pack_forget()  # Hide the start frame
    game_frame.pack()          # Show the game frame

#set theme and color
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Start frame
start_frame = Frame(root, bg=root.cget("bg"))  # Frame for start page
start_frame.pack(fill=BOTH, expand=True)

start_text = Label(start_frame, text="Welcome!", font=("Helvetica", 18), bg=start_frame.cget("bg"), fg="white")
start_text.pack(pady=20)
start_text = Label(start_frame, text="Please click the Start Game button to begin the game", font=("Helvetica", 18), bg=start_frame.cget("bg"), fg="white")
start_text.pack(pady=20)


start_button = customtkinter.CTkButton(start_frame, text="Start Game", command=start_game)  # Changed start_frame here
start_button.pack(pady=80)

# Game frame
game_frame = Frame(root, bg=root.cget("bg"))  # Frame for game page, initially hidden


# User entry (will fix later)
answer_entry = customtkinter.CTkEntry (game_frame,
   # placeholder = "Enter Your Answer",
    height = 50,
    width = 200,
    font = ("Helvetica", 18),
    corner_radius = 50,
    text_color = "green",
    placeholder_text_color = "darkgreen",
    fg_color = ("black","grey" ),   #outer,inner 
    state = "normal", 

)

answer_entry.pack()
root.mainloop()