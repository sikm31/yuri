from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.
from django.http import HttpResponse
from rango.models import Category, UserProfile
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime


#def index(request):
#    context = RequestContext(request)
#    context_dict = {'boldmessage': "I am bold font from the context"}
#    return render_to_response('rango/index.html', context_dict, context)

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_category_list():
    cat_list = Category.objects.all()

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.all()
    cat_list = get_category_list()
    context_dict = {'categories': category_list}
    context_dict['cat_list'] = cat_list
    for category in category_list:
        category.url = encode_url(category.name)

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    #### NEW CODE ####
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    # Obtain our Response object early so we can add cookie information.
    return render_to_response('rango/index.html', context_dict, context)
    #category_list = Category.objects.order_by('-likes')[:5]
    #page_list = Page.objects.order_by('-views')[:5]
    #context_dict = {'categories': category_list, 'pages': page_list}

    #if request.session.test_cookie_worked():
    #    print (">>>> TEST COOKIE WORKED!")
     #   request.session.delete_test_cookie()
    #for category in category_list:
    #    category.url = category.name.replace(' ','_')
    #for category in category_list:
    #    category.url = encode_url(category.name)
    #return  render_to_response('rango/index.html', context_dict, context)
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    #visits = int(request.COOKIES.get('visits', '0'))

    # Does the cookie last_visit exist?
    #if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
     #   last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
     #   last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
      #  if (datetime.now() - last_visit_time).days > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
       #     response.set_cookie('visits', visits+1)
            # ...and update the last visit cookie, too.
        #    response.set_cookie('last_visit', datetime.now())
    #else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
     #   response.set_cookie('last_visit', datetime.now())

    # Return response back to the user, updating any cookies that need changed.
    #return response


def about(request):
    context = RequestContext(request)
    #context_dict = {'aboutmessage': "Here is the about page"}
    category_list = Category.objects.all()
    cat_list = get_category_list()
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict = {'categories': category_list, 'visits':count}
    context_dict['cat_list'] = cat_list
    return  render_to_response('rango/about.html', context_dict, context)
    #return HttpResponse('Rango says: Here is the about page. <a href="/rango/">Index</a>')

"""
    def category(request, category_name_url):
    context = RequestContext(request)
    #category_name = category_name_url.replace('_', ' ')
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)
"""
def category(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode_url(category_name_url)

    context_dict = {'cat_list': cat_list, 'category_name': category_name, 'category_name_url': category_name_url}

    try:
            category = Category.objects.get(name=category_name)

            # Add category to the context so that we can access the id and likes
            context_dict['category'] = category

            pages = Page.objects.filter(category=category)
            context_dict['pages'] = pages
    except Category.DoesNotExist:
            pass

    return render_to_response('rango/category.html', context_dict, context)

@login_required
def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)

            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:

                return render_to_response('rango/add_page.html', {}, context)

            page.views = 0
            page.save()

            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    category_list = Category.objects.all()
    cat_list = get_category_list()
    context_dict = {'categories': category_list}
    context_dict['cat_list'] = cat_list
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'cat_list': cat_list},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    context_dict = {}
    category_list = Category.objects.all()
    cat_list = get_category_list()
    context_dict = {'categories': category_list}
    context_dict['cat_list'] = cat_list


    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                #return HttpResponse("Your Rango account is disabled.")
                context_dict['disabled_account'] = True
                return render_to_response('rango/login.html', context_dict, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            #print ("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Invalid login details supplied.")
            print ("Invalid login details: {0}, {1}".format(username, password))
            context_dict['bad_details'] = True
            return render_to_response('rango/login.html', context_dict, context)
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('rango/login.html', context_dict, context)

@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    context = RequestContext(request)
    #context_dict = {'aboutmessage': "Here is the about page"}
    return  render_to_response('rango/restricted.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('rango/profile.html', context_dict, context)

@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes =  likes
            category.save()

    return HttpResponse(likes)