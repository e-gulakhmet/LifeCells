# colony.py
#
# EnesGUL12, dr-dobermann, 2018.
#
# https://github.com/EnesGUL12/LifeCells.git
#
# Решение задачи "Клетки жизни" из книги Чарльза Уэзэрел
#
# В Пространстве существуют Колонии Клеток.
# Пространство изменяется по дням.
# По результатам каждого дня клетки могут возникать, умерать, либо оставаться
# в прежнем, постарев на один день.
# Данные Пространства представляются в виде списка колоний
# space = [space_name, age, col1, col2, col3, ...]
#
# Правила возникновения, смерти либо жизни клеток:
#     - если у клетки более трех соседей, то она умирает от тесноты
#     - если у клетки менее двух соседей, то она умирает от одиночества
#     - если у пустой клетки три соседа, то в ней возникает жизнь
#
# Если в колонии не осталось живых клеток она исчезает из пространаства.
# Соприкосающиеся колонии сливаются в одну. Более старшая колония остается,
# а младщая передает ей все клетки и исчезает из пространства.
#
# Колония представляется кординатами верхнего левого угла колонии и ее шириной
# и высотой, а также списком сторок в которых находятся клетки.
# В колонии крайние клетки должны быть отделены от границ колонии пустыми
# рядами(сверху и снизу) и пустыми столбцами(справа и слева).
# Не допускается более одного пустого столбца или ряда по границам колонии.
# Например:
#  ----
# |    |
# | X  |
# | XX |
# |    |
#  ----
#
# Данные о колонии представлены списком
# [[age, x, y, w, h, colID], [row1, row2, row3, row4]]
# Если возвраст колонии больше 0, то добавлять новые строки клеток в
# нее уже нельзя.
# Каждая строчка представляется списком клеток
# row = [cell1, cell2, cell3, cell4, ...]
#
# Клетка представляется возрастом клетки и списком соседних клеток в которых
# живая клетка обозначается 1, а пустая 0. Соседями каждой клетки считаются
# восемь клеток соприкасающимися с ней гранями и углами.
#   8 1 2
#   7 X 3
#   6 5 4
# Данные клетки представлены списком [age, [n1, n2, n3, ..., n8]]
# Если клетка пустая то ее возраст равен 0
# Номера соседних клеток начинаются с северного направления и далее по
# часовой стрелке.

# TODO: Add creating a space from a space_file


import random
import sys
import logging
from functools import reduce

###############################################################################
# Space functions
###############################################################################
def new_space(name):
    """
    Create new space

    Retruns empty list of colonies of space.
    """
    if name == "":
        logging.critical("Empty colony names aren't allowed.\n")
        sys.exit()

    logging.info("New space created with name [%s]", name)

    return list([name, 0])



def add_colony(space, col_mask = [], x = -1, y = -1):
    """
    Add an empty colony to the space

    Creates an empty colony at random coordinates and
    adds it to the space.
    If col_mask is not empty, fills the colony according
    to given mask.

    Returns updated space
    """
    if x == -1:
        x = int(random.random()*1000)
    if y == -1:
        y = int(random.random()*1000)
    space.append([
                  [0,
                   x,
                   y,
                   0, 0, len(space) - 2
                  ],
                  []
                 ])
    logging.info("An empty colony added to the space [%s]", space[0])

    for r in col_mask:
        load_row(space[len(space) - 1], r)

    return space



def next_day(space):
    """
    Sets new day for the space

    Updates all the colonies of the space.
    Removes dead colonies from the space.
    Updates the age of the space.
    """
    logging.debug("Changing day for space %s...", space[0])
    # Проверить состояние колонии и убрать отмершие
    for col in space[2:]:
        if len(col[1]) == 0:
            space.remove(col)
            logging.info("Colony #%d deleted as dead from space %s.",
                         col[0][5], space[0])

    # TODO: Перед первым днем проверить колонии на совпадения и 
    #       раздвинуть их по необходимости
    if space[1] == 0:
        for col1 in space[2:]:
            for col2 in space[2:]:
                if col1 != col2:
                    # ((x1 <= x2 and x1 + w1 >= x2) 
                    #  or (x1 >= x2 and x1 <= x2 + w2))
                    # and ((y1 <= y2 and y1 + h1 <= y2)
                    #      or (y1 >= y2 and y1 <= y2 + h2))
                    if (((col1[0][1] <= col2[0][1] 
                        and col1[0][1] + col1[0][3] >= col2[0][1])
                        or (col1[0][1] >= col2[0][1] 
                            and col1[0][1] <= col2[0][1] + col2[0][3]))
                        and ((col1[0][2] <= col2[0][2]
                            and col1[0][2] + col1[0][4] <= col2[0][2])
                            or (col1[0][2] >= col2[0][2]
                                and col1[0][2] <= col2[0][2] + col2[0][4]))):
                        # x2 = x2 + w1 + w2
                        # y2 = y2 + h1 + h2
                        logging.info("Colony #%d collides with colony #%d",
                                    col1[0][5], col2[0][5])
                        col2[0][1] += col1[0][3] + col2[0][3]
                        col2[0][2] += col1[0][4] + col2[0][4]
                        logging.info("New coordinates set for colony #%d [%d, %d]",
                                     col2[0][5], col2[0][1], col2[0][2])

    # Для каждой колонии в пространстве изменить состояние на один день
    for col in space[2:]:
        update(col)

    # расширить пространство, если колония имеет отрицательные координаты
    for col in space[2:]:
        if col[0][1] == -1:
            for ccol in space[2:]:
                if col != ccol:
                    ccol[0][1] += 1
            col[0][1] = 0         
        if col[0][2] == -1:
            for ccol in space[2:]:
                if col != ccol:
                    ccol[0][2] += 1
            col[0][2] = 0         
        
    # Проверить колонии на соприкосновение и, по-необходимости,
    # обЪединить соседние
    check_intersection(space)

    # Изменить возраст пространства на один день
    space[1] += 1
    logging.info("For the space [%s] %d day is set.", space[0], space[1])



def run(space, days = 1000):
    """
    Starts and runs the space

    Starts the space and manages its lifecycle for given amount of days
    """
    logging.info("Space %s started.", space[0])
    while len(space) > 2 and days > 0 :
        next_day(space)
        display_space(space)
        days -= 1

    logging.info("Space %s disapeared on %d day.", space[0], space[1])



def check_intersection(space):
    """
    Checks intersections of the colonies

    Checks intersections of the colonies and if so, unites them.
    The older colony inherits all the cell of the younger one.
    The younger one is disappeared from the space.
    """
    if len(space) - 2 <= 1:
        return

    for col1 in space[2:]:
        for col2 in space[space.index(col1) + 1:]:
            # isec определяет существование пересечения
            # если isec == 1, пересечение было по вертикальной оси
            # если isec == 2, пересечение было по горизонтальной оси
            isec = 0
            # Определить пересечение по вертикальной оси
            # x1 + w1 == x2 or x1 == x2 + w2
            if ((col1[0][0] >= 0 and col2[0][0] >= 0)
                and ((col1[0][1] + col1[0][3] == col2[0][1])
                or (col1[0][1] == col2[0][1] + col2[0][3]))):
                # y1 >= y2 and y1 + h1 >= y2
                if ((col1[0][2] >= col2[0][2]
                     and col1[0][2] + col1[0][4] >= col2[0][2])
                   # y1 <= y2 + h2 and y1 + h1 >= y2 + h2 
                    or (col1[0][2] <= col2[0][2] + col2[0][4]
                        and col1[0][2] + col1[0][4] >= col2[0][2] + col2[0][4])
                   # y1 <= y2 and y1 + h1 <= y2 + h2
                    or (col1[0][2] <= col2[0][2]
                        and col1[0][2] + col1[0][4]
                            <= col2[0][2] + col2[0][4])):
                    logging.debug("Colony #%d and colony #%d intersect " \
                                  "vertically", 
                                   col1[0][5], col2[0][5])
                    isec = 1

            # Определить пересечение по горизонтальной оси       
            # y1 == y2 + h2 or y1 + h1 == y2 
            if (isec == 0
                and (col1[0][2] == col2[0][2] + col2[0][4]
                     or col1[0][2] + col1[0][4] == col2[0][2])):
                # x1 >= x2 and x1 + w1 >= x2
                if ((col1[0][1] >= col2[0][1]
                     and col1[0][1] + col1[0][3] >= col2[0][1])
                     # x1 <= x2 + w2 and x1 + w1 >= x2
                     or (col1[0][1] <= col2[0][1] + col2[0][3]
                         and col1[0][1] + col1[0][3] >= col2[0][1])
                    # x1 <= x2 and x1 + w1 <= x2 + w2
                     or (col1[0][1] <= col2[0][1]
                         and col1[0][1] + col1[0][3]
                             <= col2[0][1] + col2[0][3])):
                    isec = 2
                    logging.debug("Colony #%d and colony #%d intersect " \
                                  "horizontally",
                                  col1[0][5], col2[0][5])

            # Если колонии соприкасаются по вертикальной оси
            if isec == 1:
                # Создать новую колонию, помещающую в себя обе объеденяемые
                # колонии
                ncol = list([
                                [ # age = col1.age
                                col1[0][0],
                                # x = min(x1, x2)
                                min(col1[0][1], col2[0][1]),
                                # y = min(y1, y2)
                                min(col1[0][2], col2[0][2]),
                                # w = w1 + w2
                                col1[0][3] + col2[0][3],
                                # h = max(y1 + h1, y2 + h2) - min(y1, y2)
                                max(col1[0][2] + col1[0][4],
                                    col2[0][2] + col2[0][4])
                                - min(col1[0][2], col2[0][2]),
                                # colID = col1.colID
                                col1[0][5]
                                ],
                            list()])

                # Определить левую и правую колонии 
                if col1[0][1] < col2[0][1]:
                    coll = col1
                    colr = col2
                else:
                    coll = col2
                    colr = col1
                # Для каждой строчки новой колонии из двух частей правой и
                # левой сфомировать общую строку.
                # Если првая или левая часть находится в текущей строке цикла,
                # добавить ее как есть.
                # Если там строки нет, то сформировать строку пустых клеток
                # необходимой ширины. 
                for y in range(ncol[0][4]):
                    # Сформировать левую сторону строки новой колонии.
                    if (ncol[0][2] + y >= coll[0][2] and
                        ncol[0][2] + y <= coll[0][2] + coll[0][4] - 1):
                        lpart = coll[1][ncol[0][2] + y - coll[0][2]]
                    else:
                        lpart = [[0, [0 for j in range(8)]] for i in range(coll[0][3])]
                    
                    # Сформировать правую сторону строки новой колонии.
                    if (ncol[0][2] + y >= colr[0][2] and
                        ncol[0][2] + y <= colr[0][2] + colr[0][4] - 1):
                        rpart = colr[1][ncol[0][2] + y - colr[0][2]]
                    else:
                        rpart = [[0, [0 for j in range(8)]] for i in range(colr[0][3])]
                    
                    ncol[1].append(lpart + rpart)

            # Если колонии соприкасаются по горизонтальной оси
            if isec == 2:
                # Создать новую колонию помещающую в себя обе объеденяемые
                # колонии
                ncol = list([ 
                                [ # age = col1.age
                                col1[0][0],
                                # x = min(x1, x2)
                                min(col1[0][1], col2[0][1]),
                                # y = min(y1, y2)
                                min(col1[0][2], col2[0][2]),
                                # w = max(x1 + w1, x2 + w2) - min(x1, x2)
                                max(col1[0][1] + col1[0][3], col2[0][1] + col2[0][3])
                                - min(col1[0][1], col2[0][1]),                                    
                                # h = h1 + h2
                                col1[0][4] + col2[0][4],
                                # colID = col1.colID
                                col1[0][5]
                                ],
                            list()])

                # Для всех записей новой колонии сделать следующее:
                #  - проверить какой колонии принадлежит текущая строка
                #  - взять всю строку из активной колонии 
                #  - если строка начинается не с начала новой колонии, то
                #    дополнить ее необходимым количеством пустых клеток
                #    слева
                #  - если ширина строки меньше чем ширина новой колонии,
                #    то дополнить ее необходимым количеством пустых клеток
                #    справа
                for y in range(ncol[0][4]):
                    if (ncol[0][2] + y >= col1[0][2] and
                        ncol[0][2] + y <= col1[0][2] + col1[0][4]):
                        colp = col1
                    else:
                        colp = col2

                    nrow = colp[1][ncol[0][2] + y - colp[0][2]]
                    for i in range(colp[0][1] - ncol[0][1]):
                        nrow.insert(0, [0, [0 for j in range(8)]])
                    nrow += [[0, [0 for j in range(8)]] 
                                    for i in range(ncol[0][1]
                                                    + ncol[0][3]
                                                    - colp[0][1]
                                                    + colp[0][3])]
                    
                    ncol[1].append(nrow)                        

            if isec == 1 or isec == 2:
                logging.info("New colony created instead of colony #%d and " \
                             "colony#%d.", col1[0][5], col2[0][5])
                space[space.index(col1)] = ncol
                col2[0][0] = -1 # Пометить более молодую колонию на удаление

    # Удалить все колонии, помеченные на удаление
    space[2:] = list(filter(lambda c: c[0][0] >= 0, space[2:]))


                    
def display_space(space):
    """
    Displays information about the space

    Displays detailed information about space and every colony in the space
    """
    print("Space [", space[0], "] of age [", space[1], "] consists of ",
          len(list(space))-2, " colonies.\n",
          "----------------------------------------------------------------")
    for i, col in enumerate(space[2:]):
        display_colony(col, i + 1)

###############################################################################
# Colony functions
###############################################################################
def update(col):
    """
    Updates colony

    Updates cells of the colony on every step
    """
    logging.debug("Start updating colony #%s...", col[0][5])
    if col[0][0] == 0:
        col_init(col)

    logging.debug("Checking neighbourhood for every cell...")
    # Обновить информацию по соседям для каждой клетки
    for y, row in enumerate(col[1]):
        for x, c in enumerate(row):
            # Проверить северное направление.
            if y == 0:
                c[1][0] = 0
            elif col[1][y - 1][x][0] != 0:
                c[1][0] = 1
            else:
                c[1][0] = 0
            # Проверить северо-восторчное направление.
            if y == 0 or x == col[0][3] - 1:
                c[1][1] = 0
            elif col[1][y - 1][x + 1][0] != 0:
                c[1][1] = 1
            else:
                c[1][1] = 0
            # Проверить восточное направление.
            if x == col[0][3] - 1:
                c[1][2] = 0
            elif col[1][y][x + 1][0] != 0:
                c[1][2] = 1
            else:
                c[1][2] = 0
            # Проверить юго-восточное направление.
            if x == col[0][3] - 1 or y == col[0][4] - 1:
                c[1][3] = 0
            elif col[1][y + 1][x + 1][0] != 0:
                c[1][3] = 1
            else:
                c[1][3] = 0
            # Проверить южное направление.
            if y == col[0][4] - 1:
                c[1][4] = 0
            elif col[1][y + 1][x][0] != 0:
                c[1][4] = 1
            else:
                c[1][4] = 0
            # Проверить юго-западное направление.
            if y == col[0][4] - 1 or x == 0:
                c[1][5] = 0
            elif col[1][y + 1][x - 1][0] != 0:
                c[1][5] = 1
            else:
                c[1][5] = 0
            # Проверить западное направление.
            if x == 0:
                c[1][6] = 0
            elif col[1][y][x - 1][0] != 0:
                c[1][6] = 1
            else:
                c[1][6] = 0
            # Проверить северо-западное направление.
            if y == 0 or x == 0:
                c[1][7] = 0
            elif col[1][y - 1][x - 1][0] != 0:
                c[1][7] = 1
            else:
                c[1][7] = 0

    logging.debug("Updating cells...")
    # Определить новый статус каждой клетки
    for y, row in enumerate(col[1]):
        for x, c in enumerate(row):
            nCnt = reduce(lambda x, y: x + y, c[1])
            if c[0] == 0 and nCnt == 3:
                c[0] = 1
            elif c[0] > 0:
                if nCnt > 3:
                    c[0] = 0
                elif nCnt < 2:
                    c[0] = 0
                else:
                    c[0] += 1

    minX, minY = col_init(col)

    logging.debug("Setting new coordinates for the colony")
    # Определить новые координаты и возраст колонии
    if minX == 0:
        col[0][1] -= 1
    if minY == 0:
        col[0][2] -= 1
    if minX > 1:
        col[0][1] += minX - 1
    if minY > 1:
        col[0][2] += minY - 1
    col[0][0] += 1
    logging.info("Colony #%d has dimension [%d, %d, %d, %d].", 
                 col[0][5], col[0][1], col[0][2], col[0][3], col[0][4])
    


def col_init(col):
    """
    Initializes the colony

    Removes all extra empty cells from sides of the colony and adds empty
    borders around updated colony

    Returns minX and minY of the colony before adding empty borders
    """        
    logging.debug("Start formatting colony #%d...", col[0][5])
    minX, maxX, minY, maxY = col[0][3], 0, col[0][4], 0
    for y, row in enumerate(col[1]):
        for x, cell in enumerate(row):
            if cell[0] != 0:
                if maxX < x:
                    maxX = x
                if minX > x:
                    minX = x
                if maxY < y:
                    maxY = y
                if minY > y:
                    minY = y
    logging.debug( "minX, maxX, minY, max: [%d, %d, %d, %d]",
                  minX, maxX, minY, maxY)

    if minX > maxX:
        logging.info("There are no live cells in the colony #%d. " \
                     "Will be cleared.", col[0][5])                         
        col[1] = []
        col[0][1] = 0
        col[0][2] = 0
        return -1, -1

    logging.debug("Remove %d leading empty rows.", minY)
    for row in range(minY):
        col[1].pop(0)

    logging.debug("Remove %d trailing empty rows.", col[0][4] - maxY - 1)
    for row in range(col[0][4] - maxY - 1):
        col[1].pop()

    col[0][4] = maxY - minY + 1
    logging.debug("Real heigth of the colony is %d.", col[0][4])

    for i, row in enumerate(col[1]):
        for c in range(minX):
            row.pop(0)
        for c in range(col[0][3] - maxX - 1):
            row.pop()

    col[0][3] = maxX - minX + 1
    logging.debug("Real width of the colony is %d.", col[0][3])

    col[1].insert(0, [[0, [0 for i in range(8)]] for i in range(col[0][3])])
    col[1].append([[0, [0 for i in range(8)]] for i in range(col[0][3])])
    col[0][4] += 2

    for row in col[1]:
        row.insert(0, [0, [0 for i in range(8)]])
        row.append([0, [0 for i in range(8)]])
    col[0][3] += 2
    logging.info("Size of the colony #%d after initialization is [%d, %d].",
                 col[0][5], col[0][3], col[0][4])

    return minX, minY




def load_row(colony, new_row):
    """
    Loads one cells row to the colony

    Loads one cells row to the colony and updates colony width accordingly.
    Row represent a string with '0' in place of empty cell and 
    '1' in place of live cell

    For example "000100100"
    """
    if colony[0][0] > 0:
        logging.error("Colony already changed. Adding new rows is prohibited.")
        return
    if len(new_row) == 0:
        logging.error("Will not add empty rows in a living colony.\n")
        return
    if len(set(new_row) - {'1','0'}) > 0:
        logging.error("Only 0 and 1 are allowed in row string. Got [%s]\n",
                      new_row)
        return
    
    # Если длина новой строки больше чем текущая ширина колонии, дополнить все
    # существующие строки колонии до новой длины пустыми клетками.
    if len(new_row) > colony[0][3]:
        for row in colony[1]:
            for i in range(len(new_row) - colony[0][3]):
                row.append(list([0, [0 for j in range(8)]]))
        logging.debug("Colony #%d width was expanded from %d to %d.", 
                      colony[0][5], 
                      colony[0][3],
                      len(new_row))
        colony[0][3] = len(new_row)

    # Создать новую строку, соответсвущую new_row
    nrow = list()
    for pos in new_row:
        if pos == "0":
            age = 0
        else:
            age = 1
        nrow.append(list([age, [0 for j in range(8)]]))
    logging.debug("New row was created from [%s] for colony #%d", new_row,
                  colony[0][5])

    # По необходимости дополнить новую строку пустыми клетками до текущей
    # ширины колонии
    if len(new_row) < colony[0][3]:
        for i in range(colony[0][3] - len(new_row)):
            nrow.append(list([0, [0 for j in range(8)]]))
        logging.debug(
            "Newly created row [%s] was expanded to %d length for colony #%d", 
            new_row, colony[0][3], colony[0][5])

    # Добавить новую строку в колонию
    colony[1].append(nrow)
    logging.info("Newly created row [%s] was added to the colony #%d at %d", 
                 new_row, colony[0][5], colony[0][4])
    colony[0][4] += 1



def display_colony(colony, pos):
    """
    Displays information about the colony

    Dislplays detailed information about the colony
    """
    print("Colony #", pos, "is", colony[0][0],
          "days old and takes place at[", colony[0][1], colony[0][2], "]")
    print("  colony height is", colony[0][4],
          "colony width is", colony[0][3])
    print("====== Colony map ========")
    for row in colony[1]:
        sr = ""
        for cell in row:
            if cell[0] == 0:
                sr += ' '
            elif cell[0] < 10:
                sr += str(cell[0])
            else:
                sr += '0'
        print(sr)
    print("==========================\n")



###############################################################################
# Main function
###############################################################################
def main():
    """
    Programm entry point

    Constructs an empty space
    Adds colonies to it
    Runs the space life cycle
    """
    logging.basicConfig(filename="lifecells.log",
                        level=logging.DEBUG,
                        format="%(asctime)s [%(levelname)s] : %(message)s")
     
    space = new_space("Universe")

    col1 = ["00111",
            "011011",
            "1100011",
            "011011",
            "00111"]

    col2 = ["111"]

    space = add_colony(space, col1, 10, 10)
    space = add_colony(space, col2, 12, 12)

    run(space, 12)



###############################################################################
# Entry point
###############################################################################
if __name__ == "__main__":
    main()
