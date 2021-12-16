
from datetime import date, timedelta
from django.core.mail import send_mail
from django.db.models.query_utils import check_rel_lookup_compatibility
from datetime import date, datetime, time
from django.http.request import split_domain_port
from Institute_app.models import AttendanceDetails, CertificateDetails, CourseDetails, FeeDetails, FollowUpData, FollowupStatus, HrDetails, InterviewDetails, SeatingDetails, StudentDetails, StudentModule,SystemDetails, TrainerDetails
from Institute_app.Forms.HrForms import InterviewForm, StudentForm
from django.shortcuts import render,redirect
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from .auth_gaurd import auth_hr
from ..services import AddStudentModule, GetUniqueID, InsertFeeDetails, email_service,checkSystemAvailability


@auth_hr
def HrHome(request):
    return render(request,'HR/HrHome.html')


def AddStudent(request):
    form=StudentForm()
    msg=""
    tab_selection="Register Student"
    courses=CourseDetails.objects.all()
    if request.method=='POST':
        form=StudentForm(request.POST,request.FILES)
        if form.is_valid():
            s_name=form.cleaned_data['s_name'].lower()
            s_colg=form.cleaned_data['s_colg'].lower()
            c_id=CourseDetails.objects.get(c_id=request.POST['course'])
            s_dob=form.cleaned_data['s_dob']
            s_qual=form.cleaned_data['s_qual']
            # s_type=request.POST['type']
            s_address=form.cleaned_data['s_address'].lower()
            s_gender=form.cleaned_data['s_gender']
            s_phno=form.cleaned_data['s_phno']
            s_email=form.cleaned_data['s_email']
            s_pic=form.cleaned_data['s_pic']
            s_passout=form.cleaned_data['s_passout']
            amt_payable=form.cleaned_data['amt_payable']
            s_type=form.cleaned_data['s_type']
            s_join=date.today()
            dt_covrt=s_join.strftime("%d/%m/%Y")
            passwd=get_random_string(length=8)
            passwd_enc=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            ins1=request.POST['ins1']
            ins2=request.POST['ins2']
            ins3=request.POST['ins3']

            student_exist=StudentDetails.objects.filter(s_email=s_email,status="active").exists()
            if not student_exist:
                s_id=GetUniqueID('student')   
                student=StudentDetails(s_id=s_id,s_phno=s_phno,s_join=dt_covrt,s_type=s_type,s_name=s_name,c_id=c_id,s_dob=s_dob,s_colg=s_colg,s_qual=s_qual,s_address=s_address,
                s_gender=s_gender,s_email=s_email,s_pic=s_pic,s_passout=s_passout,amt_payable=amt_payable,balance=amt_payable,
                s_passwd=passwd_enc)
                student.save()
                print('uname',s_id,passwd)
                InsertFeeDetails(s_id,s_join,[ins1,ins2,ins3])
                AddStudentModule(s_id,c_id)
                #email_service(s_email,s_id,passwd)
                msg="Student Added Successfully"
            else:
                msg="Email Already Added"
        else:
            print(form.errors)
        return render(request,'HR/AddStudent.html',{'form':form,'courses':courses,'msg':msg,'tab_selection':tab_selection}) 
    return render(request,'HR/AddStudent.html',{'form':form,'courses':courses,'tab_selection':tab_selection})

# ajax
def getSystem(request):
    lab_no=request.GET['lab_no']
    systems=SystemDetails.objects.filter(lab_no=lab_no)
    return render(request,'Hr/system_dropdown.html',{'systems':systems})


def AssignSeating(request):
    status=""
    s_name=""
    tab_selection="Assign Seat"
    st=False
    students=StudentDetails.objects.filter(status="active",s_type="offline")
    if request.method=='POST':

        
        sys_no=request.POST['system']
        lab=request.POST['lab']
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        selected_slot=request.POST['slot']

        seating_data=SeatingDetails.objects.get(sys_no=sys_no,lab_no=lab)

        status=checkSystemAvailability(seating_data,selected_slot,student)
        if status=="Seat Already Allocated For "+student.s_name.title():
            st=True
        else:
            st=False
    return render(request,'HR/AssignSeating.html',{'students':students,'status':status,'tab_selection':tab_selection,'s_name':s_name,'st':st})


def ViewSeating(request):
    seating_details=""
    tab_selection="View Seating"
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'HR/ViewSeating.html',{'seating_details':seating_details,'tab_selection':tab_selection})


def ActiveFollowUp(request):
    tab_selection="Follow Up"
    followup_data=FollowUpData.objects.filter(status="active")
    if request.method=='POST':
        data=FollowUpData.objects.get(f_id=request.POST['f_id'])
        data.status='completed'
        data.save()
    return render(request,'HR/ActiveFollowUp.html',{'followup_data':followup_data,'tab_selection':tab_selection})

def AddFollowUp(request,id):
    tab_selection="Update Follow Up"
    if request.method=='POST':
        id=FollowUpData.objects.get(f_id=id)
        cur_date=date.today()
        dt_covrt=cur_date.strftime("%d/%m/%Y") 
        status=request.POST['status']   

    
        data=FollowupStatus(f_id=id,date=dt_covrt,status=status)
        data.save()
        
        return redirect("institute_app:hr_act_followup")
       
    return render(request,'HR/FollowUp.html',{'id':id,'tab_selection':tab_selection})

def FollowUpHistory(request,f_id):
    data=FollowupStatus.objects.filter(f_id=f_id)
    tab_selection="Follow Up History"
    if request.method=='POST':
        id=request.POST['id']
        hst_data=FollowupStatus(id=id)
        hst_data.delete()
    return render(request,'HR/FollowUpHistory.html',{'data':data,'tab_selection':tab_selection})

def ViewActiveStudents(request):
    tab_selection="Active Students"
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'HR/ActiveStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection})

def TrainerAttendance(request):
    trainers=TrainerDetails.objects.filter(tr_status="active")
    tab_selection="Trainers Attendance"
    msg=""
    if request.method=='POST':
        trainer=TrainerDetails.objects.get(tr_id=request.POST['trainer'])
        dt=request.POST['date']
        status=request.POST['status']
        mnth=datetime.strptime(dt,"%Y-%m-%d").date().month
        
        yr =date.today().year
        dt_convrt=datetime.strptime(dt,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        print('lplpp',dt_str)
        is_mnth_added=AttendanceDetails.objects.filter(tr_id=trainer.tr_id,mnth=mnth).exists()
       
        if not is_mnth_added:

            mnth_data=[31,28,31,30,31,30,31,31,30,31,30,31]
            selected_mnth=mnth_data[mnth-1]
            # print('mnth',mnth)
            # print('***********************',selected_mnth)
            for d in range(1,selected_mnth+1):
                
                # date_to_enter=datetime.datetime.date()+datetime.timedelta(days=1)
                if d<10:
                    date_to_enter=f'0{d}/{mnth}/{yr}'
                else:
                    date_to_enter=f'{d}/{mnth}/{yr}'

                print('date',date_to_enter)
        
                attendance=AttendanceDetails(type="trainer",tr_id=trainer,mnth=mnth,date=date_to_enter,yr=yr,status="N/A")
                attendance.save()
            selected_attendance=AttendanceDetails.objects.get(tr_id=trainer.tr_id,mnth=mnth,yr=yr,date=dt_str)
            selected_attendance.status=status
            selected_attendance.save()
            print('edjkdhf',selected_attendance.status)
        else:
             
            selected_attendance=AttendanceDetails.objects.get(tr_id=trainer.tr_id,date=dt_str)
            selected_attendance.status=status
            selected_attendance.save()
        msg="Attendance Added Succesfully"
    # if request.method=='POST':
    #     trainer=TrainerDetails.objects.get(tr_id=request.POST['trainer'])
    #     dt=request.POST['date']
    #     status=request.POST['status']
    #     mnth=date.today().month
    #     yr =date.today().year
    #     dt_convrt=datetime.strptime(dt,"%Y-%m-%d").date()
    #     dt_str=dt_convrt.strftime("%d/%m/%Y")
    #     print(mnth,yr,dt_convrt,dt_str)

    #     already_added=AttendanceDetails.objects.filter(tr_id=trainer,date=dt_str).exists()
    #     if not already_added:
    #         attendance=AttendanceDetails(type="trainer",tr_id=trainer,date=dt_str,status=status,mnth=mnth,yr=yr)
    #         attendance.save()
    #         msg="Attendance Added Succesfully"
    #         return render(request,'HR/TrainerAttendance.html',{'trainers':trainers,'msg':msg})
    return render(request,'HR/TrainerAttendance.html',{'trainers':trainers,'tab_selection':tab_selection,'msg':msg})


def ViewTrainerAttendance(request):
    attendance_data=""
    trainer_name=""
    trainers=TrainerDetails.objects.filter(tr_status="active")
    if request.method=='POST':
        tr_id=request.POST['trainer']
        mnth=request.POST['mnth']
        yr=date.today().year
        trainer_data=TrainerDetails.objects.get(tr_id=tr_id)
        attendance_data=AttendanceDetails.objects.filter(tr_id=tr_id,mnth=mnth,yr=yr)
        trainer_name=trainer_data.tr_name
    return render(request,'HR/ViewTrainerAttendance.html',{'trainers':trainers,'attendance_data':attendance_data,'trainer_name':trainer_name})



def DueList(request):
    std_array=[]
    data=FeeDetails.objects.filter(status='not paid')
    print(data)
    ss=0
    total=0
    tab_selection="Due List"
    for i in data:
        dt=i.due_date
       
        d=datetime.strptime(dt,'%d/%m/%Y')
        dd=datetime.now()+timedelta(days=7)
        if d<=dd:
            total+=i.due_amt
            std_array.append(i)
        print(d)
        print('array',std_array)
    return render(request,'HR/DueList.html',{'data':std_array,'tab_selection':tab_selection,'total':total})

def AddPayment(request):
    tab_selection="Add Payment"
    if request.method=='GET':
        request.session['p_id']=request.GET['id']
        st=request.GET['st']
    if request.method=='POST':
        payment_data=FeeDetails.objects.get(id=request.session['p_id'])
        
        # payment_data.paid_amt=request.POST['p_amt']
        # payment_data.paid_date=request.POST['p_date']
        dt_convrt=datetime.strptime(request.POST['p_date'],"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        payment_data.paid_amt=request.POST['p_amt']
        payment_data.paid_date=dt_str
        payment_data.pay_type="offline"
        payment_data.status="paid"
        payment_data.save()
        return redirect("institute_app:hr_due_list")
    
    return render(request,'HR/OfflinePayment.html',{'st':st,'tab_selection':tab_selection})



def StudentStatus(request):
    id=request.GET['id']
    name=request.GET['st_name']
    tab_selection="Student Status"
    student_data=StudentModule.objects.filter(s_id=id)
    return render(request,'HR/StudentStatus.html',{'student_data':student_data,'tab_selection':tab_selection,'name':name})

def PaymentStatus(request):
    id=request.GET['id']
    name=request.GET['st_name']
    tab_selection="Payment Status"
    payment_data=FeeDetails.objects.filter(s_id=id)
    
    return render(request,'HR/PaymentStatus.html',{'payment_data':payment_data,'name':name,'tab_selection':tab_selection})

def ViewStudentAttendance(request):
    attendance_data=""
    student_name=""
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        s_id=request.POST['student']
        mnth=request.POST['mnth']
        yr=date.today().year
        student_data=StudentDetails.objects.get(s_id=s_id)
        attendance_data=AttendanceDetails.objects.filter(s_id=s_id,mnth=mnth,yr=yr)
        student_name=student_data.s_name
    return render(request,'Hr/ViewStudentAttendance.html',{'students':students,'attendance_data':attendance_data,'student_name':student_name})

def RequestCertificate(request):
    students=StudentDetails.objects.filter(status="active")
    tab_selection="Request Certificate"
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        hr_comnt=request.POST['hr_comnt']
        req_date= date.today()
        dt_str=req_date.strftime("%d/%m/%Y")
        is_requested=CertificateDetails.objects.filter(s_id=student).exists()
        if not is_requested:
            cert_request=CertificateDetails(s_id=student,req_date=dt_str,hr_comment=hr_comnt)
            cert_request.save()
            success_msg="Request Submitted Succesfully"
            return render(request,'Hr/RequestCertificate.html',{'students':students,'success_msg':success_msg,})
        else:
            error_msg="Certificate Already Requested"
            return render(request,'Hr/RequestCertificate.html',{'students':students,'error_msg':error_msg,'tab_selection':tab_selection})

    return render(request,'Hr/RequestCertificate.html',{'students':students,'tab_selection':tab_selection})


def CertStatus(request):
    data=CertificateDetails.objects.all()
    tab_selection="Certificate Status"
    if request.method=='POST':
        rec_date=request.POST['rec_date']
        dt_convrt=datetime.strptime(rec_date,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        
        cert_data=CertificateDetails.objects.get(s_id=request.POST['s_id'])
        cert_data.rec_date=dt_str
        cert_data.status="received"
        cert_data.save()
    
    return render(request,'Hr/CertificateStatus.html',{'data':data,'tab_selection':tab_selection})

def Logout(request):
     
    if 'hr_id' in request.session:
        del request.session['hr_id']
    request.session.flush()
    return redirect("institute_app:login")

def CompletedStudents(request):
    students=StudentDetails.objects.filter(status="completed")
    courses=CourseDetails.objects.all()
    tab_selection="Completed Students"
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="completed")
    return render(request,'Hr/CompletedStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection})

def AddInterView(request):
    form=InterviewForm()
    courses=CourseDetails.objects.all()
    tab_selection="Assign Interview"
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'HR/AddInterview.html',{'students':students,'courses':courses,'form':form,'tab_selection':tab_selection})

    
def SchedhuleInterview(request) :
    id=request.GET['id']
    msg=""
    form=InterviewForm()
    tab_selection="Schedhule Interview"
    if request.method=='POST':

        form=InterviewForm(request.POST)
        if form.is_valid():
            cmp_name=form.cleaned_data['cmp_name'].lower()
            cmp_addr=form.cleaned_data['cmp_addr'].lower()
            cmp_contact=form.cleaned_data['cmp_contact']
            int_post=form.cleaned_data['int_post'].lower()
            interview_date=request.POST['interview_date']
            int_type=form.cleaned_data['int_type']
            student=StudentDetails.objects.get(s_id=id)
            dt=date.today()
            added_date=dt.strftime("%d/%m/%Y")
            dt_convrt=datetime.strptime(interview_date,"%Y-%m-%d").date()
            dt_str=dt_convrt.strftime("%d/%m/%Y")
            interview=InterviewDetails(cmp_name=cmp_name,cmp_addr=cmp_addr,cmp_contact=cmp_contact,
            interview_date=dt_str,int_type=int_type,s_id=student,added_date=added_date,int_post=int_post)
            interview.save()
            msg="Data Submitted Succesfully"
    return render(request,'HR/SchedhuleInterview.html',{'form':form,'id':id,'msg':msg,'tab_selection':tab_selection})


def ViewInterview(request):
    data=InterviewDetails.objects.all()
    tab_selection="View Interview"
    return render(request,'Hr/ViewInter.html',{'data':data,'tab_selection':tab_selection})

def DelInterview(request):
    id=request.GET['id']
    data=InterviewDetails.objects.get(id=id)
    data.delete()
    return redirect("institute_app:hr_view_inter")

def UpdateInterview(request):
    tab_selection="Update Interview Status"
    
    if request.method=='POST':
        id=request.POST['int_id']
        data=InterviewDetails.objects.get(id=id)
        data.status=request.POST['int_status']
        data.save()
        msg="Updated Succesfully"
        return render(request,'Hr/UpdateInterview.html',{'tab_selection':tab_selection,'id':id,'msg':msg})

    id=request.GET['id']
    return render(request,'Hr/UpdateInterview.html',{'tab_selection':tab_selection,'id':id})



def ChangePassword(request):
    tab_selection="Change Password"
    if request.method=='POST':

        old_passwd=request.POST['old_passwd']
        new_passwd=request.POST['new_passwd']
        con_passwd=request.POST['con_passwd']

        hr_data=HrDetails.objects.get(hr_id=request.session['hr_id'])
        is_true=pbkdf2_sha256.verify(old_passwd,hr_data.hr_passwd)
        if is_true:
            if len(new_passwd)>8:
                if new_passwd==con_passwd:
                    new_encrypted_passwd=pbkdf2_sha256.hash(new_passwd,rounds=1000,salt_size=32)
                    hr_data.hr_passwd=new_encrypted_passwd
                    hr_data.save()
                    success_msg="Password Changed Succesfully"
                    return render(request,'Hr/ChangePassword.html',{'success_msg':success_msg,'tab_selection':tab_selection,})
                else:
                    error_msg="Password Mismatch"
                    return render(request,'Hr/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})
            else:
                error_msg="Password Should be atleast 8 characters"
                return render(request,'Hr/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})
        else:
            error_msg="Invalid Password! enter Your correct password"
            return render(request,'Hr/ChangePassword.html',{'error_msg':error_msg,'tab_selection':tab_selection,})

    return render(request,'Hr/ChangePassword.html',{'tab_selection':tab_selection,})
