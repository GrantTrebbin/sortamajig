from collections import deque, Counter
import itertools


class Command:
    """Create an undoable callable object.

    A Command is initialised with two callable objects.  One performs a task,
    the other reverses it.  The Command object can then be called to
    perform the "do" task while, the instance variable "undo" can be called to
    perform the undo task.

    Example:

    def do_print():
        print("do")

    def undo_print():
        print("undo")

    test = Command(do_print, undo_print)

    running test() will print "do" while running test.undo() will print "undo"


    """

    def __init__(self, do, undo):
        """Initialise Command instance.

        Args:
            do: callable object
            undo: callable object
        """
        assert callable(do) and callable(undo)
        self.do = do
        self.undo = undo

    def __call__(self):
        """Make the Command object callable."""
        self.do()


class SortingManager:
    def __init__(self, sortable_deque):
        self.sortableDeque = sortable_deque

        counter = itertools.chain(*self.sortableDeque)
        self.number_of_elements = sum(1 for _ in counter)

        list_of_ones = [0] + [1] * self.number_of_elements
        self.total_comparisons = self.comparisons_remaining(deque(list_of_ones))

        self.currentAction = deque()
        self.undoableActions = deque()
        self.redoableActions = deque()

        self.move_element_from_list1 = Command(self.move_element_from_list1_do,
                                               self.move_element_from_list1_undo)
        self.move_element_from_list2 = Command(self.move_element_from_list2_do,
                                               self.move_element_from_list2_undo)
        self.move_head_to_end = Command(self.move_head_to_end_do,
                                        self.move_head_to_end_undo)
        self.delete_head_list = Command(self.delete_head_list_do,
                                        self.delete_head_list_undo)
        self.determine_state()

    @staticmethod
    def comparisons_remaining(list_of_lengths):
        if len(list_of_lengths) < 3:
            return 0

        comparison_count = 0

        a = list_of_lengths.popleft()
        b = list_of_lengths.popleft()
        c = list_of_lengths.popleft()

        number_of_elements = a + b + c
        list_of_lengths.append(number_of_elements)

        comparisons = b + c - 1
        comparison_count += comparisons

        while len(list_of_lengths) > 1:
            a = list_of_lengths.popleft()
            b = list_of_lengths.popleft()
            c = a + b
            comparison_count = comparison_count + c - 1
            list_of_lengths.append(c)

        return comparison_count

    def determine_state(self):
        if self.is_sorted():
            self.wait_for_action()
        else:
            self.determine_action()

    def determine_action(self):
        list0empty = len(self.sortableDeque[0]) == 0
        list1empty = len(self.sortableDeque[1]) == 0
        list2empty = len(self.sortableDeque[2]) == 0

        state = [list0empty, list1empty, list2empty]

        if state == [False, False, False]:
            self.wait_for_action()
        elif state == [False, False, True]:
            self.move_element_from_list1()
            self.currentAction.append(self.move_element_from_list1)
            self.determine_state()
        elif state == [False, True, False]:
            self.move_element_from_list2()
            self.currentAction.append(self.move_element_from_list2)
            self.determine_state()
        elif state == [False, True, True]:
            self.move_head_to_end()
            self.currentAction.append(self.move_head_to_end)
            self.determine_state()
        elif state == [True, False, False]:
            self.wait_for_action()
        elif state == [True, False, True]:
            # Unreachable state
            pass
        elif state == [True, True, False]:
            self.delete_head_list()
            self.currentAction.append(self.delete_head_list)
            self.determine_state()
        elif state == [True, True, True]:
            # Unreachable state
            pass
        else:
            pass

    def wait_for_action(self):
        pass

    def move_element_from_list1_do(self):
        temp_element = self.sortableDeque[1].popleft()
        self.sortableDeque[0].append(temp_element)

    def move_element_from_list1_undo(self):
        temp_element = self.sortableDeque[0].pop()
        self.sortableDeque[1].appendleft(temp_element)

    def move_element_from_list2_do(self):
        temp_element = self.sortableDeque[2].popleft()
        self.sortableDeque[0].append(temp_element)

    def move_element_from_list2_undo(self):
        temp_element = self.sortableDeque[0].pop()
        self.sortableDeque[2].appendleft(temp_element)

    def move_head_to_end_do(self):
        temp_deque = self.sortableDeque.popleft()
        self.sortableDeque.append(temp_deque)

    def move_head_to_end_undo(self):
        temp_deque = self.sortableDeque.pop()
        self.sortableDeque.appendleft(temp_deque)

    def delete_head_list_do(self):
        self.sortableDeque.popleft()

    def delete_head_list_undo(self):
        self.sortableDeque.appendleft(deque())

    def select(self, selection):
        if self.is_sorted() is False:
            self.redoableActions.clear()
            if selection == 0:
                self.move_element_from_list1()
                self.currentAction.append(self.move_element_from_list1)
            elif selection == 1:
                self.move_element_from_list2()
                self.currentAction.append(self.move_element_from_list2)
            else:
                pass

            self.determine_state()

            if len(self.currentAction) != 0:
                self.undoableActions.append(self.currentAction)
                self.currentAction = deque()



    def undo(self):
        if len(self.undoableActions) >= 1:
            action_to_undo = self.undoableActions.pop()
            self.redoableActions.append(action_to_undo)
            for command_to_undo in action_to_undo.__reversed__():
                command_to_undo.undo()
            self.wait_for_action()

    def redo(self):
        if len(self.redoableActions) >= 1:
            action_to_redo = self.redoableActions.pop()
            self.undoableActions.append(action_to_redo)
            for command_to_redo in action_to_redo:
                command_to_redo()
            self.wait_for_action()

    def is_sorted(self):
        if len(self.sortableDeque) >= 3:
            return False
        else:
            return True

    @property
    def options(self):
        if not self.is_sorted():
            return [self.sortableDeque[1][0], self.sortableDeque[2][0]]
        else:
            return None

    @property
    def sorted(self):
        return self.is_sorted()

    @property
    def sorting_state(self):
        return self.sortableDeque

    @property
    def progress(self):
        S = [len(x) for x in self.sortableDeque]
        S1 = self.comparisons_remaining(deque(S))
        if 0 <= S1 <= self.total_comparisons:
            return [S1, self.total_comparisons]
        else:
            return [0, self.total_comparisons]
