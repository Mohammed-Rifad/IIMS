from django.db import models
from django.db.models.base import ModelState
from django.db.models.fields import CharField
from django.forms.models import model_to_dict
from passlib.hash import pbkdf2_sha256
# Create your models here.


class AdminDetails(models.Model):
    login_id=models.CharField(max_length=20,db_column="log_id")
    login_passwd=models.CharField(max_length=120,db_column='passwd')

    class Meta:
        db_table="tb_super"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.login_passwd)
class CourseDetails(models.Model):
    c_id=models.AutoField(primary_key=True,db_column="c_id")
    c_name=models.CharField(max_length=20,db_column="c_name")
    c_duration=models.IntegerField(db_column="c_dur")
    c_fee=models.FloatField(db_column="c_fee")
   
    class Meta:
        db_table="tb_course"

class ModuleDetails(models.Model):
    m_id=models.AutoField(primary_key=True,db_column="m_id")
    c_id=models.ForeignKey(CourseDetails,on_delete=models.CASCADE,db_column="c_id")
    m_name=models.CharField(max_length=20,db_column="m_name")
    class Meta:
        db_table="tb_module"

class SystemDetails(models.Model):
    sys_id=models.AutoField(primary_key=True,db_column="s_id")
    lab_no=models.IntegerField(db_column="lab_no")
    sys_no=models.IntegerField(db_column="s_no")
    sys_status=models.CharField(max_length=20,default="available",db_column="s_status")
    class Meta:
        db_table="tb_system"

class HrDetails(models.Model):
    hr_id=models.AutoField(primary_key=True,db_column="hr_id")
    hr_name=models.CharField(max_length=30,db_column="hr_name")
    hr_dob=models.CharField(max_length=20,db_column="hr_dob")
    hr_qual=models.CharField(max_length=20,db_column="hr_qual",default="")
    hr_gender=models.CharField(max_length=10,db_column="hr_gender")
    hr_address=models.CharField(max_length=200,db_column="hr_add")
    hr_email=models.CharField(max_length=50,db_column="hr_email")
    hr_phno=models.CharField(max_length=10,db_column="hr_phno")
    hr_pic=models.ImageField(upload_to="HR/",db_column="hr_pic")
    hr_passwd=models.CharField(max_length=20,db_column="hr_passwd")
    hr_join=models.CharField(max_length=10,db_column="hr_join")
    hr_status=models.CharField(max_length=30,default="active",db_column="hr_status")
    class Meta:
        db_table="tb_hr"
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.hr_passwd)

class TrainerDetails(models.Model):
    tr_id=models.IntegerField(primary_key=True,db_column="tr_id")
    tr_course=models.ForeignKey(CourseDetails,null=True, on_delete=models.SET_NULL,db_column="tr_course")
    tr_name=models.CharField(max_length=30,db_column="tr_name")
    tr_dob=models.CharField(max_length=20,db_column="tr_dob")
    tr_qual=models.CharField(max_length=20,db_column="tr_qual",default="")
    tr_gender=models.CharField(max_length=10,db_column="tr_gender")
    tr_address=models.CharField(max_length=200,db_column="tr_add")
    tr_email=models.CharField(max_length=50,db_column="tr_email")
    tr_phno=models.CharField(max_length=10,db_column="tr_phno")
    tr_pic=models.ImageField(upload_to="Trainer/",db_column="tr_pic")
    tr_passwd=models.CharField(max_length=20,db_column="tr_passwd")
    tr_join=models.CharField(max_length=10,db_column="tr_join")
    log_permission=models.IntegerField(default=0,db_column="log_permission")
    tr_status=models.CharField(max_length=30,default="active",db_column="tr_status")
    class Meta:
        db_table="tb_trainer"
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.tr_passwd)

class StudentDetails(models.Model):
    s_id=models.IntegerField(primary_key=True,db_column="s_id")
    c_id=models.ForeignKey(CourseDetails,on_delete=models.CASCADE,db_column="c_id")
    s_name=models.CharField(max_length=30,db_column="s_name")
    s_type=models.CharField(max_length=10,default="offline",db_column="s_type")
    s_dob=models.CharField(max_length=10,db_column="s_dob")
    s_gender=models.CharField(max_length=10,db_column="s_gender")
    s_address=models.CharField(max_length=200,db_column="s_add")
    s_qual=models.CharField(max_length=30,db_column="s_qual")
    s_colg=models.CharField(max_length=50,db_column="s_colg")
    s_email=models.CharField(max_length=50,db_column="s_email")
    s_phno=models.CharField(max_length=10,db_column="s_phno")
    s_passout=models.IntegerField(db_column="s_passout")
    s_join=models.CharField(max_length=10,db_column="s_join")
    s_completed=models.CharField(max_length=10,default="",db_column="s_join")
    amt_payable=models.FloatField(db_column="amt_payable")
    s_passwd=models.CharField(max_length=20,db_column="s_passwd")
    # balance=models.FloatField(db_column="balance")
    s_completed=models.CharField(max_length=10,db_column="s_compl")
    s_pic=models.ImageField(upload_to="Student/",db_column="s_pic")
    cert_req=models.IntegerField(default=0,db_column="c_req")
    placed=models.IntegerField(default=0,db_column="placed")
    status=models.CharField(max_length=20,default="active",db_column="status")
    

    class Meta:
        db_table="tb_student"
    
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.s_passwd)
        
class StudentModule(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    m_id=models.ForeignKey(ModuleDetails,on_delete=models.CASCADE,db_column="m_id")
    status=models.CharField(max_length=30,default="pending",db_column="status")
    
    class Meta:
        db_table="tb_stmodule"


class SeatingDetails(models.Model):
    lab_no=models.IntegerField(db_column="lab_no")
    sys_no=models.IntegerField(db_column="s_no")
    slot1=models.CharField(max_length=30,default="free",db_column="s1")
    slot2=models.CharField(max_length=30,default="free",db_column="s2")
    slot3=models.CharField(max_length=30,default="free",db_column="s3")
    slot_s1=models.ForeignKey(StudentDetails,related_name="sys1", on_delete=models.SET_NULL,null=True,db_column="slot_s1")
    slot_s2=models.ForeignKey(StudentDetails,related_name="sys2",on_delete=models.SET_NULL,null=True,db_column="slot_s2")
    slot_s3=models.ForeignKey(StudentDetails,related_name="sys3",on_delete=models.SET_NULL,null=True,db_column="slot_s3")

    class Meta:
        db_table="tb_seating"

class FeeDetails(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    ins_no=models.CharField(max_length=20,db_column="ins_no")
    due_date=models.CharField(max_length=10,db_column="due_date")
    paid_date=models.CharField(max_length=10,db_column="paid_date")
    due_amt=models.FloatField(db_column="due_amt",default=0)
    paid_amt=models.FloatField(db_column="paid_amt",default=0)
    comment=models.CharField(max_length=50,db_column="comnt")
    # mnth=models.CharField(max_length=10,db_column="mnth")
    # yr=models.IntegerField(db_column="yr")
    pay_type=models.CharField(max_length=20,db_column="type",default="nil")
    status=models.CharField(max_length=20,db_column="status",default="not paid")

    class Meta:
        db_table="tb_fee"



class FollowUpData(models.Model):
    f_id=models.IntegerField(primary_key=True,db_column="s_id")
    s_name=models.CharField(max_length=30,db_column="s_name")
    s_dob=models.CharField(max_length=10,db_column="s_dob")
    s_gender=models.CharField(max_length=10,db_column="s_gender")
    s_qual=models.CharField(max_length=30,db_column="s_qual")
    s_colg=models.CharField(max_length=50,db_column="s_colg")
    s_email=models.CharField(max_length=50,db_column="s_email")
    s_phno=models.CharField(max_length=10,db_column="s_phno")
    s_passout=models.IntegerField(db_column="s_passout")
    date_entered=models.CharField(max_length=10,db_column="date_entered")
    status=models.CharField(max_length=20,default="active",db_column="status")

    class Meta:
        db_table="tb_folloupData"
class FollowupStatus(models.Model):
    f_id=models.ForeignKey(FollowUpData,on_delete=models.CASCADE,db_column="f_id")
    date=models.CharField(max_length=10,db_column="date")
    status=models.CharField(max_length=20,db_column="status")
    class Meta:
        db_table="tb_followupStatus"

class AttendanceDetails(models.Model):
    type=models.CharField(max_length=10,db_column="type")
    hr_id=models.ForeignKey(HrDetails, null=True,  on_delete=models.CASCADE,db_column="hr")
    tr_id=models.ForeignKey(TrainerDetails,null=True,on_delete=models.CASCADE,db_column="tr")
    s_id=models.ForeignKey(StudentDetails,null=True,on_delete=models.CASCADE,db_column="st")
    date=models.CharField(max_length=10,db_column="dt")
    mnth=models.IntegerField(db_column="mnth")
    yr=models.IntegerField(db_column="yr")
    status=models.CharField(max_length=20,db_column="status")
    class Meta:
        db_table="tb_attendance"

class NotesDetails(models.Model):
    mod_id=models.ForeignKey(ModuleDetails,on_delete=models.CASCADE,db_column="mod_id")
    uploaded_by=models.CharField(max_length=20,db_column="up_by")
    uploaded_date=models.CharField(max_length=20,db_column="up_dt")
    uploaded_file=models.FileField(upload_to='Notes/')
    desc=models.CharField(max_length=200,db_column="desc")
    
    class Meta:
        db_table="tb_notes"
    
class ExamDetails(models.Model):
    date_entered=models.CharField(max_length=20,db_column="ent_dt")
    exam_date=models.CharField(max_length=20,db_column="ex_dt")
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    m_id=models.ForeignKey(ModuleDetails,on_delete=models.SET_NULL,null=True,db_column="m_id")
    status=models.CharField(max_length=20,default="pending",db_column="status")

    class Meta:
        db_table="tb_exam"

class CertificateDetails(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    req_date=models.CharField(max_length=20,db_column="req_dt")
    rec_date=models.CharField(max_length=20,db_column="rec_dt")
    hr_comment=models.CharField(max_length=100,db_column="hr_comnt")
    status=models.CharField(max_length=10,default="pending",db_column="status")

    class Meta:
        db_table="tb_cert"

class InterviewDetails(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    added_date=models.CharField(max_length=20,db_column="add_dt")
    interview_date=models.CharField(max_length=20,db_column="int_dt")
    cmp_name=models.CharField(max_length=50,db_column="cmp_name")
    cmp_addr=models.CharField(max_length=100,db_column="cmp_addr")
    cmp_contact=models.CharField(max_length=20,db_column="cmp_cont")
    int_type=models.CharField(max_length=10,db_column="int_type")
    int_post=models.CharField(max_length=50,default="",db_column="int_post")
    status=models.CharField(max_length=10,default="pending",db_column="status")

    class Meta:
        db_table="tb_inter"
    
class PlacementDetails(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    cmp_name=models.CharField(max_length=50,db_column="cmp_name")
    designation=models.CharField(max_length=50,db_column="cmp_design")
    join_date=models.CharField(max_length=50,db_column="cmp_join")

    class Meta:
        db_table="tb_placement"

    
class CertFiles(models.Model):
    s_id=models.ForeignKey(StudentDetails,on_delete=models.CASCADE,db_column="s_id")
    cert_title=models.CharField(max_length=30,db_column="cert_title",null=True)
    cert=models.FileField(upload_to="Certificate/",db_column="cert")
    

    class Meta:
        db_table="tb_certf  "





