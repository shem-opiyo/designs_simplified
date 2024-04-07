from django.urls import  path 

from .import views
urlpatterns = [
        path ( '' ,  views.index , name =  'index' ),
        path( 'portfolio/details/<str:portfolio_name>/' ,  views.portfolioDetails , name =  'portfolio-details') ,

        path( 'client/subscribe/' ,  views.clientSubscribe , name =  'client-subscribe' ),

        path( 'client/message/' ,  views.clientMessage , name =  'client-message' ),
]