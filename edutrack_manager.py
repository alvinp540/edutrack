# edutrack_manager.py
"""EduTrack manager: simple CRUD helpers for the Edutrack MongoDB database."""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, date



class EduTrackManager:
    """Manager for EduTrack data stored in MongoDB."""
    
    def __init__(self):
        """Connect to MongoDB using env or local config.json."""
        # Load MongoDB connection string from environment or local config
        # - Preferred: set environment variable `EDUTRACK_MONGODB_URI`
        # - Fallback: create a local `config.json` (not committed) with {"mongodb_uri": "<uri>"}
        import os, json
        connection_string = os.environ.get('EDUTRACK_MONGODB_URI')
        if not connection_string:
            cfg_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, 'r', encoding='utf-8') as f:
                        cfg = json.load(f)
                        connection_string = cfg.get('mongodb_uri')
                except Exception:
                    connection_string = None

        if not connection_string:
            raise RuntimeError('MongoDB connection string not found. Set EDUTRACK_MONGODB_URI env var or create config.json with {"mongodb_uri": "<uri>"}.')

        try:
            self.client = MongoClient(connection_string)
            self.db = self.client.edutrack
            
            # Test connection
            self.client.admin.command('ping')
            print(" Connected to MongoDB Atlas successfully!")
            
        except Exception as e:
            print(f" Connection failed: {e}")
            raise
    
    # Teachers
    
    def add_teacher(self, employee_number, first_name, last_name, phone, email, department):
        """Create a teacher record."""
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
        """List all teachers."""
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
            print(f" Error getting teachers: {e}")
            return []
    
    def get_teacher(self, teacher_id):
        """Get a teacher by ObjectId or employee number."""
        try:
            try:
                filter_q = {"_id": ObjectId(teacher_id)}
            except Exception:
                filter_q = {"employee_number": teacher_id}
            teacher = self.db.teachers.find_one(filter_q)
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
        """Update a teacher's details."""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            try:
                filter_q = {"_id": ObjectId(teacher_id)}
            except Exception:
                filter_q = {"employee_number": teacher_id}
            result = self.db.teachers.update_one(filter_q, {"$set": update_data})
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
        """Remove a teacher by id or employee number."""
        try:
            # Build OR filters: try to remove by ObjectId and by employee_number (trimmed)
            filters = []
            try:
                filters.append({"_id": ObjectId(teacher_id)})
            except Exception:
                pass
            filters.append({"employee_number": teacher_id.strip()})

            result = self.db.teachers.delete_many({"$or": filters})
            if result.deleted_count > 0:
                print(f" Teacher deleted successfully (removed {result.deleted_count})")
                return True
            else:
                print("No teacher found to delete")
                return False
        except Exception as e:
            print(f" Error deleting teacher: {e}")
            return False
    
    # Classes
    
    def add_class(self, class_name, form, class_teacher_id=None):
        """Create a class record."""
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
        """List all classes."""
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
        """Get a class by id or name."""
        try:
            try:
                filter_q = {"_id": ObjectId(class_id)}
            except Exception:
                filter_q = {"name": class_id}
            cls = self.db.classes.find_one(filter_q)
            if cls:
                print(f"\n Class: {cls['name']} ({cls['form']})")
                return cls
            else:
                print(f"Class with ID {class_id} not found")
                return None
        except Exception as e:
            print(f" Error getting class: {e}")
            return None
    
    # Students
    
    def add_student(self, admission_number, first_name, last_name, gender, date_of_birth, class_id, parent_phone=None):
        """Create a student. Accepts class id or class name."""
        try:
            # Convert date to datetime if necessary
            if isinstance(date_of_birth, date) and not isinstance(date_of_birth, datetime):
                date_of_birth = datetime.combine(date_of_birth, datetime.min.time())
            
            # Resolve class_id: accept ObjectId or class name
            class_obj_id = None
            if class_id:
                try:
                    class_obj_id = ObjectId(class_id)
                except Exception:
                    cls = self.db.classes.find_one({"name": class_id})
                    if cls:
                        class_obj_id = cls['_id']
                    else:
                        print(f" Class with identifier {class_id} not found")
                        return None
            
            student_document = {
                "admission_number": admission_number,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "class_id": class_obj_id,
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
        """List all students."""
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
        """Get a student by id or admission number."""
        try:
            try:
                filter_q = {"_id": ObjectId(student_id)}
            except Exception:
                filter_q = {"admission_number": student_id}
            student = self.db.students.find_one(filter_q)
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
        """List students in a class. Accepts class id or name."""
        try:
            # class_id may be an ObjectId string or class name; resolve accordingly
            try:
                cls_obj_id = ObjectId(class_id)
            except Exception:
                cls = self.db.classes.find_one({"name": class_id})
                if not cls:
                    print(f"Class with identifier {class_id} not found")
                    return []
                cls_obj_id = cls['_id']
            students = list(self.db.students.find({"class_id": cls_obj_id}))
            if students:
                print(f"\n Students in Class: {len(students)}")
                for student in students:
                    print(f"  • {student['first_name']} {student['last_name']} ({student['admission_number']})")
                return students
            else:
                print("No students found in this class")
                return []
        except Exception as e:
            print(f" Error getting students: {e}")
            return []
    
    def update_student(self, student_id, **kwargs):
        """Update a student's details."""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            try:
                filter_q = {"_id": ObjectId(student_id)}
            except Exception:
                filter_q = {"admission_number": student_id}
            result = self.db.students.update_one(filter_q, {"$set": update_data})
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
        """Remove a student by id or admission number."""
        try:
            # Build OR filters: try to remove by ObjectId and by admission_number (trimmed)
            filters = []
            try:
                filters.append({"_id": ObjectId(student_id)})
            except Exception:
                pass
            filters.append({"admission_number": student_id.strip()})

            result = self.db.students.delete_many({"$or": filters})
            if result.deleted_count > 0:
                print(f" Student deleted successfully (removed {result.deleted_count})")
                return True
            else:
                print("No student found to delete")
                return False
        except Exception as e:
            print(f" Error deleting student: {e}")
            return False
    
    # Subjects
    
    def add_subject(self, name, code, teacher_id=None):
        """Create a subject. Teacher id is optional."""
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
        """List all subjects."""
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

    def update_subject(self, subject_id, **kwargs):
        """Update a subject by id or code."""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            if not update_data:
                print("No updates provided")
                return False
            try:
                filter_q = {"_id": ObjectId(subject_id)}
            except Exception:
                filter_q = {"code": subject_id}
            result = self.db.subjects.update_one(filter_q, {"$set": update_data})
            if result.modified_count > 0:
                print(" Subject updated successfully")
                return True
            else:
                print("No subject found to update")
                return False
        except Exception as e:
            print(f" Error updating subject: {e}")
            return False

    def delete_subject(self, subject_id):
        """Remove a subject by id or code."""
        try:
            filters = []
            try:
                filters.append({"_id": ObjectId(subject_id)})
            except Exception:
                pass
            filters.append({"code": subject_id.strip()})
            result = self.db.subjects.delete_many({"$or": filters})
            if result.deleted_count > 0:
                print(f" Subject deleted successfully (removed {result.deleted_count})")
                return True
            else:
                print("No subject found to delete")
                return False
        except Exception as e:
            print(f" Error deleting subject: {e}")
            return False
    
    # Attendance
    
    def record_attendance(self, student_id, attendance_date, status):
        """Save an attendance record for a student."""
        try:
            # Convert date to datetime if necessary
            if isinstance(attendance_date, date) and not isinstance(attendance_date, datetime):
                attendance_date = datetime.combine(attendance_date, datetime.min.time())
            
            # resolve student identifier: ObjectId or admission_number
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print(f" Student not found for identifier: {student_id}")
                    return None
                sid_obj = s['_id']

            attendance_document = {
                "student_id": sid_obj,
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
        """Return attendance records for a student."""
        try:
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print(f"Student not found for identifier: {student_id}")
                    return []
                sid_obj = s['_id']
            records = list(self.db.attendance.find({"student_id": sid_obj}).sort("date", -1))
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
        """Show a simple attendance summary for a student."""
        try:
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print(f"Student not found for identifier: {student_id}")
                    return None
                sid_obj = s['_id']

            stats = list(self.db.attendance.aggregate([
                {"$match": {"student_id": sid_obj}},
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

        def get_all_attendance(self):
            """List all attendance records."""
            try:
                records = list(self.db.attendance.find().sort("date", -1))
                if records:
                    print(f"\n Total Attendance Records: {len(records)}")
                    for r in records:
                        sid = r.get('student_id')
                        # try to fetch admission number
                        try:
                            st = self.db.students.find_one({"_id": sid}) if sid else None
                            adm = st['admission_number'] if st else str(sid)
                        except Exception:
                            adm = str(sid)
                        print(f"  • {r['_id']} | Student: {adm} | {r.get('date')} | {r.get('status')}")
                    return records
                else:
                    print("No attendance records found")
                    return []
            except Exception as e:
                print(f" Error listing attendance: {e}")
                return []

        def update_attendance(self, attendance_id, date=None, status=None):
            """Update an attendance record. Use id or 'admission|YYYY-MM-DD'."""
            try:
                # resolve filter
                filter_q = None
                if isinstance(attendance_id, str) and '|' in attendance_id:
                    adm, date_s = attendance_id.split('|', 1)
                    s = self.db.students.find_one({"admission_number": adm})
                    if not s:
                        print(f"Student not found for admission: {adm}")
                        return False
                    try:
                        date_obj = datetime.strptime(date_s, '%Y-%m-%d').date()
                    except Exception:
                        print('Invalid date in composite identifier')
                        return False
                    filter_q = {"student_id": s['_id'], "date": date_obj}
                else:
                    try:
                        filter_q = {"_id": ObjectId(attendance_id)}
                    except Exception:
                        print('Invalid attendance identifier')
                        return False

                update_data = {}
                if date is not None:
                    if isinstance(date, str):
                        try:
                            date_val = datetime.strptime(date, '%Y-%m-%d').date()
                        except Exception:
                            print('Invalid date format')
                            return False
                    else:
                        date_val = date
                    update_data['date'] = date_val
                if status is not None:
                    update_data['status'] = status

                if not update_data:
                    print('No updates provided')
                    return False

                result = self.db.attendance.update_one(filter_q, {"$set": update_data})
                if result.modified_count > 0:
                    print(' Attendance updated successfully')
                    return True
                else:
                    print('No attendance record found to update')
                    return False
            except Exception as e:
                print(f" Error updating attendance: {e}")
                return False

        def delete_attendance(self, attendance_id):
            """Delete attendance by id or 'admission|YYYY-MM-DD'."""
            try:
                # composite
                if isinstance(attendance_id, str) and '|' in attendance_id:
                    adm, date_s = attendance_id.split('|', 1)
                    s = self.db.students.find_one({"admission_number": adm})
                    if not s:
                        print(f"Student not found for admission: {adm}")
                        return False
                    try:
                        date_obj = datetime.strptime(date_s, '%Y-%m-%d').date()
                    except Exception:
                        print('Invalid date in composite identifier')
                        return False
                    result = self.db.attendance.delete_many({"student_id": s['_id'], "date": date_obj})
                else:
                    try:
                        result = self.db.attendance.delete_many({"_id": ObjectId(attendance_id)})
                    except Exception:
                        print('Invalid attendance identifier')
                        return False

                if result.deleted_count > 0:
                    print(f' Attendance deleted successfully (removed {result.deleted_count})')
                    return True
                else:
                    print('No attendance found to delete')
                    return False
            except Exception as e:
                print(f" Error deleting attendance: {e}")
                return False
    
    # Exams
    
    def add_exam(self, name, exam_date, class_id):
        """Create an exam for a class."""
        try:
            # Convert date to datetime if necessary
            if isinstance(exam_date, date) and not isinstance(exam_date, datetime):
                exam_date = datetime.combine(exam_date, datetime.min.time())
            # resolve class identifier: ObjectId or class name
            try:
                cls_obj_id = ObjectId(class_id)
            except Exception:
                cls = self.db.classes.find_one({"name": class_id})
                if not cls:
                    print(f" Class not found for identifier: {class_id}")
                    return None
                cls_obj_id = cls['_id']

            exam_document = {
                "name": name,
                "date": exam_date,
                "class_id": cls_obj_id,
                "created_at": datetime.utcnow()
            }
            
            result = self.db.exams.insert_one(exam_document)
            print(f" Exam '{name}' added with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f" Error adding exam: {e}")
            return None
    
    def get_all_exams(self):
        """List all exams."""
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

    def get_exam(self, exam_id):
        """Get an exam by id or name."""
        try:
            try:
                filter_q = {"_id": ObjectId(exam_id)}
            except Exception:
                filter_q = {"name": exam_id}
            exam = self.db.exams.find_one(filter_q)
            if exam:
                print(f"\n Exam: {exam['name']} | Date: {exam.get('date')}")
                return exam
            else:
                print(f"Exam with ID {exam_id} not found")
                return None
        except Exception as e:
            print(f" Error getting exam: {e}")
            return None

    def update_exam(self, exam_id, **kwargs):
        """Update exam fields like name, date, or class."""
        try:
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            # normalize date if present
            if 'date' in update_data:
                d = update_data['date']
                if isinstance(d, date) and not isinstance(d, datetime):
                    update_data['date'] = datetime.combine(d, datetime.min.time())
            # resolve class_id if provided (accept name or id)
            if 'class_id' in update_data and update_data['class_id']:
                cid = update_data['class_id']
                try:
                    update_data['class_id'] = ObjectId(cid)
                except Exception:
                    cls = self.db.classes.find_one({"name": cid})
                    update_data['class_id'] = cls['_id'] if cls else None

            try:
                filter_q = {"_id": ObjectId(exam_id)}
            except Exception:
                filter_q = {"name": exam_id}

            if not update_data:
                print('No updates provided')
                return False

            result = self.db.exams.update_one(filter_q, {"$set": update_data})
            if result.modified_count > 0:
                print(' Exam updated successfully')
                return True
            else:
                print('No exam found to update')
                return False
        except Exception as e:
            print(f" Error updating exam: {e}")
            return False

    def delete_exam(self, exam_id):
        """Remove an exam by id or name."""
        try:
            filters = []
            try:
                filters.append({"_id": ObjectId(exam_id)})
            except Exception:
                pass
            filters.append({"name": exam_id})

            result = self.db.exams.delete_many({"$or": filters})
            if result.deleted_count > 0:
                print(f" Exam deleted successfully (removed {result.deleted_count})")
                return True
            else:
                print('No exam found to delete')
                return False
        except Exception as e:
            print(f" Error deleting exam: {e}")
            return False
    
    # Results
    
    def record_result(self, student_id, exam_id, subject_id, score, remarks=None):
        """Save a student's result for an exam+subject."""
        try:
            # Calculate grade
            grade = self.calculate_grade(score)
            # Resolve IDs: accept ObjectId strings or alternate identifiers
            # student: admission_number fallback
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print(f" Student not found for identifier: {student_id}")
                    return None
                sid_obj = s['_id']

            # exam: name fallback
            try:
                eid_obj = ObjectId(exam_id)
            except Exception:
                e = self.db.exams.find_one({"name": exam_id})
                if not e:
                    print(f" Exam not found for identifier: {exam_id}")
                    return None
                eid_obj = e['_id']

            # subject: code fallback
            try:
                subid_obj = ObjectId(subject_id)
            except Exception:
                sub = self.db.subjects.find_one({"code": subject_id})
                if not sub:
                    print(f" Subject not found for identifier: {subject_id}")
                    return None
                subid_obj = sub['_id']

            result_document = {
                "student_id": sid_obj,
                "exam_id": eid_obj,
                "subject_id": subid_obj,
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
        """List results for a student and show a simple average."""
        try:
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print(f"Student not found for identifier: {student_id}")
                    return []
                sid_obj = s['_id']
            results = list(self.db.results.find({"student_id": sid_obj}))
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
        """Print student info and all their results."""
        try:
            try:
                sid_obj = ObjectId(student_id)
            except Exception:
                s = self.db.students.find_one({"admission_number": student_id})
                if not s:
                    print("Student not found")
                    return None
                sid_obj = s['_id']

            student = self.db.students.find_one({"_id": sid_obj})
            if not student:
                print("Student not found")
                return None

            results = list(self.db.results.find({"student_id": sid_obj}))
            
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

    def get_all_results(self):
        """List all results with human-friendly references"""
        try:
            results = list(self.db.results.find())
            if results:
                print(f"\n Total Results: {len(results)}")
                for r in results:
                    # try to resolve student admission, exam name, subject code
                    try:
                        st = self.db.students.find_one({"_id": r.get('student_id')})
                        adm = st['admission_number'] if st else str(r.get('student_id'))
                    except Exception:
                        adm = str(r.get('student_id'))
                    try:
                        ex = self.db.exams.find_one({"_id": r.get('exam_id')})
                        en = ex['name'] if ex else str(r.get('exam_id'))
                    except Exception:
                        en = str(r.get('exam_id'))
                    try:
                        sub = self.db.subjects.find_one({"_id": r.get('subject_id')})
                        sc = sub['code'] if sub else str(r.get('subject_id'))
                    except Exception:
                        sc = str(r.get('subject_id'))

                    print(f"  • {r['_id']} | Student: {adm} | Exam: {en} | Subject: {sc} | Score: {r.get('score')} | Grade: {r.get('grade')}")
                return results
            else:
                print('No results found')
                return []
        except Exception as e:
            print(f" Error listing results: {e}")
            return []

    def update_result(self, result_id, score=None, remarks=None):
        """Update a result record by ObjectId. Score will recompute grade."""
        try:
            try:
                filter_q = {"_id": ObjectId(result_id)}
            except Exception:
                print('Invalid result identifier')
                return False

            update_data = {}
            if score is not None:
                try:
                    sc = float(score)
                except Exception:
                    print('Invalid score')
                    return False
                update_data['score'] = sc
                update_data['grade'] = self.calculate_grade(sc)
            if remarks is not None:
                update_data['remarks'] = remarks

            if not update_data:
                print('No updates provided')
                return False

            result = self.db.results.update_one(filter_q, {'$set': update_data})
            if result.modified_count > 0:
                print(' Result updated successfully')
                return True
            else:
                print('No result found to update')
                return False
        except Exception as e:
            print(f" Error updating result: {e}")
            return False

    def delete_result(self, result_id):
        """Delete result by ObjectId"""
        try:
            try:
                res = self.db.results.delete_many({"_id": ObjectId(result_id)})
            except Exception:
                print('Invalid result identifier')
                return False

            if res.deleted_count > 0:
                print(f' Result deleted successfully (removed {res.deleted_count})')
                return True
            else:
                print('No result found to delete')
                return False
        except Exception as e:
            print(f" Error deleting result: {e}")
            return False
    
    # Helper functions
    
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

        print("\nSample :\n" )
        manager.get_all_teachers()
        manager.get_all_classes()
        manager.get_all_subjects()
        manager.get_all_exams()

        # Show transcript for the first student found 
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