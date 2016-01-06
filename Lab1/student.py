class Student:
    courseMarks = {}
    name = ""

    def __init__(self, name, family):
        self.name = name
        self.family = family

    def addCourseMark(self, course, mark):
        self.courseMarks[course] = mark

    def average(self,courseMarks):
        sum_grade = 0
        count = 0
        if len(courseMarks) == 0:
            return 0
        for k in self.courseMarks:
            count += 1
            sum_grade += self.courseMarks[k]
            avg = float(sum_grade) / float(count)
        return avg

    def __str__(self):
        return "Name:" + self.name + " " + self.family + "\nCourse Catalog: " + \
               str(self.courseMarks) + "\nAverage: " + str(self.average(self.courseMarks))



# basic test cases
a = Student("Ji","Yang")
a.addCourseMark("CMPUT 101", 4.0)
a.addCourseMark("CMPUT 174", 3.5)
print a