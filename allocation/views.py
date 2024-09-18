from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import *
from django.db.models import Q
from Logic.logic import *
from django.http import FileResponse
import os
from django.http import HttpResponse
from django.core.files import File
import tempfile
import zipfile
import os

from .forms import CreateUserForm

user=''
index1=[]
name2={}
index2=[]
date=[]
tot=0
exam=''
mselected_staff=[]
fselected_staff=[]
rooms=[]
single=[]
girl=[]
name=[]
exam1=[]
sessions=[]

def home(request):
    return render(request,"homepage.html")

def download_multiple_files(request):
    global date,exam,tot,mselected_staff,fselected_staff,single,rooms,girl,user,exam1,sessions,name,name2
    try:
        if exam=="END SEMESTER":
            file_paths=['Internal_Allocation.pdf','External_Allocation.pdf','SEMESTER_SQUAD_DUTY_Allocation.pdf']
        else:
            file_paths = ['Invigilator_Work_Schedule.pdf','Invigilator_Work_Count.pdf','merged_days.pdf']
        user=''
        date=[]
        tot=0
        name2={}
        exam=''
        mselected_staff=[]
        fselected_staff=[]
        rooms=[]
        single=[]
        girl=[]
        name=[]
        sessions=[]
        exam1=[]
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_filename = os.path.join(temp_dir, 'files.zip')
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_paths:
                    zipf.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_path), os.path.basename(file_path))
            with open(zip_filename, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="files.zip"'
        return response
    except:
        return d(request)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            department = form.cleaned_data['department']
            Profile.objects.create(username=user, department=department)
            messages.success(request, 'User was created successfully')
            return redirect('/logins')
        else:
            print(form.errors)
            messages.error(request, "Form submission failed. Please correct the errors below.")
            return redirect('/logins')
    context = {'form' : form}

    return render(request,"login.html",context)


def endsem1(request):
    global mselected_staff,fselected_staff,index2,index1
    return render(request,'staffoption.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})


def noend(request):
    pass


def logins(request):
    form = CreateUserForm()
    context = {'form' : form}

    if request.method == "POST":
        try:  
            username = request.POST.get('username')
            password = request.POST.get('password')

            checkuser = authenticate(request, username=username, password=password)
            if checkuser is not None:
                auth_login(request, checkuser)
                print("DONE")
                return redirect('/')
            else:
                messages.info(request, 'Wrong login credentials')
        except:
            return redirect('/login')
    else:
        return render(request,'login.html', context)


def admins(request):
    global mselected_staff,user,fselected_staff
    current_user = request.user
    username = current_user.username
    email = current_user.email

    if (username == 'admin'):
        staff1=Staff.objects.exclude(Q(name__in=mselected_staff)|Q(name__in=fselected_staff)|Q(designation='HOD')).order_by().values()
        dept1=Staff.objects.values_list('department').distinct()
        dept=[]
        for i in dept1:
            dept.append(i[0])
        user='all'
        return render(request,"edit2.html",{'mstaff':staff1,'dept':dept})
    else:
        profile = Profile.objects.get(username=current_user)
        department = profile.department

        staff1=Staff.objects.filter(Q(department=department)&Q(gender='M')).exclude(Q(name__in=mselected_staff)|Q(designation='HOD')).values()
        staff2=Staff.objects.filter(Q(department=department)&Q(gender='F')).exclude(Q(name__in=fselected_staff)|Q(designation='HOD')).values()
        user=department
        return render(request,"staff.html",{'mstaff':staff1,'fstaff':staff2})
    
    return redirect('/')


def staffselection(request):
    global mselected_staff,fselected_staff,index2,index1
    selected=request.POST.getlist('staff_name')
    for i in selected:
        staff=Staff.objects.filter(id=i).values()
        if staff[0]['gender']=='M':
            mselected_staff.append(staff[0]['name'])
            index1.append(staff[0]['id'])
            mselected_staff=list(set(mselected_staff))
        else:
            fselected_staff.append(staff[0]['name'])
            index2.append(staff[0]['id'])
            fselected_staff=list(set(fselected_staff))
    return render(request,"viewstaff.html",{'mstaff':mselected_staff,'fstaff':fselected_staff})


def edit(request):
    global user,mselected_staff,fselected_staff
    mselectedstaff=[]
    fselectedstaff=[]
    if user=='all':
        return render(request,'edit.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})
    for i in mselected_staff:
        if user in i.lower():
            mselectedstaff.append(i)
    for i in fselected_staff:
        if user in i.lower():
            fselectedstaff.append(i)
    return render(request,'edit.html',{'mstaff':mselectedstaff,'fstaff':fselectedstaff})


def edition(request):
    global mselected_staff,fselected_staff
    sel1=request.POST.getlist('mstaff_name')
    sel2=request.POST.getlist('fstaff_name')
    for i in sel1:
        mselected_staff.remove(i)
    for i in sel2:
        fselected_staff.remove(i)
    return render(request,'viewstaff.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})


def end1(request):
    return render(request,'endsem.html')


def roomss(request):
    if user=='all':
        rooms=Rooms.objects.order_by('roomno').values()
        return render(request,'rooms.html',{'rooms':rooms})
    return render(request,'finished.html')


def roomselect(request):
    global rooms,single,girl
    rooms=request.POST.getlist('roomInput')
    single=request.POST.getlist('singlestaff')
    girl=request.POST.getlist('girlroom')
    if single==['none']:
        single=[]
    if girl==['none']:
        girl=[]
    if rooms!=[]:
        return render(request,'examtype2.html')
    return roomss(request)
    pass


def examdate(request):
        global date,exam,tot,mselected_staff,fselected_staff,single,rooms,girl,name2,sessions,exam1
        date=request.POST['date'].split()
        exam=request.POST['exam']
        tot=int(request.POST['tot'])
        if exam=="END SEMESTER":
            endsem(name2,date[0])
            return render(request,'download.html')
        superlogic(date,exam,rooms,tot,single,girl,mselected_staff,fselected_staff)
        return render(request,'download.html')
    

def d(request):
    return render(request,'download.html')


def staffed(request):
    global user,mselected_staff,fselected_staff
    if user=='all':
        staff1=Staff.objects.exclude(Q(name__in=mselected_staff)|Q(name__in=fselected_staff)|Q(designation='HOD')).order_by().values()
        dept1=Staff.objects.values_list('department').distinct()
        dept=[]
        for i in dept1:
            dept.append(i[0])
        return render(request,"admindelete.html",{'mstaff':staff1,'dept':dept})
    stff=Staff.objects.filter(department=user.upper()).exclude(Q(name__in=mselected_staff)|Q(name__in=fselected_staff)).values()
    return render(request,'EditStaff.html',{'staff':stff})


def addition(request):
    title=request.POST['courtesyTitle']
    name=request.POST['username']
    gender=request.POST['gender']
    desig=request.POST['desig']
    dept=request.POST['dept'].upper()
    names=title+name
    User=Staff.objects.create(name=names,designation=desig,gender=gender,subcode='abcd',department=dept)
    User.save()
    return staffed(request)


def deletion(request):
    a=request.POST.getlist('del')
    for i in a:
        Staff.objects.filter(id=i).delete()
    return staffed(request)

def edstaff(request):
    global name,exam1,sessions,dept,index1,index2,name2
    name=request.POST.getlist('staff')
    sessions=request.POST.getlist('session')
    k=0
    exam1=request.POST.getlist('examDuty')
    s={}
    e={}
    for i in sessions:
        m=i.split(":")
        s[m[0]]=m[1]
    for i in exam1:
        m=i.split(":")
        e[m[0]]=m[1]
    for i in index1:
        d=Staff.objects.filter(id=i).values()[0]['name']
        name2[d]={}
        name2[d]['dept']=(Staff.objects.filter(id=i).values()[0]['department'])
        name2[d]['session']=s[d]
        name2[d]['duty']=e[d]
    for i in index2:
        d=Staff.objects.filter(id=i).values()[0]['name']
        name2[d]={}
        name2[d]['dept']=(Staff.objects.filter(id=i).values()[0]['department'])
        name2[d]['session']=s[d]
        name2[d]['duty']=e[d]
    if user=='all':
            return render(request,'examtype2.html')
    return render(request,'finished.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('logout successfull'))
    return redirect('/')