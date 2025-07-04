from django.shortcuts import render, get_object_or_404, redirect
from .models import Gadget, Review, WishlistItem
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm
from django.contrib.auth.decorators import login_required


def gadget_detail(request, gadget_id):
    gadget = get_object_or_404(Gadget, id=gadget_id)
    reviews = gadget.reviews.all()  # Fetch all reviews for this gadget

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.gadget = gadget
            review.user = request.user
            review.save()
            # Refresh page after submission
            return redirect('gadget_detail', gadget_id=gadget.id)
    else:
        form = ReviewForm()

    return render(request, "gadget_detail.html", {
        "gadget": gadget,
        "reviews": reviews,
        "form": form
    })


def user_login(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Get the next parameter or default to home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Add login_required to the home view to ensure authentication


@login_required
def home(request):
    query = request.GET.get('search', '')
    gadgets = Gadget.objects.filter(
        name__icontains=query) if query else Gadget.objects.all()

    most_reviewed = Gadget.objects.order_by('-reviews_count')[:5]
    most_compared = Gadget.objects.order_by('-comparisons_count')[:5]
    top_rated = Gadget.objects.order_by('-average_rating')[:5]
    latest_gadgets = Gadget.objects.order_by('-release_date')[:5]

    context = {
        'gadgets': gadgets,
        'query': query,
        'most_reviewed': most_reviewed,
        'most_compared': most_compared,
        'top_rated': top_rated,
        'latest_gadgets': latest_gadgets,
    }

    return render(request, 'index.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to home after logout


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def compare_gadgets(request):
    # Get the 'gadgets' query parameter and split it into a list
    gadget_ids = request.GET.get('gadgets', '').split(',')

    # Convert each gadget_id to an integer, ignoring empty strings
    gadget_ids = [int(gadget_id)
                  for gadget_id in gadget_ids if gadget_id.isdigit()]

    # Fetch gadgets from the database by their IDs
    gadgets = Gadget.objects.filter(id__in=gadget_ids)

    # Pass the gadgets to the template
    return render(request, 'compare.html', {'gadgets': gadgets})


def reviews(request):
    gadgets = Gadget.objects.all()
    reviews = Review.objects.all().order_by(
        '-created_at')  # Assuming a Review model exists
    return render(request, 'reviews.html', {'reviews': reviews, 'gadgets': gadgets})


@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})
