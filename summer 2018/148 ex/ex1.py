""" Define your class up here. """


class Course:
    """A representation of course.
    """
    name: str
    capacity: int
    enrolled: list
    waiting: list

    def __init__(self, name: str) -> None:
        self.name = name
        self.capacity = 0
        self.enrolled = []
        self.waiting = []

    def set_course_capacity(self, num: int) -> None:
        """
        set the capacity of the course
        """
        self.capacity = num

    def add_student(self, name: str) -> None:
        """
        add new student to the course, if it's full add to waiting list
        """
        if self.capacity > len(self.enrolled):
            self.enrolled.append(name)
        else:
            self.waiting.append(name)

    def get_enrolled_students(self) -> list:
        """
        return current enrolled students in sorted order
        """
        return sorted(self.enrolled)

    def get_waitlist(self) -> list:
        """
        return current waiting students
        """
        return self.waiting

    def remove_student(self, name: str) -> None:
        """
        remove a student from course or waiting list
        """
        if name in self.enrolled:
            self.enrolled.remove(name)
            if self.waiting:
                self.enrolled.append(self.waiting.pop(0))
        else:
            self.waiting.remove(name)

    def __eq__(self, other) -> bool:
        """
        return whether self is same to other

        """
        if type(self) != type(other):
            return False
        for name in self.enrolled:
            if name not in other.enrolled:
                return False
        return self.name == other.name and \
               self.capacity == other.capacity and \
               self.waiting == other.waiting

    def __str__(self) -> str:
        """
        return a string representation of self
        """
        return "The course {} has {} student(s)"\
                   .format(self.name, len(self.enrolled)) + \
               " enrolled with {} student(s) on the waitlist."\
                   .format(len(self.waiting))


# ---- Everything below this is client code. Do NOT modify anything! ----
if __name__ == '__main__':
    c = Course("CSC148")
    c.set_course_capacity(2) # You may assume this number will always be a
                             # positive integer and that set_course_capacity()
                             # will be called before adding students and
                             # never after adding students.

    c.add_student("Sophia")
    c.add_student("Danny")
    c.add_student("Jacqueline")

    assert str(c) == ("The course CSC148 has 2 student(s) enrolled with" +
                      " 1 student(s) on the waitlist.")

    # get_enrolled_students() should return the enrolled students in sorted
    # order.
    assert c.get_enrolled_students() == ['Danny', 'Sophia']

    # get_waitlist() should return the students on the waitlist in the order
    # that they were added.
    assert c.get_waitlist() == ['Jacqueline']

    c.add_student("David")
    assert c.get_waitlist() == ['Jacqueline', 'David']

    # if remove_student() removes an enrolled student, add in the first
    # waitlisted student to enrolled students.
    # HINT: The list method .pop() might be useful here.
    #       See help(list.pop) for details.
    c.remove_student("Danny")
    assert c.get_enrolled_students() == ['Jacqueline', 'Sophia']
    assert c.get_waitlist() == ['David']

    c.remove_student("David")
    assert c.get_waitlist() == []

    # When comparing 2 courses, they are the same if the enrolled students
    # are the same (regardless of order), the waitlist is the same
    # (and in the same order), and the course code and capacity are the same.
    c2 = Course("CSC148")
    c2.set_course_capacity(2)
    c2.add_student("Jacqueline")
    c2.add_student("Sophia")
    assert c == c2

    c2.add_student("David")
    assert c != c2

    # Below is how python_ta (PythonTA/pyTA/etc.) is called.
    # When run, your code should produce no errors from python_ta.
    # You must have python_ta installed for this to work (see Lab 1 and
    # the Software Installation page).
    import python_ta
    python_ta.check_all(config="ex1_pyta.txt")
