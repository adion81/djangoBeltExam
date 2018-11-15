from django.shortcuts import render, HttpResponse, redirect
from time import strftime, strptime
from apps.author_quotes.models import *
from django.contrib import messages

def index(request):
    return render(request, "author_quotes/index.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    emailCheck = []
    for user in User.objects.all():
        emailCheck.append(user.email)
    if request.POST['email'] in emailCheck:
        errors['duplicate'] = "That email is already in use"
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        print('*'*20)
        print(user.id)
        request.session['user'] = user.id
        print(request.session['user'])
        print('*'*20)
        return redirect('/quotes')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['login_email'])
        print(user.id)
        request.session['user'] = user.id
        return redirect('/quotes')

def quotes(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user'])
        postQuote = []
        for quote in Quote.objects.all():
            q = Quote.objects.get(id=quote.id)
            QuoteToPost = {
                'id' : quote.id,
                'author' : quote.author,
                'quote' : quote.quote,
                'posted_by' : User.objects.get(id=quote.posted_by_id).first_name,
                'current_user' : User.objects.get(id=request.session['user']),
                'delete_id' : User.objects.get(id=quote.posted_by_id),
                'likes' : q.likes.all().count()
            }
            print(QuoteToPost['delete_id'].id)
            postQuote.append(QuoteToPost)
        print(user.first_name)
        context = {
            'user' : user,
            'postQuote' : postQuote
        }
        return render(request, "author_quotes/quotes.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def myaccount(request, id):
    if 'user' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user'])
        context = {
            'user' : user
        }
    return render(request, "author_quotes/myaccount.html", context)

def myaccount_errors(request):
    if 'user' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user'])
        context = {
            'user' : user
        }
    return render(request, "author_quotes/myaccount.html", context)

def edit(request, id):
    errors = User.objects.edit_validator(request.POST)
    emailCheck = []
    user = User.objects.get(id=request.session['user'])
    for otherUser in User.objects.all():
        if otherUser.id == request.session['user']:
            continue
        else:
            emailCheck.append(otherUser.email)
    if request.POST['edit_email'] in emailCheck:
        errors['duplicate'] = "That email is already in use"
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/myaccount_errors')
    else:
        user = User.objects.get(id=request.session['user'])
        user.first_name = request.POST['edit_first_name']
        user.last_name = request.POST['edit_last_name']
        user.email = request.POST['edit_email']
        user.save()
        return redirect('/quotes')

def create(request, id):
    errors = Quote.objects.quote_validator(request.POST)
    if request.POST['quote'] in Quote.objects.all():
        errors['duplicate'] = "That quote was already posted"
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/quotes')
    else:
        user = User.objects.get(id=request.session['user'])
        Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], posted_by=User.objects.get(id=request.session['user']))

        return redirect('/quotes')

def show(request, id):
    print(id)
    quote = Quote.objects.get(id=id)
    print(quote.id)
    this_user = User.objects.get(id=quote.posted_by_id)
    postQuote = []
    for quote in Quote.objects.all():
        QuoteToPost = {
            'id' : quote.id,
            'author' : quote.author,
            'quote' : quote.quote,
            'posted_by' : User.objects.get(id=quote.posted_by_id).first_name
        }
        postQuote.append(QuoteToPost)

    print(this_user.first_name)
    context = {
        'this_user' : this_user,
        'postQuote' : postQuote
    }
    print(postQuote)
    return render(request, "author_quotes/show.html", context)

def delete_quote(request,id):
    quote = Quote.objects.get(id=id)
    quote.delete()
    return redirect('/quotes')

def like(request, id):
    likeUpdate = Quote.objects.get(id=id)
    u = User.objects.get(id=request.session['user'])
    likeUpdate.likes.add(u)
    likeUpdate.save()
    return redirect('/quotes')
# Create your views here.
