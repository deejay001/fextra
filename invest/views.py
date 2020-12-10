from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, WithdrawalForm
from .models import Coupon, Profile, Withdrawal, Wtype
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.http import Http404


# Create your views here.


def index(request):
    return render(request, 'landing/index.html')


def about(request):
    return render(request, 'landing/about.html')


def vendors(request):
    return render(request, 'landing/coupon.html')


def contact(request):
    return render(request, 'landing/contact.html')


def how(request):
    return render(request, 'landing/how.html')


def terms(request):
    return render(request, 'landing/terms.html')


def privacy(request):
    return render(request, 'landing/privacy.html')


def timer(request):
    return render(request, 'users/timer.html')


def sign_up(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        coupon = request.POST['coupon']
        ref_code = request.POST['referal']

        coupon = get_coupon(request, coupon, 'sign_up')

        if form.is_valid():

            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            profile = get_object_or_404(Profile, user=user)
            expire_date = datetime.now() + coupon.plan.time

            coupon.user = profile
            coupon.expire_on = expire_date
            coupon.save()

            add_ref(ref_code)

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "please fill in the required details")
    else:
        form = SignUpForm()

    user_num = User.objects.all().count()
    return render(request, 'landing/signup.html', {'form': form,
                                                   'user_num': user_num,
                                                   })


def get_coupon(request, code, loc):

    try:
        coupon = get_object_or_404(Coupon, code=code)

        if coupon.status == 1:
            messages.error(request, "Coupon already used")
            return redirect(loc)

        else:
            coupon.status = 1

    except Http404:
        messages.error(request, "Coupon code is not valid")
        return redirect(loc)

    return coupon


def add_ref(ref_code):

    try:
        profile = get_object_or_404(Profile, ref_code=ref_code)

    except Http404:
        return

    profile.ref_num += 1
    profile.save()


def log_in(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'landing/login.html')


def home_page(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        try:
            coupon = get_object_or_404(Coupon, user=profile)
        except Http404:
            coupon = None

        if coupon:
            expire_date = get_date(coupon)
        else:
            expire_date = None
        return render(request, 'users/index.html', {'profile': profile,
                                                    'coupon': coupon,
                                                    'date': expire_date,
                                                    })
    else:
        return redirect('log_in')


def invest(request):
    if request.method == "POST":
        code = request.POST['code']

        try:
            coupon = get_object_or_404(Coupon, code=code)
        except Http404:
            messages.error(request, "The coupon code is Invalid")
            return redirect('invest')

        profile = get_object_or_404(Profile, user=request.user)
        expire_date = datetime.now() + coupon.plan.time

        coupon.user = profile
        coupon.expire_on = expire_date
        coupon.save()
        return redirect('home')

    return render(request, 'users/invest.html')


def get_date(coupon):

    if coupon.status == 0 or coupon.status == 1:
        expire_date = coupon.expire_on
        year = expire_date.year
        month = expire_date.month
        day = expire_date.day

        hour = expire_date.hour
        minu = expire_date.minute
        sec = expire_date.second

        expire_date = "{}/{}/{} {}:{}:{}".format(year, month, day, hour, minu, sec)

        return expire_date
    else:
        return None


def withdraw(request, w_name):
    profile = get_object_or_404(Profile, user=request.user)
    w_type = Wtype.objects.get(name=w_name)

    if request.method == "POST":
        form = WithdrawalForm(request.POST)

        if w_name == "Coupon":

            coupon = get_object_or_404(Coupon, user=profile)
            cash = coupon.output
            profile = None

        else:
            profile = get_object_or_404(Profile, user=request.user)
            cash = profile.ref_num * 200
            coupon = None

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.name = request.user
            withdrawal.cash = cash
            withdrawal.w_type = w_type
            withdrawal.save()

            if coupon:
                coupon.delete()

            if profile:
                profile.ref_num = 0
                profile.save()

            return redirect('home')

        else:
            messages.error(request, "Please fill in the required details correctly")
            return redirect('w_draw')

    form = WithdrawalForm()
    return render(request, 'users/withdrawal.html', {'form': form,
                                                     'profile': profile,
                                                     'w_type': w_type,
                                                     })


def admine_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_staff:
                login(request, user)
                return redirect('admine')

            else:
                messages.error(request, "Only admins are allowed to login here")
                return redirect('a_login')

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('a_login')

    return render(request, 'admine/login.html')


def admine_page(request):
    user = request.user
    if user.is_authenticated and user.is_staff:
        withdrawals = Withdrawal.objects.order_by('-created_on')[:5]
        user_count = User.objects.all().count()

        today = date.today()
        last_week = today - timedelta(days=1)

        num_login = User.objects.filter(last_login__range=(last_week, today)).count()

        return render(request, 'admine/index.html', {'user': user,
                                                     'user_count': user_count,
                                                     'num_login': num_login,
                                                     'withdrawals': withdrawals})
    else:
        return redirect('a_login')


def check_with(request, w_name):
    w_type = Wtype.objects.get(name=w_name)
    withdrawals = Withdrawal.objects.filter(w_type=w_type)

    return render(request, 'admine/withdrawals.html', {'user': request.user,
                                                       'withdrawals': withdrawals,
                                                       'w_name': w_name})


def admin_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'admine/users.html', {'users': users})


def log_out(request):
    logout(request)
    return redirect('log_in')
