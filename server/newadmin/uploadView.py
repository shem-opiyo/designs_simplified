import uuid
from django.http import JsonResponse
from django.shortcuts import render , redirect
from .models import *
from .views import getAdminData 
from django.core.files.storage import default_storage
import os 

from urllib.parse import urlencode
from django.urls import reverse

# Upload  Views Reside here 


def adminUpload(request):

    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        if request.method == "POST":
            name  =  request.POST['name'].strip() 
            title =  request.POST['title'].strip()
            description = request.POST['description'].strip()
            images   = request.FILES.getlist('images')
            type  = request.POST['type'].strip()

            # checking  if a  project with same name exists
            if Project.objects.filter(name=name).first() != None:
                params = {'status':"error" , 'task' : "project with same name already exists"}
                queryString = urlencode(params)
                print(queryString , "  -----------------> QUERY STRING") 
                # getting url for admin-upload
                
                return redirect(f'{reverse("admin-upload")}?{queryString}')
            else:
                print("project upload in progress......") 


                for img in images :
                    image = Image.objects.create(
                        project_name =  name,
                        image = img
                    )
                    image.save()    

                Project.objects.create(
                    admin= admin ,name=name,title=title,type=type ,
                    description=description,album = ImagesAlbum.objects.create(project_name=name)
                ).save() 



    
                params = {'status':"success" , 'task' : "project uploaded successfully"}
                queryString = urlencode(params)
                print(queryString , "  -----------------> QUERY STRING") 
                # getting url for admin-upload
                
                return redirect(f'{reverse("admin-upload")}?{queryString}')
            
        else:
            # checking the request args if it has status argument
            status = request.GET.get('status') 
            task = request.GET.get('task')
            script = None
            if status == "success" or status == "error":
                # redirecting  to  the  home page  to  view  projects  using timeout
                script = "setTimeout(function(){window.location.href = '/admin/projects/view/';},1500);"
            return render(request , 'newadmin/admin-upload.html' , {'admin' : admin , 'status' : status , 'task' : task , 'script' : script})
 

def adminProjectsView(request , action=None):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        script = None
        manager = ProjectsManager()
        projects = manager.getProjectsData()
        # script = f"console.log({projects});" 

        if action == "delete":
            if request.method == "POST":
                project_id = request.POST.get('unique_id')
                project = Project.objects.filter(unique_id=project_id).first()  

                # delete  the  images that have the project_names as the  project name 
                images = ImagesAlbum().getProjectImages(project_name=project.name) 
                for image in images :
                    image.delete() 
                # delete the Images Album from  the  database

                ImagesAlbum.objects.filter(project_name=project.name).delete()

                project.delete() 

                # checking  if the project is deleted 
                if Project.objects.filter(unique_id=project_id).first() == None:
                    json = {'status' : 'success' , 'task' : f'{project.name}project deleted successfully' , 'projects' : projects}
                    return JsonResponse(json)
                else:
                    json = {'status' : 'error' , 'task' : 'project not deleted' , 'projects' : projects}
                    return JsonResponse(json)

                
                # params = {'status':"success" , 'task' : f"{project.name}  project deleted successfully"} 
                # script = "setTimeout((e)=>{ window.location.href='/admin/projects/view/'} , 1500)"
                # # queryString = urlencode(params)
                # # print(queryString , "  -----------------> QUERY STRING")  

                # # getting url for admin-upload
                
                # return render(request , 'newadmin/admin-projects-view.html' , params ,  {'admin' : admin , 'projects' : projects ,'script' : script }) 
            
            else:
                return redirect('admin-projects-view')
        elif action == "view":
            return render(request , 'newadmin/admin-projects-view.html' , {'admin' : admin , 'projects' : projects , 'script' : script}) 
        
        elif action == "edit":
            pass

        else: 
            return redirect('admin-index')



def adminViewOneProject(request , project_name):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        # checking if the projects exists first 
        if Project.objects.filter(name=project_name).first() == None:
            return redirect('admin-projects-view' , action="view")
        script = None
        manager = ProjectsManager()
        project = manager.getOneProjectData(project_name=project_name)
        # script = f"console.log({projects});" 
        return render(request , 'newadmin/admin-view-one-project.html' , {'admin' : admin , 'project' : project , 'script' : script})
        

      