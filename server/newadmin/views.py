import json
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .models import AdminUser , Project
import uuid
import os
#Global functions reside here 
def getAdminData(request):
    # checking if the user is logged in
    if 'unique_id' in request.session:
         return  AdminUser.objects.get(unique_id=request.session['unique_id'])
    else:
        return None 



def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', filename)



# import all  the  viewsComponents here 
from .uploadView import *




def index(request):
    # checking if the user is logged in
    if 'unique_id' in request.session:
         admin = AdminUser.objects.get(unique_id=request.session['unique_id'])
         if admin :
            projects = ProjectsManager().getProjectsData()
            project_types = ProjectsManager().getProjectTypes()
            print("--------->>>>>Admin Logged In ==== " ,admin)
            return render(request, 'newadmin/admin.html' , {'admin':admin ,'project_types':project_types , 'projects':projects })
         
         else:
             return redirect('admin-login')
    else:
        return redirect('admin-login')



def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = AdminUser.objects.get(username=username, password=password)
            if user:
                # set sessions fo the unique_id  as the  unique_id of the user
                request.session['unique_id'] = user.unique_id
                return redirect('admin-index')
            else : 
                message = "Invalid Username or Password"
                return render(request, 'newadmin/admin-login.html' , {'message':message})
        except:
            message = "Invalid Username or Password"
            return render(request, 'newadmin/admin-login.html' , {'message':message})
    else:
        # checking if the user is logged in
        if 'unique_id' in request.session:
            # checking  if the use is valid
            try:
                user = AdminUser.objects.get(unique_id=request.session['unique_id'])
                if user:
                    return redirect('admin-index')
                else:
                    return render(request, 'newadmin/admin-login.html') 
            except:
                return render(request, 'newadmin/admin-login.html') 
        else:
            return  render(request , 'newadmin/admin-login.html')
def adminLogout(request):
    # checking if the user has sent a session
    if 'unique_id' in request.session :
        # lets  logout the user 
        del request.session['unique_id']
        return redirect('admin-login')
    else:
        return redirect('admin-login') 
def adminRegister(request):
    # checking if the user is logged in
    if 'unique_id' in request.session:
        if request.method == 'POST':
            username = request.POST['username']
            fullName = request.POST['fullName']
            password = request.POST['password']
            email = request.POST['email']
            job = request.POST['job']

            # checking if the username already exists
            try:
                user = AdminUser.objects.get(username=username)
                if user:
                    message = "Username already exists"
                    return render(request, 'newadmin/admin-register.html' , {'message':message})
            except:
                # create a new user
                user = AdminUser(username=username, fullName=fullName, password=password, email=email, job=job)
                user.save()
                message ="User created successfully"
                print("--------->>>>>" ,message)
                return redirect('admin-login')
        return render(request, 'newadmin/admin-register.html')
    else:
        return redirect('admin-login')

def adminProfile(request):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        return render(request , 'newadmin/admin-profile.html'  , {'admin':admin}) 

def adminProfileEdit(request):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        if request.method == 'POST':
            # getting  the  admin user  from  the admin unique_id and updating the  admin profile

            

            fullName = request.POST['fullName'].strip()

            username = request.POST['username'].strip()
            email = request.POST['email'].strip()
            job = request.POST['job'].strip()
            facebook = request.POST['facebook'].strip()
            twitter = request.POST['twitter'].strip()
            instagram = request.POST['instagram'].strip()
            linkedin = request.POST['linkedin'].strip()

            print("--------->>>>>" ,fullName)
            print("--------->>>>>" ,username)
            print("--------->>>>>" ,email)

            # updating the admin profile
            admin.fullName = fullName
            admin.username = username
            admin.email = email
            admin.job = job
            admin.facebook = facebook
            admin.twitter = twitter
            admin.instagram = instagram
            admin.linkedin = linkedin

            #lets return   a  json response if the admin has been updated
            admin.save()
            return HttpResponse(json.dumps({'status':'success' , 'message':'Profile updated successfully'}))
         

        else:
            return render(request , 'newadmin/admin-profile.html'  , {'admin':admin}) 

def adminProfileChangePassword(request):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        if request.method == 'POST':
            # getting  the  admin user  from  the admin unique_id and updating the  admin profile

            currentPassword = request.POST['currentPassword'].strip()
            newPassword = request.POST['newPassword'].strip()
            confirmPassword = request.POST['confirmPassword'].strip()

            # checking  if any password is empty 
            if currentPassword == '' or newPassword == '' or confirmPassword == '':
                return HttpResponse(json.dumps({'status':'error' , 'message':'All fields are required'})) 
            

            # checking if the old password is correct
            if admin.password == currentPassword: 
                # checking if the new password is the same as the old password
                if newPassword == currentPassword or confirmPassword == currentPassword:
                    return HttpResponse(json.dumps({'status':'error' , 'message':'New password cannot be the same as the old password'}))
                
                # checking if the new password and confirm password are the same
                if newPassword == confirmPassword:
                    # updating the password
                    admin.password = newPassword
                    admin.save()
                    return HttpResponse(json.dumps({'status':'success' , 'message':'Password updated successfully'}))
                else:
                    return HttpResponse(json.dumps({'status':'error' , 'message':'New password and confirm password do not match'}))
            else:
                return HttpResponse(json.dumps({'status':'error' , 'message':'Old password is incorrect'}))
        else:
            return render(request , 'newadmin/admin-profile.html'  , {'admin':admin}) 

def adminProfileChangeImage(request):
    admin = getAdminData(request)
    if admin == None :
        return redirect('admin-login')
    else:
        if request.method == 'POST':
            # getting  the  admin user  from  the admin unique_id and updating the  admin profile

            image = request.FILES['image']
            print("--------->>>>>" ,image)
            # updating the image 
            admin.image = image
            admin.save()
            return HttpResponse(json.dumps({'status':'success' , 'message':'Profile Image updated successfully'})) 
        
        else:
            return render(request , 'newadmin/admin-profile.html'  , {'admin':admin}) 
        
