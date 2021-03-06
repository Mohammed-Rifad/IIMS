from django.db import models
from Institute_app.models import StudentDetails
from django import forms
import re


class StudentForm(forms.ModelForm):
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
    mode_choices=(
        ('offline','Offline'),
        ('online','Online'),
    )
    s_name=forms.CharField(label="Student Name",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    s_colg=forms.CharField(label="College",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    s_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px','placeholder':'dd-mm-yyyy'}))
    s_qual=forms.CharField(label="Qualification",widget=forms.Select(choices=qual_choices, attrs={'class':'form-control','style':'width:300px',}))
    s_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choices, ))
    s_type=forms.CharField(label="Mode",widget=forms.Select(choices=mode_choices, attrs={'class':'form-control',}))
    s_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    s_passout=forms.CharField(label="Year PassOut",widget=forms.NumberInput(attrs={'class':'form-control','style':'width:300px',}))
    s_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    s_email=forms.CharField(label="Email",widget=forms.TextInput(attrs={'style':'width:300px','class':'form-control'}))
    s_pic=forms.ImageField(label="Pic",widget=forms.FileInput(attrs={'style':'width:300px','class':'form-control',}))
    amt_payable=forms.CharField(label="Amount Payable",widget=forms.NumberInput(attrs={'class':'form-control','style':'width:300px','min':'100'}))
    class Meta:
        model=StudentDetails
        fields=('s_name','s_colg','s_dob','s_qual','s_gender','s_address','s_passout','s_phno','s_email','s_pic','amt_payable')




class InterviewForm(forms.ModelForm):

    int_type=(
        ('direct','direct'),
        ('online','online')
    )
    
    cmp_name=forms.CharField(label="Company Name",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    cmp_addr=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'5','cols':'25','class':'form-control'}))
    cmp_contact=forms.CharField(label="Contact",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    int_type=forms.CharField(label="Type",widget=forms.Select(choices=int_type,attrs={'class':'form-control','style':'width:300px',}))
    cmp_contact=forms.CharField(label="Contact",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    int_post=forms.CharField(label="Interview Post",widget=forms.TextInput(attrs={'class':'form-control','style':'width:300px',}))
    class Meta:   
        model=StudentDetails
        fields=('cmp_name','cmp_addr','cmp_contact','int_type','int_post')
