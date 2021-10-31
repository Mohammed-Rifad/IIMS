

from Institute_app.models import AttendanceDetails, CourseDetails, FollowUpData, FollowupStatus, HrDetails, ModuleDetails, SeatingDetails, StudentDetails, SystemDetails, TrainerDetails
from django.db import models
from django.shortcuts import render,redirect
from datetime import date, datetime, time
from passlib.hash import pbkdf2_sha256
from django.utils.crypto import get_random_string
from ..services import GetUniqueID, checkSystemAvailability, email_service
from Institute_app.Forms.AdminForms import CourseForm, HrForm, ModuleForm, SystemForm, TrainerForm,FollowupForm

def AdminHome(request):
    return render(request,'Admin/AdminHome.html')


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
                return render(request,'Admin/AddModule.html',{'form':form,'msg':success_msg,'courses':courses})
            else:
                error_msg="Module Already Added For The Course"
                return render(request,'Admin/AddModule.html',{'form':form,'msg':error_msg,'courses':courses})
    return render(request,'Admin/AddModule.html',{'form':form,'courses':courses})



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
                return render(request,'Admin/AddCourse.html',{'form':form,'msg':success_msg})
            else:
                error_msg="Course Already Added"
                return render(request,'Admin/AddCourse.html',{'form':form,'msg':error_msg})
    return render(request,'Admin/AddCourse.html',{'form':form,})


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
                
                success_msg="System Allocated Succesfully"
                return render(request,'Admin/AddSystem.html',{'form':form,'msg':success_msg})
            else:
                error_msg="System Already Added For Selected Lab"
                return render(request,'Admin/AddSystem.html',{'form':form,'msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddSystem.html',{'form':form,})


def ViewSeating(request):
    seating_details=""
    if request.method=='POST':
        lab_no=request.POST['lab']
        seating_details=SeatingDetails.objects.filter(lab_no=lab_no)
    return render(request,'Admin/ViewSeating.html',{'seating_details':seating_details})



def AddHr(request):
    
    form=HrForm()
    if request.method=='POST':
        form=HrForm(request.POST,request.FILES)
        if form.is_valid():
            hr_name=form.cleaned_data['hr_name'].lower()
            hr_dob=form.cleaned_data['hr_dob']
            hr_qual=form.cleaned_data['hr_qual']
            hr_gender=form.cleaned_data['hr_gender']   
            hr_address=form.cleaned_data['hr_address']
            hr_phno=form.cleaned_data['hr_phno']
            hr_email=form.cleaned_data['hr_email']
            hr_pic=form.cleaned_data['hr_pic']  
            join_date=date.today()
            dt_covrt=join_date.strftime("%d/%m/%Y")      
            passwd=pbkdf2_sha256.hash(hr_phno,rounds=1000,salt_size=32)
            data_exist=HrDetails.objects.filter(hr_email=hr_email,hr_status='active').exists()
            if not data_exist:
                hr_detail=HrDetails(hr_name=hr_name,hr_dob=hr_dob,hr_qual=hr_qual,hr_gender=hr_gender,hr_email=hr_email,hr_address=hr_address,hr_phno=hr_phno,
                hr_pic=hr_pic,hr_join=dt_covrt,hr_passwd=passwd)
                try:
                    hr=HrDetails.objects.latest('hr_id')
                    current_hr=HrDetails.objects.get(hr_id=hr.hr_id)
                    current_hr.hr_status="disabled"
                    
                    current_hr.save()
                except Exception as e:
                    print(e)
                hr_detail.save()
                
                success_msg="HR Added Succesfully"
                return render(request,'Admin/AddHr.html',{'form':form,'msg':success_msg})
            else:
                error_msg="Email Exist"
                return render(request,'Admin/AddHr.html',{'form':form,'msg':error_msg})
        else:
            print(form.errors)
    return render(request,'Admin/AddHr.html',{'form':form,})


def AddTrainer(request):
    courses=CourseDetails.objects.all()   
    form=TrainerForm()
    if request.method=='POST':
        form=TrainerForm(request.POST,request.FILES)
        if form.is_valid():
            tr_name=form.cleaned_data['tr_name'].lower()
            tr_dob=form.cleaned_data['tr_dob']
            tr_qual=form.cleaned_data['tr_qual']
            tr_gender=form.cleaned_data['tr_gender']   
            tr_address=form.cleaned_data['tr_address']
            tr_phno=form.cleaned_data['tr_phno']
            tr_email=form.cleaned_data['tr_email']
            tr_pic=form.cleaned_data['tr_pic']  
            log_permission=form.cleaned_data['log_permission']
            join_date=date.today()
            tr_id=GetUniqueID('trainer')
            tr_course=CourseDetails.objects.get(c_id=request.POST['course'])
            dt_covrt=join_date.strftime("%d/%m/%Y")    
            passwd=get_random_string(length=8)  
            passwd_enc=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            print(tr_id,passwd,'0000')
            data_exist=TrainerDetails.objects.filter(tr_email=tr_email,tr_status='active').exists()
            if not data_exist:
                if log_permission ==0:
                    passwd=""
                else:
                    pass
                    #email_service(tr_email,tr_id,tr_phno)
                trainer=TrainerDetails(tr_id=tr_id,tr_name=tr_name,tr_dob=tr_dob,tr_course=tr_course,tr_qual=tr_qual,tr_gender=tr_gender,tr_email=tr_email,tr_address=tr_address,tr_phno=tr_phno,
                tr_pic=tr_pic,tr_join=dt_covrt,tr_passwd=passwd_enc,log_permission=log_permission)
                trainer.save()
                #email_service(tr_email,tr_id,tr_phno)
                success_msg="Trainer Added Succesfully"
                return render(request,'Admin/AddTrainer.html',{'form':form,'msg':success_msg,'courses':courses})
            else:
                error_msg="Email Exist"
                return render(request,'Admin/AddTrainer.html',{'form':form,'msg':error_msg,'courses':courses})
        else:
            print(form.errors)
    return render(request,'Admin/AddTrainer.html',{'form':form,'courses':courses})


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

def ActiveFollowUp(request):
    followup_data=FollowUpData.objects.filter(status="active")
    return render(request,'Admin/ActiveFollowUp.html',{'followup_data':followup_data,})

def FollowUpHistory(request,f_id):
    data=FollowupStatus.objects.filter(f_id=f_id)
    if request.method=='POST':
        id=request.POST['id']
        hst_data=FollowupStatus(id=id)
        hst_data.delete()
    return render(request,'Admin/FollowUpHistory.html',{'data':data})

def ViewActiveStudents(request):
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'Admin/ActiveStudents.html',{'students':students,'courses':courses})

def UpdatePermission(request):
    msg=""
    trainers=TrainerDetails.objects.filter(tr_status="active")
    if request.method=='POST':
        trainer=TrainerDetails.objects.get(tr_id=request.POST['trainer'])
        
        permission_type=request.POST['permission_type']
        if permission_type=='grand':
            trainer.log_permission=1
            if trainer.tr_passwd=="":
                passwd=get_random_string(8)
                enc_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
                trainer.tr_passwd=enc_passwd
                print('passwd',passwd,'id',trainer.tr_id)
                #email_service(trainer.tr_email,trainer.tr_id,passwd)
                
        else:
            trainer.log_permission=0
            
        msg="Permission Updated Succesfully"
        trainer.save()
    return render(request,'Admin/SetPermission.html',{'trainers':trainers,'msg':msg})


def ViewTrainerAttendance(request):
    attendance_data=""
    print('*********************')
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
