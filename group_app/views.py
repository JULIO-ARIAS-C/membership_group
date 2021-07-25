from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import request
import re
import bcrypt
from .models import User, Org

# Registration / Login Template
def main(request):
    return render(request, 'main.html')


# Creating a new user
def create_user(request):
    if request.method == "POST":
        
        # Validations for DB
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/main')

        # Create user in the DB
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['logged_user'] = new_user.id
        return redirect('/groups')

    return redirect('/main')


def create_org(request):
    if request.method == "POST":
        
        # Validations for DB
        errors = Org.objects.org_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/groups')

        # Create new organization in the DB
        new_org = Org(name=request.POST['name'], description=request.POST['description'])
        new_org.save()
        return redirect('/groups')

    return redirect('/groups')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user [0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/groups')
        messages.error(request, "Email or Password are incorrect. Please try again")

    return redirect("/main")


def groups(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!!!")
        return redirect('/main')

    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'all_org': Org.objects.all(),
        'all_members_orgs': User.objects.all(),
    }
    return render(request, 'groups.html', context)

def logout(request):
    request.session.flush()
    return redirect('/main')

def view_group(request, organization_id):
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'id_org': Org.objects.get(id=organization_id),
        'all_members_orgs': this_user.orgs.all(),
    }
    return render(request, 'view_group.html', context)