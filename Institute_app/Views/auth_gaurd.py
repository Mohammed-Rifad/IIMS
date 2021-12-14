from django.shortcuts import render,redirect

def auth_hr(func):
    def wrap(request,*args,**kwargs):
        if 'hr_id' in request.session:
           
            return func(request,*args,**kwargs)
        else:
            return redirect('institute_app:proj_home')


    return wrap