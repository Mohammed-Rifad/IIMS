from django.urls import path
from . import views
from .Views import CommonViews,AdminViews,HrViews,TrainerViews

app_name="institute_app"

urlpatterns = [


    path('',CommonViews.Login,name="login"),
    path('AdminHome',AdminViews.AdminHome,name="admin_home"),
    path('AdminHome/AddCourse',AdminViews.AddCourse,name="add_course"),
    path('AdminHome/AddModule',AdminViews.AddModule,name="add_module"),
    path('AdminHome/AddSystem',AdminViews.AddSystem,name="add_system"),
    path('AdminHome/AddHr',AdminViews.AddHr,name="add_hr"),
    path('AdminHome/AddTrainer',AdminViews.AddTrainer,name="add_trainer"),    
    path('AdminData',CommonViews.AdminData),
    path('AdminHome/FollowUp',AdminViews.AddFollowUp,name="add_followup"),
    path('AdminHome/Students',AdminViews.ViewActiveStudents,name="admin_active_students"),
    path('AdminHome/Seating',AdminViews.ViewSeating,name="view_seating_admin"),
    path('AdminHome/ActiveFollowup',AdminViews.ActiveFollowUp,name="admin_active_followup"),
    path('AdminHome/History/<int:f_id>',AdminViews.FollowUpHistory,name="admin_followup_hst"),
    path('AdminHome/SetPermission/',AdminViews.UpdatePermission,name="set_permission"),
    path('HrHome',HrViews.HrHome,name="hr_home"),
    path('AdminHome/TrainerAttendance',AdminViews.ViewTrainerAttendance,name="view_tr_attendance"),



    path('HrHome/AddStudent',HrViews.AddStudent,name="add_student"),
    path('HrHome/TrainerAttendance',HrViews.TrainerAttendance,name="trainer_att"),
    path('HrHome/ViewTrAttendance',HrViews.ViewTrainerAttendance,name="tr_attendance"),
    path('HrHome/AssignSeat',HrViews.AssignSeating,name="assign_seat"),
    path('HrHome/Seating',HrViews.ViewSeating,name="view_seating_hr"),
    path('HrHome/getSystem',HrViews.getSystem),
    path('HrHome/ActiveStudents',HrViews.ViewActiveStudents,name="hr_active_students"),
    path('HrHome/ActiveFollowup',HrViews.ActiveFollowUp,name="hr_act_followup"),
    path('HrHome/Followup/<int:id>',HrViews.AddFollowUp,name="hr_add_followup"),
    path('HrHome/History/<int:f_id>',HrViews.FollowUpHistory,name="hr_followup_hst"),
    path('HrHome/DueList',HrViews.DueList,name="hr_due_list"),
    path('HrHome/AddPayment',HrViews.AddPayment,name="hr_add_pay"),

    path('TrainerHome',TrainerViews.TrainerHome,name="tr_home"),
    path('TrainerHome/ActiveStudents',TrainerViews.ViewActiveStudents,name="tr_active_students"),
 
    path('TrainerHome/UpdateSeat',TrainerViews.UpdateSeating,name="tr_assign_seat"),
    path('TrainerHome/AddNotes',TrainerViews.AddNotes,name="add_notes"),
    path('TrainerHome/Status',TrainerViews.ViewStudentStatus,name="tr_st_status"),
    path('TrainerHome/getModules',TrainerViews.getModules),
    path('TrainerHome/Update',TrainerViews.UpdateStatus,name="upd_status"),
    path('TrainerHome/ViewNotes',TrainerViews.ViewNotes,name="tr_view_notes"),
]
