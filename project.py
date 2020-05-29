import random
from simpleimage import SimpleImage
import tkinter
from PIL import ImageTk
from PIL import Image
import time

"""
This programme allows the user to do silly things with a ball, Simba and Karel
The images needed for this file can be found here:
little_simba: https://1drv.ms/u/s!AkIsdlUtRueqgadJTaSawsWCGVSMsw?e=qsa9IM
karel: https://1drv.ms/u/s!AkIsdlUtRueqgadK0IILPEXApFNncg?e=hDqsI8
flipped_karel: https://1drv.ms/u/s!AkIsdlUtRueqgadSowxhES8Gmb7u4w?e=dABnnT
"""
CANVAS_WIDTH = 1040
CANVAS_HEIGHT = 640
SIZE = 80
N_ROWS = int(CANVAS_HEIGHT / SIZE)
N_COLS = int(CANVAS_WIDTH / SIZE)
BALL_SIZE = 40
MENU_CHOICES = ["Bouncing Ball", "Bouncing & Sliding Ball", "Clean-Up Ball", "Bouncing Simba",
                "Bouncing Karel", "Switch at Bounce", "Simba Chasing", "Karel Chasing", "Random",
                "End"]
VALID_CHOICES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
BALL_CHOICES = [1, 2, 3, 7, 8]
SIMBA_PLAYS = [4, 6, 7]
KAREL_PLAYS = [5, 8]
HIDDEN_CHASING = [4, 5, 6]
CHASE_MODES = SIMBA_PLAYS + KAREL_PLAYS
VALID_RUN_TIMES = VALID_CHOICES[0:3]
START_POINT_Y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2
OFFSET = 1.5
X_MOVE = 5
Y_MOVE = 2
SIMBA_W = 51
SIMBA_H = 53
KAREL_W = 48
KAREL_H = 62
DEMO = "on"


def main():
    """
    The user at the terminal is offered 10 choices - see MENU_CHOICES above.  Once a valid choice is made, the chosen
    animation is triggered.  The animation runs for the time period selected ( 1, 2 or 3 minutes);
    after which the menu is presented again. This continues until the user selects End; after which a thank you
    animation is displayed.
    pre-condition: Constants have been set and the requisite images are available in the folder specified
    post-condition: at least one animation has run (if only the End) and the user has experienced a modicum of pleasure
    """

    display_menu()  # Offer menu choices to user
    animation_mode = int(get_choice())  # determine choice
    while animation_mode != 10:  # keep running until end selected
        if animation_mode == 9:  # randomly set the animation mode
            animation_mode = random.randint(1, 8)
        canvas = prepare_canvas(animation_mode)  # prepare the animation board
        if animation_mode in BALL_CHOICES:  # bouncing ball selected
            projectile = prepare_ball(canvas, animation_mode)  # prepare the ball
        if animation_mode in HIDDEN_CHASING:  # Simba or Karel selected
            projectile = prepare_hidden_projectile(canvas,
                                                   animation_mode)  # simba or karel chase an invisible projectile
        run_animation(animation_mode, canvas, projectile)  # run the animation
        display_menu()  # Offer menu choices to user
        animation_mode = int(get_choice())  # determine choice

    end_game()  # user is finished; thank them for playing


def display_menu():
    """
    The menu is displayed
    pre-condition: Constants have been set
    post-condition: the menu has been displayed
    """
    print("\nWELCOME TO CODE-IN-PLACE ANIMATION")
    print("\nYour choices are:")
    for i in range(10):
        print("\t" + str(i + 1) + ". " + MENU_CHOICES[i] + ":")


def get_choice():
    """
    The menu selection is input and validated
    pre-condition: The menu has been presented
    post-condition: A valid choice - as per the VALID_CHOICES list - has been entered and returned
    """
    choice = input("\nselect 1 to 10: ")
    while choice not in VALID_CHOICES:
        choice = input("\nselect 1 to 10 only: ")
    return choice


def prepare_canvas(mode):
    """
    Create a blank canvas and, if the animation mode requires additional graphics, embellish it.
    pre-condition: The animation mode has been passed.
    post-condition: The canvas is created, embellished and returned
    """
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, MENU_CHOICES[mode - 1])
    if mode == 3 or mode in CHASE_MODES[1:5] or mode == 2:  # paint the canvas
        for row in range(N_ROWS):
            for col in range(N_COLS):
                draw_square(canvas, row, col, mode)

    return canvas


def draw_square(canvas, row, col, mode):
    """
    Draw a square on the canvas with the colour of the square being determined from the animation mode.
    pre-condition: The canvas, row, column and mode have been passed
    post-condition: the canvas has had a square added, of the required colour and in the required position
    """
    x = col * SIZE
    y = row * SIZE
    if mode in CHASE_MODES[1:5] or mode == 2:  # grey is used to allow subsequent cleaning of the canvas
        color = "grey"
    else:
        color = get_color(row, col)  # get colour to draw a checkerboard pattern
    canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=color, outline=color)


def get_color(row, col):
    """
    Determine the colour required for a checkerboard effect and return it.
    pre-condition: The row and column have been passed
    post-condition: The required colour has been returned
    """

    if (row + col) % 2 == 1:
        return 'white'
    return 'green'
    # return int_to_color(col * row * row)


def prepare_ball(canvas, mode):
    """
    Prepare the initial attributes for the ball (required for the animation modes in the BALL_CHOICES list),
    call the function that creates the ball and return the ball
    pre-condition: The canvas and mode have been passed
    post-condition: The ball has been created and returned in the required position
    """
    start_y = START_POINT_Y
    start_x = 0
    if mode == 7 or mode == 8:  # ball starts forward as image is chasing
        start_y += (BALL_SIZE * OFFSET)
        start_x += (BALL_SIZE * OFFSET)
    return display_ball(canvas, start_x, start_y)


def display_ball(canvas, start_x, start_y):
    """
    Create a the ball on the canvas at the required start position.
    pre-condition: The canvas and start coordinates have been passed
    post-condition: The ball has been created and returned in the required position
    """
    end_y = start_y + BALL_SIZE
    end_x = start_x + BALL_SIZE
    return canvas.create_oval(start_x, start_y, end_x, end_y, fill="blue")


def prepare_hidden_projectile(canvas, mode):
    """
    Create the initial invisible ball on the canvas with the same dimensions as Simba.
    pre-condition: The canvas and mode have been passed
    post-condition: A hidden ball has been created with Simba's dimensions and returned
    """
    start_y = START_POINT_Y
    start_x = 0
    icon = "Simba"
    return display_hidden_projectile(canvas, mode, start_x, start_y, icon)


def display_hidden_projectile(canvas, mode, start_x, start_y, icon):
    """
    Create an invisible ball on the canvas with the same dimensions as the icon passed.
    pre-condition: The canvas, mode, start position and name of the icon have been passed
    post-condition: A hidden ball has been created with the specified attributes and has been returned
    """
    if mode == 4 or (mode == 6 and icon == "Simba"):  # simba showing
        end_x = start_x + SIMBA_W - 3
        end_y = start_y + SIMBA_H - 3
    if mode == 5 or (mode == 6 and icon == "Karel"):  # karel showing
        end_x = start_x + KAREL_W - 3
        end_y = start_y + KAREL_H - 3
    return canvas.create_oval(start_x, start_y, end_x, end_y, fill="", outline="")


def run_animation(mode, canvas, projectile):
    """
    Determine the time required for the animation and then start the animation.
    pre-condition: The canvas, mode, and projectile have been prepared and passed.
    post-condition: The animation has run for the specified time.
    """
    animation_time = ask_for_runtime()  # ask the user how long it should run
    time_start = time.time()
    time_end = time.time()
    if DEMO == "on":  # override animation time if demon mode on
        animation_time = 30
    while (time_end - time_start) < 3:  # delay the start by 3 seconds (to allow switch from terminal)
        time_end = time.time()
    move_frame(mode, canvas, projectile, animation_time)  # kick of the animation
    canvas.mainloop()


def ask_for_runtime():
    """
    Allows the user to specify the run time.
    pre-condition: none
    post-condition: A valid run time has been selected and returned.
    """
    print("\nYou can run this for " + str(VALID_RUN_TIMES[0]) + " to " + str(VALID_RUN_TIMES[-1]) + " minutes:")
    run_time = input("\nhow many minutes? ")
    while run_time not in VALID_RUN_TIMES:
        run_time = input("\nselect " + str(VALID_RUN_TIMES[0]) + " to " + str(VALID_RUN_TIMES[-1]) + " only: ")
    return int(run_time) * 60  # set the time to run in seconds


def move_frame(mode, canvas, projectile, run_time):
    """
    Runs the animation for the time specified
    pre-condition: the canvas and projectile have been created; the mode and run time have been selected;
                   all four have been passed as parameters.
    post-condition: The selected animation has run
    """
    move_x = X_MOVE  # the distance to be moved to the right is set to its initial value
    move_y = Y_MOVE  # the distance to be moved downwards is set to its initial value
    time_start = time.time()  # get the current time
    time_end = time.time()  # set the end time to the current time.
    simba = ImageTk.PhotoImage(Image.open("images/litle_simba.jpg"))  # load simba
    karel = ImageTk.PhotoImage(Image.open("images/karel.jpg"))  # load karel
    karel_flipped = ImageTk.PhotoImage(Image.open("images/flipped_karel.jpg"))  # load flipped karel
    going_right = True  # to be used in mode 6
    ball_sliding = False  # used in mode 2
    bounce_turn = False  # used in mode 2 to determine whether a slide or bounce is made
    if mode in SIMBA_PLAYS:  # simba gets to play!
        chaser = canvas.create_image(0, START_POINT_Y, anchor="nw", image=simba)
        current_chaser = "Simba"  # to be used in mode 6
    if mode in KAREL_PLAYS:  # karel gets to play!
        chaser = canvas.create_image(0, START_POINT_Y, anchor="nw", image=karel)
        current_chaser = "Karel"  # to be used in mode 6
    while (time_end - time_start) <= run_time:  # keep running until time limit reached
        if mode == 3:  # canvas is cleared behind the moving ball
            column_x = get_left_x(canvas, projectile)
            row_y = get_top_y(canvas, projectile)
            clear_oval(canvas, column_x, row_y)
            projectile = display_ball(canvas, column_x, row_y)  # needed so that ball stays visible
        canvas.move(projectile, move_x, move_y)
        if mode in CHASE_MODES:  # move the chaser as well
            canvas.move(chaser, move_x, move_y)
        if mode == 2:  # sliding & bouncing
            if corner_hit(canvas, projectile):  # has a corner been reached?
                ball_sliding = False  # stop sliding
                bounce_turn = True  # ball to bounce when it next hits a wall
                # ball has to be repositioned to avoid hitting corner twice & canvas cleaned
                projectile = reposition_ball(canvas, projectile)
                move_x = X_MOVE * random.randint(1, 3)
                move_y = Y_MOVE * random.randint(2, 5)
                if top_right(canvas, projectile) or bottom_right(canvas, projectile):
                    move_x *= -1  # move ball left
                if bottom_left(canvas, projectile) or bottom_right(canvas, projectile):
                    move_y *= -1  # move ball up
            else:  # corner hasn't been reached
                if hit_left_wall(canvas, projectile) or hit_right_wall(canvas, projectile):  # side wall reached?
                    if not ball_sliding:  # not already sliding?
                        if bounce_turn:  # bounce turn or slide turn?
                            move_x *= -1    # make ball bounce
                            bounce_turn = False
                        else:
                            move_x = 0  # start sliding
                            move_y *= 2  # pick up speed
                            ball_sliding = True
                if hit_top_wall(canvas, projectile) or hit_bottom_wall(canvas, projectile):  # top or bottom reached?
                    if not ball_sliding:  # not already sliding?
                        if bounce_turn:     # bounce turn or slide turn?
                            move_y *= -1    # make ball bounce
                            bounce_turn = False
                        else:
                            move_y = 0  # start sliding
                            move_x *= 2  # pick up speed
                            ball_sliding = True
        else:  # not mode 2 (i.e. not sliding & bouncing)
            if hit_top_wall(canvas, projectile) or hit_bottom_wall(canvas, projectile):  # top or bottom reached?
                move_y *= -1  # reverse direction of projectile
                if mode == 6:  # Simba & Karel switch when the top or bottom reached
                    projectile = reposition_hidden_ball(canvas, mode, projectile, current_chaser)
                    if current_chaser == "Simba":  # simba needs to change to karel
                        if going_right:  # simba changes to right facing karel
                            chaser = canvas.create_image(get_left_x(canvas, projectile), get_top_y(canvas, projectile),
                                                         anchor="nw", image=karel)
                        else:  # simba changes to left facing karel
                            chaser = canvas.create_image(get_left_x(canvas, projectile), get_top_y(canvas, projectile),
                                                         anchor="nw", image=karel_flipped)
                        current_chaser = "Karel"  # karel is now the chaser
                    else:  # karel needs to change to simba
                        chaser = canvas.create_image(get_left_x(canvas, projectile), get_top_y(canvas, projectile),
                                                     anchor="nw", image=simba)
                        current_chaser = "Simba"  # simba is now the chaser
            if hit_left_wall(canvas, projectile) or hit_right_wall(canvas, projectile):  # side wall reached?
                move_x *= -1  # reverse direction of projectile
                going_right = not going_right  # change the direction flag
                # karel needs to reflect change of direction, some clearing also required behind both karel and simba
                if mode in KAREL_PLAYS \
                        or (mode == 6 and current_chaser == "Karel") \
                        or mode == 7:
                    column_x = get_left_x(canvas, projectile)
                    row_y = get_top_y(canvas, projectile)
                    # replaced icon needs to be cleared from canvas
                    clear_behind(canvas, column_x, row_y)
                    if mode == 7 or mode == 8:  # ball needs to be repainted
                        projectile = display_ball(canvas, column_x, row_y)
                    if mode == 5:  # hidden projectile needs to be recreated
                        display_hidden_projectile(canvas, mode, column_x, row_y, current_chaser)
                    if hit_left_wall(canvas, projectile):  # on the left hand side?
                        if mode == 7 or mode == 8:
                            column_x -= BALL_SIZE * 2  # move chaser behind ball
                        if mode == 7:  # simba needs to be recreated
                            chaser = canvas.create_image(column_x, row_y, anchor="nw", image=simba)
                        else:  # karel needs to be recreated
                            chaser = canvas.create_image(column_x, row_y, anchor="nw", image=karel)
                    else:  # on the right hand side
                        if mode == 7 or mode == 8:
                            column_x += BALL_SIZE * 2  # move chaser behind ball
                        if mode == 7:  # simba needs to be recreated
                            chaser = canvas.create_image(column_x, row_y, anchor="nw", image=simba)
                        else:  # karel needs to be recreated
                            chaser = canvas.create_image(column_x, row_y, anchor="nw", image=karel_flipped)
        canvas.update()
        time.sleep(1 / 50)
        time_end = time.time()


def corner_hit(canvas, object):
    return top_left(canvas, object) or top_right(canvas, object) \
           or bottom_left(canvas, object) or bottom_right(canvas, object)


def top_left(canvas, object):
    return hit_top_wall(canvas, object) and hit_left_wall(canvas, object)


def top_right(canvas, object):
    return hit_top_wall(canvas, object) and hit_right_wall(canvas, object)


def bottom_left(canvas, object):
    return hit_bottom_wall(canvas, object) and hit_left_wall(canvas, object)


def bottom_right(canvas, object):
    return hit_bottom_wall(canvas, object) and hit_right_wall(canvas, object)


def hit_left_wall(canvas, object):
    return get_left_x(canvas, object) <= 0


def hit_top_wall(canvas, object):
    return get_top_y(canvas, object) <= 0


def hit_right_wall(canvas, object):
    return get_right_x(canvas, object) >= CANVAS_WIDTH


def hit_bottom_wall(canvas, object):
    return get_bottom_y(canvas, object) >= CANVAS_HEIGHT


def reposition_ball(canvas, projectile):
    """
    Clear the canvas and put a replica ball in the exact location of the corner
    pre-condition: the canvas and projectile have already been defined and passed across as parameters
    post-condition: The ball that reached the corner has been erased from the canvas and a replica created in the
    exact location of the corner
    """
    if top_left(canvas, projectile):  # ball reached the top left corner?
        col_x = 0
        row_y = 0
    if top_right(canvas, projectile):  # ball reached the top right corner?
        col_x = CANVAS_WIDTH - BALL_SIZE
        row_y = 0
    if bottom_left(canvas, projectile):  # ball reached the bottom left corner?
        col_x = 0
        row_y = CANVAS_HEIGHT - BALL_SIZE
    if bottom_right(canvas, projectile):  # ball reached the bottom right corner?
        col_x = CANVAS_WIDTH - BALL_SIZE
        row_y = CANVAS_HEIGHT - BALL_SIZE
    clear_behind(canvas, col_x, row_y)  # clear the replaced ball
    return display_ball(canvas, col_x, row_y)


def reposition_hidden_ball(canvas, mode, projectile, current_chaser):
    """
    Clear the canvas and put a hidden ball in the required position
    pre-condition: the canvas and projectile have already been created and passed across as parameter.  The 
    mode and the current chaser have been specified and passed across.
    post-condition: The hidden projectile has been erased from the canvas and a replica created in the
   required location
    """
    column_x = get_left_x(canvas, projectile)
    row_y = get_top_y(canvas, projectile)
    clear_behind(canvas, column_x, row_y)  # canvas needs to be cleared of replaced icon
    # hidden projectile needs to be recreated
    return display_hidden_projectile(canvas, mode, column_x, row_y, current_chaser)


def end_game():
    """
    Runs the animation for the End frame and thereby thanks the user for playing
    pre-condition: the option to end the game has been selected
    post-condition: An animated thank you graphic has been displayed and the programme has ended
    """
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Good Bye')  # Create white square canvas
    # 	Create thank you text
    text = canvas.create_text(0, CANVAS_HEIGHT / 2, anchor='w', font='Courier 52', fill="green",
                              text='Thank You for Playing!')
    column_x = get_left_x(canvas, text)  # find initial left most position of text
    simba = ImageTk.PhotoImage(Image.open("images/litle_simba.jpg"))  # load simba
    karel = ImageTk.PhotoImage(Image.open("images/karel.jpg"))  # load karel
    karel_flipped = ImageTk.PhotoImage(Image.open("images/flipped_karel.jpg"))  # load flipped karel
    chaser = canvas.create_image(350, START_POINT_Y / 3, anchor="nw", image=karel)
    chaser1 = canvas.create_image(700, START_POINT_Y / 3, anchor="nw", image=karel_flipped)
    chaser2 = canvas.create_image(520, START_POINT_Y * 2 / 3, anchor="nw", image=simba)

    while column_x < (CANVAS_WIDTH / 15):
        canvas.move(text, 1, 0)
        canvas.update()
        time.sleep(1 / 50)
        column_x = get_left_x(canvas, text)
    canvas.mainloop()


def clear_oval(canvas, x, y):
    canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill="white", outline="white")


def clear_behind(canvas, x, y):
    if x > 0:
        x = x - BALL_SIZE * 2
        y = y - BALL_SIZE * 2
    canvas.create_rectangle(x, y, x + BALL_SIZE * 5, y + BALL_SIZE * 5, fill="grey", outline="grey")


def get_left_x(canvas, projectile):
    return canvas.coords(projectile)[0]


def get_top_y(canvas, projectile):
    return canvas.coords(projectile)[1]


def get_right_x(canvas, projectile):
    return canvas.coords(projectile)[2]


def get_bottom_y(canvas, projectile):
    return canvas.coords(projectile)[3]


def int_to_color(value):
    # white is the largest value one can represent
    white_dec = int('ffffff', 16)
    # change your value into "hexadecimal" representation
    hex_str = format(value % white_dec, 'x')
    # add 0s to the end until its the right length
    while len(hex_str) < 6:
        hex_str += '0'
    # you now have a color!
    return '#' + hex_str


def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    projectiles = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


if __name__ == '__main__':
    main()
