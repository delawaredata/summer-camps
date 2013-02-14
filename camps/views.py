from myproject.camps.models import *
from myproject.camps.forms import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout


def main_page(request):
    user = request.user
    new_account = False
    org = None
    if user.is_authenticated():
        try:
            org = Organization.objects.get(user=user)
        except:
            return redirect('myproject.camps.views.userlogout')
    if request.session.get('new_account'):
        new_account = request.session.get('new_account')
        request.session['new_account'] = False
    camps = Camp.objects.all()
    variables = RequestContext(request, {
        'camps': camps,
        'new_account': new_account,
        'org': org
    })
    return render_to_response('camps/main.html', variables)


def organization_page(request, org_id):
    pass


def edit_organization_page(request):
    user = request.user
    try:
        org = Organization.objects.get(user=user)
    except:
        org = None
    if user.is_authenticated():
        edit = True
        if request.method == 'POST':
            uf = EditUserForm(request.POST, prefix='user', instance=user)
            upf = OrganizationForm(request.POST, prefix='organization', instance=org)
            if uf.is_valid() and upf.is_valid():
                user = uf.save()
                userprofile = upf.save(commit=False)
                userprofile.user = user
                userprofile.save()
                request.session['message'] = "Organization info changed successfully."
                return redirect('myproject.camps.views.management_page')
        else:
            uf = EditUserForm(prefix='user', instance=user)
            upf = OrganizationForm(prefix='organization', instance=org)
        variables = RequestContext(request, {
            'edit': edit,
            'userform': uf,
            'userprofileform': upf
        })
        return render_to_response('camps/register.html', variables)
    else:
        return redirect('myproject.camps.views.org_login')


def change_password_page(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            cpf = ChangePasswordForm(request.POST)
            if cpf.is_valid():
                password = cpf.cleaned_data['password']
                user.set_password(password)
                user.save()
                request.session['message'] = "Password changed successfully."
                return redirect('myproject.camps.views.management_page')
        else:
            cpf = ChangePasswordForm()
        variables = RequestContext(request, {
            'change_pw_form': cpf
        })
        return render_to_response('camps/change_password.html', variables)
    else:
        return redirect('myproject.camps.views.org_login')


def delete_camp_page(request, camp_id):
    user = request.user
    camp = get_object_or_404(Camp, id=camp_id)
    if user.is_authenticated():
        if user == camp.organization.user:
            request.session['message'] = "%s was deleted." % camp.camp_name
            camp.delete()
            return redirect('myproject.camps.views.management_page')
        else:
            request.session['message'] = "Cannot delete camp that is not yours."
            return redirect('myproject.camps.views.management_page')
    else:
        return redirect('myproject.camps.views.org_login')


def edit_camp_page(request, org_id, camp_id):
    user = request.user
    org = get_object_or_404(Organization, id=org_id)
    camp = get_object_or_404(Camp, id=camp_id, organization=org)
    if user.is_authenticated():
        if user == camp.organization.user:
            if request.method == 'POST':
                cf = CampForm(request.POST, instance=camp)
                if cf.is_valid():
                    camp_name = cf.cleaned_data['camp_name']
                    cf.save()
                    request.session['message'] = "Successfully edited %s" % camp_name
                    return redirect('myproject.camps.views.management_page')
            else:
                cf = CampForm(instance=camp)
            variables = RequestContext(request, {
                'campform': cf,
                'camp': camp,
                'org': org
            })
            return render_to_response('camps/edit.html', variables)
        else:
            request.session['message'] = "Cannot edit camp that is not yours."
            return redirect('myproject.camps.views.management_page')
    else:
        return redirect('myproject.camps.views.org_login')


def add_camp_page(request):
    user = request.user
    org = get_object_or_404(Organization, user=user)
    if user.is_authenticated():
        if user == org.user:
            if request.method == 'POST':
                cf = CampForm(request.POST)
                if cf.is_valid():
                    camp_name = cf.cleaned_data['camp_name']
                    new_camp = cf.save(commit=False)
                    new_camp.organization = org
                    new_camp.save()
                    request.session['message'] = "Successfully added %s" % camp_name
                    return redirect('myproject.camps.views.management_page')
            else:
                cf = CampForm()
            variables = RequestContext(request, {
                'campform': cf,
                'org': org
            })
            return render_to_response('camps/edit.html', variables)
        else:
            request.session['message'] = "Cannot add camp to someone else's organization."
            return redirect('myproject.camps.views.management_page')
    else:
        return redirect('myproject.camps.views.org_login')


def management_page(request):
    user = request.user
    if user.is_authenticated():
        if request.session.get('message'):
            message = request.session.get('message')
            request.session['message'] = None
        else:
            message = None
        try:
            org = Organization.objects.get(user=user)
        except:
            return redirect('myproject.camps.views.edit_organization_page')
        variables = RequestContext(request, {
            'org': org,
            'message': message
        })
        return render_to_response('camps/manage.html', variables)
    else:
        return redirect('myproject.camps.views.org_login')


def userlogout(request):
    response = logout(request, next_page=reverse('myproject.camps.views.main_page'))
    return response


def org_login(request):
    if request.user.is_authenticated():
        return redirect('myproject.camps.views.main_page')
    else:
        state = "Please log in below..."
        username = password = ''
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('myproject.camps.views.management_page')
                else:
                    state = "Your acount is not active please contact the site."
            else:
                state = "Your username and/or password were incorrect."

        variables = RequestContext(request, {
            'state': state,
            'username': username
        })
        return render_to_response('camps/login.html', variables)


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = OrganizationForm(request.POST, prefix='organization')
        if uf.is_valid() and upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            request.session['new_account'] = True
            return redirect('myproject.camps.views.main_page')
    else:
        uf = UserForm(prefix='user')
        upf = OrganizationForm(prefix='organization')
    variables = RequestContext(request, {
        'userform': uf,
        'userprofileform': upf
    })
    return render_to_response('camps/register.html', variables)


def newsgate(request):
    if request.user.is_authenticated() and request.user.is_staff:
        art_camps = Camp.objects.filter(category="a").order_by('camp_name')
        day_camps = Camp.objects.filter(category="d").order_by('camp_name')
        edu_camps = Camp.objects.filter(category="e").order_by('camp_name')
        half_camps = Camp.objects.filter(category="h").order_by('camp_name')
        resid_camps = Camp.objects.filter(category="r").order_by('camp_name')
        sports_camps = Camp.objects.filter(category="s").order_by('camp_name')
        spring_camps = Camp.objects.filter(category="b").order_by('camp_name')

        variables = RequestContext(request, {
            'art_camps': art_camps,
            'day_camps': day_camps,
            'edu_camps': edu_camps,
            'half_camps': half_camps,
            'resid_camps': resid_camps,
            'sports_camps': sports_camps,
            'spring_camps': spring_camps
        })
        return render_to_response('camps/newsgate.html', variables, mimetype="text/plain")
    else:
        return redirect('myproject.camps.views.management_page')
