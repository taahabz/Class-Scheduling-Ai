class WeeklyClassroomScheduling:
    def __init__(self, courses, instructors, classrooms, timeslots, special_courses, course_schedule, permanent_assignments):
        self.courses = courses
        self.instructors = instructors
        self.classrooms = classrooms
        self.timeslots = timeslots
        self.special_courses = special_courses
        self.course_schedule = course_schedule
        self.permanent_assignments = permanent_assignments  # Fixed instructor assignments
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.assignments = []

    def is_instructor_available(self, instructor, day, timeslot, section):
        # Ensure that the instructor is not scheduled in the same section for the same time and day
        for assignment in self.assignments:
            if (assignment["instructor"] == instructor and
                assignment["day"] == day and
                assignment["timeslot"] == timeslot and
                assignment["section"] == section):
                return False
        return True
    
    def is_classroom_available(self, classroom, day, timeslot, section):
        # Ensure the classroom is available for the section at the given time
        for assignment in self.assignments:
            if (assignment["classroom"]["name"] == classroom["name"] and
                assignment["day"] == day and
                assignment["timeslot"] == timeslot and
                assignment["section"] == section):  # Ensure no overlap in same section
                return False
        return True

    def has_sufficient_resources(self, required_sessions):
        total_needed = sum(required_sessions.values())
        total_available = len(self.classrooms) * len(self.days) * len(self.timeslots) * 2  # Two sections
        print(f"Total needed: {total_needed}, Total available: {total_available}")
        return total_needed <= total_available

    def schedule(self):
        # Prepare the required sessions dictionary for both sections
        required_sessions = {
            course: self.course_schedule[course]["lectures"] + self.course_schedule[course]["labs"]
            for course in self.courses
        }

        # Assign instructors to courses
        course_to_instructor = {
            course: self.permanent_assignments.get(course, None)
            for course in self.courses
        }
        for course, instructor in course_to_instructor.items():
            if not instructor:
                print(f"No instructor assigned for course {course}.")
                return None

        # Check if resources are sufficient
        if not self.has_sufficient_resources(required_sessions):
            print("Insufficient resources to schedule all sessions.")
            return None

        # Begin the recursive backtracking algorithm for both sections
        for section in ["A", "B"]:
            print(f"Scheduling for Section {section}")
            if not self.backtrack(required_sessions.copy(), course_to_instructor, section):
                print(f"Failed to schedule for Section {section}.")
                return None
        return True

    def backtrack(self, required_sessions, course_to_instructor, section):
        # Base case: All sessions are scheduled
        if all(sessions == 0 for sessions in required_sessions.values()):
            return True

        # Select a course that still has unscheduled sessions
        course = next((c for c in required_sessions if required_sessions[c] > 0), None)
        if not course:
            return False

        instructor = course_to_instructor[course]
        for day in self.days:
            for timeslot in self.timeslots:
                # Check if the assignment is valid
                classroom = self.get_classroom_for_course(course)
                if classroom and self.is_instructor_available(instructor, day, timeslot, section) and \
                        self.is_classroom_available(classroom, day, timeslot, section):  # Check section validity

                    # Assign the session
                    self.assignments.append({
                        "course": course,
                        "instructor": instructor,
                        "classroom": classroom,
                        "day": day,
                        "timeslot": timeslot,
                        "section": section
                    })
                    required_sessions[course] -= 1

                    print(f"Assigned {course} to {instructor} in {classroom['name']} on {day} at {timeslot} for Section {section}.")

                    # Recursive step
                    if self.backtrack(required_sessions, course_to_instructor, section):
                        return True

                    # Undo the assignment (backtrack)
                    self.assignments.pop()
                    required_sessions[course] += 1
                    print(f"Backtracking on {course} from {day} at {timeslot} for Section {section}.")

        return False

    def get_classroom_for_course(self, course):
        # Determine the appropriate classroom based on whether the course has labs
        if self.course_schedule[course]["labs"] > 0:
            # If the course has labs, assign to Room 102
            return next((room for room in self.classrooms if room["name"] == "Room 102"), None)
        else:
            # Otherwise, assign to any available classroom
            return next((room for room in self.classrooms if room["name"] != "Room 102"), None)

    def display_schedule(self):
        if not self.assignments:
            print("No valid schedule found.")
        else:
            print("Weekly Schedule:")
            for assignment in self.assignments:
                print(f"Course: {assignment['course']}, Instructor: {assignment['instructor']}, "
                      f"Classroom: {assignment['classroom']['name']}, Day: {assignment['day']}, "
                      f"Timeslot: {assignment['timeslot']}, Section: {assignment['section']}")

# --- Test Cases ---
def main():
    courses = ["Probability and Statistics", "Artificial Intelligence", "Computer Network", "Islamiat", "DSA", "Information Security"]
    instructors = ["Dr. Ansar", "Dr. Momeena", "Dr. Khurram", "Dr. Ammar", "Dr. Farzana", "Dr. Ayesha"]
    classrooms = [{"name": "Room 101", "has_Lab": False}, {"name": "Room 102", "has_Lab": True}]
    timeslots = ["9-10AM", "10-11AM", "11-12PM", "12-1PM", "2-3PM", "3-4PM", "4-5PM"]
    special_courses = []
    course_schedule = {
        "Probability and Statistics": {"lectures": 3, "labs": 0},
        "Artificial Intelligence": {"lectures": 2, "labs": 1},
        "Computer Network": {"lectures": 2, "labs": 1},
        "Islamiat": {"lectures": 2, "labs": 0},
        "DSA": {"lectures": 3, "labs": 1},
        "Information Security": {"lectures": 2, "labs": 1},
    }
    permanent_assignments = {
        "Probability and Statistics": "Dr. Ansar",
        "Artificial Intelligence": "Dr. Momeena",
        "Computer Network": "Dr. Khurram",
        "Islamiat": "Dr. Ammar",
        "DSA": "Dr. Farzana",
        "Information Security": "Dr. Ayesha"
    }

    scheduler = WeeklyClassroomScheduling(courses, instructors, classrooms, timeslots, special_courses, course_schedule, permanent_assignments)

    if scheduler.schedule():
        scheduler.display_schedule()
    else:
        print("Failed to generate a schedule.")

if __name__ == "__main__":
    main()
