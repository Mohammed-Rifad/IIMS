

from Institute_app.Views.auth_gaurd import auth_admin
from Institute_app.models import CertFiles, ExamDetails, AttendanceDetails, CertificateDetails, CourseDetails, FeeDetails, FollowUpData, FollowupStatus, HrDetails, InterviewDetails, ModuleDetails, NotesDetails, PlacementDetails, SeatingDetails, StudentDetails, StudentModule, SystemDetails, TrainerDetails
from django.db import models
from django.shortcuts import render,redirect
from datetime import date, datetime, time, timedelta
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import GetUniqueID, checkSystemAvailability, email_service
from Institute_app.Forms.AdminForms import CourseForm, HrForm, ModuleForm, SystemForm, TrainerForm,FollowupForm

@auth_admin
def AdminHome(request):
    
    data=FeeDetails.objects.filter(status='not paid')
    std_count=StudentDetails.objects.filter(status='active').count()
    cert_count=CertificateDetails.objects.filter(status='pending').count()
    trainer_count=TrainerDetails.objects.filter(tr_status='active').count()
    system_count=SystemDetails.objects.all().count()
    recent_exams=ExamDetails.objects.filter(status='pending').count()
    
    total=0
    
    for i in data:
        dt=i.due_date
        
        d=datetime.strptime(dt,'%d/%m/%Y')
        dd=datetime.now()+timedelta(days=7)
        if d<=dd:
            total+=i.due_amt
            
    return render(request,'Admin/AdminHome.html',{'total':total,'std_count':std_count,'cert_count':cert_count,'trainer_count':trainer_count,'system_count':system_count,
    'recent_exams':recent_exams})


@auth_admin
def AddModule(request):
    courses=CourseDetails.objects.all()
    form=ModuleForm()
    print(courses)
    if request.method=='POST':
      
        form=ModuleForm(request.POST)
        if form.is_valid():
            c_id=CourseDetails.objects.get(c_id=request.POST['course'])
            m_name=form.cleaned_data['m_name'].lower()
           

            module_exist=ModuleDetails.objects.filter(m_name=m_name,c_id=c_id).exists()
            if not module_exist:
              
                module=ModuleDetails(m_name=m_name,c_id=c_id)
                module.save()
                success_msg="Module Added Succesfully"
                return render(request,'Admin/AddModule.html',{'form':form,'success_msg':success_msg,'courses':courses})
            else:
                error_msg="Module Already Added For The Course"
                return render(request,'Admin/AddModule.html',{'form':form,'error_msg':error_msg,'courses':courses})
    return render(request,'Admin/AddModule.html',{'form':form,'courses':courses})



@auth_admin
def AddCourse(request):
   
    form=CourseForm()
    if request.method=='POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            c_name=form.cleaned_data['c_name'].lower()
            c_duration=form.cleaned_data['c_duration']
            c_fee=form.cleaned_data['c_fee']

            course_exist=CourseDetails.objects.filter(c_name=c_name).exists()
            if not course_exist:
                course=CourseDetails(c_name=c_name,c_duration=c_duration,c_fee=c_fee)
                course.save()
                success_msg="Course Added Succesfully"
                form=CourseForm()
                return render(request,'Admin/AddCourse.html',{'form':form,'success_msg':success_msg})
            else:
                error_msg="Course Already Added"
                return render(request,'Admin/AddCourse.html',{'form':form,'error_msg':error_msg})
    return render(request,'Admin/AddCourse.html',{'form':form,})


@auth_admin
def AddSystem(request):
       
    form=SystemForm()
    if request.method=='POST':
        form=SystemForm(request.POST)
        if form.is_valid():
            sys_no=form.cleaned_data['sys_no'].lower()
            lab_no=form.cleaned_data['lab_no']
           

            system_exist=SystemDetails.objects.filter(lab_no=lab_no,sys_no=sys_no).exists()
            if not system_exist:
                system=SystemDetails(lab_no=lab_no,sys_no=sys_no)
                system.save()
                

                seating=SeatingDetails(sys_no=sys_no,lab_no=lab_no)
                seating.save()
                
                success_msg="System Added Succesfully"
                return render(request,'Admin/AddSystem.html',{'form':form,'success_msg':success_msg})
            else:
                error_msg="System Already Added For Selected Lab"
                return render(request,'Admin/AddSystem.html',{'form':form,'error_msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddSystem.html',{'form':form,})


@auth_admin
def ViewSeating(request):
    seating_details=""
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'Admin/ViewSeating.html',{'seating_details':seating_details})



@auth_admin
def AddHr(request):
    
    
    if request.method=='POST':
        
        
        hr_name=request.POST['hr_name'].lower()
        hr_dob=request.POST['hr_dob']
        hr_qual=request.POST['hr_qual']
        hr_gender=request.POST['hr_gender']   
        hr_address=request.POST['hr_add']
        hr_phno=request.POST['hr_phno']
        hr_email=request.POST['hr_email']
        hr_pic=request.FILES['hr_pic']  
        join_date=date.today()
        dt_covrt=join_date.strftime("%d/%m/%Y") 
        dob_convrt=datetime.strptime(hr_dob,"%Y-%m-%d").date()
        dt_str=dob_convrt.strftime("%d/%m/%Y")     
        # passwd=pbkdf2_sha256.hash(hr_phno,rounds=1000,salt_size=32)
        passwd=get_random_string(length=8)
        passwd_enc=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
        data_exist=HrDetails.objects.filter(hr_email=hr_email,hr_status='active').exists()
        if not data_exist:
            hr_detail=HrDetails(hr_name=hr_name,hr_dob=dt_str,hr_qual=hr_qual,hr_gender=hr_gender,hr_email=hr_email,hr_address=hr_address,hr_phno=hr_phno,
            hr_pic=hr_pic,hr_join=dt_covrt,hr_passwd=passwd_enc)
            try:
                hr=HrDetails.objects.latest('hr_id')
                current_hr=HrDetails.objects.get(hr_id=hr.hr_id)
                current_hr.hr_status="disabled"
                
                current_hr.save()
            except Exception as e:
                print(e)
            hr_detail.save()
            email_service(hr_email,hr_email,passwd)
            success_msg="HR Added Succesfully"
            return render(request,'Admin/AddHr.html',{ 'success_msg':success_msg})
        else:
            error_msg="Email Already Exist"
            return render(request,'Admin/AddHr.html',{ 'error_msg':error_msg})
         
    return render(request,'Admin/AddHr.html')

def Logout(request):
     
    if 'admin_id' in request.session:
        del request.session['admin_id']
    request.session.flush()
    return redirect("institute_app:proj_home")

@auth_admin
def AddTrainer(request):
    courses=CourseDetails.objects.all()   
    
    if request.method=='POST':
       
        tr_name=request.POST['tr_name'].lower()
        tr_dob=request.POST['tr_dob']
        tr_qual=request.POST['tr_qual']
        tr_gender=request.POST['tr_gender']   
        tr_address=request.POST['tr_add']
        tr_phno=request.POST['tr_phno']
        tr_email=request.POST['tr_email']
        tr_pic=request.FILES['tr_pic']  
        # log_permission=form.cleaned_data['log_permission']
        join_date=date.today()
        tr_id=GetUniqueID('trainer')
        tr_course=CourseDetails.objects.get(c_id=request.POST['course'])
        dt_covrt=join_date.strftime("%d/%m/%Y")    
        passwd=get_random_string(length=8)  
        passwd_enc=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
        
        dob_convrt=datetime.strptime(tr_dob,"%Y-%m-%d").date()
        dt_str=dob_convrt.strftime("%d/%m/%Y")   
        data_exist=TrainerDetails.objects.filter(tr_email=tr_email,tr_status='active').exists()
        if not data_exist:
             
            trainer=TrainerDetails(tr_id=tr_id,tr_name=tr_name,tr_dob=dt_str,tr_course=tr_course,tr_qual=tr_qual,tr_gender=tr_gender,tr_email=tr_email,tr_address=tr_address,tr_phno=tr_phno,
            tr_pic=tr_pic,tr_join=dt_covrt,tr_passwd=passwd_enc)
            trainer.save()
            email_service(tr_email,tr_id,passwd)
            success_msg="Trainer Added Succesfully"
            return render(request,'Admin/AddTrainer.html',{ 'success_msg':success_msg,'courses':courses})
        else:
            error_msg="Email Exist"
            return render(request,'Admin/AddTrainer.html',{ 'error_msg':error_msg,'courses':courses})
       
    return render(request,'Admin/AddTrainer.html',{ 'courses':courses})


@auth_admin
def AddFollowUp(request):
    msg=""
    form=FollowupForm()
    if request.method=='POST':
        form=FollowupForm(request.POST)
        if form.is_valid():
            s_name=form.cleaned_data['s_name'].lower()
            s_colg=form.cleaned_data['s_colg'].lower()
            s_dob=form.cleaned_data['s_dob']
            s_qual=form.cleaned_data['s_qual']
            s_gender=form.cleaned_data['s_gender']
            s_phno=form.cleaned_data['s_phno']
            s_email=form.cleaned_data['s_email']
            s_passout=form.cleaned_data['s_passout']
            entered_date=date.today()
            dt_covrt=entered_date.strftime("%d/%m/%Y")    
            data_exist=FollowUpData.objects.filter(s_email=s_email).exists()
            if not data_exist:
                data=FollowUpData(s_name=s_name,s_colg=s_colg,s_dob=s_dob,s_qual=s_qual,s_gender=s_gender,
                s_phno=s_phno,s_email=s_email,s_passout=s_passout,date_entered=dt_covrt)
                data.save()
                success_msg="Data Entered Succesfully"
                return render(request,'Admin/AddFollowUp.html',{'form':form,'success_msg':success_msg})
            else:
                error_msg="Data Already Entered"
                return render(request,'Admin/AddFollowUp.html',{'form':form,'error_msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddFollowUp.html',{'form':form,})

@auth_admin
def ActiveFollowUp(request):
    followup_data=FollowUpData.objects.filter(status="active")
    return render(request,'Admin/ActiveFollowUp.html',{'followup_data':followup_data,})

@auth_admin
def FollowUpHistory(request,f_id):
    data=FollowupStatus.objects.filter(f_id=f_id)
    if request.method=='POST':
        id=request.POST['id']
        hst_data=FollowupStatus(id=id)
        hst_data.delete()
    return render(request,'Admin/FollowUpHistory.html',{'data':data})

@auth_admin
def ViewActiveStudents(request):
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'Admin/ActiveStudents.html',{'students':students,'courses':courses})



@auth_admin
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
    return render(request,'Admin/ViewTrainerAttendance.html',{'trainers':trainers,'attendance_data':attendance_data,'trainer_name':trainer_name})

@auth_admin
def ViewStudentStatus(request):
    if request.method=='POST':
        s_id=request.POST['s_id']
        student=StudentDetails.objects.get(s_id=s_id)
        data=StudentModule.objects.filter(s_id=s_id)
        return render(request,'Admin/StudentStatus.html',{'modules':data,'name':student.s_name})
    
    return render(request,'Admin/StudentStatus.html',)

@auth_admin    
def CompletedStudents(request):
    students=StudentDetails.objects.filter(status="course completed")
    courses=CourseDetails.objects.all()
    tab_selection="Completed Students"
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="course completed")
    return render(request,'Admin/CompletedStudents.html',{'students':students,'courses':courses,'tab_selection':tab_selection})


@auth_admin
def ViewInterview(request):
    data=InterviewDetails.objects.all()
     
    return render(request,'Admin/ViewInter.html',{'data':data,})


@auth_admin
def DueList(request):
    std_array=[]
    data=FeeDetails.objects.filter(status='not paid')
    print(data)
    total=0
    ss=0
    for i in data:
        dt=i.due_date
        
        d=datetime.strptime(dt,'%d/%m/%Y')
        dd=datetime.now()+timedelta(days=7)
        if d<=dd:
            total+=i.due_amt
            std_array.append(i)
        print(d)
        print('array',std_array)
    return render(request,'Admin/DueList.html',{'data':std_array,'total':total})

@auth_admin
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
    return render(request,'Admin/ViewTrainerAttendance.html',{'trainers':trainers,'attendance_data':attendance_data,'trainer_name':trainer_name})

@auth_admin
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
    return render(request,'Admin/ViewStudentAttendance.html',{'students':students,'attendance_data':attendance_data,'student_name':student_name})

@auth_admin
def CertPending(request):
    data=CertificateDetails.objects.filter(status="pending")
    
    return render(request,'Admin/CertificateStatus.html',{'data':data,})

@auth_admin
def UploadCert(request):
    s_id=request.GET['s_id']
    success_msg=""
    error_msg=""
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['s_id'])
        cert_title=request.POST['cert_title']
        cert_file=request.FILES['cert_file']
        already_added=CertFiles.objects.filter(s_id=s_id,cert_title=cert_title).exists()
        if not already_added:
            certificate=CertFiles(s_id=student,cert_title=cert_title,cert=cert_file)
            certificate.save()
            success_msg="Certificate Uploaded Succesfully"
            return render(request,'Admin/UploadCert.html',{'s_id':s_id,'success_msg':success_msg})

        else:
            error_msg="Certificate Already Added"
            return render(request,'Admin/UploadCert.html',{'s_id':s_id,'error_msg':error_msg})

    return render(request,'Admin/UploadCert.html',{'s_id':s_id,})

@auth_admin
def CertUpdate(request):
    
    s_id=request.GET['s_id']
    if request.method=='POST':
        rec_date=request.POST['rec_date']
        dt_convrt=datetime.strptime(rec_date,"%Y-%m-%d").date()
        dt_str=dt_convrt.strftime("%d/%m/%Y")
        
        cert_data=CertificateDetails.objects.get(s_id=request.POST['s_id'])
        cert_data.rec_date=dt_str
        cert_data.status="received"
        cert_data.save()
        msg="Status Updated Succesfully"
        return render(request,'Admin/CertUpdate.html',{'s_id':s_id,'msg':msg})
        
    
    return render(request,'Admin/CertUpdate.html',{'s_id':s_id,})

@auth_admin
def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    if request.method=='POST':
        
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Admin/ViewNotes.html',{'modules':modules,'notes':notes,})

@auth_admin
def StudentExam(request):
    exams=ExamDetails.objects.filter(status='pending')
    return render(request,'Admin/Exams.html',{'exams':exams,})

@auth_admin
def ViewProfile(request):
    print('yes')
    if request.method=='GET':
        return redirect("institute_app:admin_active_students")
    id=request.POST['id']
    data=StudentDetails.objects.get(s_id=id)
    tot_modules=StudentModule.objects.filter(s_id=id).count()
    mod_completed=StudentModule.objects.filter(s_id=id,status='completed').count()
    payment_data=FeeDetails.objects.filter(s_id=id)
    std_exam=ExamDetails.objects.filter(s_id=id)
    
    perc=""
    try:
        perc=(mod_completed/tot_modules) *100
        print(perc)
    except:
        perc=0
    
    return render(request,'Admin/StudentProfile.html',{'data':data,'perc':perc,'payment_data':payment_data,'exams':std_exam,})


@auth_admin
def ViewCompProfile(request):
     
    if request.method=='GET':
        return redirect("institute_app:admin_comp")
    id=request.POST['id']
    placement_detail=""
    data=StudentDetails.objects.get(s_id=id)
    try:
        placement_detail=PlacementDetails.objects.get(s_id=id)
    except:
        None
    tot_modules=StudentModule.objects.filter(s_id=id).count()
    mod_completed=StudentModule.objects.filter(s_id=id,status='completed').count()
    payment_data=FeeDetails.objects.filter(s_id=id)
    std_exam=ExamDetails.objects.filter(s_id=id)
    perc=""
    try:
        perc=(mod_completed/tot_modules) *100
        print(perc)
    except:
        perc=0
    
    return render(request,'Admin/CompStudentProfile.html',{'data':data,'perc':perc,'payment_data':payment_data,'exams':std_exam,'placement_detail':placement_detail})
