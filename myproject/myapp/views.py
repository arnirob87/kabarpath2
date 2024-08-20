from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm, ApplicationForm, PostForm, CommentForm, ProductForm
from .models import User, Referral, Product, Post, Like, Withdrawal
from django.contrib.auth.decorators import user_passes_test

POINT_CONVERSION_RATE = 1000

def user_can_create_post(user):
    return user.is_authenticated and user.can_create_post

def user_can_create_product(user):
    return user.is_authenticated and user.can_create_product

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            referral_id = form.cleaned_data.get('referral_id')
            if referral_id:
                try:
                    referrer = User.objects.get(phone_number=referral_id)
                    Referral.objects.create(referrer=referrer, referred=user)
                    update_referrer_level(referrer)
                    referrer.points += 5  # Add 5 points to the referrer
                    referrer.save()
                except User.DoesNotExist:
                    pass
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    referrals = user.referrals.all()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'profile.html', {'user': user, 'referrals': referrals, 'form': form})

@login_required
def decorative_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'decorative_profile.html', {'user': user, 'form': form})

@login_required
def referral_list(request):
    referrals = request.user.referrals.all()
    return render(request, 'referral_list.html', {'referrals': referrals})

@login_required
def referred_by(request):
    referred_by = request.user.referred_by.all()
    return render(request, 'referred_by.html', {'referred_by': referred_by})

def update_referrer_level(referrer):
    referral_count = referrer.referrals.count()
    if referral_count >= 10:
        referrer.level = (referral_count // 10) + 1
        referrer.save()

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again.")
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out. Thanks for visiting!")
    return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'user_profile.html', {'user': user})

@login_required
def apply_for_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.product = product
            application.save()
            messages.success(request, "Application submitted successfully.")
            return render(request, 'application_success.html')
    else:
        form = ApplicationForm()
    return render(request, 'apply_for_product.html', {'form': form, 'product': product})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    is_liked = False
    if request.user.is_authenticated:
        if post.likes.filter(user=request.user).exists():
            is_liked = True
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'is_liked': is_liked})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = False
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
        messages.success(request, "Post unliked.")
    else:
        Like.objects.create(user=request.user, post=post)
        messages.success(request, "Post liked.")
        is_liked = True
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "Post updated successfully.")
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'post': post})
    else:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post_detail', pk=post.pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('post_list')
        return render(request, 'blog/post_delete_confirm.html', {'post': post})
    else:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_detail', pk=post.pk)

@login_required
@user_passes_test(user_can_create_post)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def ledger(request):
    user = request.user
    withdrawals = Withdrawal.objects.filter(user=user)

    # Calculate points
    processed_withdrawals = withdrawals.filter(is_processed=True)
    total_withdrawn_points = sum(withdrawal.points for withdrawal in processed_withdrawals)

    # Remaining points and balance
    remaining_points = user.points - total_withdrawn_points
    remaining_balance = remaining_points * POINT_CONVERSION_RATE

    return render(request, 'ledger.html', {
        'withdrawals': withdrawals,
        'remaining_points': remaining_points,
        'remaining_balance': remaining_balance,
    })

@login_required
def withdraw_points(request):
    user = request.user
    # Calculate remaining points
    withdrawals = Withdrawal.objects.filter(user=user, is_processed=True)
    total_withdrawn_points = sum(withdrawal.points for withdrawal in withdrawals)
    remaining_points = user.points - total_withdrawn_points

    if request.method == 'POST':
        points = int(request.POST.get('points'))
        if points <= remaining_points and points > 0:
            Withdrawal.objects.create(
                user=user,
                points=points,
                money_amount=points * POINT_CONVERSION_RATE,
                is_processed=False
            )
            messages.success(request, "Your withdrawal request has been submitted.")
            return redirect('ledger')
        else:
            messages.error(request, "Invalid points amount.")
            return redirect('withdraw_points')

    return render(request, 'withdraw_point.html', {
        'remaining_points': remaining_points,
    })

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    withdrawal_requests = Withdrawal.objects.filter(is_processed=False)
    return render(request, 'admin.html', {'users': users, 'withdrawal_requests': withdrawal_requests})

@user_passes_test(is_superuser)
def toggle_permission(request, user_id, permission):
    user = get_object_or_404(User, id=user_id)
    if permission == 'post':
        user.can_create_post = not user.can_create_post
    elif permission == 'product':
        user.can_create_product = not user.can_create_product
    user.save()
    return redirect('admin_dashboard')

@user_passes_test(is_superuser)
def process_withdrawal(request, withdrawal_id):
    withdrawal_request = get_object_or_404(Withdrawal, id=withdrawal_id)
    withdrawal_request.is_processed = True
    withdrawal_request.save()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(user_can_create_product)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product created successfully.")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})
