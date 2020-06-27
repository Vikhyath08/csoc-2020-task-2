from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book = Book.objects.get(pk = bid)
    num_available = BookCopy.objects.filter(status__exact = True, book__exact = book).count()
    context = {
        'book': book, # set this to an instance of the required book
        'num_available': num_available, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    if len(get_data) > 0:
        books = Book.objects.filter(title__icontains = get_data['title'], author__icontains = get_data['author'], genre__icontains = get_data['genre'])
    else:
        books = Book.objects.all()
    context = {
        'books': books, # set this to the list of required books upon filtering using the GET parameters 
        # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books = BookCopy.objects.filter(borrower__exact = request.user)
    context = {
        'books': books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    


    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    bid = request.POST.get('bid')
    book = BookCopy.objects.filter(status__exact = True, book__exact = Book.objects.get(pk = bid))
    message = 'success' if book else 'failure'
    if message == 'success':
        book[0].borrow_date = datetime.date.today()
        book[0].status = False
        print(book[0].status)
        book[0].borrower = request.user
        book[0].save()

    response_data = {
        'message': message,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    bid  = request.POST.get('bid')
    book = BookCopy.objects.get(pk = bid)
    if book:
        message = 'success'
        book.borrow_date = None
        book.status = True
        book.borrower = None
        book.save()
    else:
        message = 'failure'
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)
    

@login_required
def rateBookView(request, bid):
    book = Book.objects.get(pk = bid)
    try:
        usrRating = float(request.POST.get('rating'))
    except:
        messages.error(request, "Please Enter a Valid Rating")
        return redirect(f'/book/{bid}/')
    if usrRating <= 10 and usrRating >= 0:
        oldRating = Ratings.objects.filter(book__exact = book, borrower__exact = request.user)
        print(oldRating)
        if oldRating.exists():
            oldRating = Ratings.objects.get(book__exact = book, borrower__exact = request.user)
            oldRating.rating = usrRating
            oldRating.save()
            print("New Rating:", oldRating)
        else:
            Ratings.objects.create(book = book, borrower = request.user, rating = usrRating)
            print("New Rating Registered")
        messages.success(request, 'Your Rating has been registered successfully!')
    else:
        messages.error(request,'Please Enter A Valid Rating')
    ratingsOfBook = Ratings.objects.filter(book__exact = book)
    if ratingsOfBook.exists():
        avg = 0
        i = 0
        for ratingOfBook in ratingsOfBook:
            i+=1
            avg = avg + ratingOfBook.rating
        avg = avg / i
        book.rating = avg
        book.save()
    return redirect(f'/book/{bid}/')

