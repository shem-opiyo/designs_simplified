from django.db import models
from datetime import datetime
import uuid , os  

# from django.conf import settings

# Create your models here.

def generateUniqueId():
    import uuid
    return str(uuid.uuid4()) 

def get_project_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}" 
    project_name = instance.project_name
    return os.path.join(f'projects/{project_name}/{filename}')



class AdminUser(models.Model):
    username = models.CharField(max_length=50)
    fullName = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='admin_images' , null=True, blank=True , default=None)
    job = models.CharField(max_length=50)
    unique_id = models.CharField(default=generateUniqueId ,max_length=50, unique=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    facebook = models.CharField(max_length=100 , default='https://www.facebook.com/#')
    twitter = models.CharField(max_length=100 , default='https://www.twitter.com/#' )
    instagram = models.CharField(max_length=100 , default='https://www.instagram.com/#' )  
    linkedin = models.CharField(max_length=100 , default='https://www.linkedin.com/#')
    youtube = models.CharField(max_length=100 , default='https://www.youtube.com/#')
    github = models.CharField(max_length=100 , default='https://www.github.com/#')
    whatsapp = models.CharField(max_length=100 , default='https://www.whatsapp.com/#')

    def getAdminDetails(self , unique_id):
        return AdminUser.objects.get(unique_id=self.unique_id)  


class ImagesAlbum(models.Model):

    project_name = models.CharField(max_length=50 , default=generateUniqueId , blank=True) 
    def getImagesLength(self , project_name):
        return Image.objects.filter(project_name=project_name).count()

    def getProjectImages(self , project_name):
        return Image.objects.filter(project_name=project_name)
    
    def getProfileImages(self , unique_id):
        return Image.objects.filter(project_name=unique_id) 
    
    def deleteImage(self , image_name):
        return Image.objects.filter(name=image_name).delete()
    



    # change  the  above  model tobe ImagesAlbum and return the  images  in the  album depending  on types passsed  in the  function 

class Image(models.Model):

    name = models.CharField(max_length=50 , default=generateUniqueId , blank=True)
    project_name = models.CharField(max_length=50 , default=generateUniqueId , blank=True)
    image = models.ImageField(upload_to=get_project_file_path ,null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    album = models.ForeignKey(ImagesAlbum , on_delete=models.CASCADE , related_name= 'images' , null=True) 
    
    def delete(self, *args, **kwargs):
        # deleting  the parent folder if  it  is empty
        # if self.album.getImagesLength(self.project_name) == 1:
        #     self.album.delete()
        self.image.delete()
        super().delete(*args, **kwargs)


class ProjectsManager(models.Model): 

    def getCompanyData(self):
        # creating company data manually but a model should be created for this
        company = {}
        company['name'] = 'shem Interiors'
        company['email'] =  'shem@gmail.com'
        company['phone'] =  '+254742667594'
        company['street'] = 'A104 Gitaru'
        company['city'] = 'Nairobi'
        company['country'] = 'Kenya'
        company['address'] =  'Gitaru , Nairobi, Kenya'
        company['services'] = ['Interior Design' , 'Architectural Design' , '3D Design' , 'Site Supervision' , 'Project Management']
        # the logo will be designed to fit the company name and the brand
        # company['logo'] =  'https://res.cloudinary.com/shem/image/upload/v1622021004/shem-logo.png'
        company['title'] = 'SHEM INTERIORS'
        company['who_we_are'] = "At <strong> shem Interiors</strong>, we are passionate about creating beautiful spaces that are functional and comfortable. We are a team of highly skilled and experienced interior designers and architects who are committed to delivering the best interior design solutions for our clients. We are a one-stop shop for all your interior design needs. We offer a wide range of interior design services including interior design, architectural design, 3D design, and construction management. We are a team of highly skilled and experienced interior designers and architects who are committed to delivering the best interior design solutions for our clients. We are a one-stop shop for all your interior design needs. We offer a wide range of interior design services including interior design, architectural design, 3D design, and construction management."
        company['what_we_do'] = "We are a team of highly skilled and experienced interior designers and architects who are committed to delivering the best interior design solutions for our clients. We are a one-stop shop for all your interior design needs. We offer a wide range of interior design services including interior design, architectural design, 3D design, and construction management."
        company['why_us'] = "We are a team of highly skilled and experienced interior designers and architects who are committed to delivering the best interior design solutions for our clients. We are a one-stop shop for all your interior design needs. We offer a wide range of interior design services including interior design, architectural design, 3D design, and construction management."

        company['facebook'] = 'https://www.facebook.com/#'
        company['twitter'] = 'https://www.twitter.com/#'
        company['instagram'] = 'https://www.instagram.com/#'
        company['linkedin'] = 'https://www.linkedin.com/#'
        company['instagram']  = 'https://www.instagram.com/#'


        return company

    def getTeamMembers(self):
        return AdminUser.objects.all() 
    
    def isProjectNameValid(self , project_name):
        return Project.objects.filter(name=project_name).exists()

    def decodeProjectObject(self , raw_project):
        project = {}
        project['id'] = int(raw_project.id)
        project['name'] = raw_project.name
        project['title'] = raw_project.title
        project['description'] = raw_project.description 
        project['unique_id'] = raw_project.unique_id 
        project['type'] = raw_project.type 
        project['category_name'] = raw_project.type.replace('_' , ' ' ).title()
        
        # images = []
        # for img in  raw_project.album.getProjectImages(raw_project.name):
        #     images.append(img.image.url)
        
        project['images'] = [img.image.url for img in raw_project.album.getProjectImages(raw_project.name)]
        project['images_length']= project['images'].__len__() 
        # print('--------=========' , project)
        return project

    def getOneProjectData(self , project_name):
        return self.decodeProjectObject(Project.objects.get(name=project_name))

    def getProjectsData(self) :
        raw_projects = Project.objects.all().order_by('-created_at')
        projects = [] 
        # projects = [project for project in projects if project.admin == admin]  

        # converting  the  projects to a  list 
        for index , raw_project in enumerate(raw_projects):
            project = self.decodeProjectObject(raw_project)
            project['index'] = index+1
            projects.append(project)  

        return projects 
    
    
    
    def getProjectTypes(self):
        project_types = Project.objects.values('type').distinct()  
        # for project_type in project_types:
        #     print('----------------->' ,project_type)

        categories = [
            { 'type' : project_type['type'] , 
              'name' : project_type['type'].replace('_' , ' ').title() ,
              'length' : Project.objects.filter(type=project_type['type']).count()

            }
            for project_type in project_types
        ]

        return categories



class Project(models.Model):
    name = models.CharField(max_length=50 , blank=True)
    title = models.CharField(max_length=50 , blank=True)
    description = models.TextField()
    type = models.CharField(max_length=50 , default="interior_design" , null=False , blank=True) 
    # images = models.ForeignKey(Image, on_delete=models.CASCADE , null=True)
    album = models.ForeignKey(ImagesAlbum ,  on_delete=models.CASCADE, related_name='projects' , null=True)
    unique_id = models.CharField(max_length=100 , default=generateUniqueId  , null= True , blank=True)
    
    admin = models.ForeignKey(AdminUser , on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True) 






            
