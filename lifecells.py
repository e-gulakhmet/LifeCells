# lifecells.py
# 
# Графическое представление жизни колонии клеток из библиотеки colony.py
# 
#
#
#

import logging
import pygame
import pygame.locals
import colony

# Define some colors
C_HDR_TEXT   = (   0,   0,   0)
C_VAL_TEXT   = ( 255, 255, 255)
C_SPLIT_LINE = (   0, 255,   0)
C_BKGROUND   = (   0,   0,   0)




def grp_init(size):
    pygame.init()

    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("Life Cells demonstration")

    return screen



def init_space():
    space = colony.new_space("Universe")

    col1 = ["00111",
            "011011",
            "1100011",
            "011011",
            "00111"]

    col2 = ["111"]

    space = colony.add_colony(space, col1)
    space = colony.add_colony(space, col2)

    return space

def draw_col(screen, x, y, col):
    """
    Draws single colony

    Draws single colony at given position
    """
    c_Cell = [
              (0, 75, 0),
              (0, 255, 0),
              (0, 235, 0),
              (0, 215, 0),
              (0, 195, 0),
              (0, 175, 0),
              (0, 155, 0),
              (0, 135, 0),
              (0, 115, 0),
              (0, 95, 0),
             ]

    # pygame.draw.rect(screen, 
    #                  C_BKGROUND, 
    #                  (x * 10 + 5, 
    #                   y * 10 + 5, 
    #                   (col[0][3] + x) * 10 + 5,
    #                   (col[0][4] + y) * 10 + 5))

    for yy, row in enumerate(col[1]):
        for xx, cell in enumerate(row):
            if cell[0] != 0:
                if cell[0] > 9:
                    cIdx = 0
                else:
                    cIdx = cell[0]
                pygame.draw.circle(screen, c_Cell[cIdx], ((x + xx)*10 + 5, (y + yy)*10 + 5), 5)



def run():
    # active colony
    active_col = 0

    # viewPort shift
    v_shift, h_shift = 0, 0


    size = [700, 500]

    space = init_space()

    screen = grp_init(size)

    clock = pygame.time.Clock()
    # space day change speed
    # it could be:
    #       - slow   ( 1 day per 5 seconds)
    #       - normal ( 1 day per second) 
    #       - fast   ( 5 days per second)
    speed_steps = (5000, 1000, 200) # time in milliseconds to change a day
    curr_speed = 1
    pygame.time.set_timer(pygame.USEREVENT, speed_steps[curr_speed])
    

    done = False
    newDay = False
    # -------- Main Program Loop -----------
    while not done:

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                newDay = True

            if event.type == pygame.QUIT:
                done = True
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # select previous colony as active
                    active_col -= 1
                    if active_col < 0:
                        active_col = 0
                elif event.key == pygame.K_n: # select next colony as active
                    active_col += 1
                    if active_col > len(space) - 3:
                        active_col = len(space) - 3
                elif event.key == pygame.K_q: # quit 
                    done = True
                    continue
                elif event.key == pygame.K_UP:   # shift viewport up
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        v_shift = -10
                    else:
                        v_shift = -1
                elif event.key == pygame.K_RIGHT: # shift viewport right
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift = -10
                    else:
                        h_shift = -1
                elif event.key == pygame.K_LEFT: # shift viewport left
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift = -10
                    else:
                        h_shift = - 1
                elif event.key == pygame.K_DOWN: # shift viewport down
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        v_shift = -10
                    else:
                        v_shift = - 1
                elif event.key == pygame.K_s:   # make speed slower
                    if curr_speed > 0:
                        curr_speed -= 1
                        pygame.time.set_timer(pygame.USEREVENT, speed_steps[curr_speed])
                elif event.key == pygame.K_f:   # make speed faster
                    if curr_speed < 2:
                        curr_speed += 1
                        pygame.time.set_timer(pygame.USEREVENT, speed_steps[curr_speed])


        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        

        # --- Drawing code should go here
        if newDay:
            colony.next_day(space)
            if active_col > len(space) - 3:
                active_col = len(space) - 3
            screen.fill(C_BKGROUND)
            x = int((size[0]/10 - space[2 + active_col][0][3])/2)
            y = int((size[1]/10 - space[2 + active_col][0][4])/2)
            draw_col(screen, x, y, space[2 + active_col])
            newDay = False

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    #font = pygame.font.Font(None, 25)

    # Воспроизвести текст. "True" значит,
    # что текст будет сглаженным (anti-aliased).
    # Чёрный - цвет. Переменную black мы задали ранее,
    # списком [0,0,0]
    # Заметьте: эта строка создаёт картинку с буквами,
    # но пока не выводит её на экран.
    # text = font.render("My text", True, c_valueTxt)

    # Вывести сделанную картинку на экран в точке (250, 250)
    # screen.blit(text, [250,250])

    # Close the window and quit.
    pygame.quit()



###############################################################################
# Main function
###############################################################################
def main():
    """
    Programm entry point

    
    """
    logging.basicConfig(filename="lifecells.log",
                        level=logging.ERROR,
                        format="%(asctime)s [%(levelname)s] : %(message)s")
     
    run()



###############################################################################
# Entry point
###############################################################################
if __name__ == "__main__":
    main()