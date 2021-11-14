

from Institute_app.models import AttendanceDetails, CourseDetails, ExamDetails, FeeDetails, FollowUpData, FollowupStatus, HrDetails, ModuleDetails, NotesDetails, SeatingDetails, StudentDetails, StudentModule, SystemDetails, TrainerDetails
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
    if request.method=='POST':
      
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Student/ViewNotes.html',{'modules':modules,'notes':notes,})

def ExamShedhule(request):
    exams=ExamDetails.objects.filter(s_id=request.session['s_id'])
    return render(request,'Student/Exam.html',{'exams':exams,})

