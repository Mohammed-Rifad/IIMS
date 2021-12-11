import datetime

from Institute_app.services import UpdateSeat, getFileName
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from ..models import AttendanceDetails, CourseDetails, ExamDetails, ModuleDetails, NotesDetails, SeatingDetails,StudentDetails, StudentModule, SystemDetails, TrainerDetails

def TrainerHome(request):
    return render(request,'Trainer/TrainerHome.html')


# ajax
def getSystem(request):
    lab_no=request.GET['lab_no']
    systems=SystemDetails.objects.filter(lab_no=lab_no)
    return render(request,'Trainer/system_dropdown.html',{'systems':systems})

def ViewActiveStudents(request):

    courses=CourseDetails.objects.all()
    tab_selection="View Students"
    students=StudentDetails.objects.filter(status="active")

    if request.method=='POST':
        if 'filter' in request.POST:
            course=request.POST['course']
            students=StudentDetails.objects.filter(c_id=course, status="active")
        if 'status' in request.POST:
            s_id=request.POST['s_id']
            data=StudentModule.objects.filter(s_id=s_id)
            s_name=StudentDetails.objects.get(s_id=s_id)
            tab_selection="Module Status"
            return render(request,'Trainer/StudentStatus.html',{'modules':data,'tab_selection':tab_selection,'s_name':s_name})
        if 'update' in request.POST:
            s_id=request.POST['s_id']
            data=StudentModule.objects.filter(s_id=s_id)
            tab_selection="Update Status"
            return render(request,'Trainer/UpdateStudentModule.html',{'s_id':s_id,'modules':data,'tab_selection':tab_selection})
    return render(request,'Trainer/ActiveStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection})


def UpdateStatus(request):
    s_id=request.POST['s_id']
    m_id=request.POST['module']
    data=StudentModule.objects.get(s_id=s_id,m_id=m_id)
    data.status="completed"
    data.save()
    return redirect("institute_app:tr_active_students")



def UpdateSeating(request):
    status=""
    students=StudentDetails.objects.filter(status="active")
    tab_selection="Update Seating"
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        lab=request.POST['lab']
        system=request.POST['system']
        slot=request.POST['slot']

        seating_data=SeatingDetails.objects.get(lab_no=lab,sys_no=system)

        status=UpdateSeat(seating_data,student,slot)
        print(status)
    return render(request,'Trainer/UpdateSeating.html',{'students':students,'status':status,'tab_selection':tab_selection})

def AddNotes(request):
    course_data=CourseDetails.objects.all()
    tab_selection="Upload Notes"
    msg=""
    if request.method=='POST':
        tr_data=TrainerDetails.objects.get(tr_id=request.session['tr_id'])
        uploaded_by=tr_data.tr_name
        dt=datetime.date.today()
        uploaded_date=dt.strftime("%d/%m/%Y")
        module=ModuleDetails.objects.get(m_id=request.POST['module'])
        desc=request.POST['desc']
        file=request.FILES['notes']
        #file_name=getFileName(module.m_name)
        
        notes=NotesDetails(mod_id=module,uploaded_by=uploaded_by,uploaded_date=uploaded_date,uploaded_file=file,desc=desc)
        notes.save()
        # n=NotesDetails.objects.get(id=1)
        # print(request.FILES['notes'])
        msg="Notes Uploaded Succesfully"
    return render(request,'Trainer/AddNotes.html',{'courses':course_data,'tab_selection':tab_selection,'msg':msg})

#ajax
def getModules(request):
    c_id=request.GET['c_id']
    modules=ModuleDetails.objects.filter(c_id=c_id)
    return render(request,'Trainer/modulesDropdown.html',{'modules':modules})

def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    tab_selection="View Notes"
    if request.method=='POST':
        if 'del' in request.POST:
            id=request.POST['n_id']
            note=NotesDetails.objects.get(id=id)
            note.delete()
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Trainer/ViewNotes.html',{'modules':modules,'notes':notes,'tab_selection':tab_selection})

def ViewStudentStatus(request):
    student=''
    return render(request,'Trainer/StudentModule.html',)

def AddExam(request):
    tab_selection="Add Exam"
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        st_id=request.POST['student']
        m_id=request.POST['module']
        exam_date=request.POST['ex_date']
        dt=datetime.date.today()
        date_entered=dt.strftime("%d/%m/%Y")
        dt_exam=datetime.datetime.strptime(exam_date, '%Y-%m-%d')
        dt_ex_str=dt_exam.strftime("%d/%m/%Y")
        exam_exist=ExamDetails.objects.filter(s_id=st_id,m_id=m_id,exam_date=dt_ex_str).exists()
        if not exam_exist:
            student=StudentDetails.objects.get(s_id=st_id)
            module=ModuleDetails.objects.get(m_id=m_id)
            exam=ExamDetails(s_id=student,m_id=module,exam_date=dt_ex_str,date_entered=date_entered)
            exam.save()
            success_msg="Exam Added Succesfully"
            return render(request,'Trainer/AddExam.html',{'students':students,'success_msg':success_msg,'tab_selection':tab_selection})
        else:
            error_msg="Exam Already Added"
            return render(request,'Trainer/AddExam.html',{'students':students,'error_msg':error_msg,'tab_selection':tab_selection})
    return render(request,'Trainer/AddExam.html',{'students':students,'tab_selection':tab_selection})

def getStudentModule(request):
    data=StudentDetails.objects.get(s_id=request.GET['s_id'])
    modules=ModuleDetails.objects.filter(c_id=data.c_id)
    return render(request,'Trainer/modulesDropdown.html',{'modules':modules})


def StudentAttendance(request):
    students=StudentDetails.objects.filter(status="active")
    tab_selection="Add Attendance"
    msg=""
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        dt=request.POST['date']
        status=request.POST['status']
        mnth=datetime.datetime.strptime(dt,"%Y-%m-%d").date().month
        
        yr =datetime.date.today().year
        dt_convrt=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        print('lplpp',dt_str)
        is_mnth_added=AttendanceDetails.objects.filter(s_id=student.s_id,mnth=mnth).exists()
       
        if not is_mnth_added:

            mnth_data=[31,28,31,30,31,30,31,31,30,31,30,31]
            selected_mnth=mnth_data[mnth-1]
            print('mnth',mnth)
            print('***********************',selected_mnth)
            for d in range(1,selected_mnth+1):
                
                # date_to_enter=datetime.datetime.date()+datetime.timedelta(days=1)
                if d<10:
                    date_to_enter=f'0{d}/{mnth}/{yr}'
                else:
                    date_to_enter=f'{d}/{mnth}/{yr}'

                print('date',date_to_enter)
        
                attendance=AttendanceDetails(type="student",s_id=student,mnth=mnth,date=date_to_enter,yr=yr,status="N/A")
                attendance.save()
            selected_attendance=AttendanceDetails.objects.get(s_id=student.s_id,mnth=mnth,yr=yr,date=dt_str)
            selected_attendance.status=status
            selected_attendance.save()
            print('edjkdhf',selected_attendance.status)
        else:
             
            selected_attendance=AttendanceDetails.objects.get(s_id=student.s_id,date=dt_str)
            selected_attendance.status=status
            selected_attendance.save()
        msg="Attendance Added Succesfully"
        # already_added=AttendanceDetails.objects.filter(s_id=request.POST['student'],date=dt_str).exists()
        # if not already_added:
        #     attendance=AttendanceDetails(type="student",s_id=student,date=dt_str,status=status,mnth=mnth,yr=yr)
        #     attendance.save()
        #     success_msg="Attendance Added Succesfully"
        #     return render(request,'Trainer/StudentAttendance.html',{'students':students,'success_msg':success_msg,'tab_selection':tab_selection})
        # else:
        #     error_msg="Attendance Already Added"
        #     return render(request,'Trainer/StudentAttendance.html',{'students':students,'error_msg':error_msg,'tab_selection':tab_selection})
    return render(request,'Trainer/StudentAttendance.html',{'students':students,'tab_selection':tab_selection,'msg':msg})


def ViewStudentAttendance(request):
    tab_selection="View Attendance"
    attendance_data=""
    student_name=""
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        s_id=request.POST['student']
        mnth=request.POST['mnth']
        yr=datetime.date.today().year
        # dt_convrt=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
        # dt_str=dt_convrt.strftime("%d/%m/%Y")
        student_data=StudentDetails.objects.get(s_id=s_id)
        attendance_data=AttendanceDetails.objects.filter(s_id=s_id,mnth=mnth,yr=yr)
        student_name=student_data.s_name
        print(student_data)
    return render(request,'Trainer/ViewStudentAttendance.html',{'students':students,'attendance_data':attendance_data,'student_name':student_name,'tab_selection':tab_selection})


def StudentExam(request):
    tab_selection="View Exam"
    exams=ExamDetails.objects.filter(status='pending')
    return render(request,'Trainer/Exams.html',{'exams':exams,'tab_selection':tab_selection})

def DeleteExam(request):
    id=request.GET['id']
    exam=ExamDetails.objects.get(id=id)
    exam.delete()
    return redirect("institute_app:tr_view_exam")

def UpdateExam(request):
    
    if request.method=='POST':
        id=request.POST['id']
        exam=ExamDetails.objects.get(id=id)
        exam.status=request.POST['status']
        exam.save()
        return redirect("institute_app:tr_view_exam")
    id=request.GET['id']
    
    return render(request,'Trainer/UpdateExam.html',{'id':id,})


def ViewSeating(request):
    seating_details=""
    tab_selection="View Seating"
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'Trainer/ViewSeating.html',{'seating_details':seating_details,'tab_selection':tab_selection})

