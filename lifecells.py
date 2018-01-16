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

# Minimap colors
C_MM_BORDER = ( 128,   0,   0)
C_MM_SPACE  = (  10,  10,  10)
C_MM_VPORT  = ( 130, 130, 130)
C_MM_COLONY = (   0, 255,   0)


# Размер одной клетки
CELL_SIZE = 10
MINIMAP_SIZE = 150

# Найстройка повторения клавиш
KEY_DELAY = 100
KEY_INTERVAL = 100

# Минимальные размеры экрана
SCR_MIN_WIDTH = 700
SCR_MIN_HEIGHT = 500

# Отступы экрана
N_OFFSET = 40
E_OFFSET = 30
S_OFFSET = 30
W_OFFSET = 0

def grp_init(size):
    """
    Initializes Graphics.

    Pygame initialize. Creates application window.

    Returns screen - main surface of application.
    """
    pygame.init()

    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Life Cells demonstration")

    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
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



def vport_center_on(vport, active_col):
    """
    Centers viewport over the active colony
    """
    if active_col >= 0 and active_col <= len(vport[0]) - 3:
        # Найти центр активной колонии
        #       xc = col_x + col_w / 2
        #       yc = col_y + col_h / 2
        x = int(vport[0][2 + active_col][0][1] + vport[0][2 + active_col][0][3] / 2)
        y = int(vport[0][2 + active_col][0][2] + vport[0][2 + active_col][0][4] / 2)
        # Найти левый-верхний край viewport
        #       xv = xc - vport_w / 2
        #       yv = yc - vport_h / 2
        x -= int(vport[4] / 2)
        y -= int(vport[5] / 2)
        # Проверить положительность координат левого-верхнего угла viewport
        # если они отрицательные дать им нулевые значения
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        vport[2], vport[3] = x, y

        ws, hs = get_space_size(vport[0])
        if vport[2] + vport[4] > ws:
            vport[2] = ws - vport[4]
        if vport[3] + vport[5] > hs:
            vport[3] = hs - vport[5]
    else:
        vport[2], vport[3] = 0, 0



def update_vport_size(vport):
    """
    Updates viewport size according to screen size
    """
    # Получить размеры экрана
    s_rect = vport[1].get_rect()
    # Отнять отступы (offsets)
    w = s_rect.w - vport[6][1] - vport[6][3]
    h = s_rect.h - vport[6][0] - vport[6][2]
    # Разделить на размер одной клетки
    w = int(w / CELL_SIZE)
    h = int(h / CELL_SIZE)
    # Найти левый-верхний край viewport
    #       xv = xv - (w - vport_w) / 2
    #       yv = yv - (h - vport_h) / 2
    vport[2] -= int((w - vport[4]) / 2)
    vport[3] -= int((h - vport[5]) / 2)
    vport[4] = w
    vport[5] = h
    # Проверить выход viewport за границы экрана
    if vport[2] < 0:
        vport[2] = 0
    if vport[3] < 0:
        vport[3] = 0

    ws, hs = get_space_size(vport[0])
    if vport[2] + vport[4] - 1 > ws:
        vport[2] = ws - vport[4]
    if vport[3] + vport[5] - 1 > hs:
        vport[3] = hs - vport[5]



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
    vport = [space, screen, 0, 0, 0, 0, offset]

    update_vport_size(vport)
    vport_center_on(vport, active_col)

    logging.debug("Viewport for space %s created [%d, %d, %d, %d]",
                  space[0], vport[2], vport[3], vport[4], vport[5])

    return vport



# TODO: Add scrollbars on the right and bottom side of the screen
# TODO: Add statistics on screen

def draw_minimap(vport):
    """
    Draws a minimap
    Draws minimap in left-bottom corner
    """
    s_rect = vport[1].get_rect()
    size = (s_rect.w, s_rect.h)

    surf = vport[1].subsurface(
            pygame.Rect(0, size[1] - MINIMAP_SIZE - 3,
                        MINIMAP_SIZE + 3, MINIMAP_SIZE + 3))

    # Нарисовать space
    w, h = get_space_size(vport[0])
    h_offset, v_offset = 0, 0
    # Определить ширину отступов по бокам либо сверху и снизу
    # Если ширина space больше чем его высота, то отступы будут сверху и снизу
    if w > h:
        # h_offset = (100 - (w / 100) * h) / 2
        h_offset = int((MINIMAP_SIZE - h / (w / MINIMAP_SIZE)) / 2)
    # Если высота space больше чем его ширина, то отступы будут слева и справа
    if h > w:
        v_offset = int((MINIMAP_SIZE - w / (h / MINIMAP_SIZE)) / 2)

    # Нарисовать пространство
    pygame.draw.rect(surf, C_MM_SPACE,
                     pygame.Rect(1 + v_offset, 1 + h_offset,
                                 MINIMAP_SIZE - 2 * v_offset,
                                 MINIMAP_SIZE - 2 * h_offset))

    # Нарисовать рамку viewport
    if w > h:
        scale = w / MINIMAP_SIZE
    else:
        scale = h / MINIMAP_SIZE
    pygame.draw.rect(surf, C_MM_VPORT,
                     pygame.Rect(1 + v_offset + int(vport[2] / scale),
                                 1 + h_offset + int(vport[3] / scale),
                                 int(vport[4] / scale),
                                 int(vport[5] / scale)),
                     1)

    # Нарисовать рамку minimap
    pygame.draw.rect(surf, C_MM_BORDER,
                     pygame.Rect(0, 0, MINIMAP_SIZE + 2, MINIMAP_SIZE + 2), 1)

    # Отобразить все колонии
    for col in vport[0][2:]:
        # Поскольку колонии очень малы по отношению к space
        # отобразить центр колонии
        # xcc = xc + w / 2
        # ycc = yc + h / 2
        xcc = 1 + v_offset + int((col[0][1] + col[0][3] / 2) / scale)
        ycc = 1 + h_offset + int((col[0][2] + col[0][4] / 2) / scale)
        pygame.draw.line(surf, C_MM_COLONY,
                         (xcc, ycc), (xcc, ycc), 1)



def draw_vport(vport):
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

    s_rect = vport[1].get_rect()
    size = (s_rect.w, s_rect.h)

    surf = vport[1].subsurface(
            pygame.Rect(vport[6][3], vport[6][0],
                        size[0] - vport[6][3] - vport[6][1],
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
                        # Определить цвет клетки в зависимости от ее возраста
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
                                           (int((xc - vport[2])*CELL_SIZE
                                                + CELL_SIZE / 2),
                                            int((yc - vport[3])*CELL_SIZE
                                                + CELL_SIZE / 2)),
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

    space = init_space()

    screen = grp_init((SCR_MIN_WIDTH, SCR_MIN_HEIGHT))

    vport = viewport_init(space, active_col, screen, 
                         (N_OFFSET, E_OFFSET, S_OFFSET, W_OFFSET))

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
            # Обработать события таймера,
            # запускающего новый день
            if event.type == pygame.USEREVENT:
                newDay = True

            if event.type == pygame.QUIT:
                done = True
                continue

            # Обработать событие изменения размеров экрана
            if event.type == pygame.VIDEORESIZE:
                size = list(event.dict["size"])
                if size[0] < SCR_MIN_WIDTH:
                    size[0] = SCR_MIN_WIDTH
                if size[1] < SCR_MIN_HEIGHT:
                    size[1] = SCR_MIN_HEIGHT    
                screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.RESIZABLE)
                vport[1] = screen
                update_vport_size(vport)

            # Обработать нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # select previous colony as active
                    active_col -= 1
                    if active_col < 0:
                        active_col = 0

                elif event.key == pygame.K_n: # select next colony as active
                    active_col += 1
                    if active_col > len(space) - 3:
                        active_col = len(space) - 3

                # center viewport on the active_col
                elif event.key == pygame.K_SPACE: 
                    vport_center_on(vport, active_col)

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
            nCol = len(space) - 3
            colony.next_day(space)
            if len(space) < 3:
                done = True
                continue
            if nCol != len(space) - 3:
                if active_col > len(space) - 3:
                    active_col = len(space) - 3
                update_vport_size(vport)
                vport_center_on(vport, active_col)
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
                    if vport[2] < 0:
                        vport[2] = 0
                    if vport[2] + vport[4] - 1 > w:
                        vport[2] = w - vport[4]
                
            if vport[5] >= h:
                vport[3] = 0
            else:   
                if v_shift != 0:
                    vport[3] += v_shift
                    if vport[3] < 0:
                        vport[3] = 0
                    if vport[3] + vport[5] - 1 > h:
                        vport[3] = h - vport[5]
            v_shift = 0
            h_shift = 0

        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        

        # --- Drawing code should go here      
        draw_vport(vport)
        draw_minimap(vport)


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