import datetime
from Institute_app.services import UpdateSeat, getFileName
from django.shortcuts import render,redirect
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
            print('data',data)
            tab_selection="Module Status"
            return render(request,'Trainer/StudentStatus.html',{'modules':data,'tab_selection':tab_selection})
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
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        lab=request.POST['lab']
        system=request.POST['system']
        slot=request.POST['slot']

        seating_data=SeatingDetails.objects.get(lab_no=lab,sys_no=system)

        status=UpdateSeat(seating_data,student,slot)
        print(status)
    return render(request,'Trainer/UpdateSeating.html',{'students':students,'status':status})

def AddNotes(request):
    course_data=CourseDetails.objects.all()
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

    return render(request,'Trainer/AddNotes.html',{'courses':course_data})

#ajax
def getModules(request):
    c_id=request.GET['c_id']
    modules=ModuleDetails.objects.filter(c_id=c_id)
    return render(request,'Trainer/modulesDropdown.html',{'modules':modules})

def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    if request.method=='POST':
        if 'del' in request.POST:
            id=request.POST['n_id']
            note=NotesDetails.objects.get(id=id)
            note.delete()
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Trainer/ViewNotes.html',{'modules':modules,'notes':notes,})

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

        exam_exist=ExamDetails.objects.filter(s_id=st_id,m_id=m_id,exam_date=exam_date).exists()
        if not exam_exist:
            student=StudentDetails.objects.get(s_id=st_id)
            module=ModuleDetails.objects.get(m_id=m_id)
            exam=ExamDetails(s_id=student,m_id=module,exam_date=exam_date,date_entered=date_entered)
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
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        dt=request.POST['date']
        status=request.POST['status']
        mnth=datetime.date.today().month
        yr =datetime.date.today().year
        dt_convrt=datetime.datetime.strptime(dt,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        print(mnth,yr,dt_convrt,dt_str)

        already_added=AttendanceDetails.objects.filter(s_id=request.POST['student'],date=dt_str).exists()
        if not already_added:
            attendance=AttendanceDetails(type="student",s_id=student,date=dt_str,status=status,mnth=mnth,yr=yr)
            attendance.save()
            success_msg="Attendance Added Succesfully"
            return render(request,'Trainer/StudentAttendance.html',{'students':students,'success_msg':success_msg})
        else:
            error_msg="Attendance Already Added"
            return render(request,'Trainer/StudentAttendance.html',{'students':students,'error_msg':error_msg})
    return render(request,'Trainer/StudentAttendance.html',{'students':students})


def ViewStudentAttendance(request):
    attendance_data=""
    student_name=""
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        s_id=request.POST['student']
        mnth=request.POST['mnth']
        yr=datetime.date.today().year
        student_data=StudentDetails.objects.get(s_id=s_id)
        attendance_data=AttendanceDetails.objects.filter(s_id=s_id,mnth=mnth,yr=yr)
        student_name=student_data.s_name
    return render(request,'Trainer/ViewStudentAttendance.html',{'students':students,'attendance_data':attendance_data,'student_name':student_name})


def StudentExam(request):
    exams=ExamDetails.objects.filter(status='pending')
    return render(request,'Trainer/Exams.html',{'exams':exams,})

def DeleteExam(request):
    id=request.GET['id']
    exam=ExamDetails.objects.get(id=id)
    exam.delete()
    return render("institute_app:tr_view_exam")

def UpdateExam(request):
    
    if request.method=='POST':
        id=request.POST['id']
        exam=ExamDetails.objects.get(id=id)
        exam.status=request.POST['status']
        exam.save()
        return redirect("institute_app:tr_view_exam")
    id=request.GET['id']
    return render(request,'Trainer/UpdateExam.html',{'id':id,})