

from Institute_app.models import AttendanceDetails, CourseDetails, ExamDetails, FeeDetails, FollowUpData, FollowupStatus, HrDetails, InterviewDetails, ModuleDetails, NotesDetails, SeatingDetails, StudentDetails, StudentModule, SystemDetails, TrainerDetails
from django.db import models
from django.shortcuts import render,redirect
from datetime import date, datetime, time, timedelta
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import GetUniqueID, checkSystemAvailability, email_service
from Institute_app.Forms.AdminForms import CourseForm, HrForm, ModuleForm, SystemForm, TrainerForm,FollowupForm

def StudentHome(request):
    return render(request,'Student/StudentHome.html')

def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    tab_selection="View Notes"
    if request.method=='POST':
      
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Student/ViewNotes.html',{'modules':modules,'notes':notes,'tab_selection':tab_selection})

def ExamShedhule(request):
    exams=ExamDetails.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/Exam.html',{'exams':exams,})


def MyAttendance(request):
    tab_selection="My Attendance"
    attendance_data=""
    if request.method=='POST':
       
        mnth=request.POST['mnth']
        yr=date.today().year
     
        
        attendance_data=AttendanceDetails.objects.filter(s_id=request.session['s_id'],mnth=mnth,yr=yr)
        
    return render(request,'Student/ViewAttendance.html',{'attendance_data':attendance_data,'tab_selection':tab_selection})

def ViewAllExam(request):
    tab_selection="View Exam"
    exams=ExamDetails.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/ViewExams.html',{'exams':exams,'tab_selection':tab_selection})


def PaymentStatus(request):
   
     
    tab_selection="Payment Status"
    payment_data=FeeDetails.objects.filter(s_id=request.session['s_id'])
    
    return render(request,'Student/PaymentStatus.html',{'payment_data':payment_data,'tab_selection':tab_selection})


def ViewInterview(request):
    data=InterviewDetails.objects.filter(s_id=request.session['s_id'])
    tab_selection="View Interview"
    return render(request,'Student/ViewInter.html',{'data':data,'tab_selection':tab_selection})


def ChangePassword(request):
    tab_selection="Change Password"
    if request.method=='POST':

        old_passwd=request.POST['old_passwd']
        new_passwd=request.POST['new_passwd']
        con_passwd=request.POST['con_passwd']

        Student_data=StudentDetails.objects.get(s_id=request.session['s_id'])
        is_true=pbkdf2_sha256.verify(old_passwd,Student_data.s_passwd)
        if is_true:
            if len(new_passwd)>8:
                if new_passwd==con_passwd:
                    new_encrypted_passwd=pbkdf2_sha256.hash(new_passwd,rounds=1000,salt_size=32)
                    Student_data.tr_passwd=new_encrypted_passwd
                    Student_data.save()
                    success_msg="Password Changed Succesfully"
                    return render(request,'Student/ChangePassword.html',{'success_msg':success_msg,'tab_selection':tab_selection,})
                else:
                    error_msg="Password Mismatch"
                    return render(request,'Student/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})
            else:
                error_msg="Password Should be atleast 8 characters"
                return render(request,'Student/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})
        else:
            error_msg="Invalid Password! enter Your correct password"
            return render(request,'Student/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})

    return render(request,'Student/ChangePassword.html',{'tab_selection':tab_selection,})
