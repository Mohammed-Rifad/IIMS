from django import forms
import re

from django.forms import fields
from ..models import CourseDetails, FollowUpData, HrDetails, ModuleDetails, SystemDetails, TrainerDetails


class CourseForm(forms.ModelForm):
    c_name=forms.CharField(label="Course Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    c_duration=forms.CharField(label="Duration",widget=forms.NumberInput(attrs={'class':'form-control'}))
    c_fee=forms.CharField(label="Fee",widget=forms.NumberInput(attrs={'class':'form-control','min':'1'}))
    class Meta:
        model=CourseDetails
        exclude=('c_id',)
    

class ModuleForm(forms.ModelForm):
    m_name=forms.CharField(label="Course Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=ModuleDetails
        fields=('m_name',)

class SystemForm(forms.ModelForm):
    lab_choice=(
        ('1','1'),
        ('2','2')
    )
    lab_no=forms.CharField(label="Lab No",widget=forms.Select(choices=lab_choice, attrs={'class':'form-control'}))
    sys_no=forms.CharField(label="System No",widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=SystemDetails
        exclude=('sys_id','sys_status')


class HrForm(forms.ModelForm):
    gender_choices=(
        ('male','Male'),
        ('female','Female')
    )

    qual_choices=(
        ('bba','BBA'),
        ('mba','MBA'),
        ('bca','BCA'),
        ('mca','MCA')
    )
    
    hr_name=forms.CharField(label="HR Name",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    hr_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    hr_qual=forms.CharField(label="Qualification",widget=forms.Select(choices=qual_choices, attrs={'class':'form-control','style':'width:300px',}))
    hr_gender=forms.CharField(label="Gender",widget=forms.Select(choices=gender_choices, attrs={'class':'form-control','style':'width:300px',}))
    hr_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    hr_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    hr_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    hr_pic=forms.ImageField(label="Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    
    class Meta:
        model=HrDetails
        exclude=('hr_id','hr_join','hr_passwd','hr_status',)


class TrainerForm(forms.ModelForm):
    gender_choices=(
        ('male','Male'),
        ('female','Female')
    )
    qual_choices=(
        ('bba','BBA'),
        ('mba','MBA'),
        ('bca','BCA'),
        ('mca','MCA')
    )
    permission_set=(
        (1,'Yes'),
        (0,'No')
    )
    log_permission=forms.IntegerField(label="Login Permission",widget=forms.RadioSelect(choices=permission_set,)) 
    tr_name=forms.CharField(label="Trainer Name",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    tr_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    tr_qual=forms.CharField(label="Qualification",widget=forms.Select(choices=qual_choices, attrs={'class':'form-control','style':'width:300px',}))
    tr_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choices, ))
    tr_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    tr_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    tr_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    tr_pic=forms.ImageField(label="Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control'}))
    
    class Meta:
        model=TrainerDetails
        exclude=('tr_id','tr_join','tr_passwd','tr_status','tr_course')

class FollowupForm(forms.ModelForm):
    gender_choices=(
        ('male','Male'),
        ('female','Female')
    )
    qual_choices=(
        ('bba','BBA'),
        ('mba','MBA'),
        ('bca','BCA'),
        ('mca','MCA')
    )
    s_name=forms.CharField(label="Student Name",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    s_colg=forms.CharField(label="College",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    s_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    s_qual=forms.CharField(label="Qualification",widget=forms.Select(choices=qual_choices, attrs={'class':'form-control','style':'width:300px',}))
    s_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choices, ))
    s_passout=forms.CharField(label="Year PassOut",widget=forms.NumberInput(attrs={'class':'form-control','style':'width:300px',}))
    s_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    s_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    
    class Meta:
        model=FollowUpData
        exclude=('f_id','date_entered','status',)
    