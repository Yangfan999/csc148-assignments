""" Define your class up here. """


class Person:
    """ A representation of Person
    """
    name: str
    food_list: list

    def __init__(self, name: str) -> None:
        self.name = name
        self.food_list = []

    def eat(self, food: str) -> None:
        """
        this person eat food
        """
        self.food_list.append(food)

    def get_eaten_food(self) -> list:
        """
        return a list of foods this person has eaton
        """
        return self.food_list

    def change_name(self, name: str) -> None:
        """
        change the name of this person
        """
        self.name = name

    def __eq__(self, other) -> bool:
        """
        return whether self is same to other

        """
        return isinstance(Person, other) and \
               self.name == other.name and \
               sorted(self.food_list) == sorted(other.food_list)

    def __str__(self) -> str:
        """
        return a string representation of self
        """
        return "{} is a Person who has eaten {} thing(s)." \
            .format(self.name, len(self.food_list))


class Student(Person):
    """A representation of Student
    """
    course_list: list

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.course_list = []

    def __str__(self) -> str:
        """
        return a string representation of self
        """
        return "{} is a Student who has eaten {} thing(s)." \
            .format(self.name, len(self.food_list))

    def get_courses(self) -> list:
        """
        return a list of courses this student has taken
        """
        return self.course_list


class Course:
    """A representation of Course
    """
    name: str
    student_list: list

    def __init__(self, name: str) -> None:
        self.name = name
        self.student_list = []

    def add_student(self, student: Student) -> None:
        """
        add a new student to the student list
        """
        student.course_list.append(self.name)
        self.student_list.append(student)

    def __str__(self) -> str:
        """
        return a string representation of self
        """
        result = "{} Student log:".format(self.name)
        for student in self.student_list:
            result += "\n" + str(student)
        return result


# ---- Everything below this is client code. Do NOT modify anything! ----
if __name__ == '__main__':
    s = Student("Sophia")
    p = Person("Jen")

    # A Student should be a Person, but a Person should not be a Student
    assert isinstance(s, Person), "A Student should also be a Person"
    assert not isinstance(p, Student), "A Person should not be a Student"

    s.eat("Cupcake")
    s.eat("Apple")

    # get_eaten_food() should return a list of foods in the order they were
    # eaten
    expected = ("s.get_eaten_food() returned {} instead " +
                "of ['Cupcake, 'Apple']").format(s.get_eaten_food())
    assert s.get_eaten_food() == ['Cupcake', 'Apple'], expected

    p.eat("Cupcake")
    p.eat("Apple")

    expected = ("p.get_eaten_food() returned {} instead " +
                "of ['Cupcake, 'Apple']").format(s.get_eaten_food())
    assert p.get_eaten_food() == ['Cupcake', 'Apple'], expected

    assert p != s, ("A Person should only be equal to another object if they" +
                    " have the same name and eaten foods.")

    p.change_name("Sophia")

    assert p == s, ("A Person should be equal to another object if they" +
                    " have the same name and eaten foods.")
    assert s == p, ("A Student should be equal to another object if they" +
                    " have the same name and eaten foods.")

    error = ("str(p) was expected to return\nSophia is a Person who has " +
             "eaten 2 thing(s).\nBut got\n{}\ninstead.").format(str(p))

    assert str(p) == "Sophia is a Person who has eaten 2 thing(s).", error

    error = ("str(s) was expected to return\nSophia is a Student who has " +
             "eaten 2 thing(s).\nBut got\n{}\ninstead.").format(str(s))
    assert str(s) == "Sophia is a Student who has eaten 2 thing(s).", error

    c = Course("CSC148")
    c.add_student(s)

    # Assume that get_courses() returns a list in the order that the
    # courses were added
    expected = ("After adding a Student to a Course, that Student should " +
                "have that course in the list returned by get_courses but " +
                "got {} instead.").format(s.get_courses())
    assert s.get_courses() == ["CSC148"], expected

    assert s == p, ("After adding a course to a Student, that Student should " +
                    "be equal to a Person with the same foods eaten and name.")
    assert p == s, ("After adding a course to a Student, that Person should " +
                    "be equal to a Student with the same foods eaten and name.")

    assert not getattr(p, 'get_courses', None), ("Person should not have a " +
                                                 "get_courses() method.")

    expected = ("When printing a Course, the string\n" +
                "CSC148 Student log:\nSophia is a Student " +
                "who has eaten 2 thing(s).\nWas expected" +
                ", but we got\n{}\ninstead").format(str(c))
    assert str(c) == ("CSC148 Student log:\nSophia is a Student " +
                      "who has eaten 2 thing(s)."), expected

    s2 = Student("Jacqueline")
    c.add_student(s2)

    expected = ("When printing a Course, the string\n" +
                "CSC148 Student log:\nSophia is a Student " +
                "who has eaten 2 thing(s).\nJacqueline " +
                "is a Student who has eaten 0 thing(s).\nWas expected" +
                ", but we got\n{}\ninstead").format(str(c))
    assert str(c) == ("CSC148 Student log:\nSophia is a Student " +
                      "who has eaten 2 thing(s).\nJacqueline is a Student " +
                      "who has eaten 0 thing(s)."), expected

    # Below is how python_ta (PythonTA/pyTA/etc.) is called.
    # When run, your code should produce no errors from python_ta.
    # You must have python_ta installed for this to work (see Lab 1 and
    # the Software Installation page).
    import python_ta

    python_ta.check_all(config="ex2_pyta.txt")
