from django.shortcuts import render
from django.http import HttpResponse
import json 

# import the ProjectManager class from ADMIN app 
from newadmin.models import ProjectsManager 

# import mail from newadmin 

from newadmin.Mail import send_email

# Create your views here.

def index (request):
    projects  , categories = getPortfolio()
    team = getTeamMembers() 

    # pass all site data  such as  headername , email , phone ,     
    company = ProjectsManager().getCompanyData()

    return render(request,  'home/index.html' , { 'projects' : projects  ,  'categories' : categories , 'team' : team , 'company' : company} ) 

def getPortfolio():
    projects = ProjectsManager().getProjectsData()
    categories = ProjectsManager().getProjectTypes()
    return projects , categories
 
def portfolioDetails(request , portfolio_name):
    # check if portfolio_name is valid
    if not ProjectsManager().isProjectNameValid(portfolio_name):
        return HttpResponse( 'Invalid project name' )
    else :
        project = ProjectsManager().getOneProjectData(portfolio_name)
        return render(request,  'home/portfolio-details.html' , { 'project' : project , 'company' : ProjectsManager().getCompanyData() , 'categories' : ProjectsManager().getProjectTypes() })

def getTeamMembers():
    return ProjectsManager().getTeamMembers() 

def clientSubscribe(request):
    if request.method == 'POST':
        # gettig the json data from the request
        data = json.loads(request.body)
        email = data['email']
        name = email.split('@')[0]
        # email = request.POST['email']
        print('email' , email)
        msg = f"Hello {name}, welcome to SHEM INTERIORS . We are glad to have you on board. We will get back to you shortly"
        # add the functionality for mailing the user  here 
        if send_email(recipient=email , subject='Welcome to SHEM INTERIORS' , message=msg) :
            return HttpResponse(json.dumps({'status' : 'success' , 'message' : "Thank you for subscribing to our news letter " })  )
        else:
            return HttpResponse(json.dumps({'status' : 'error' , 'message' : "Error sending email" })  )
    else :
        return HttpResponse(json.dumps({'status' : 'error' , 'message' : "Invalid request" }) )  

def clientMessage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        print('name' , name)
        print('email' , email)
        print('subject' , subject)
        print('message' , message)

        # send email to the user to welcome them  in a charming way 
        msg = f"Hello {name} , welcome to SHEM INTERIORS . We are glad to have you on board. We will get back to you shortly"

        # add the functionality for mailing the user  here 

        if send_email(recipient=email , subject='Welcome to SHEM INTERIORS' , message=msg) : 
             return HttpResponse(json.dumps({'status' : 'success' , 'message' : "Thank you for contacting us. We will get back to you shortly" })  )
        else :
            return HttpResponse(json.dumps({'status' : 'error' , 'message' : "Error sending email" })  )

    else :
        return HttpResponse(json.dumps({'status' : 'error' , 'message' : "Invalid request" }) )