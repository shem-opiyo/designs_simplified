from django.urls import  path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path ( '' ,  views.index , name =  'admin-index' ),
        path( 'login/' ,  views.adminLogin, name =  'admin-login'),
        path( 'register/' ,  views.adminRegister, name =  'admin-register'),
        path('profile/' , views.adminProfile , name="admin-profile") , 

        path('profile/edit/' , views.adminProfileEdit , name="admin-profile-edit") ,
        
        path('profile/change-password/' , views.adminProfileChangePassword , name="admin-profile-change-password") ,

        # change  profile image 
        path('profile/change-image/' , views.adminProfileChangeImage , name="admin-profile-change-image") ,


        path('projects/upload/' , views.adminUpload , name="admin-upload" ) ,
        # path('projects/uploaded/<str:status>/' , views.adminUploaded , name="admin-uploaded") ,
        # path('projects/edit/<str:project_name>' , views.adminEdit , name="admin-edit") , 
        # path('projects/edited/<str:status>/' , views.adminEdited , name="admin-edited") ,
        # path('projects/delete/<str:project_name>' , views.adminDelete , name="admin-delete") ,
        path('projects/<action>/' , views.adminProjectsView , name="admin-projects-view" ) ,  

        path('projects/view/<str:project_name>/' , views.adminViewOneProject , name="admin-view-one-project" ) ,

        path( 'logout/' ,  views.adminLogout, name =  'admin-logout'),  

        # SETTING  UP THE PATH  FOR THE MEDIA FILES         
] 
