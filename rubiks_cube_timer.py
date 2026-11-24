# Rubik's Cube Timer
# Times 5 solves, then shows the best single solve, every mean of 3 (MO3),
# the best MO3, and the average of 5 (AO5).
#
# Author: Ali Imran

import tkinter as tk
import time

# ---------------- State ----------------
starting_time = None      # time.time() when the current solve started
timer_running = False     # True while a solve is being timed
solve_list = []           # solve times in seconds (max 5 per session)
previous_time = None      # last solve time, used to color the next result

# ---------------- Styling ----------------
all_fonts = '@Kozuka Mincho Pro B'   # font used for all text
buttonFont = 15                      # font size for buttons and tables

# ---------------- Main window ----------------
cubeTimer_frame = tk.Tk()
cubeTimer_frame.title("Rubik's Cube Timer")
cubeTimer_frame.configure(bg = 'black')
cubeTimer_frame.geometry("1600x900")


# Starts the timer if it isn't already running and fewer than 5 solves are recorded
def startTimer():
    global timer_running, starting_time
    if not timer_running and len(solve_list) < 5:
        starting_time = time.time()
        timer_running = True
        updateTimer()


# Refreshes the timer display every 10 ms while a solve is running
def updateTimer():
    if timer_running:
        elapsed_time = time.time() - starting_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        timer.config(text = f"{minutes:02}:{seconds:05.2f}")   # MM:SS.hh format
        cubeTimer_frame.after(10, updateTimer)


# Called by the Stop button
def stop():
    stopTimer(solve_list)


# Stops the timer, saves the solve, updates the solves table,
# and colors the time green (faster) or red (slower) than the previous solve
def stopTimer(solve_list):
    global previous_time, timer_running

    if timer_running:
        elapsed_time = time.time() - starting_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        timer.config(text = f"{minutes:02}:{seconds:05.2f}")
        solve_list.append(float(f"{elapsed_time:.2f}"))

        # After the 5th solve, disable Start/Stop and show the statistics
        if len(solve_list) == 5:
            startbutton.config(state = "disabled")
            stopbutton.config(state = "disabled")
            calculateStats()

        # Redraw the solves table: headings in column 0, one column per solve
        solveHeading = tk.Label(solveList_frame, text = 'Solve #', font = (all_fonts, buttonFont, 'bold'), fg = 'white', bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 10)
        solveHeading.grid(row = 0, column = 0)

        timeHeading = tk.Label(solveList_frame, text = 'Time (s)', font = (all_fonts, buttonFont, 'bold'), fg = 'white', bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 10)
        timeHeading.grid(row = 1, column = 0)

        lastfive = solve_list[-5:]
        length = len(solve_list[-5:])

        for i in range(length):
            tk.Label(solveList_frame, text = i + 1, font = (all_fonts, buttonFont, 'bold'), fg = 'white', bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 10).grid(row = 0, column = i + 1)
            tk.Label(solveList_frame, text = f"{lastfive[i]:.2f}s", font = (all_fonts, buttonFont, 'bold'), fg = 'white', bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 10).grid(row = 1, column = i + 1)

        # Green = faster than the previous solve, red = slower, white = first solve
        if previous_time is not None:
            if elapsed_time < previous_time:
                timer.config(fg = 'green')
            else:
                timer.config(fg = 'red')
        else:
            timer.config(fg = 'white')
        previous_time = elapsed_time

    timer_running = False


# Calculates the best single solve, each mean of 3 (MO3), the best MO3,
# and the average of 5 (AO5), then shows them in the stats table
def calculateStats():
    if len(solve_list) < 5:
        return

    best_singleSolve = min(solve_list)

    # Mean of every 3 consecutive solves (solves 1-3, 2-4, 3-5)
    mo3_values = []
    for i in range(len(solve_list) - 2):
        mo3_values.append(sum(solve_list[i:i + 3]) / 3)

    best_mo3 = min(mo3_values)

    # AO5 (official WCA method): drop the best and worst solve, average the middle 3
    avgof5 = (sum(solve_list) - max(solve_list) - min(solve_list)) / 3

    # Heading names, heading colors, and values for the stats table
    headings = ['Best Single Solve', 'Best MO3', 'First MO3', 'Second MO3', 'Third MO3', 'AO5']
    headingFont_color = ['gold', 'chocolate2', 'greenyellow', 'limegreen', 'turquoise1', 'darkorchid3']
    stats = [best_singleSolve, best_mo3, mo3_values[0], mo3_values[1], mo3_values[2], avgof5]

    for i in range(len(headings)):
        statHeading = tk.Label(stats_frame, text = f"{headings[i]}", font = (all_fonts, buttonFont, 'bold'), fg = headingFont_color[i], bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 15)
        statHeading.grid(row = 0, column = i)

    for x in range(len(stats)):
        statValue = tk.Label(stats_frame, text = f"{stats[x]:.2f}", font = (all_fonts, buttonFont, 'bold'), fg = 'white', bg = 'black', highlightbackground = "white", highlightthickness = 1, width = 15)
        statValue.grid(row = 1, column = x)


# Clears all solves and stats and starts a new session
def resetTimer():
    global solve_list, timer_running, starting_time, previous_time

    # Remove every widget from the stats and solves tables
    for widget in stats_frame.winfo_children():
        widget.destroy()

    for widget in solveList_frame.winfo_children():
        widget.destroy()

    solve_list = []
    timer_running = False
    starting_time = None
    previous_time = None

    timer.config(text = "00:00.00", fg = "white")

    startbutton.config(state = "normal")
    stopbutton.config(state = "normal")


# ---------------- GUI layout ----------------

# Title and timer display
title = tk.Label(cubeTimer_frame, text = "Rubik's Cube Timer", font = (all_fonts, 30, 'bold'), fg = 'white', bg = 'black')
title.pack(pady = 10)

timer = tk.Label(cubeTimer_frame, text = '00:00.00', font = (all_fonts, 70, 'bold'), fg = 'white', bg = 'black')
timer.pack(pady = 2)

# Buttons
button_frame = tk.Frame(cubeTimer_frame, bg = 'black')
button_frame.pack(pady = 15)

startbutton = tk.Button(button_frame, text = 'Start', command = startTimer, font = (all_fonts, buttonFont, 'bold'), width = 10, bg = 'green3', fg = 'black')
startbutton.pack(padx = 5, side = 'left')

stopbutton = tk.Button(button_frame, text = 'Stop', command = stop, font = (all_fonts, buttonFont, 'bold'), width = 10, bg = 'red', fg = 'black')
stopbutton.pack(padx = 5, side = 'left')

resetbutton = tk.Button(button_frame, text = 'Reset', command = resetTimer, font = (all_fonts, buttonFont, 'bold'), width = 10, bg = 'dodger blue', fg = 'black')
resetbutton.pack(padx = 5, side = 'right')

# Solves table and statistics table
solveList_frame = tk.Frame(cubeTimer_frame, bg = 'black')
solveList_frame.pack(pady = 20)

stats_frame = tk.Frame(cubeTimer_frame, bg = 'black')
stats_frame.pack(pady = 20)
stats_frame.pack_propagate(False)

cubeTimer_frame.mainloop()
