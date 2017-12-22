from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,'exam/index.html')

def regis(request):
    result = User.objects.regis_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/main')
    
    request.session['user_id'] = result.id
    messages.error(request, "Successfully registered!")
    return redirect('/travels')

def login(request):
    result = User.objects.login_validator(request.POST)
    if not result:
        messages.error(request, "login info invalid")
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/main')

def add(request):
    return render(request,'exam/add.html')

def createplans(request):
    if request.method == 'GET':        
        return render(request,'travels/add.html')
    if request.method == 'POST':
        errors = User.objects.plan_validator(request.POST)
    # if type(result) == list:
    #     for error in result:
    #         messages.error(request, error)
    #     return redirect('/add')
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags=tag )
        return redirect('/travels/add')

    else:
        startdate = datetime.strptime(request.POST['startdate'], '%Y-%m-%d')
        enddate = datetime.strptime(request.POST['enddate'], '%Y-%m-%d')

        Plan.objects.create(destination=request.POST["destination"],description=request.POST["description"],creator=User.objects.get(id=request.session['user_id']),startdate=startdate,enddate=enddate)

        return redirect('/travels')

def travels(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'userplans': User.objects.get(id=request.session['user_id']).joinplan.all(),
            'allplans': Plan.objects.exclude(follower=request.session['user_id']),
        }
        return render(request,'exam/result.html',context)

    except KeyError:
        return redirect('/main')

def join(request,planid):
    Plan.objects.get(id=planid).follower.add(User.objects.get(id=request.session['user_id']))
        
    return redirect('/travels')
    

def showuser(request,planid):

    trip = Plan.objects.get(id=planid)
    print trip.creator
    followers = trip.follower.all()
    context = {
        'trip': trip,
        'followers': followers,
    }
    return render(request,'exam/user.html',context)
