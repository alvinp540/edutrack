# populate_edutrack.py
"""
Populate EduTrack database with Makini School data
"""

from edutrack_manager import EduTrackManager
from datetime import date

def populate_makini_school():
    """Populate database with Makini School comprehensive data"""
    
    # Initialize manager
    manager = EduTrackManager()
    
    try:
        
        print("POPULATING MAKINI SCHOOL DATABASE")
        
        
        #  ADD TEACHERS 
        print("\n Adding Teachers...")
        
        
        teachers = {}
        
        teachers['math'] = manager.add_teacher(
            employee_number="MAKI001",
            first_name="Peter",
            last_name="Kamau",
            phone="+254722123456",
            email="p.kamau@makinischool.ac.ke",
            department="Mathematics"
        )
        
        teachers['english'] = manager.add_teacher(
            employee_number="MAKI002",
            first_name="Grace",
            last_name="Mwangi",
            phone="+254722234567",
            email="g.mwangi@makinischool.ac.ke",
            department="English"
        )
        
        teachers['science'] = manager.add_teacher(
            employee_number="MAKI003",
            first_name="David",
            last_name="Kipchoge",
            phone="+254722345678",
            email="d.kipchoge@makinischool.ac.ke",
            department="Science"
        )
        
        teachers['history'] = manager.add_teacher(
            employee_number="MAKI004",
            first_name="Margaret",
            last_name="Ochieng",
            phone="+254722456789",
            email="m.ochieng@makinischool.ac.ke",
            department="History & Government"
        )
        
        teachers['ict'] = manager.add_teacher(
            employee_number="MAKI005",
            first_name="Samuel",
            last_name="Kariuki",
            phone="+254722567890",
            email="s.kariuki@makinischool.ac.ke",
            department="Information Technology"
        )
        
        #  ADD CLASSES 
        print("\n Adding Classes...")
      
        
        classes = {}
        
        classes['form1a'] = manager.add_class(
            class_name="Form 1A",
            form="Form 1",
            class_teacher_id=teachers['english']
        )
        
        classes['form1b'] = manager.add_class(
            class_name="Form 1B",
            form="Form 1",
            class_teacher_id=teachers['math']
        )
        
        classes['form2a'] = manager.add_class(
            class_name="Form 2A",
            form="Form 2",
            class_teacher_id=teachers['science']
        )
        
        classes['form2b'] = manager.add_class(
            class_name="Form 2B",
            form="Form 2",
            class_teacher_id=teachers['history']
        )
        
        classes['form3a'] = manager.add_class(
            class_name="Form 3A",
            form="Form 3",
            class_teacher_id=teachers['ict']
        )
        
        classes['form4a'] = manager.add_class(
            class_name="Form 4A",
            form="Form 4",
            class_teacher_id=teachers['math']
        )
        
        #  ADD SUBJECTS 
        print("\n Adding Subjects...")
        
        
        subjects = {}
        
        subjects['math'] = manager.add_subject(
            name="Mathematics",
            code="MATH101",
            teacher_id=teachers['math']
        )
        
        subjects['english'] = manager.add_subject(
            name="English Language",
            code="ENG101",
            teacher_id=teachers['english']
        )
        
        subjects['biology'] = manager.add_subject(
            name="Biology",
            code="BIO101",
            teacher_id=teachers['science']
        )
        
        subjects['chemistry'] = manager.add_subject(
            name="Chemistry",
            code="CHEM101",
            teacher_id=teachers['science']
        )
        
        subjects['physics'] = manager.add_subject(
            name="Physics",
            code="PHYS101",
            teacher_id=teachers['science']
        )
        
        subjects['history'] = manager.add_subject(
            name="History & Government",
            code="HIST101",
            teacher_id=teachers['history']
        )
        
        subjects['ict'] = manager.add_subject(
            name="Information & Communication Technology",
            code="ICT101",
            teacher_id=teachers['ict']
        )
        
        subjects['kiswahili'] = manager.add_subject(
            name="Kiswahili",
            code="KISW101",
            teacher_id=teachers['english']
        )
        
        #  ADD STUDENTS - FORM 1A 
        print("\n Adding Students to Form 1A...")
        print("-"*70)
        
        students = {}
        
        students['stu001'] = manager.add_student(
            admission_number="MAKI2024001",
            first_name="Juma",
            last_name="Hassan",
            gender="Male",
            date_of_birth=date(2010, 3, 15),
            class_id=classes['form1a'],
            parent_phone="+254700001001"
        )
        
        students['stu002'] = manager.add_student(
            admission_number="MAKI2024002",
            first_name="Amira",
            last_name="Mohamed",
            gender="Female",
            date_of_birth=date(2010, 5, 22),
            class_id=classes['form1a'],
            parent_phone="+254700001002"
        )
        
        students['stu003'] = manager.add_student(
            admission_number="MAKI2024003",
            first_name="Brian",
            last_name="Kipchoge",
            gender="Male",
            date_of_birth=date(2010, 7, 10),
            class_id=classes['form1a'],
            parent_phone="+254700001003"
        )
        
        students['stu004'] = manager.add_student(
            admission_number="MAKI2024004",
            first_name="Lucy",
            last_name="Mwangi",
            gender="Female",
            date_of_birth=date(2010, 2, 28),
            class_id=classes['form1a'],
            parent_phone="+254700001004"
        )
        
        students['stu005'] = manager.add_student(
            admission_number="MAKI2024005",
            first_name="Victor",
            last_name="Kariuki",
            gender="Male",
            date_of_birth=date(2010, 9, 5),
            class_id=classes['form1a'],
            parent_phone="+254700001005"
        )
        
        #  ADD STUDENTS - FORM 1B 
        print("\n Adding Students to Form 1B...")
       
        students['stu006'] = manager.add_student(
            admission_number="MAKI2024006",
            first_name="Sarah",
            last_name="Kimani",
            gender="Female",
            date_of_birth=date(2010, 4, 12),
            class_id=classes['form1b'],
            parent_phone="+254700001006"
        )
        
        students['stu007'] = manager.add_student(
            admission_number="MAKI2024007",
            first_name="Michael",
            last_name="Kipchoge",
            gender="Male",
            date_of_birth=date(2010, 6, 8),
            class_id=classes['form1b'],
            parent_phone="+254700001007"
        )
        
        students['stu008'] = manager.add_student(
            admission_number="MAKI2024008",
            first_name="Diana",
            last_name="Ochieng",
            gender="Female",
            date_of_birth=date(2010, 1, 20),
            class_id=classes['form1b'],
            parent_phone="+254700001008"
        )
        
        #  ADD EXAMS 
        print("\n Adding Exams...")
       
        
        exams = {}
        
        exams['term1'] = manager.add_exam(
            name="Term 1 Final Examination",
            exam_date=date(2024, 4, 15),
            class_id=classes['form1a']
        )
        
        exams['term2'] = manager.add_exam(
            name="Term 2 Final Examination",
            exam_date=date(2024, 8, 20),
            class_id=classes['form1a']
        )
        
        exams['term3'] = manager.add_exam(
            name="Term 3 Final Examination",
            exam_date=date(2024, 11, 25),
            class_id=classes['form1a']
        )
        
        #  RECORD ATTENDANCE 
        print("\n Recording Attendance...")
        
        
        # Juma Hassan attendance
        manager.record_attendance(students['stu001'], date(2024, 1, 8), "Present")
        manager.record_attendance(students['stu001'], date(2024, 1, 9), "Present")
        manager.record_attendance(students['stu001'], date(2024, 1, 10), "Late")
        manager.record_attendance(students['stu001'], date(2024, 1, 11), "Present")
        manager.record_attendance(students['stu001'], date(2024, 1, 12), "Absent")
        
        # Amira Mohamed attendance
        manager.record_attendance(students['stu002'], date(2024, 1, 8), "Present")
        manager.record_attendance(students['stu002'], date(2024, 1, 9), "Present")
        manager.record_attendance(students['stu002'], date(2024, 1, 10), "Present")
        manager.record_attendance(students['stu002'], date(2024, 1, 11), "Present")
        manager.record_attendance(students['stu002'], date(2024, 1, 12), "Present")
        
        # Brian Kipchoge attendance
        manager.record_attendance(students['stu003'], date(2024, 1, 8), "Absent")
        manager.record_attendance(students['stu003'], date(2024, 1, 9), "Present")
        manager.record_attendance(students['stu003'], date(2024, 1, 10), "Present")
        manager.record_attendance(students['stu003'], date(2024, 1, 11), "Late")
        manager.record_attendance(students['stu003'], date(2024, 1, 12), "Present")
        
        #  RECORD EXAM RESULTS 
        print("\n Recording Exam Results...")
       
        
        # Juma Hassan - Term 1 Results
        manager.record_result(students['stu001'], exams['term1'], subjects['math'], 82, "Good")
        manager.record_result(students['stu001'], exams['term1'], subjects['english'], 75, "Satisfactory")
        manager.record_result(students['stu001'], exams['term1'], subjects['biology'], 88, "Excellent")
        manager.record_result(students['stu001'], exams['term1'], subjects['kiswahili'], 79, "Satisfactory")
        
        # Amira Mohamed - Term 1 Results
        manager.record_result(students['stu002'], exams['term1'], subjects['math'], 92, "Excellent")
        manager.record_result(students['stu002'], exams['term1'], subjects['english'], 95, "Excellent")
        manager.record_result(students['stu002'], exams['term1'], subjects['biology'], 85, "Good")
        manager.record_result(students['stu002'], exams['term1'], subjects['kiswahili'], 88, "Good")
        
        # Brian Kipchoge - Term 1 Results
        manager.record_result(students['stu003'], exams['term1'], subjects['math'], 78, "Satisfactory")
        manager.record_result(students['stu003'], exams['term1'], subjects['english'], 72, "Satisfactory")
        manager.record_result(students['stu003'], exams['term1'], subjects['biology'], 81, "Good")
        manager.record_result(students['stu003'], exams['term1'], subjects['kiswahili'], 68, "Satisfactory")
        
        # Lucy Mwangi - Term 1 Results
        manager.record_result(students['stu004'], exams['term1'], subjects['math'], 88, "Good")
        manager.record_result(students['stu004'], exams['term1'], subjects['english'], 91, "Excellent")
        manager.record_result(students['stu004'], exams['term1'], subjects['biology'], 87, "Good")
        manager.record_result(students['stu004'], exams['term1'], subjects['kiswahili'], 93, "Excellent")
        
        #  DISPLAY REPORTS 
       
        print("DATABASE SUMMARY - MAKINI SCHOOL")
    
        
        manager.get_database_stats()
        
        print("\n All Teachers at Makini School:")
        manager.get_all_teachers()
        
        print("\n All Classes:")
        manager.get_all_classes()
        
        print("\n All Students in Form 1A:")
        manager.get_students_by_class(classes['form1a'])
        
        print("\n All Subjects Offered:")
        manager.get_all_subjects()
        
        print("\n All Exams:")
        manager.get_all_exams()
        
        # Show detailed information
        
        print("STUDENT TRANSCRIPTS - MAKINI SCHOOL")
       
        
        manager.get_student_transcript(students['stu001'])
        print("\n")
        manager.get_attendance_summary(students['stu001'])
        
        print("\n\n")
        manager.get_student_transcript(students['stu002'])
        print("\n")
        manager.get_attendance_summary(students['stu002'])
        
      
        print("MAKINI SCHOOL DATABASE POPULATED SUCCESSFULLY!")
       
    except Exception as e:
        print(f"\n Error during population: {e}")
        raise
    
    finally:
        # Close connection
        manager.close_connection()


if __name__ == "__main__":
    populate_makini_school()
