"""
URL configuration for testbed_emulator_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from testbed_emulator_backend_app.views import AssemblyWorkflowViewSet, WorkCellStateViewSet, AMRStateViewSet, TestbedTaskViewSet, MaterialTransportTaskChainViewSet, AMRMissionViewSet

router = DefaultRouter()
router.register(r'assembly-workflows', AssemblyWorkflowViewSet, basename='assemblyworkflow')
router.register(r'workcellstates', WorkCellStateViewSet, basename='workcellstate')
router.register(r'amrstates', AMRStateViewSet, basename='amrstate')
router.register(r'testbedtasks', TestbedTaskViewSet, basename='testbedtask')
router.register(r'amrmissions', AMRMissionViewSet, basename='amrmission')
router.register(r'materialtransporttaskchains', MaterialTransportTaskChainViewSet, basename='materialtransporttaskchain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
