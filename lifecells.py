# lifecells.py
# 
# Графическое представление жизни колонии клеток из библиотеки colony.py
# 
#
#
#

import logging
import pygame
import colony



def grp_init():
    pygame.init()

    size=[700, 500]
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
    x = int((70 - col[0][3])/2)
    y = int((50 - col[0][4])/2)
    for yy, row in enumerate(col[1]):
        for xx, cell in enumerate(row):
            if cell[0] != 0:
                if cell[0] > 9:
                    cIdx = 0
                else:
                    cIdx = cell[0]
                pygame.draw.circle(screen, c_Cell[cIdx], ((x + xx)*10 + 5, (y + yy)*10 + 5), 5)



def run():
    
    space = init_space()

    screen = grp_init()

    clock = pygame.time.Clock()

    # Define some colors
    c_headerTxt      = (   0,   0,   0)
    c_valueTxt       = ( 255, 255, 255)
    c_splitLine      = (   0, 255,   0)
    c_bkGround       = (   0,   0,   0)
    c_cells         = [(),
                       ()
                      ] 
    

    font = pygame.font.Font(None, 25)
 
    # Воспроизвести текст. "True" значит,
    # что текст будет сглаженным (anti-aliased).
    # Чёрный - цвет. Переменную black мы задали ранее,
    # списком [0,0,0]
    # Заметьте: эта строка создаёт картинку с буквами,
    # но пока не выводит её на экран.
    # text = font.render("My text", True, c_valueTxt)
    
    # Вывести сделанную картинку на экран в точке (250, 250)
    # screen.blit(text, [250,250])

    active_col = 0

    v_shift, h_shift = 0, 0

    done = False
    # -------- Main Program Loop -----------
    while not done:

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    active_col -= 1
                    if active_col < 0:
                        active_col = 0
                elif event.key == pygame.K_n:
                    active_col += 1
                    if active_col > len(space) - 3:
                        active_col = len(space) - 3
                elif event.key == pygame.K_q:
                    done = True
                    continue
                elif event.key == pygame.K_UP:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        v_shift = -10
                    else:
                        v_shift = -1
                elif event.key == pygame.K_RIGHT:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift = -10
                    else:
                        h_shift = -1
                elif event.key == pygame.K_LEFT:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift = -10
                    else:
                        h_shift = - 1
                elif event.key == pygame.K_DOWN:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        v_shift = -10
                    else:
                        v_shift = - 1
 
                
        # --- Game logic should go here
    
        # --- Screen-clearing code goes here
    
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(c_bkGround)
    
        # --- Drawing code should go here
        draw_col(screen, 0, 0, space[2 + active_col])
    
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        colony.next_day(space)

        if active_col > len(space) - 3:
            active_col = len(space) -3
    
        # --- Limit to 60 frames per second
        clock.tick(1)
    
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