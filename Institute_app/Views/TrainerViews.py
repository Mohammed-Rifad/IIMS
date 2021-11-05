import datetime
from Institute_app.services import UpdateSeat, getFileName
from django.shortcuts import render,redirect
from ..models import CourseDetails, ModuleDetails, NotesDetails, SeatingDetails,StudentDetails, StudentModule, TrainerDetails

def TrainerHome(request):
    return render(request,'Trainer/TrainerHome.html')

def ViewActiveStudents(request):
    courses=CourseDetails.objects.all()
    students=StudentDetails.objects.filter(status="active")
    if request.method=='POST':
        if 'filter' in request.POST:
            course=request.POST['course']
            students=StudentDetails.objects.filter(c_id=course, status="active")
        if 'status' in request.POST:
            s_id=request.POST['s_id']
            data=StudentModule.objects.filter(s_id=s_id)
            print('data',data)
            return render(request,'Trainer/StudentStatus.html',{'modules':data,})
        if 'update' in request.POST:
            s_id=request.POST['s_id']
            data=StudentModule.objects.filter(s_id=s_id)
            print('SSSSSSSSSS',data)
            return render(request,'Trainer/UpdateStudentModule.html',{'s_id':s_id,'modules':data})
    return render(request,'Trainer/ActiveStudents.html',{'students':students,'courses':courses})


def UpdateStatus(request):
    s_id=request.POST['s_id']
    m_id=request.POST['module']
    data=StudentModule.objects.get(s_id=s_id,m_id=m_id)
    data.status="completed"
    data.save()
    return redirect("institute_app:tr_active_students")



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

def AddNotes(request):
    course_data=CourseDetails.objects.all()
    if request.method=='POST':
        tr_data=TrainerDetails.objects.get(tr_id=request.session['tr_id'])
        uploaded_by=tr_data.tr_name
        dt=datetime.date.today()
        uploaded_date=dt.strftime("%d/%m/%Y")
        module=ModuleDetails.objects.get(m_id=request.POST['module'])
        desc=request.POST['desc']
        file=request.FILES['notes']
        #file_name=getFileName(module.m_name)
        
        notes=NotesDetails(mod_id=module,uploaded_by=uploaded_by,uploaded_date=uploaded_date,uploaded_file=file,desc=desc)
        notes.save()
        # n=NotesDetails.objects.get(id=1)
        # print(request.FILES['notes'])

    return render(request,'Trainer/AddNotes.html',{'courses':course_data})

#ajax
def getModules(request):
    c_id=request.GET['c_id']
    modules=ModuleDetails.objects.filter(c_id=c_id)
    return render(request,'Trainer/modulesDropdown.html',{'modules':modules})

def ViewNotes(request):
    modules=ModuleDetails.objects.all()
    notes =NotesDetails.objects.all()
    if request.method=='POST':
        if 'del' in request.POST:
            id=request.POST['n_id']
            note=NotesDetails.objects.get(id=id)
            note.delete()
        if 'search' in request.POST:
            module=request.POST['module']
            notes=NotesDetails.objects.filter(mod_id=module)
    return render(request,'Trainer/ViewNotes.html',{'modules':modules,'notes':notes,})

def ViewStudentStatus(request):
    student=''
    return render(request,'Trainer/StudentModule.html',)