from django.shortcuts import render,redirect

def auth_hr(func):
    def wrap(request,*args,**kwargs):
        if 'hr_id' in request.session:
           
            return func(request,*args,**kwargs)
        else:
            return redirect('institute_app:proj_home')


    return wrap

def auth_admin(func):
    def wrap(request,*args,**kwargs):
        if 'admin_id' in request.session:
           
            return func(request,*args,**kwargs)
        else:
            return redirect('institute_app:proj_home')


    return wrap

def auth_st(func):
    def wrap(request,*args,**kwargs):
        if 's_id' in request.session:
           
            return func(request,*args,**kwargs)
        else:
            return redirect('institute_app:proj_home')


    return wrap

def auth_tr(func):
    def wrap(request,*args,**kwargs):
        if 'tr_id' in request.session:
           
            return func(request,*args,**kwargs)
        else:
            return redirect('institute_app:proj_home')


    return wrap