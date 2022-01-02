

from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from Institute_app.Forms.HrForms import StudentForm
from Institute_app.Views.auth_gaurd import auth_st
from Institute_app.models import AttendanceDetails, CertFiles, CourseDetails, ExamDetails, FeeDetails, FollowUpData, FollowupStatus, HrDetails, InterviewDetails, ModuleDetails, NotesDetails, SeatingDetails, StudentDetails, StudentModule, SystemDetails, TrainerDetails
from django.db import models
from django.shortcuts import render,redirect
from datetime import date, datetime, time, timedelta
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import GetUniqueID, checkSystemAvailability, email_service
from Institute_app.Forms.AdminForms import CourseForm, HrForm, ModuleForm, SystemForm, TrainerForm,FollowupForm

@auth_st
def StudentHome(request):
    return render(request,'Student/StudentHome.html')

@auth_st
def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    tab_selection="View Notes"
    if request.method=='POST':
      
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Student/ViewNotes.html',{'modules':modules,'notes':notes,'tab_selection':tab_selection})

@auth_st
def ExamShedhule(request):
    exams=ExamDetails.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/Exam.html',{'exams':exams,})

@auth_st
def MyAttendance(request):
    tab_selection="My Attendance"
    attendance_data=""
    if request.method=='POST':
       
        mnth=request.POST['mnth']
        yr=date.today().year
     
        
        attendance_data=AttendanceDetails.objects.filter(s_id=request.session['s_id'],mnth=mnth,yr=yr)
        
    return render(request,'Student/ViewAttendance.html',{'attendance_data':attendance_data,'tab_selection':tab_selection})

@auth_st
def ViewAllExam(request):
    tab_selection="View Exam"
    exams=ExamDetails.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/ViewExams.html',{'exams':exams,'tab_selection':tab_selection})

@auth_st
def PaymentStatus(request):
   
     
    tab_selection="Payment Status"
    payment_data=FeeDetails.objects.filter(s_id=request.session['s_id'])
    
    return render(request,'Student/PaymentStatus.html',{'payment_data':payment_data,'tab_selection':tab_selection})

@auth_st
def ViewInterview(request):
    data=InterviewDetails.objects.filter(s_id=request.session['s_id'])
    tab_selection="View Interview"
    return render(request,'Student/ViewInter.html',{'data':data,'tab_selection':tab_selection})

@auth_st
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
                    Student_data.s_passwd=new_encrypted_passwd
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


def Logout(request):
     
    if 's_id' in request.session:
        del request.session['s_id']
    request.session.flush()
    return redirect("institute_app:proj_home")

@auth_st
def LoadPay(request):
    tab_selection="Select Installment"
    data=FeeDetails.objects.filter(~Q(status='paid'),s_id=request.session['s_id'])
    student=StudentDetails.objects.get(s_id=request.session['s_id'])
    fee=FeeDetails.objects.filter(s_id=request.session['s_id'])
    if 'ins' in request.GET:
        print(request.GET['ins'])
        i=FeeDetails.objects.get(id=request.GET['ins'])
        print(i.due_amt)
        return JsonResponse({'amt':i.due_amt,'inst':i.ins_no})
    if request.method=='POST':
        tab_selection="Confirm And Pay"
        amt=request.POST['amt_to_pay'] 
        no=request.POST['ins_no']
        d=FeeDetails.objects.get(id=no)
        return render(request,'Student/ConfirmPayment.html',{'amt':amt,'no':no,'d':d,'tab_selection':tab_selection})
    return render(request,'Student/LoadPay.html',{'tab_selection':tab_selection,'data':data,'student':student,'fee':fee})

@auth_st
def PaySuccess(request):
    print(request.GET['no'],'kkaka')
    cur_date=date.today()
    dt_covrt=cur_date.strftime("%d/%m/%Y") 
    data=FeeDetails.objects.get(id=request.GET['no'])
    data.paid_amt=request.GET['amt']
    data.paid_date=dt_covrt
    data.status='paid'
    data.pay_type='online'
    data.save()
    return redirect("institute_app:st_home")

@auth_st
def MyProfile(request):
    std_data=StudentDetails.objects.get(s_id=request.session['s_id'])
    
    tab_selection="My Profile"
    return render(request,'Student/UpdateProfile.html',{'data':std_data,'tab_selection':tab_selection,})

@auth_st
def DownloadCert(request):
    tab_selection="Download Certificate"
    cert_data=CertFiles.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/DownloadCert.html',{'data':cert_data,'tab_selection':tab_selection,})

