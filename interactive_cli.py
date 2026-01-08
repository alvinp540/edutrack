# interactive_cli.py
"""Simple interactive CLI for EduTrack manager."""
from edutrack_manager import EduTrackManager
from datetime import datetime
from bson import ObjectId


def prompt(msg, required=True):
    try:
        while True:
            v = input(msg).strip()
            if required and not v:
                print(' Input required')
                continue
            return v
    except (KeyboardInterrupt, EOFError):
        print()
        return None


def is_back_choice(val):
    """Return True when the user chose to go back (b/back or empty)."""
    if val is None:
        return True
    v = val.strip().lower()
    return v in ('b', 'back')


class CLI:
    def __init__(self):
        self.mgr = EduTrackManager()

    def teachers(self):
        while True:
            print('\nTeachers: 1)Add 2)List 3)Get 4)Update 5)Delete 6)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                emp = prompt('Employee number: ')
                fn = prompt('First name: ')
                ln = prompt('Last name: ')
                phone = prompt('Phone: ')
                email = prompt('Email: ')
                dept = prompt('Department: ')
                self.mgr.add_teacher(emp, fn, ln, phone, email, dept)
            elif c == '2':
                self.mgr.get_all_teachers()
            elif c == '3':
                tid = prompt('Teacher ID or employee number: ')
                self.mgr.get_teacher(tid)
            elif c == '4':
                tid = prompt('Teacher ID or employee number: ')
                print('leave blank to skip')
                fn = prompt('First name: ', required=False)
                ln = prompt('Last name: ', required=False)
                phone = prompt('Phone: ', required=False)
                email = prompt('Email: ', required=False)
                dept = prompt('Department: ', required=False)
                update = {k: v for k, v in [('first_name', fn), ('last_name', ln), ('phone', phone), ('email', email), ('department', dept)] if v}
                if update:
                    self.mgr.update_teacher(tid, **update)
                else:
                    print('No updates provided')
            elif c == '5':
                tid = prompt('Teacher ID or employee number: ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_teacher(tid)
                    if ok:
                        print('\nUpdated teachers list:')
                        self.mgr.get_all_teachers()
            # accept explicit back keys
            if c in ('6',) or is_back_choice(c):
                break
            # any other invalid choice will loop

    def classes(self):
        while True:
            print('\nClasses: 1)Add 2)List 3)Get 4)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                name = prompt('Class name: ')
                form = prompt('Form: ')
                tid = prompt('Class teacher ID (optional): ', required=False)
                self.mgr.add_class(name, form, tid if tid else None)
            elif c == '2':
                self.mgr.get_all_classes()
            elif c == '3':
                cid = prompt('Class ID or class name: ')
                self.mgr.get_class(cid)
            if c in ('6',) or is_back_choice(c):
                break

    def students(self):
        while True:
            print('\nStudents: 1)Add 2)List 3)Get 4)Update 5)Delete 6)By class 7)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                adm = prompt('Admission number: ')
                fn = prompt('First name: ')
                ln = prompt('Last name: ')
                gender = prompt('Gender: ')
                dob_s = prompt('DOB (YYYY-MM-DD): ')
                try:
                    dob = datetime.strptime(dob_s, '%Y-%m-%d').date()
                except Exception:
                    print('Invalid date')
                    continue
                class_id = prompt('Class ID or class name: ')
                parent = prompt('Parent phone (optional): ', required=False)
                self.mgr.add_student(adm, fn, ln, gender, dob, class_id, parent if parent else None)
            elif c == '2':
                self.mgr.get_all_students()
            elif c == '3':
                sid = prompt('Student ID or admission number: ')
                self.mgr.get_student(sid)
            elif c == '4':
                sid = prompt('Student ID or admission number: ')
                print('leave blank to skip')
                fn = prompt('First name: ', required=False)
                ln = prompt('Last name: ', required=False)
                gender = prompt('Gender: ', required=False)
                parent = prompt('Parent phone: ', required=False)
                class_id = prompt('Class ID: ', required=False)
                update = {}
                if fn: update['first_name'] = fn
                if ln: update['last_name'] = ln
                if gender: update['gender'] = gender
                if parent: update['parent_phone'] = parent
                if class_id:
                    try:
                        update['class_id'] = ObjectId(class_id)
                    except Exception:
                        update['class_id'] = class_id
                if update:
                    self.mgr.update_student(sid, **update)
                else:
                    print('No updates provided')
            elif c == '5':
                sid = prompt('Student ID or admission number: ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_student(sid)
                    if ok:
                        print('\nUpdated students list:')
                        self.mgr.get_all_students()
            elif c == '6':
                cid = prompt('Class ID or class name: ')
                self.mgr.get_students_by_class(cid)
            if c in ('7',) or is_back_choice(c):
                break

    def subjects(self):
        while True:
            print('\nSubjects: 1)Add 2)List 3)Get 4)Update 5)Delete 6)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                name = prompt('Name: ')
                code = prompt('Code: ')
                tid = prompt('Teacher ID (optional): ', required=False)
                # try to convert teacher id to ObjectId, otherwise pass raw
                if tid:
                    try:
                        tid_val = ObjectId(tid)
                    except Exception:
                        tid_val = tid
                else:
                    tid_val = None
                self.mgr.add_subject(name, code, tid_val)
            elif c == '2':
                self.mgr.get_all_subjects()
            elif c == '3':
                sid = prompt('Subject ID or subject code: ')
                self.mgr.get_subject(sid)
            elif c == '4':
                sid = prompt('Subject ID or subject code: ')
                print('leave blank to skip')
                name = prompt('Name: ', required=False)
                code = prompt('Code: ', required=False)
                tid = prompt('Teacher ID (optional): ', required=False)
                if tid:
                    try:
                        tid_val = ObjectId(tid)
                    except Exception:
                        tid_val = tid
                else:
                    tid_val = None
                update = {}
                if name: update['name'] = name
                if code: update['code'] = code
                if tid is not None: update['teacher_id'] = tid_val
                if update:
                    ok = self.mgr.update_subject(sid, **update)
                    if ok:
                        print('\nUpdated subjects list:')
                        self.mgr.get_all_subjects()
                else:
                    print('No updates provided')
            elif c == '5':
                sid = prompt('Subject ID or subject code: ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_subject(sid)
                    if ok:
                        print('\nUpdated subjects list:')
                        self.mgr.get_all_subjects()
            if c in ('6',) or is_back_choice(c):
                break

    def attendance(self):
        while True:
            print('\nAttendance: 1)Record 2)List all 3)View student 4)Summary 5)Update 6)Delete 7)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                sid = prompt('Student ID or admission number: ')
                date_s = prompt('Date (YYYY-MM-DD): ')
                status = prompt('Status (Present/Absent/Late): ')
                try:
                    date_obj = datetime.strptime(date_s, '%Y-%m-%d').date()
                except Exception:
                    print('Invalid date')
                    continue
                self.mgr.record_attendance(sid, date_obj, status)
            elif c == '2':
                self.mgr.get_all_attendance()
            elif c == '3':
                sid = prompt('Student ID or admission number: ')
                self.mgr.get_student_attendance(sid)
            elif c == '4':
                sid = prompt('Student ID or admission number: ')
                self.mgr.get_attendance_summary(sid)
            elif c == '5':
                aid = prompt('Attendance ID or composite (admission|YYYY-MM-DD): ')
                print('leave blank to skip')
                date_in = prompt('New Date (YYYY-MM-DD): ', required=False)
                status = prompt('New Status (Present/Absent/Late): ', required=False)
                date_val = None
                if date_in:
                    try:
                        date_val = datetime.strptime(date_in, '%Y-%m-%d').date()
                    except Exception:
                        print('Invalid date')
                        continue
                ok = self.mgr.update_attendance(aid, date=date_val, status=status if status else None)
                if ok:
                    print('\nUpdated attendance list:')
                    self.mgr.get_all_attendance()
            elif c == '6':
                aid = prompt('Attendance ID or composite (admission|YYYY-MM-DD): ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_attendance(aid)
                    if ok:
                        print('\nUpdated attendance list:')
                        self.mgr.get_all_attendance()
            if c in ('7',) or is_back_choice(c):
                break

    def exams(self):
        while True:
            print('\nExams: 1)Add 2)List 3)Get 4)Update 5)Delete 6)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                name = prompt('Exam name: ')
                date_s = prompt('Date (YYYY-MM-DD): ')
                class_id = prompt('Class ID or class name: ')
                try:
                    date_obj = datetime.strptime(date_s, '%Y-%m-%d').date()
                except Exception:
                    print('Invalid date')
                    continue
                self.mgr.add_exam(name, date_obj, class_id)
            elif c == '2':
                self.mgr.get_all_exams()
            elif c == '3':
                eid = prompt('Exam ID or exam name: ')
                self.mgr.get_exam(eid)
            elif c == '4':
                eid = prompt('Exam ID or exam name: ')
                print('leave blank to skip')
                name = prompt('Name: ', required=False)
                date_in = prompt('Date (YYYY-MM-DD): ', required=False)
                class_id = prompt('Class ID or class name: ', required=False)
                date_val = None
                if date_in:
                    try:
                        date_val = datetime.strptime(date_in, '%Y-%m-%d').date()
                    except Exception:
                        print('Invalid date')
                        continue
                update = {}
                if name: update['name'] = name
                if date_val is not None: update['date'] = date_val
                if class_id: update['class_id'] = class_id
                if update:
                    ok = self.mgr.update_exam(eid, **update)
                    if ok:
                        print('\nUpdated exams list:')
                        self.mgr.get_all_exams()
                else:
                    print('No updates provided')
            elif c == '5':
                eid = prompt('Exam ID or exam name: ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_exam(eid)
                    if ok:
                        print('\nUpdated exams list:')
                        self.mgr.get_all_exams()
            if c in ('8',) or is_back_choice(c):
                break

    def results(self):
        while True:
            print('\nResults: 1)Record 2)List all 3)Get result 4)Update 5)Delete 6)View student results 7)Transcript 8)Back (or b)')
            c = prompt('Choice: ')
            if c == '1':
                sid = prompt('Student ID or admission number: ')
                eid = prompt('Exam ID or exam name: ')
                subid = prompt('Subject ID or subject code: ')
                try:
                    score = int(prompt('Score (0-100): '))
                except Exception:
                    print('Invalid score')
                    continue
                remarks = prompt('Remarks (optional): ', required=False)
                self.mgr.record_result(sid, eid, subid, score, remarks if remarks else None)
            elif c == '2':
                self.mgr.get_all_results()
            elif c == '3':
                rid = prompt('Result ID: ')
                try:
                    doc = self.mgr.db.results.find_one({"_id": ObjectId(rid)})
                    if doc:
                        print(doc)
                    else:
                        print('Result not found')
                except Exception:
                    print('Invalid result identifier')
            elif c == '4':
                rid = prompt('Result ID: ')
                print('leave blank to skip')
                score_in = prompt('New Score (0-100): ', required=False)
                remarks = prompt('New Remarks: ', required=False)
                score_val = None
                if score_in:
                    try:
                        score_val = float(score_in)
                    except Exception:
                        print('Invalid score')
                        continue
                ok = self.mgr.update_result(rid, score=score_val, remarks=remarks if remarks else None)
                if ok:
                    print('\nUpdated results list:')
                    self.mgr.get_all_results()
            elif c == '5':
                rid = prompt('Result ID: ')
                if prompt('Confirm delete (yes/no): ').lower().startswith('y'):
                    ok = self.mgr.delete_result(rid)
                    if ok:
                        print('\nUpdated results list:')
                        self.mgr.get_all_results()
            elif c == '6':
                sid = prompt('Student ID or admission number: ')
                self.mgr.get_student_results(sid)
            elif c == '7':
                sid = prompt('Student ID or admission number: ')
                self.mgr.get_student_transcript(sid)
            if c in ('4',) or is_back_choice(c):
                break

    def run(self):
        try:
            while True:
    
                print(' EduTrack - No.1 schooling solution')
                print('1)Teachers 2)Classes 3)Students 4)Subjects')
                print('5)Attendance 6)Exams 7)Results 8)Stats 9)Exit')
                c = prompt('Select: ')
                if c == '1':
                    self.teachers()
                elif c == '2':
                    self.classes()
                elif c == '3':
                    self.students()
                elif c == '4':
                    self.subjects()
                elif c == '5':
                    self.attendance()
                elif c == '6':
                    self.exams()
                elif c == '7':
                    self.results()
                elif c == '8':
                    self.mgr.get_database_stats()
                elif c == '9' or c is None:
                    break
                else:
                    print('Invalid choice')
        finally:
            self.mgr.close_connection()


if __name__ == '__main__':
    CLI().run()
