from collections import deque
from sortingmanager import SortingManager

toSort = deque([deque(),
               deque([4]),
               deque([10]),
               deque([1]),
               deque([8]),
               deque([5]),
               deque([2]),
               deque([9]),
               deque([3]),
               deque([6]),
               deque([7])])
sm = SortingManager(toSort)

print("enter\n1 for option 1\n2 for option 2\n8 for undo\n9 for redo")
while sm.progress[0] != 0:
    print(' ')
    print(sm.sorting_state)
    print((100*sm.progress[0]/sm.progress[1]))
    print(sm.options)
    user_input = input(">")
    if user_input == '1':
        sm.select(0)
    if user_input == '2':
        sm.select(1)
    if user_input == '8':
        sm.undo()
    if user_input == '9':
        sm.redo()

print((100*sm.progress[0]/sm.progress[1]))
print(sm.sorting_state)
