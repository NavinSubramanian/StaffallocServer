from django.shortcuts import render
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

user=''
date=[]
tot=0
exam=''
mselected_staff=[]
sitaf=[]
deptar=[]
depttar={}
fselected_staff=[]
rooms=[]
single=[]
girl=[]
name=[]
exam1=[]
sessions=[]

def login(request):
    return render(request,"login.html")


def download_multiple_files(request):
    global date,exam,tot,mselected_staff,fselected_staff,single,rooms,girl,user,exam1,sessions,name
    try:
        if exam=="END SEMESTER":
            file_paths=['Internal_Allocation.pdf','External_Allocation.pdf']
        else:
            file_paths = ['Invigilator_Shedule.pdf','Invigilator_Work_Count.pdf','merged_days.pdf']
        user=''
        date=[]
        tot=0
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
    name=request.POST['name']
    password=request.POST['password']
    confirmation=request.POST['confirmation']
    department=request.POST['department']
    email=request.POST['email']
    names=Users.objects.values_list('name')
    if name!='' and password==confirmation and name not in names[0]:
        user=Users(name=name,password=password,department=department,email=email)
        user.save()
    return render(request,"login.html")


def endsem1(request):
    global mselected_staff,fselected_staff
    print('end')
    print(repr(mselected_staff))
    print(fselected_staff)
    return render(request,'staffoption.html',{'mstaff':mselected_staff,'fstaff':fselected_staff})


def noend(request):
    pass


def logins(request):
    name=request.POST['name']
    global mselected_staff,user,fselected_staff,sitaf,deptar,depttar
    password=request.POST['password']
    names=Users.objects.filter(name=name).values()
    if (names[0]['name']=='admin4' and names[0]['password']==password):
        staff1=Staff.objects.exclude(Q(name__in=mselected_staff)|Q(name__in=fselected_staff)|Q(designation='HOD')).order_by().values()
        dept1=Staff.objects.values_list('department').distinct()
        sitaf=Staff.objects.values_list('name')
        deptar=Staff.objects.values_list('department')
        j = 0
        for i in sitaf:
            depttar[i[0]]=deptar[j][0]
            j += 1
        dept=[]
        for i in dept1:
            dept.append(i[0])
        user='all'
        return render(request,"edit2.html",{'mstaff':staff1,'dept':dept})
    elif (names[0]['name']==name and names[0]['password']==password):
        staff1=Staff.objects.filter(Q(department=names[0]['department'].upper())&Q(gender='M')).exclude(Q(name__in=mselected_staff)|Q(designation='HOD')).values()
        staff2=Staff.objects.filter(Q(department=names[0]['department'].upper())&Q(gender='F')).exclude(Q(name__in=fselected_staff)|Q(designation='HOD')).values()
        user=names[0]['department']
        return render(request,"staff.html",{'mstaff':staff1,'fstaff':staff2})
    return render(request,"login.html")


def admins(request):
        global user
        staff1=Staff.objects.exclude(Q(name__in=mselected_staff)|Q(name__in=fselected_staff)|Q(designation='HOD')).order_by().values()
        dept1=Staff.objects.values_list('department').distinct()
        dept=[]
        for i in dept1:
            dept.append(i[0])
        user='all'
        return render(request,"edit2.html",{'mstaff':staff1,'dept':dept})


def staffselection(request):
    global mselected_staff,fselected_staff
    selected=request.POST.getlist('staff_name')
    print('s')
    print(selected)
    for i in selected:
        staff=Staff.objects.filter(id=i).values()
        if staff[0]['gender']=='M':
            mselected_staff.append(staff[0]['name'])
            mselected_staff=list(set(mselected_staff))
        else:
            fselected_staff.append(staff[0]['name'])
            fselected_staff=list(set(fselected_staff))
        print(mselected_staff)
        print(fselected_staff)
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
        global date,exam,tot,mselected_staff,fselected_staff,single,rooms,girl,name,sessions,exam1,depttar
        date=request.POST['date'].split()
        exam=request.POST['exam']
        tot=int(request.POST['tot'])
        if exam=="END SEMESTER":
            print(name,date[0],sessions,exam1)
            endsem(name,date[0],sessions,exam1,depttar)
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
    global name,exam1,sessions
    name=request.POST.getlist('staff')
    sessions=request.POST.getlist('session')
    exam1=request.POST.getlist('examDuty')
    print(name)
    if user=='all':
        return render(request,'examtype2.html')
    return render(request,'finished.html')