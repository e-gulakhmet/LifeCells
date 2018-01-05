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

    size=[700,500]
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



def run():
    
    space = init_space()

    screen = grp_init()

    clock = pygame.time.Clock()

    # Define some colors
    c_headerTxt      = (   0,   0,   0)
    c_valueTxt       = ( 255, 255, 255)
    c_splitLine      = (   0, 255,   0)
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
    text = font.render("My text", True, c_valueTxt)
    
    # Вывести сделанную картинку на экран в точке (250, 250)
    screen.blit(text, [250,250])

    done = False
    # -------- Main Program Loop -----------
    while not done:

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # --- Game logic should go here
    
        # --- Screen-clearing code goes here
    
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        # screen.fill(WHITE)
    
        # --- Drawing code should go here
    
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
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
                        level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] : %(message)s")
     
    run()



###############################################################################
# Entry point
###############################################################################
if __name__ == "__main__":
    main()