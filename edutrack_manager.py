# edutrack_manager.py
"""
EduTrack Manager 
Manage students, teachers, classes, subjects, attendance, exams, and results for makini school using MongoDB Atlas.
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, date


# ==================== MongoDB Connection ====================

class EduTrackManager:
    """Manage EduTrack data in MongoDB Atlas"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        # MongoDB Atlas connection string
        connection_string = "mongodb+srv://alvinpofficial_db_user:lciIDtd6hrm5t4yN@edutrack.hfgk1gk.mongodb.net/edutrack?retryWrites=true&w=majority"
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client.edutrack
            
            # Test connection
            self.client.admin.command('ping')
            print(" Connected to MongoDB Atlas successfully!")
            
        except Exception as e:
            print(f" Connection failed: {e}")
            raise
    
    # TEACHERS MANAGEMENT 
    
    def add_teacher(self, employee_number, first_name, last_name, phone, email, department):
        """Add a new teacher"""
        try:
            teacher_document = {
                "employee_number": employee_number,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "email": email,
                "department": department,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.teachers.insert_one(teacher_document)
            print(f" Teacher '{first_name} {last_name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error adding teacher: {e}")
            return None
    
    def get_all_teachers(self):
        """Get all teachers"""
        try:
            teachers = list(self.db.teachers.find())
            if teachers:
                print(f"\n Total Teachers: {len(teachers)}")
                for teacher in teachers:
                    print(f"  • {teacher['first_name']} {teacher['last_name']} - {teacher['department']} ({teacher['employee_number']})")
                return teachers
            else:
                print("No teachers found")
                return []
        except Exception as e:
            print(f"✗ Error getting teachers: {e}")
            return []
    
    def get_teacher(self, teacher_id):
        """Get specific teacher by ID"""
        try:
            teacher = self.db.teachers.find_one({"_id": ObjectId(teacher_id)})
            if teacher:
                print(f"\n Teacher: {teacher['first_name']} {teacher['last_name']}")
                print(f"   Department: {teacher['department']}")
                print(f"   Phone: {teacher['phone']}")
                print(f"   Email: {teacher['email']}")
                return teacher
            else:
                print(f"Teacher with ID {teacher_id} not found")
                return None
        except Exception as e:
            print(f" Error getting teacher: {e}")
            return None
    
    def update_teacher(self, teacher_id, **kwargs):
        """Update teacher information"""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            result = self.db.teachers.update_one(
                {"_id": ObjectId(teacher_id)},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f" Teacher updated successfully")
                return True
            else:
                print("No teacher found to update")
                return False
        except Exception as e:
            print(f" Error updating teacher: {e}")
            return False
    
    def delete_teacher(self, teacher_id):
        """Delete a teacher"""
        try:
            result = self.db.teachers.delete_one({"_id": ObjectId(teacher_id)})
            if result.deleted_count > 0:
                print(f" Teacher deleted successfully")
                return True
            else:
                print("No teacher found to delete")
                return False
        except Exception as e:
            print(f" Error deleting teacher: {e}")
            return False
    
    # CLASSES MANAGEMENT 
    
    def add_class(self, class_name, form, class_teacher_id=None):
        """Add a new class"""
        try:
            class_document = {
                "name": class_name,
                "form": form,
                "class_teacher_id": ObjectId(class_teacher_id) if class_teacher_id else None,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.classes.insert_one(class_document)
            print(f" Class '{class_name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error adding class: {e}")
            return None
    
    def get_all_classes(self):
        """Get all classes"""
        try:
            classes = list(self.db.classes.find())
            if classes:
                print(f"\n Total Classes: {len(classes)}")
                for cls in classes:
                    print(f"  • {cls['name']} ({cls['form']})")
                return classes
            else:
                print("No classes found")
                return []
        except Exception as e:
            print(f" Error getting classes: {e}")
            return []
    
    def get_class(self, class_id):
        """Get specific class"""
        try:
            cls = self.db.classes.find_one({"_id": ObjectId(class_id)})
            if cls:
                print(f"\n Class: {cls['name']} ({cls['form']})")
                return cls
            else:
                print(f"Class with ID {class_id} not found")
                return None
        except Exception as e:
            print(f" Error getting class: {e}")
            return None
    
    #  STUDENTS MANAGEMENT
    
    def add_student(self, admission_number, first_name, last_name, gender, date_of_birth, class_id, parent_phone=None):
        """Add a new student"""
        try:
            # Convert date to datetime if necessary
            if isinstance(date_of_birth, date) and not isinstance(date_of_birth, datetime):
                date_of_birth = datetime.combine(date_of_birth, datetime.min.time())
            
            student_document = {
                "admission_number": admission_number,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "class_id": ObjectId(class_id) if class_id else None,
                "parent_phone": parent_phone,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.students.insert_one(student_document)
            print(f" Student '{first_name} {last_name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error adding student: {e}")
            return None
    
    def get_all_students(self):
        """Get all students"""
        try:
            students = list(self.db.students.find())
            if students:
                print(f"\n Total Students: {len(students)}")
                for student in students:
                    print(f"  • {student['first_name']} {student['last_name']} ({student['admission_number']})")
                return students
            else:
                print("No students found")
                return []
        except Exception as e:
            print(f" Error getting students: {e}")
            return []
    
    def get_student(self, student_id):
        """Get specific student"""
        try:
            student = self.db.students.find_one({"_id": ObjectId(student_id)})
            if student:
                print(f"\n Student: {student['first_name']} {student['last_name']}")
                print(f"   Admission: {student['admission_number']}")
                print(f"   Gender: {student['gender']}")
                print(f"   DOB: {student['date_of_birth']}")
                return student
            else:
                print(f"Student with ID {student_id} not found")
                return None
        except Exception as e:
            print(f" Error getting student: {e}")
            return None
    
    def get_students_by_class(self, class_id):
        """Get all students in a class"""
        try:
            students = list(self.db.students.find({"class_id": ObjectId(class_id)}))
            if students:
                print(f"\n Students in Class: {len(students)}")
                for student in students:
                    print(f"  • {student['first_name']} {student['last_name']} ({student['admission_number']})")
                return students
            else:
                print("No students found in this class")
                return []
        except Exception as e:
            print(f"✗ Error getting students: {e}")
            return []
    
    def update_student(self, student_id, **kwargs):
        """Update student information"""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            result = self.db.students.update_one(
                {"_id": ObjectId(student_id)},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f" Student updated successfully")
                return True
            else:
                print("No student found to update")
                return False
        except Exception as e:
            print(f" Error updating student: {e}")
            return False
    
    def delete_student(self, student_id):
        """Delete a student"""
        try:
            result = self.db.students.delete_one({"_id": ObjectId(student_id)})
            if result.deleted_count > 0:
                print(f" Student deleted successfully")
                return True
            else:
                print("No student found to delete")
                return False
        except Exception as e:
            print(f" Error deleting student: {e}")
            return False
    
    #  SUBJECTS MANAGEMENT 
    
    def add_subject(self, name, code, teacher_id=None):
        """Add a new subject"""
        try:
            subject_document = {
                "name": name,
                "code": code,
                "teacher_id": ObjectId(teacher_id) if teacher_id else None,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.subjects.insert_one(subject_document)
            print(f" Subject '{name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error adding subject: {e}")
            return None
    
    def get_all_subjects(self):
        """Get all subjects"""
        try:
            subjects = list(self.db.subjects.find())
            if subjects:
                print(f"\n Total Subjects: {len(subjects)}")
                for subject in subjects:
                    print(f"  • {subject['name']} ({subject['code']})")
                return subjects
            else:
                print("No subjects found")
                return []
        except Exception as e:
            print(f" Error getting subjects: {e}")
            return []
    
    #  ATTENDANCE MANAGEMENT 
    
    def record_attendance(self, student_id, attendance_date, status):
        """Record student attendance"""
        try:
            # Convert date to datetime if necessary
            if isinstance(attendance_date, date) and not isinstance(attendance_date, datetime):
                attendance_date = datetime.combine(attendance_date, datetime.min.time())
            
            attendance_document = {
                "student_id": ObjectId(student_id),
                "date": attendance_date,
                "status": status,  # Present, Absent, Late
                "created_at": datetime.utcnow()
            }
            
            result = self.db.attendance.insert_one(attendance_document)
            print(f" Attendance recorded: {status}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error recording attendance: {e}")
            return None
    
    def get_student_attendance(self, student_id):
        """Get attendance records for a student"""
        try:
            records = list(self.db.attendance.find({"student_id": ObjectId(student_id)}).sort("date", -1))
            if records:
                print(f"\n Attendance Records: {len(records)}")
                for record in records:
                    print(f"  • {record['date']}: {record['status']}")
                return records
            else:
                print("No attendance records found")
                return []
        except Exception as e:
            print(f" Error getting attendance: {e}")
            return []
    
    def get_attendance_summary(self, student_id):
        """Get attendance summary for a student"""
        try:
            stats = list(self.db.attendance.aggregate([
                {"$match": {"student_id": ObjectId(student_id)}},
                {"$group": {
                    "_id": "$student_id",
                    "total": {"$sum": 1},
                    "present": {"$sum": {"$cond": [{"$eq": ["$status", "Present"]}, 1, 0]}},
                    "absent": {"$sum": {"$cond": [{"$eq": ["$status", "Absent"]}, 1, 0]}},
                    "late": {"$sum": {"$cond": [{"$eq": ["$status", "Late"]}, 1, 0]}}
                }}
            ]))
            
            if stats:
                s = stats[0]
                print(f"\n Attendance Summary:")
                print(f"   Total Days: {s['total']}")
                print(f"   Present: {s['present']}")
                print(f"   Absent: {s['absent']}")
                print(f"   Late: {s['late']}")
                if s['total'] > 0:
                    percentage = (s['present'] / s['total']) * 100
                    print(f"   Attendance: {percentage:.1f}%")
                return s
            else:
                print("No attendance data found")
                return None
        except Exception as e:
            print(f"✗ Error getting attendance summary: {e}")
            return None
    
    # ==================== EXAMS MANAGEMENT ====================
    
    def add_exam(self, name, exam_date, class_id):
        """Add a new exam"""
        try:
            # Convert date to datetime if necessary
            if isinstance(exam_date, date) and not isinstance(exam_date, datetime):
                exam_date = datetime.combine(exam_date, datetime.min.time())
            
            exam_document = {
                "name": name,
                "date": exam_date,
                "class_id": ObjectId(class_id),
                "created_at": datetime.utcnow()
            }
            
            result = self.db.exams.insert_one(exam_document)
            print(f" Exam '{name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error adding exam: {e}")
            return None
    
    def get_all_exams(self):
        """Get all exams"""
        try:
            exams = list(self.db.exams.find())
            if exams:
                print(f"\n Total Exams: {len(exams)}")
                for exam in exams:
                    print(f"  • {exam['name']} - {exam['date']}")
                return exams
            else:
                print("No exams found")
                return []
        except Exception as e:
            print(f" Error getting exams: {e}")
            return []
    
    #  RESULTS MANAGEMENT 
    
    def record_result(self, student_id, exam_id, subject_id, score, remarks=None):
        """Record exam result"""
        try:
            # Calculate grade
            grade = self.calculate_grade(score)
            
            result_document = {
                "student_id": ObjectId(student_id),
                "exam_id": ObjectId(exam_id),
                "subject_id": ObjectId(subject_id),
                "score": score,
                "grade": grade,
                "remarks": remarks,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.results.insert_one(result_document)
            print(f" Result recorded: Score {score} = Grade {grade}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error recording result: {e}")
            return None
    
    def get_student_results(self, student_id):
        """Get all results for a student"""
        try:
            results = list(self.db.results.find({"student_id": ObjectId(student_id)}))
            if results:
                print(f"\n Student Results: {len(results)}")
                total_score = 0
                for result in results:
                    print(f"  • Score: {result['score']} - Grade: {result['grade']}")
                    total_score += result['score']
                
                if len(results) > 0:
                    average = total_score / len(results)
                    print(f"\n   Average Score: {average:.2f}")
                
                return results
            else:
                print("No results found")
                return []
        except Exception as e:
            print(f" Error getting results: {e}")
            return []
    
    def get_student_transcript(self, student_id):
        """Get full transcript (student info + results)"""
        try:
            student = self.db.students.find_one({"_id": ObjectId(student_id)})
            if not student:
                print("Student not found")
                return None
            
            results = list(self.db.results.find({"student_id": ObjectId(student_id)}))
            
            print(f"\n TRANSCRIPT")
            print(f"Name: {student['first_name']} {student['last_name']}")
            print(f"Admission: {student['admission_number']}")
            print(f"\nResults:")
            
            for result in results:
                print(f"  • Score: {result['score']} - Grade: {result['grade']}")
            
            return {"student": student, "results": results}
            
        except Exception as e:
            print(f" Error getting transcript: {e}")
            return None
    
    #  HELPER FUNCTIONS 
    
    @staticmethod
    def calculate_grade(score):
        """Calculate grade from score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            students_count = self.db.students.count_documents({})
            teachers_count = self.db.teachers.count_documents({})
            classes_count = self.db.classes.count_documents({})
            subjects_count = self.db.subjects.count_documents({})
            attendance_count = self.db.attendance.count_documents({})
            exams_count = self.db.exams.count_documents({})
            results_count = self.db.results.count_documents({})
            
            print(f"\n DATABASE STATISTICS")
            print(f"  Students: {students_count}")
            print(f"  Teachers: {teachers_count}")
            print(f"  Classes: {classes_count}")
            print(f"  Subjects: {subjects_count}")
            print(f"  Attendance Records: {attendance_count}")
            print(f"  Exams: {exams_count}")
            print(f"  Results: {results_count}")
            
            return {
                "students": students_count,
                "teachers": teachers_count,
                "classes": classes_count,
                "subjects": subjects_count,
                "attendance": attendance_count,
                "exams": exams_count,
                "results": results_count
            }
        except Exception as e:
            print(f" Error getting stats: {e}")
            return None
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("\n MongoDB connection closed")


# MAIN EXAMPLE 

def main():
    """
    Main example update to use Makini School sample data.
    """

    #  run the population script first (it contains Makini School data)
    try:
        from populate_edutrack import populate_makini_school
        print("Running Makini School population script...")
        populate_makini_school()
    except Exception:
        # If the population script is not available or fails, continue with manager-only demo
        print("Could not run populate_edutrack.populate_makini_school(); continuing with manager demo.")

    # Initialize manager and show summaries
    manager = EduTrackManager()
    try:
        print("\nSummary after population:\n" )
        manager.get_database_stats()

        print("\nSample queries:\n" )
        manager.get_all_teachers()
        manager.get_all_classes()
        manager.get_all_subjects()
        manager.get_all_exams()

        # Show transcript for the first student found (if any)
        students = manager.get_all_students()
        if students:
            first_student_id = str(students[0]['_id'])
            print("\nTranscript and attendance for first student:\n" + "-"*50)
            manager.get_student_transcript(first_student_id)
            manager.get_attendance_summary(first_student_id)

    finally:
        manager.close_connection()


if __name__ == "__main__":
    main()