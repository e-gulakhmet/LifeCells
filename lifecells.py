# lifecells.py
# 
# Графическое представление жизни колонии клеток из библиотеки colony.py
#
# EnesGUL12, dr-dobermann, 2018.
#
# https://github.com/EnesGUL12/LifeCells.git
#
# viewport - Подвижная лупа через которую смотрят на space.
# viewport = [space, screen, x, y, w, h, offset]
# space - Пространство которое мы наблюдаем
# screen - Эктран на котором мы рисуем
# x, y, w, h, - Начальные кардинаты и размеры viewport (еденица измерения в клетках)
# offset - Отступы в точках от границ экрана

import logging
import pygame
import pygame.locals
import colony

# Define some colors
C_HDR_TEXT   = (   0,   0,   0)
C_VAL_TEXT   = ( 255, 255, 255)
C_SPLIT_LINE = (   0, 255,   0)
C_BKGROUND   = (   0,   0,   0)

# Размер одной клетки
CELL_SIZE = 10



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
def viewport_init(space, active_col, screen, offset):
    """
    Creates viewport for space.

    Creates viewport for space and set it over active colony.

    Parameters:
      space      - Space the viewport linked to
      active_col - index of active colony to view in the viewport
      screen     - screen to draw viewport on
      offset     - offset from edges of display (north, east, south, west)

    Returns viewport.
    """
    if len(space) > 2:
        # Найти центр активной колонии
        #       xc = col_x + col_w / 2
        #       yc = col_y + col_h / 2
        x = int(space[2 + active_col][0][1] + space[2 + active_col][0][3] / 2)
        y = int(space[2 + active_col][0][2] + space[2 + active_col][0][4] / 2)
        # Получить размеры экрана
        s_rect = screen.get_rect()
        # Отнять отступы (offsets)
        w = s_rect.w - offset[1] - offset[3]
        h = s_rect.h - offset[0] - offset[2]
        # Разделить на размер одной клетки
        w = int(w / CELL_SIZE)
        h = int(h / CELL_SIZE)
        # Найти левый-верхний край viewport
        #       xv = xc - vport_w / 2
        #       yv = yc - vport_h / 2
        x -= int(w / 2)
        y -= int(h / 2)
        # Проверить положительность координат левого-верхнего угла viewport
        # если они отрицательные дать им нулевые значения
        if x < 0:
            x = 0
        if y < 0:
            y = 0 
    else:
        x, y = 0, 0
    logging.debug("Viewport for space %s created [%d, %d, %d, %d]", space[0], x, y, w, h)

    return [space, screen, x, y, w, h, offset]



# TODO: Add scrollbars on the right and bottom side of the screen
# TODO: Make screen size dynamic
# TODO: Add minimap in left-bottom angle of the screen 
#       with viewport and colonies representation
# TODO: Add positioning of an active colony in the viewport center
#       on Space-key hit
# TODO: Add statistics on screen



def draw_vport(vport, size):
    """
    Draw viewport.

    Draw viewport for space.
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

    surf = vport[1].subsurface(
            pygame.Rect(vport[6][3], vport[6][0],
                        size[0]- vport[6][3] - vport[6][1],
                        size[1] - vport[6][0] - vport[6][2]))

    for col in vport[0][2:]:
        # Проверить попадание левого нижнего угла колонии во viewport
        # (xc <= xv + wv - 1 and xc >= xv) and (yc + hc - 1 >= yv and yc + hc - 1 <= yv + hv - 1)
        if (((col[0][1] <= vport[2] + vport[4] - 1 and col[0][1] >= vport[2])
             and (col[0][2] + col[0][4] - 1 >= vport[3] 
                  and col[0][2] + col[0][4] - 1 <= vport[3] + vport[5] - 1))
           # Проверить пападание правого нижнего угла колонии во viewport
           # (xc + wc - 1 >= xv and xc + wc - 1 <= xv + wv - 1)
           # and (yc + hc - 1 >= yv and yc + hc - 1 <= yv + hv - 1)
            or ((col[0][1] + col[0][3] - 1 >= vport[2]
                 and col[0][1] + col[0][3] - 1 <= vport[2] + vport[4] - 1)
                and (col[0][2] + col[0][4] - 1 >= vport[3]
                     and col[0][2] + col[0][4] - 1 <= vport[3] + vport[5] - 1))
          # Проверить попадания левого верхнего угла колонии во viewport
          # (xc >= xv and xc <= xv + wv - 1) 
          # and (yc >= yv and yc <= yv + hv - 1)
            or ((col[0][1] >= vport[2] 
                 and col[0][1] <= vport[2] + vport[4] - 1)
                and (col[0][2] >= vport[3] 
                     and col[0][2] <= vport[3] + vport[5] - 1))
          # Проверить попадение правого верхнего угла колонии во viewport
          # (xc + wc - 1 >= xv and xc + wc - 1 <= xv + wv - 1)
          # and (yc >= yv and yc <= yv + hv - 1)
            or ((col[0][1] + col[0][3] - 1 >= vport[2]
                 and col[0][1] + col[0][3] - 1 <= vport[2] + vport[4] - 1)
                and (col[0][2] >= vport[3]
                     and col[0][2] <= vport[3] + vport[5] - 1))):
            for yc, row in enumerate(col[1]):
                yc += col[0][2]
                for xc, cell in enumerate(row):
                    # Для каждой живой клетки колонии, проверить попадание во viewport
                    # (xc >= xv and xc <= xv + wv - 1)
                    # and (yc >= yv and yc <= yv + hv - 1)
                    # Найти кординаты клетки в space
                    xc += col[0][1]
                    if (cell[0] > 0
                       and ((xc >= vport[2] 
                             and xc <= vport[2] + vport[4] - 1)
                            and (yc >= vport[3]
                                 and yc <= vport[3] + vport[5] - 1))):
                        if cell[0] > 9:
                            cIdx = 0
                        else:
                            cIdx = cell[0]
                        # Найти положение клетки внутри viewport
                        # xcv = xc - xv
                        # ycv = yc - yv
                        # Найти центр окружности которая будет изображать клетку
                        # Cxcv = xcv * CELL_SIZE + CELL_SIZE / 2
                        # Cycv = ycv * CELL_SIZE + CELL_SIZE / 2 
                        pygame.draw.circle(surf,
                                           c_Cell[cIdx],
                                           (int((xc - vport[2])*CELL_SIZE + CELL_SIZE / 2),
                                            int((yc - vport[3])*CELL_SIZE + CELL_SIZE / 2)),
                                           int(CELL_SIZE / 2))



def get_space_size(space):
    """
    Get spase size.

    Get space size with help colonies
    """
    w, h = 0, 0 
    for col in space[2:]:
        # Если xс + wс > ws, присвоить ws значение xс + wс
        if col[0][1] + col[0][3] > w:
            w = col[0][1] + col[0][3]
        # Если yс + hс > hs, присвоить hs значение yс + hс
        if col[0][2] + col[0][4] > h:
            h = col[0][2] + col[0][4]
        
    return w, h



def run():
    """
    Executes application.

    Creates context of application and runs event loop processing
    """
    # Индекс активной колонии. Viewport будет центрироваться на эту колонию.
    active_col = 0

    # viewPort shift
    v_shift, h_shift = 0, 0

    # size хранит текушие размеры окна приложения в точках [w, h]
    size = [700, 500]

    space = init_space()

    screen = grp_init(size)

    vport = viewport_init(space, active_col, screen, (40, 30, 30, 0))

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
    w, h = 0, 0
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
                        v_shift -= 10
                    else:
                        v_shift -= 1
                elif event.key == pygame.K_RIGHT: # shift viewport right
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift += 10
                    else:
                        h_shift += 1
                elif event.key == pygame.K_LEFT: # shift viewport left
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        h_shift -= 10
                    else:
                        h_shift -= 1
                elif event.key == pygame.K_DOWN: # shift viewport down
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        v_shift += 10
                    else:
                        v_shift += 1
                elif event.key == pygame.K_s:   # make speed slower
                    if curr_speed > 0:
                        curr_speed -= 1
                        pygame.time.set_timer(pygame.USEREVENT, speed_steps[curr_speed])
                elif event.key == pygame.K_f:   # make speed faster
                    if curr_speed < 2:
                        curr_speed += 1
                        pygame.time.set_timer(pygame.USEREVENT, speed_steps[curr_speed])


        # --- Game logic should go here
        if newDay:
            colony.next_day(space)
            if len(space) < 3:
                done = True
                continue
            if active_col > len(space) - 3:
                active_col = len(space) - 3
            newDay = False

        # Если сдвиг по вертикали(v_shift) либо по горизонтали(h_shift) не равен нулю,
        # сдвинуть viewport на необходимое количество клеток
        # [space, screen, x, y, w, h, offset]
        if v_shift != 0 or h_shift != 0:
            w, h = get_space_size(space)
            if vport[4] >= w:
                vport[2] = 0
            else:
                if h_shift != 0:
                    vport[2] += h_shift
                    if vport[2] + vport[4] - 1 > w:
                        vport[2] = w - vport[4]
                    if vport[2] < 0:
                        vport[2] = 0
                
            if vport[5] >= h:
                vport[3] = 0
            else:   
                if v_shift != 0:
                    vport[3] += v_shift
                    if vport[3] + vport[5] - 1 > h:
                        vport[3] = h - vport[5]
                    if vport[3] < 0:
                        vport[3] = 0
            v_shift = 0
            h_shift = 0
        
            





        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        

        # --- Drawing code should go here

        # TODO: Draw all colonies which are in viewport      
        draw_vport(vport, size)

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