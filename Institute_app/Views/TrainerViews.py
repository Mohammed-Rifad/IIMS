import datetime

from django.db.models.query_utils import Q
from Institute_app.Views.auth_gaurd import auth_tr

from Institute_app.services import UpdateSeat, getFileName
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from passlib.hash import pbkdf2_sha256

from ..models import AttendanceDetails, CourseDetails, ExamDetails, FeeDetails, ModuleDetails, NotesDetails, PlacementDetails, SeatingDetails,StudentDetails, StudentModule, SystemDetails, TrainerDetails

@auth_tr
def TrainerHome(request):
    return render(request,'Trainer/TrainerHome.html')


# ajax
def getSystem(request):
    lab_no=request.GET['lab_no']
    systems=SystemDetails.objects.filter(lab_no=lab_no)
    return render(request,'Trainer/system_dropdown.html',{'systems':systems})


@auth_tr
def ViewActiveStudents(request):

    courses=CourseDetails.objects.all()
    tab_selection="View Students"
    students=StudentDetails.objects.filter(status="active")
    data=''
    
    s_id=''
    if request.method=='POST':
        if 'filter' in request.POST:
            course=request.POST['course']
            # s_id=request.POST['s_id']
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
        if 'completed' in request.POST:
            s_id=request.POST['s_id']
            flag=0
            fee_detail=FeeDetails.objects.filter(s_id=s_id)
            for f in fee_detail:
                if f.status=='not paid':
                    flag=1
            print('fffffffffffffff',flag)
            if flag==0:
                std=StudentDetails.objects.get(s_id=s_id)
                std.status='course completed'
                std.save()
                return redirect('institute_app:tr_active_students')
            else:
                fee_msg="Payment Not Completed"
                return render(request,'Trainer/ActiveStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection,'fee_msg':fee_msg})


        return render(request,'Trainer/UpdateStudentModule.html',{'s_id':s_id,'modules':data,'tab_selection':tab_selection})
    return render(request,'Trainer/ActiveStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection})

@auth_tr
def ViewPlacement(request):
    tab_selection="View Placement"
    placements=PlacementDetails.objects.all()
    if request.method=='POST':
        id=request.POST['id']
        placement=PlacementDetails.objects.get(id=id)
        placement.delete()
        student=StudentDetails.objects.get(s_id=id)
        student.placed=0
        student.save()
    return render(request,'Trainer/ViewPlacement.html',{'placements':placements,'tab_selection':tab_selection,})

def UpdateStatus(request):
    s_id=request.POST['s_id']
    m_id=request.POST['module']
    data=StudentModule.objects.get(s_id=s_id,m_id=m_id)
    data.status="completed"
    data.save()
    return redirect("institute_app:tr_active_students")



@auth_tr
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

@auth_tr
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

@auth_tr
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

@auth_tr
def ViewStudentStatus(request):
    student=''
    return render(request,'Trainer/StudentModule.html',)

@auth_tr
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

@auth_tr
def getStudentModule(request):
    data=StudentDetails.objects.get(s_id=request.GET['s_id'])
    modules=ModuleDetails.objects.filter(c_id=data.c_id)
    return render(request,'Trainer/modulesDropdown.html',{'modules':modules})


@auth_tr
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


@auth_tr
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


@auth_tr
def StudentExam(request):
    tab_selection="Update Exam"
    exams=ExamDetails.objects.filter(status='pending')
    return render(request,'Trainer/Exams.html',{'exams':exams,'tab_selection':tab_selection})

@auth_tr
def ViewAllExam(request):
    tab_selection="View Exam"
    exams=ExamDetails.objects.filter(~Q(status='pending'))
    return render(request,'Trainer/AllExams.html',{'exams':exams,'tab_selection':tab_selection})


@auth_tr
def DeleteExam(request):
    id=request.GET['id']
    exam=ExamDetails.objects.get(id=id)
    exam.delete()
    return redirect("institute_app:tr_view_exam")

@auth_tr
def UpdateExam(request):
    tab_selection="Update Exam"
    if request.method=='POST':
        id=request.POST['id']
        exam=ExamDetails.objects.get(id=id)
        exam.status=request.POST['status']
        exam.save()
        return redirect("institute_app:tr_view_exam")
    id=request.GET['id']
    
    return render(request,'Trainer/UpdateExam.html',{'id':id,'tab_selection':tab_selection})


@auth_tr
def ViewSeating(request):
    seating_details=""
    tab_selection="View Seating"
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'Trainer/ViewSeating.html',{'seating_details':seating_details,'tab_selection':tab_selection})


@auth_tr
def ChangePassword(request):
    tab_selection="Change Password"
    if request.method=='POST':

        old_passwd=request.POST['old_passwd']
        new_passwd=request.POST['new_passwd']
        con_passwd=request.POST['con_passwd']

        trainer_data=TrainerDetails.objects.get(tr_id=request.session['tr_id'])
        is_true=pbkdf2_sha256.verify(old_passwd,trainer_data.tr_passwd)
        if is_true:
            if len(new_passwd)>8:
                if new_passwd==con_passwd:
                    new_encrypted_passwd=pbkdf2_sha256.hash(new_passwd,rounds=1000,salt_size=32)
                    trainer_data.tr_passwd=new_encrypted_passwd
                    trainer_data.save()
                    success_msg="Password Changed Succesfully"
                    return render(request,'Trainer/ChangePassword.html',{'success_msg':success_msg,})
                else:
                    error_msg="Password Mismatch"
                    return render(request,'Trainer/ChangePassword.html',{'error_msg':error_msg,})
            else:
                error_msg="Password Should be atleast 8 characters"
                return render(request,'Trainer/ChangePassword.html',{'error_msg':error_msg,})
        else:
            error_msg="Invalid Password! enter Your correct password"
            return render(request,'Trainer/ChangePassword.html',{'error_msg':error_msg,})

    return render(request,'Trainer/ChangePassword.html',{'tab_selection':tab_selection,})

def Logout(request):
     
    if 'tr_id' in request.session:
        del request.session['tr_id']
    request.session.flush()
    return redirect("institute_app:proj_home")

@auth_tr
def MyAttendance(request):
    tab_selection="My Attendance"
    attendance_data=""
    if request.method=='POST':
       
        mnth=request.POST['mnth']
        yr=datetime.date.today().year
     
        
        attendance_data=AttendanceDetails.objects.filter(tr_id=request.session['tr_id'],mnth=mnth,yr=yr)
        
    return render(request,'Trainer/MyAttendance.html',{'attendance_data':attendance_data,'tab_selection':tab_selection})