from Institute_app.services import UpdateSeat
from django.shortcuts import render,redirect
from ..models import CourseDetails, SeatingDetails,StudentDetails

def TrainerHome(request):
    return render(request,'Trainer/TrainerHome.html')

def ViewActiveStudents(request):
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        course=request.POST['course']
        students=StudentDetails.objects.filter(c_id=course, status="active")
    return render(request,'Trainer/ActiveStudents.html',{'students':students,'courses':courses})

def UpdateSeating(request):
    status=""
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        student=StudentDetails.objects.get(s_id=request.POST['student'])
        lab=request.POST['lab']
        system=request.POST['system']
        slot=request.POST['slot']

        seating_data=SeatingDetails.objects.get(lab_no=lab,sys_no=system)

        status=UpdateSeat(seating_data,student,slot)
    return render(request,'Trainer/UpdateSeating.html',{'students':students,'status':status})