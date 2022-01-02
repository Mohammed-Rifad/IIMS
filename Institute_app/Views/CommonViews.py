from django.shortcuts import redirect, render
from ..models import AdminDetails, HrDetails, StudentDetails, TrainerDetails
from Institute_app.Forms.CommonForms import LoginForm
from passlib.hash import pbkdf2_sha256


def AdminData(request):
    passwd=pbkdf2_sha256.hash("admin",rounds=1000,salt_size=32)
    qry=AdminDetails(login_id="Admin",login_passwd=passwd)
    qry.save()
    return redirect("e_nursery:login")

def ProjectHome(request):
    return render(request,'Common/ProjectHome.html')
    
def Login(request):
    form=LoginForm()
    msg=""
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            login_id=form.cleaned_data['login_id']
            login_passwd=form.cleaned_data['login_passwd']
            if login_id=='Admin':
                auth_check=AdminDetails.objects.filter(login_id=login_id).exists()
                if auth_check:
                    auth_data=AdminDetails.objects.get(login_id=login_id)
                    auth_passwd=auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        request.session['admin_id']=1005
                        return redirect("institute_app:admin_home")
                    else:
                        msg="Incorrect Password"
                    
                else:
                    msg="Incorrect UserName or Password"
            elif '@' in login_id:
                auth_check=HrDetails.objects.filter(hr_email=login_id,hr_status='active').exists()
                if auth_check:
                    auth_data=HrDetails.objects.get(hr_email=login_id,hr_status="active")
                    auth_passwd=auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        request.session['hr_id']=auth_data.hr_id
                        return redirect("institute_app:hr_home")
                    else:
                        msg="Incorrect Password"
                    
                else:
                    msg="Incorrect UserName or Password"
            elif login_id.isdigit()==True and len(login_id)==5:
                auth_check=TrainerDetails.objects.filter(tr_id=login_id,tr_status='active').exists()
                if auth_check:
                    auth_data=TrainerDetails.objects.get(tr_id=login_id)
                    print('yesss')
                    auth_passwd=auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        request.session['tr_id']=auth_data.tr_id
                        return redirect("institute_app:tr_home")
                    else:
                        msg="Incorrect Password"
                    
                else:
                    msg="Incorrect UserName or Password"
            elif login_id.isdigit()==True and len(login_id)==4:
                print('here')
                auth_check=StudentDetails.objects.filter(s_id=login_id).exists()
                if auth_check:
                    auth_data=StudentDetails.objects.get(s_id=login_id)
                    auth_passwd=auth_data.verifyPasswd(login_passwd)
                    if auth_passwd:
                        request.session['s_id']=auth_data.s_id
                        return redirect("institute_app:st_home")
                    else:
                        msg="Incorrect Password"
                else:
                    msg="Incorrect UserName or Password"
            else:
                    msg="Incorrect UserName or Password"
        else:
            print('error')
    return render(request,'Common/Login.html',{'form':form,'msg':msg})