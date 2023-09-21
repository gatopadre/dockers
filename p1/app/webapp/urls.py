"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from report.views import (  
    test,  
    show_report,  
    get_data,  
    send_report_by_email,  
    process_data
)

urlpatterns = [
    path('', show_report),
    path('email/', send_report_by_email),
    path('get_data/', get_data),
    path('process_data/', process_data),
    path('test/', test),
]
