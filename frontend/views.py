import json
import logging
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
# Create your views here.
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from admin_app.models import User
from admin_app.serializers import UserSerializer
from renter.forms import ClothPostForm

logger = logging.getLogger(__name__)
from datetime import datetime
# from django_ratelimit.decorators import ratelimit

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_new_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@login_required
def home(request):
    user = request.user
    # if user.is_borrower():
    #     return redirect("index.html")
    # if user.is_renter():
    #     return redirect("index.html")
    return render(request, "index.html")

@login_required
def aboutus(request):
    return render(request, 'subpage.html')

def rental_home(request):
    return render(request, 'rental_home.html')

# @ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if getattr(request, 'limited', False):
        return render(request, '429.html', status=429)

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(email=username_or_email).first()

        if user:
            username = user.username
        else:
            username = username_or_email

        user = authenticate(username=username, password=password)        


        if user is not None:
            login(request, user)
            logger.info(f"User Logged In>>>>>>>>>>>>>>>>>> : username: {user.username} email: {user.email} time: {datetime.now()}")
            return redirect("home")  # Redirect to home page or dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

@login_required
def ProfilePage(request):
    try:
        current_user = User.objects.get(username=request.user.username)
        return render(request, "profile.html", {"context": current_user})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")  # Optional error message


def forgetpasswordPage(request):
    return render(request, 'forget_password.html')

@csrf_exempt
def forgotpassword(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")

            if not username and not email:
                return JsonResponse({"error": "Please provide a username or email."}, status=400)

            user = User.objects.filter(username=username).first() if username else User.objects.filter(email=email).first()

            if not user:
                return JsonResponse({"error": "User not found."}, status=404)

            # Set and hash temporary password
            temporary_password = "please_change@123"
            user.set_password(temporary_password)  # Hash the password
            user.save()

            # Send email
            send_mail(
                "Temporary Password",
                f"Temporary password: {temporary_password}\n\n"
                "This is a system-generated password. Please change it after first login.",
                "dheeraj.systango@gmail.com",  # Sender
                [user.email],  # Recipient
                fail_silently=False,
            )

            return JsonResponse(
                {
                    "message": f"Temporary password has been sent to {user.email}. Please change it after first login."
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def changes_password_page(request):
    return render(request, "change_password_page.html")


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    # breakpoint()
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user  # Get logged-in user
            oldpassword = data.get("oldpassword")
            newpassword = data.get("newpassword")

            if not oldpassword or not newpassword:
                return JsonResponse(
                    {"detail": "Both old and new passwords are required."}, status=400
                )

            if not check_password(oldpassword, user.password):
                return JsonResponse(
                    {"detail": "Old password is incorrect."}, status=400
                )

            user.set_password(newpassword)  # Securely hash new password
            user.save()

            return JsonResponse({"detail": "Password updated successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON data."}, status=400)

    return JsonResponse({"detail": "Invalid request method."}, status=405)


def signup(request):
    return render(request, 'signup.html')

from admin_app.forms import SignupForm
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()
            login(request, user)
            logger.info(f"New user registered: {user.username}")
            return redirect("home")  # Redirect to homepage after signup
        return render(request, "signup.html", {"form": form})


#Chatbot
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # retrived_docs = retrieve_documents(user_message)
        # context = " ".join(retrived_docs) if retrived_docs else ""

        PROMPT = (f": \nYou are a assistant.\nThis is a rented cloths website where user can borrow or rent there cloths.\nso help them with there questions.\nAnswer questions related to docs which are in db or anything asked for.\n"
                  f"if user ask about the services tell them = we have 2 services 1. is rent your cloths 2. buy rented cloths\n if you are agree we will store your cloths in our rentbuy HUB and it will be stored there for 7 days and in between\n"
                  f"if any borrower rent your cloths the delivery charges will be free so feel free to rent and buy cloths.")
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": PROMPT},  # System prompt
                    {"role": "user", "content": user_message}],
                model="llama-3.1-8b-instant",
            )

            bot_reply = chat_completion.choices[0].message.content
            # breakpoint()
            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

#export GROQ_API_KEY="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"
from django.shortcuts import render

def chatbot_page(request):
    return render(request, 'chatbot.html')


@login_required
def cloth_form_view(request):
    if request.method == "POST":
        # breakpoint()
        form = ClothPostForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "cloth add post Created Successfully!"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = ClothPostForm()
    return render(request, "cloth_form.html", {"form": form})