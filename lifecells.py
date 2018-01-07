# lifecells.py
# 
# Графическое представление жизни колонии клеток из библиотеки colony.py
#
# EnesGUL12, dr-dobermann, 2018.
#
# https://github.com/EnesGUL12/LifeCells.git
#
# viewport - Подвижная лупа через которую смотрят на space.
# viewport = [space, x, y, w, h]

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
    """
    Initializes Graphics.

    Pygame initialize. Creates application window.

    Returns screen - main surface of application.
    """
    pygame.init()

    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("Life Cells demonstration")
    logging.debug("Graphics initialized")

    return screen



def init_space(name = "Universe"):
    """
    Creates space.

    Creates empty space and adds two colonies.

    Returns newly created space.
    """
    space = colony.new_space(name)

    col1 = ["00111",
            "011011",
            "1100011",
            "011011",
            "00111"]

    col2 = ["111"]

    space = colony.add_colony(space, col1)
    space = colony.add_colony(space, col2)
    logging.debug("Space [%s] created", name)

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
                pygame.draw.circle(screen,
                                   c_Cell[cIdx],
                                   ((x + xx)*10 + 5, (y + yy)*10 + 5),
                                   5)



# TODO: Add scrollable viewport for the space
def viewport_init(space, active_col, size):
    """
    Creates viewport for space.

    Creates viewport for space and set it over active colony.

    Returns viewport.
    """
    if len(space) > 2:
        # Найти центр активной колонии
        #       xc = col_x + col_w / 2
        #       yc = col_y + col_h / 2
        x = space[2 + active_col][0][1] + space[2 + active_col][0][3] / 2
        y = space[2 + active_col][0][2] + space[2 + active_col][0][4] / 2
        # Найти левый-верхний край viewport
        #       xv = xc - vport_w / 2
        #       yv = yc - vport_h / 2
        x -= size[0] / 2
        y -= size[1] / 2
        # Проверить положительность координат левого-верхнего угла viewport
        # если они отрицательные дать им нулевые значения
        if x < 0:
            x = 0
        if y < 0:
            y = 0 
    else:
        x, y = 0, 0
    logging.debug("Viewport for space %s created [%d, %d, %d, %d]", space[0], x, y, size[0], size[1])

    return [space, x, y, size[0], size[1]]




# TODO: Add scrollbars on the right and bottom side of the screen
# TODO: Make screen size dynamic
# TODO: Add minimap in left-bottom angle of the screen 
#       with viewport and colonies representation
# TODO: Add positioning of an active colony in the viewport center
#       on Space-key hit
# TODO: Add statistics on screen



def run():
    """
    Executes application.

    Creates context of application and runs event loop processing
    """
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
            if len(space) < 3:
                done = True
                continue
            if active_col > len(space) - 3:
                active_col = len(space) - 3
            screen.fill(C_BKGROUND)
            x = int((size[0]/10 - space[2 + active_col][0][3])/2)
            y = int((size[1]/10 - space[2 + active_col][0][4])/2)
            # TODO: Draw all colonies which are in viewport      
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