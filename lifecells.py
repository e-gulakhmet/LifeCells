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
import os.path

import pygame
import pygame.locals

import colony

# Define some colors
C_HDR_TEXT   = ( 255, 242,   0)
C_VAL_TEXT   = ( 255, 255, 255)
C_SPLIT_LINE = (   0, 255,   0)
C_BKGROUND   = (   0,   0,   0)

# Minimap colors
C_MM_BORDER = ( 128,   0,   0)
C_MM_SPACE  = (  10,  10,  10)
C_MM_VPORT  = ( 130, 130, 130)
C_MM_COLONY = (   0, 255,   0)

# Scrollbar colors
C_SB_END    = (255, 242,   0)
C_SB_LINE   = C_SB_END
C_SB_RUNNER = (255, 255, 255)

# Размер одной клетки
CELL_SIZE = 10
MINIMAP_SIZE = 150

# Размер окна помощи
HWND_SIZE = (200, 154)

# Найстройка повторения клавиш
KEY_DELAY = 100
KEY_INTERVAL = 100

# Минимальные размеры экрана
SCR_MIN_WIDTH = 700
SCR_MIN_HEIGHT = 500

# Размер полосы прокрутки
SBAR_SIZE = 30

# Отступы экрана
N_OFFSET = 40
E_OFFSET = 30
S_OFFSET = 30 + SBAR_SIZE + 4
W_OFFSET = 0

SPEED_NAME = ("SLW", "NRM", "FST")

def grp_init(size, spc_name):
    """
    Initializes Graphics.

    Pygame initialize. Creates application window.

    Returns screen - main surface of application.
    """
    pygame.init()

    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Life Cells demonstration for space ["
                                + spc_name + "]")

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
        x = int(vport[0][2 + active_col][0][1]
                + vport[0][2 + active_col][0][3] / 2)
        y = int(vport[0][2 + active_col][0][2]
                + vport[0][2 + active_col][0][4] / 2)
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
        # (xc <= xv + wv - 1 and xc >= xv) and
        # (yc + hc - 1 >= yv and yc + hc - 1 <= yv + hv - 1)
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
                    # Для каждой живой клетки колонии,
                    # проверить попадание во viewport
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
                        # Найти центр окружности
                        # которая будет изображать клетку
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




def info_space(space, screen, active_col):
    """
    Shows space info.

    Shows space size, number of colonies, active colony ID.
    """
    s_rect = screen.get_rect()

    surf = screen.subsurface(
            pygame.Rect(0, 0,
                        s_rect.w, N_OFFSET))
    
    font = pygame.font.SysFont("Consolas", 16, bold = True)

    # Воспроизвести текст. "True" значит,
    # что текст будет сглаженным (anti-aliased).
    # Чёрный - цвет. Переменную black мы задали ранее,
    # списком [0,0,0]
    # Заметьте: эта строка создаёт картинку с буквами,
    # но пока не выводит её на экран.
    hdr =      font.render("SPC_SZ[           ] NBR_COLS[     ] ACTV_COL#[   ] AGE_SPC[    ]" ,
                           True, C_HDR_TEXT)

    spc_size = get_space_size(space)
    spc_sz   = font.render("        " + str(spc_size[0]) + " , " + str(spc_size[1]),
                           True, C_VAL_TEXT)
    nbr_cols = font.render("                              " + str(len(space) - 2),
                           True, C_VAL_TEXT)
    actv_col = font.render("                                               "
                           + str(active_col), True, C_VAL_TEXT)
    age_spc  = font.render("                                                            "
                           + str(space[1]), True, C_VAL_TEXT)

    # Вывести сделанную картинку на экран в точке (250, 250)
    surf.blit(hdr, [10,int((N_OFFSET - 16) / 2)])
    surf.blit(spc_sz, [10,int((N_OFFSET - 16) / 2)])
    surf.blit(nbr_cols, [10,int((N_OFFSET - 16) / 2)])
    surf.blit(actv_col, [10,int((N_OFFSET - 16) / 2)])
    surf.blit(age_spc, [10,int((N_OFFSET - 16) / 2)])

    pygame.draw.line(surf, C_HDR_TEXT, (2, N_OFFSET - 4),
                    (s_rect.w - 2, N_OFFSET - 4), 2)



def speed_info(screen, speed):
    """
    Shows speed.

    Shows speed change of day.
    """
    s_rect = screen.get_rect()

    surf = screen.subsurface(
            pygame.Rect(MINIMAP_SIZE, s_rect.h - S_OFFSET,
                        s_rect.w - MINIMAP_SIZE, S_OFFSET))
    
    font = pygame.font.SysFont("Consolas", 16, bold = True)

    # Воспроизвести текст. "True" значит,
    # что текст будет сглаженным (anti-aliased).
    # Чёрный - цвет. Переменную black мы задали ранее,
    # списком [0,0,0]
    # Заметьте: эта строка создаёт картинку с буквами,
    # но пока не выводит её на экран.
    hdr_low = font.render("SPD[   ] Q for exit, H for help", True, C_HDR_TEXT)
    spd     = font.render("    " + SPEED_NAME[speed], True, C_VAL_TEXT)

    surf.blit(hdr_low, [10,int((30 - 16) / 2) + SBAR_SIZE + 4])
    surf.blit(spd, [10,int((30 - 16) / 2) + SBAR_SIZE + 4])
    
    pygame.draw.line(surf, C_HDR_TEXT, (2, SBAR_SIZE + 4),
                     (s_rect.w - MINIMAP_SIZE - 2, SBAR_SIZE + 4), 2)



def draw_help(screen):
    """
    Shows help screen.
    """
    s_rect = screen.get_rect()
    surf = screen.subsurface(
             pygame.Rect(5, N_OFFSET + 5, HWND_SIZE[0], HWND_SIZE[1]))

    font = pygame.font.SysFont("Consolas", 16, bold = True)
    # Рисуем рамку
    pygame.draw.rect(surf, C_MM_SPACE, (0, 0, HWND_SIZE[0], HWND_SIZE[1]))
    pygame.draw.rect(surf, C_HDR_TEXT, (2, 10,
                                        HWND_SIZE[0] - 4, HWND_SIZE[1] - 25),
                     2)
    nm_win = font.render(" Help ", True, C_VAL_TEXT)
    sz_txt = nm_win.get_rect()
    pygame.draw.rect(surf, C_MM_SPACE, (2 + int((HWND_SIZE[0] - sz_txt.w) / 2),
                                        2, sz_txt.w, sz_txt.h))
    surf.blit(nm_win, [2 + int((HWND_SIZE[0] - sz_txt.w) / 2), 2])

    nm_win = font.render(" ESC to close ", True, C_VAL_TEXT)
    sz_txt = nm_win.get_rect()
    pygame.draw.rect(surf, C_MM_SPACE, (2 + int((HWND_SIZE[0] - sz_txt.w) / 2),
                                        (HWND_SIZE[1] - sz_txt.h) - 5,
                     sz_txt.w, sz_txt.h))
    surf.blit(nm_win, [2 + int((HWND_SIZE[0] - sz_txt.w) / 2),
                       (HWND_SIZE[1] - sz_txt.h) - 5])
    
    # Вывести помощь в управлении
    h_txt = [["F", "Faster"],
             ["S", "Slower"],
             ["N", "Next colony"],
             ["P", "Prev. colony"],
             ["SPC", "Center vport"],
             ["←↑→↓", "Move vport"]]
    v_txt = 22
    for h_line in h_txt:
        h_key = font.render(h_line[0], True, C_HDR_TEXT)
        h_hint = font.render(h_line[1], True, C_VAL_TEXT)
        surf.blit(h_key, [15, v_txt])
        surf.blit(h_hint, [60, v_txt])
        v_txt += 16 + 2



def draw_hscroll(vport):
    """
    Draw horizontal scrollbar.
    """
    screen = vport[1]
    s_rect = screen.get_rect()
    sfw = s_rect.w - MINIMAP_SIZE
    surf = screen.subsurface(
             pygame.Rect(MINIMAP_SIZE, s_rect.h - S_OFFSET,
                         sfw, SBAR_SIZE))
    # Нарисовать левую стрелку
    pygame.draw.polygon(surf, C_SB_END, [(2, int(SBAR_SIZE / 2)),
                                         (int(SBAR_SIZE / 2) + 2, 0),
                                         (int(SBAR_SIZE / 2) + 2, SBAR_SIZE)],
                        2)
    # Нарисовать правую стрелку
    pygame.draw.polygon(surf, C_SB_END, [(sfw - int(SBAR_SIZE / 2) - 2, 0),
                                         (sfw - 2, int(SBAR_SIZE / 2)),
                                         (sfw - int(SBAR_SIZE / 2)
                                          - 2, SBAR_SIZE)], 2)
    # Нарисовать ленту
    pygame.draw.line(surf, C_SB_END,
                     (SBAR_SIZE + 2, int(SBAR_SIZE / 2)),
                     (sfw - SBAR_SIZE - 2, int(SBAR_SIZE / 2)), 2)
    # Нарисовать бегунок
    xr = get_hrunner_pos(vport) - MINIMAP_SIZE
    pygame.draw.circle(surf, C_BKGROUND, (xr,
                                          int(SBAR_SIZE / 2)),
                                          int(SBAR_SIZE / 2))
    pygame.draw.circle(surf, C_SB_RUNNER, (xr,
                                           int(SBAR_SIZE / 2)),
                       int(SBAR_SIZE / 2) - 4, 2)



def get_hrunner_pos(vport):
    """
    Calculate position of center of the hrunner
    """
    w, h = get_space_size(vport[0])
    s_rect = vport[1].get_rect()
    sfw = s_rect.w - MINIMAP_SIZE
    # Рассчитать масштаб
    # масштаб = реальный размер объекта / на размер его представления
    scale = (w - vport[4]) / (sfw - SBAR_SIZE * 2 - 4)

    return MINIMAP_SIZE + int(vport[2] / scale) + SBAR_SIZE + 2



def draw_vscroll(vport):
    """
    Draw vertical scrollbar.
    """
    screen = vport[1]
    s_rect = screen.get_rect()
    sfh = s_rect.h - N_OFFSET - S_OFFSET - 60
    surf = screen.subsurface(
             pygame.Rect(s_rect.w - E_OFFSET, N_OFFSET + 30,
                         SBAR_SIZE, sfh))
    # Нарисовать верхнюю стрелку
    pygame.draw.polygon(surf, C_SB_END, [(int(SBAR_SIZE / 2), 2),
                                         (0, int(SBAR_SIZE / 2) + 2),
                                         (SBAR_SIZE,
                                          int(SBAR_SIZE / 2) + 2)], 2)
    # Нарисовать нижнюю стрелку
    pygame.draw.polygon(surf, C_SB_END, [(int(SBAR_SIZE / 2), sfh - 2),
                                         (0, sfh - int(SBAR_SIZE / 2) - 2),
                                         (SBAR_SIZE,
                                          sfh - int(SBAR_SIZE / 2) - 2)], 2)
    # Нарисовать ленту
    pygame.draw.line(surf, C_SB_END,
                     (int(SBAR_SIZE / 2), SBAR_SIZE),
                     (int(SBAR_SIZE / 2), sfh - SBAR_SIZE - 2), 2)
    # Нарисовать бегунок
    yr = get_vrunner_pos(vport) - (N_OFFSET + 30) 
    pygame.draw.circle(surf, C_BKGROUND, (int(SBAR_SIZE / 2),
                                          yr), int(SBAR_SIZE / 2))
    pygame.draw.circle(surf, C_SB_RUNNER, (int(SBAR_SIZE / 2),
                                           yr),
                       int(SBAR_SIZE / 2) - 4, 2)



def get_vrunner_pos(vport):
    """
    Calculate position of center of the vrunner
    """
    w, h = get_space_size(vport[0])
    s_rect = vport[1].get_rect()
    sfh = s_rect.h - N_OFFSET - S_OFFSET - 60
    # Рассчитать масштаб
    # масштаб = реальный размер объекта / на размер его представления 
    scale = (h - vport[5]) / (sfh - SBAR_SIZE * 2 - 4)

    return N_OFFSET + 30 + int(vport[3] / scale) + SBAR_SIZE + 2
    


def run(space = None):
    """
    Executes application.

    Creates context of application and runs event loop processing
    """
    # Индекс активной колонии. Viewport будет центрироваться на эту колонию.
    active_col = 0

    # viewPort shift
    v_shift, h_shift = 0, 0

    if space == None:   
        space = init_space()

    screen = grp_init((SCR_MIN_WIDTH, SCR_MIN_HEIGHT), space[0])

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
    
    help = False
    h_runner = False
    v_runner = False
    mm_move = False
    
    full_screen = False
    prev_screen_size = screen.get_rect()
    # -------- Main Program Loop -----------
    while not done:

        # --- Main event loop
        for event in pygame.event.get():
            # Обработать события таймера,
            # запускающего новый день
            if event.type == pygame.USEREVENT:
                logging.debug("[EVT] New day.")
                newDay = True

            if event.type == pygame.QUIT:
                done = True
                logging.debug("[EVT] Quit")
                continue

            # Обработать событие изменения размеров экрана
            if event.type == pygame.VIDEORESIZE:
                size = list(event.dict["size"])
                logging.debug("[EVT] Video resize to [%d, %d]",
                              size[0], size[1])
                if size[0] < SCR_MIN_WIDTH:
                    size[0] = SCR_MIN_WIDTH
                if size[1] < SCR_MIN_HEIGHT:
                    size[1] = SCR_MIN_HEIGHT
                screen = pygame.display.set_mode(size,
                                                 pygame.DOUBLEBUF |
                                                 pygame.RESIZABLE)
                vport[1] = screen
                update_vport_size(vport)

            if event.type == pygame.MOUSEBUTTONUP:
                h_runner, v_runner = False, False
                mm_move = False
            
            if event.type == pygame.MOUSEMOTION:
                if h_runner or v_runner or mm_move:
                    mx, my = pygame.mouse.get_rel()
                    w, h = get_space_size(space)
                    s_rect = screen.get_rect()

                if h_runner:
                    sfw = s_rect.w - MINIMAP_SIZE
                    # Рассчитать масштаб
                    # масштаб = реальный размер объекта / на размер
                    # его представления
                    scale = (w - vport[4]) / (sfw - SBAR_SIZE * 2 - 4)
                    h_shift += int(mx * scale)
                
                if v_runner:
                    sfh = s_rect.h - N_OFFSET - S_OFFSET - 60
                    # Рассчитать масштаб
                    # масштаб = реальный размер объекта / на размер
                    # его представления 
                    scale = (h - vport[5]) / (sfh - SBAR_SIZE * 2 - 4)
                    v_shift += int(my * scale)
                
                if mm_move:
                    if h > w:
                        scale = h / MINIMAP_SIZE
                    else:
                        scale = w / MINIMAP_SIZE 
                    h_shift += int(mx * scale)
                    v_shift += int(my * scale)

            # Обработать нажатия мыши
            if (event.type == pygame.MOUSEBUTTONDOWN and
                pygame.mouse.get_pressed()[0]):
                mx, my = pygame.mouse.get_pos()
                s_rect = screen.get_rect()
                # Проверить попадание мыши в горизотальный скроллбар
                if (mx >= MINIMAP_SIZE + 2 and mx <= s_rect.w and
                    my >= s_rect.h - S_OFFSET and
                    s_rect.h - S_OFFSET + SBAR_SIZE):
                    xr = get_hrunner_pos(vport)
                    # Проверяем попадание в левый треугольник
                    if (mx >= MINIMAP_SIZE + 2 and
                        mx <= MINIMAP_SIZE + 2 + int(SBAR_SIZE / 2)):
                        h_shift -= 1
                    # Проверяем попадание в правый треугольник
                    elif (mx >= s_rect.w - int(SBAR_SIZE / 2) + 2 and
                         mx <= s_rect.w):
                        h_shift += 1
                    # Проверяем попадание мыши на ленту слева от бегунка
                    elif (mx >= MINIMAP_SIZE + SBAR_SIZE + 2 and
                          mx <= xr - int(SBAR_SIZE / 2)):
                        h_shift -= 10
                    # Проверяем попадание мыши на ленту справа от бугунка
                    elif (mx >= xr + int(SBAR_SIZE / 2) and
                          mx <= s_rect.w - SBAR_SIZE):
                        h_shift +=10
                    # При попадание в бегунок ставим флаг что курсор
                    # находится на бегунке
                    else:
                        pygame.mouse.get_rel()
                        h_runner = True
                
                # Проверить попадание мыши в minimap
                elif (mx >= 1 and mx <= MINIMAP_SIZE + 3 and
                      my >= s_rect.h - MINIMAP_SIZE - 3 and
                      my <= s_rect.h - 1):
                    # Найти значения x, y курсора внутри minimap
                    mmx = mx
                    mmy = my - (s_rect.h - MINIMAP_SIZE)
                    w, h = get_space_size(space)
                    h_offset, v_offset = 0, 0
                    scale = 0.0
                    if w > h:
                        scale = w / MINIMAP_SIZE
                        v_offset = int((MINIMAP_SIZE - (h / scale)) / 2)
                    else:
                        scale = h / MINIMAP_SIZE
                        h_offset = int((MINIMAP_SIZE - (w / scale)) / 2)
                    mmx -= h_offset
                    mmy -= v_offset
                    vx = int(mmx * scale)
                    vy = int(mmy * scale)
                    if vx < 0:
                        vx = 0
                    elif vx + vport[4] > w:
                        vx = w - vport[4]
                    if vy < 0:
                        vy = 0
                    elif vy + vport[5] > h:
                        vy = h - vport[5]
                    vport[2] = vx
                    vport[3] = vy

                    pygame.mouse.get_rel()
                    mm_move = True

                # Проверить попадение мыши в веритикальный скроллбар
                elif (mx >= s_rect.w - SBAR_SIZE and mx <= s_rect.w and
                      my >= N_OFFSET + 30 and my <= s_rect.h - S_OFFSET - 30):
                    yr = get_vrunner_pos(vport)
                    # Проверяем попадание мыши в верхний треугольник
                    if my >= N_OFFSET + 30 and my <= N_OFFSET + 30 + SBAR_SIZE:
                        v_shift -= 1
                    # Проверяем попадание мыши в нижний треугольник
                    elif (my >= s_rect.h - S_OFFSET - 30 - SBAR_SIZE and
                          my <= s_rect.h - S_OFFSET - 30):
                        v_shift += 1
                    # Проверяем попадание мыши на ленту сверху от бегунка 
                    elif (my >= N_OFFSET + 30 + SBAR_SIZE and
                          my <= yr - int(SBAR_SIZE / 2)):
                        v_shift -= 10
                    # Проверяем попадение мыши на ленту снизу от бегунка
                    elif (my >= yr + int(SBAR_SIZE / 2) and
                          my <= s_rect.h - S_OFFSET - 30 - SBAR_SIZE):
                        v_shift += 10
                    else:
                        pygame.mouse.get_rel()
                        v_runner = True

            # Обработать нажатия клавиш
            if event.type == pygame.KEYDOWN:
                logging.debug("[EVT] Key pressed [%s]",
                              pygame.key.name(event.key))
                if event.key == pygame.K_p: # select previous colony as active
                    active_col -= 1
                    if active_col < 0:
                        active_col = 0
                    vport_center_on(vport, active_col)

                elif event.key == pygame.K_n: # select next colony as active
                    active_col += 1
                    if active_col > len(space) - 3:
                        active_col = len(space) - 3
                    vport_center_on(vport, active_col)
                
                # center viewport on the active_col
                elif event.key == pygame.K_SPACE: 
                    vport_center_on(vport, active_col)

                elif event.key == pygame.K_q: # quit 
                    done = True
                    continue
                elif event.key == pygame.K_RETURN:
                    if pygame.key.get_mods() & pygame.KMOD_ALT:
                        if full_screen:
                            screen = pygame.display.set_mode(
                                        (prev_screen_size.w,
                                         prev_screen_size.h),
                                        pygame.DOUBLEBUF | pygame.RESIZABLE)
                            vport[1] = screen
                            update_vport_size(vport)
                            full_screen = False
                        else:
                            prev_screen_size = screen.get_rect()
                            screen = pygame.display.set_mode((1920, 1080),
                                                             pygame.FULLSCREEN)
                            vport[1] = screen
                            update_vport_size(vport)
                            full_screen = True
                            
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
                
                elif event.key == pygame.K_h: # open help window
                    help = True
                elif event.key == pygame.K_ESCAPE: # close help window
                    help = False

                elif event.key == pygame.K_s:   # make speed slower
                    if curr_speed > 0:
                        curr_speed -= 1
                        pygame.time.set_timer(pygame.USEREVENT,
                                              speed_steps[curr_speed])
                elif event.key == pygame.K_f:   # make speed faster
                    if curr_speed < 2:
                        curr_speed += 1
                        pygame.time.set_timer(pygame.USEREVENT,
                                              speed_steps[curr_speed])

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

        # Если сдвиг по вертикали(v_shift)
        # либо по горизонтали(h_shift) не равен нулю,
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
        info_space(space, screen, active_col)
        speed_info(screen, curr_speed)
        if help:
            draw_help(screen)
        draw_hscroll(vport)
        draw_vscroll(vport)

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
                        level=logging.ERROR,
                        format="%(asctime)s [%(levelname)s] : %(message)s")

    if os.path.isfile("lifecells.lcsf"):
        with open("lifecells.lcsf") as f:
            space = colony.load_from_file(f) 
    else:
        space = None

    run(space)



###############################################################################
# Entry point
###############################################################################
if __name__ == "__main__":
    main()