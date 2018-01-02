# colony.py
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
#     - если у клетки два соседа, то она продолжает жить
#     - если у клетки три и более соседей, то она умирает от тесноты
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
# [[age, x, y, w, h], [row1, row2, row3, row4]]
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

import random
import sys

###############################################################################
# Space functions
###############################################################################
def new_space(name):
    """
    Create new space

    Retruns empty list of colonies of space.
    """
    if name == "":
        print("ERR: Empty colony names aren't allowed.\n")
        sys.exit()

    print("DEBUG: New space created with name", name, "\n")

    return list([name, 0])



def add_colony(space):
    """
    Add an empty colony to the space

    Creates an empty colony at random coordinates and
    adds it to the space.

    Returns updated space
    """
    space.append(list([list([0,
                             int(random.random()*1000000),
                             int(random.random()*1000000),
                             0, 0]),
                       list()]))

    return space



def display_space(space):
    """
    Displays information about the space

    Displays detailed information about every colony in the space
    """
    print("Space [", space[0], "] of age [", space[1], "] consists of ",
          len(list(space))-2, " colonies.\n",
          "----------------------------------------------------------------")
    for i, col in enumerate(space[2:]):
        display_colony(col, i + 1)

###############################################################################
# Colony functions
###############################################################################
def update(colony):
    """
    Updates colony

    Updates cells of the colony on every step
    """
    pass



def load_row(colony, new_row):
    """
    Loads one cells row to the colony

    Loads one cell row to the colony and updates its borders.
    row represent a string with '0' in place of empty cell and 
    '1' in place of live cell

    For example "000100100"
    """
    if colony[0][0] > 0:
        print("ERR: Colony already changed. Adding new rows is prohibited.\n")
        return
    if len(new_row) == 0:
        print("ERR: Will not add empty rows in colony.\n")
        return
    if len(set(new_row) - {'1','0'}) > 0:
        print("ERR: Only 0 and 1 are allowed in row string.\n")
        return
    
    # Если длина новой строки больше чем текущая ширина колонии, дополнить все
    # существующие строки колонии до новой длины пустыми клетками.
    if len(new_row) > colony[0][3]:
        for row in colony[1]:
            for i in range(len(new_row) - colony[0][3]):
                row.append(list([0, [0 for j in range(8)]]))
        colony[0][3] = len(new_row)

    # Создаем новую строку, соответсвущую new_row
    nrow = list()
    for pos in new_row:
        if pos == "0":
            age = 0
        else:
            age = 1
        nrow.append(list([age, [0 for j in range(8)]]))

    # По-необходимости дополняем новую строку пустыми клетками до текущей
    # ширины колонии
    if len(new_row) < colony[0][3]:
        for i in range(colony[0][3] - len(new_row)):
            nrow.append(list([0, [0 for j in range(8)]]))

    # Добавить новую строку в колонию
    colony[1].append(nrow)
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
    Adds three empty colony to it
    Displays the space info
    """
    space = new_space("Universe")
    for i in range(3):
        space = add_colony(space)

    col1 = ["00111",
            "011011",
            "1100011",
            "011011",
            "00111"]

    for sf in col1:
        load_row(space[2], sf)

    display_space(space)


###############################################################################
# Entry point
###############################################################################
if __name__ == "__main__":
    main()
