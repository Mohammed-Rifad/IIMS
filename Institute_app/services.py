from random import randint
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime,timedelta
import os
from django.db.models.query_utils import Q
from django.forms.widgets import NullBooleanSelect
from .models import FeeDetails, ModuleDetails, NotesDetails, SeatingDetails, StudentDetails, StudentModule,TrainerDetails

def GetUniqueID(user):
    if user == 'trainer':
        id = randint(10000,99999)
        exist=TrainerDetails.objects.filter(tr_id=id).exists()
        if exist:
            GetUniqueID('trainer')
        
    
    if user == 'student':
        id = randint(1000,9999)
        exist=StudentDetails.objects.filter(s_id=id).exists()
        if exist:
            GetUniqueID('student')
    return id


def email_service(mail_recipient,user_name,passwd):
    subject="username and password"
    message="Hi your username is "+str(user_name)+" and temporary password is "+str(passwd)
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)
    
def InsertFeeDetails(s_id,j_date,ins_arr):
    
    no=1
    dt=j_date
    # j_date=j_date.strftime("%d/%m/%Y")
    s_id=StudentDetails.objects.get(s_id=s_id)
    for i in range(3):
        due_amt=ins_arr[i]
        if i==0:
            due_date=dt+timedelta(days=7)
            print(due_date)
            date_convrt=due_date.strftime("%d/%m/%Y")
            fee_detail=FeeDetails(s_id=s_id,due_date=date_convrt,ins_no=no,due_amt=due_amt)
            due_date=due_date+timedelta(days=30)
            no+=1
            
            fee_detail.save()
        else:
            date_convrt=due_date.strftime("%d/%m/%Y")
            fee_detail=FeeDetails(s_id=s_id,due_date=date_convrt,ins_no=no,due_amt=due_amt)
            due_date=due_date+timedelta(days=30)
            fee_detail.save()
            no+=1
            print('iii')
         

def checkSystemAvailability(seating_data,slot_selected,student_id):
    already_allocated=SeatingDetails.objects.filter(Q(slot_s1=student_id)|Q(slot_s2=student_id)|Q(slot_s3=student_id))
    if not already_allocated:
        if slot_selected=="slot1":
            if seating_data.slot1=="free":
                seating_data.slot1=student_id.s_name+" ("+student_id.c_id.c_name+")"
                seating_data.slot_s1=student_id
                seating_data.save()
                return "Seat Allocated Succesfully"
            else:
                return "Selected System Not free"
        if slot_selected=="slot2":
            if seating_data.slot2=="free":
                seating_data.slot2=student_id.s_name+" ("+student_id.c_id.c_name+")"
                seating_data.slot_s2=student_id 
                seating_data.save()
                return "Seat Allocated Succesfully"
            else:
                return "Selected System Not free"
        
        if slot_selected=="slot3":
            if seating_data.slot3=="free":
                seating_data.slot3=student_id.s_name+" ("+student_id.c_id.c_name+")"
                seating_data.slot_s3=student_id
                seating_data.save()
                return "Seat Allocated Succesfully"
            else:
                return "Selected System Not free"
    else:
        return "Seat Already Allocated For "+student_id.s_name.title()


def UpdateSeat(seating_data,student,selected_slot):
    current_seating=SeatingDetails.objects.get(Q(slot_s1=student.s_id)|Q(slot_s2=student.s_id)|Q(slot_s3=student.s_id))
    
    print('current seating',current_seating)
    if current_seating.slot_s1==student:
        print('slot1')
        cur_slot="slot1"
    if current_seating.slot_s2==student:
        print('slot2')
        cur_slot="slot2"
    if current_seating.slot_s3==student:
        print('slot3')
        cur_slot="slot3"
    if selected_slot=="slot1":
        if seating_data.slot1=="free":
            print('first one')
            seating_data.slot1=student.s_name+" ("+student.c_id.c_name+")"
            seating_data.slot_s1=student
            seating_data.save()
            if cur_slot=="slot1":
                current_seating.slot1="free"
                current_seating.slot_s1=None    
                
            elif cur_slot=="slot2":
                current_seating.slot2="free"
                current_seating.slot_s2=None    
            else:
                current_seating.slot3="free"
                current_seating.slot_s3=None  
            current_seating.save()  
            return "Seat Updated Succesfully"
        else:
            return "Seleted System Not Free"
    if selected_slot=="slot2":
        
        if seating_data.slot2=="free":
                print('second one')
                try:
                    seating_data.slot2=student.s_name+" ("+student.c_id.c_name+")"
                    print('name added')
                    seating_data.slot_s2=student
                    print('id added')
                    seating_data.save()
                except print(0):
                    print('error')
                current_seating.slot2="free"
                if cur_slot=="slot1":
                    current_seating.slot1="free"
                    current_seating.slot_s1=None    
                
                elif cur_slot=="slot2":
                    current_seating.slot2="free"
                    current_seating.slot_s2=None    
                else:
                    current_seating.slot3="free"
                    current_seating.slot_s3=None  
                current_seating.save()  
                return "Seat Updated Succesfully"
        else:
            return "Seleted System Not Free"
    if selected_slot=="slot3":
        print('third one')
        if seating_data.slot3=="free":
                seating_data.slot3=student.s_name+" ("+student.c_id.c_name+")"
                seating_data.slot_s3=student
                seating_data.save()
                if cur_slot=="slot1":
                    current_seating.slot1="free"
                    current_seating.slot_s1=None    
                
                elif cur_slot=="slot2":
                    current_seating.slot2="free"
                    current_seating.slot_s2=None    
                else:
                    current_seating.slot3="free"
                    current_seating.slot_s3=None  
                
                current_seating.save()
                return "Seat Updated Succesfully"
        else:
            return "Seleted System Not Free"

def getFileName(m_name):
    path="Notes/"
    id = randint(10000,99999)
    module=ModuleDetails.objects.get(m_name=m_name)
    file_name=module.m_name+str(id)
    exist=NotesDetails.objects.filter(uploaded_file=file_name).exists()

    if exist:
        getFileName(module.m_name)
     
    return os.path.join(path,file_name)
    

def AddStudentModule(st_id,c_id):
    module_details=ModuleDetails.objects.filter(c_id=c_id)
    st_id=StudentDetails.objects.get(s_id=st_id)
    print('yes')
    for module in module_details:
        mod=ModuleDetails.objects.get(m_id=module.m_id)
        print('here')
        data=StudentModule(m_id=mod,s_id=st_id)
        data.save()