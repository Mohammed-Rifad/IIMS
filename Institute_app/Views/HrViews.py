
from datetime import date, timedelta
from django.core.mail import send_mail
from django.db.models.query_utils import check_rel_lookup_compatibility
from datetime import date, datetime, time
from django.http.request import split_domain_port
from Institute_app.models import AttendanceDetails, CertificateDetails, CourseDetails, FeeDetails, FollowUpData, FollowupStatus, InterviewDetails, SeatingDetails, StudentDetails, StudentModule,SystemDetails, TrainerDetails
from Institute_app.Forms.HrForms import InterviewForm, StudentForm
from django.shortcuts import render,redirect
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import AddStudentModule, GetUniqueID, InsertFeeDetails, email_service,checkSystemAvailability

def HrHome(request):
    return render(request,'HR/HrHome.html')


def AddStudent(request):
    form=StudentForm()
    msg=""
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
        return render(request,'HR/AddStudent.html',{'form':form,'courses':courses,'msg':msg}) 
    return render(request,'HR/AddStudent.html',{'form':form,'courses':courses})

# ajax
def getSystem(request):
    lab_no=request.GET['lab_no']
    systems=SystemDetails.objects.filter(lab_no=lab_no)
    return render(request,'Hr/system_dropdown.html',{'systems':systems})


def AssignSeating(request):
    status=""
    students=StudentDetails.objects.filter(status="active",s_type="offline")
    if request.method=='POST':

        
        sys_no=request.POST['system']
        lab=request.POST['lab']
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        selected_slot=request.POST['slot']

        seating_data=SeatingDetails.objects.get(sys_no=sys_no,lab_no=lab)

        status=checkSystemAvailability(seating_data,selected_slot,student)
        
    return render(request,'HR/AssignSeating.html',{'students':students,'status':status})


def ViewSeating(request):
    seating_details=""
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'HR/ViewSeating.html',{'seating_details':seating_details})


def ActiveFollowUp(request):
    followup_data=FollowUpData.objects.filter(status="active")
    return render(request,'HR/ActiveFollowUp.html',{'followup_data':followup_data,})

def AddFollowUp(request,id):

    if request.method=='POST':
        id=FollowUpData.objects.get(f_id=id)
        cur_date=date.today()
        dt_covrt=cur_date.strftime("%d/%m/%Y") 
        status=request.POST['status']   

    
        data=FollowupStatus(f_id=id,date=dt_covrt,status=status)
        data.save()
        
        return redirect("institute_app:hr_act_followup")
       
    return render(request,'HR/FollowUp.html',{'id':id})

def FollowUpHistory(request,f_id):
    data=FollowupStatus.objects.filter(f_id=f_id)
    if request.method=='POST':
        id=request.POST['id']
        hst_data=FollowupStatus(id=id)
        hst_data.delete()
    return render(request,'HR/FollowUpHistory.html',{'data':data})

def ViewActiveStudents(request):
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'HR/ActiveStudents.html',{'students':students,'courses':courses})

def TrainerAttendance(request):
    trainers=TrainerDetails.objects.filter(tr_status="active")
    if request.method=='POST':
        trainer=TrainerDetails.objects.get(tr_id=request.POST['trainer'])
        dt=request.POST['date']
        status=request.POST['status']
        mnth=date.today().month
        yr =date.today().year
        dt_convrt=datetime.strptime(dt,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        print(mnth,yr,dt_convrt,dt_str)

        already_added=AttendanceDetails.objects.filter(tr_id=trainer,date=dt_str).exists()
        if not already_added:
            attendance=AttendanceDetails(type="trainer",tr_id=trainer,date=dt_str,status=status,mnth=mnth,yr=yr)
            attendance.save()
            success_msg="Attendance Added Succesfully"
            return render(request,'HR/TrainerAttendance.html',{'trainers':trainers,'success_msg':success_msg})
    return render(request,'HR/TrainerAttendance.html',{'trainers':trainers})


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
    for i in data:
        dt=i.due_date
       
        d=datetime.strptime(dt,'%d/%m/%Y')
        dd=datetime.now()+timedelta(days=7)
        if d<=dd:
            std_array.append(i)
        print(d)
        print('array',std_array)
    return render(request,'HR/DueList.html',{'data':std_array})

def AddPayment(request):
    if request.method=='GET':
        request.session['p_id']=request.GET['id']
        st=request.GET['st']
    if request.method=='POST':
        payment_data=FeeDetails.objects.get(id=request.session['p_id'])
        
        payment_data.paid_amt=request.POST['p_amt']
        payment_data.paid_date=request.POST['p_date']
        payment_data.pay_type="offline"
        payment_data.status="paid"
        payment_data.save()
        return redirect("institute_app:hr_due_list")
    
    return render(request,'HR/OfflinePayment.html',{'st':st})



def StudentStatus(request):
    id=request.GET['id']
    student_data=StudentModule.objects.filter(s_id=id)
    return render(request,'HR/StudentStatus.html',{'student_data':student_data})

def PaymentStatus(request):
    id=request.GET['id']
    payment_data=FeeDetails.objects.filter(s_id=id)
    return render(request,'HR/PaymentStatus.html',{'payment_data':payment_data})

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
    return render(request,'Hr/ViewStudentAttendance.html',{'students':students,'attendance_data':attendance_data,'student_name':student_name})

def RequestCertificate(request):
    students=StudentDetails.objects.filter(status="active")
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
            return render(request,'Hr/RequestCertificate.html',{'students':students,'error_msg':error_msg,})

    return render(request,'Hr/RequestCertificate.html',{'students':students,})


def CertStatus(request):
    data=CertificateDetails.objects.all()
    if request.method=='POST':
        rec_date=request.POST['rec_date']
        dt_convrt=datetime.strptime(rec_date,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        
        cert_data=CertificateDetails.objects.get(s_id=request.POST['s_id'])
        cert_data.rec_date=dt_str
        cert_data.status="received"
        cert_data.save()
    
    return render(request,'Hr/CertificateStatus.html',{'data':data,})

def CompletedStudents(request):
    students=StudentDetails.objects.filter(status="completed")
    courses=CourseDetails.objects.all()
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="completed")
    return render(request,'Hr/CompletedStudents.html',{'students':students,'courses':courses})

def AddInterView(request):
    form=InterviewForm()
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'HR/AddInterview.html',{'students':students,'courses':courses,'form':form})

    
def SchedhuleInterview(request) :
    id=request.GET['id']
    msg=""
    form=InterviewForm()
    if request.method=='POST':

        form=InterviewForm(request.POST)
        if form.is_valid():
            cmp_name=form.cleaned_data['cmp_name'].lower()
            cmp_addr=form.cleaned_data['cmp_addr'].lower()
            cmp_contact=form.cleaned_data['cmp_contact']
            int_post=form.cleaned_data['int_post'].lower()
            interview_date=form.cleaned_data['interview_date']
            int_type=form.cleaned_data['int_type']
            student=StudentDetails.objects.get(s_id=id)
            dt=date.today()
            added_date=dt.strftime("%d/%m/%Y")
            interview=InterviewDetails(cmp_name=cmp_name,cmp_addr=cmp_addr,cmp_contact=cmp_contact,
            interview_date=interview_date,int_type=int_type,s_id=student,added_date=added_date,int_post=int_post)
            interview.save()
            msg="Data Submitted Succesfully"
    return render(request,'HR/SchedhuleInterview.html',{'form':form,'id':id,'msg':msg})


def ViewInterview(request):
    data=InterviewDetails.objects.all()
    return render(request,'Hr/ViewInter.html',{'data':data,})

def DelInterview(request):
    id=request.GET['id']
    data=InterviewDetails.objects.get(id=id)
    data.delete()
    return redirect("institute_app:hr_view_inter")