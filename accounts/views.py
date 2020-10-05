from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from serializers.user_serializer import UsersSerializer, UserSerializer
from accounts.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import views

import json


class usersListView(ListCreateAPIView):
    '''gets a list of user, or create a new user'''
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

class userView(RetrieveUpdateDestroyAPIView):
    ''' View for managing specific user '''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


class CustomLoginView(LoginView):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                data = {'id':user.id, 'username':user.username, 'email': user.email, 'fullname': user.fullname, 'image_url': user.image_url, 'token':token.key}
                # import pdb ; pdb.set_trace()
                print(data)
                return JsonResponse(status=200, data=data)
            else:               
                return JsonResponse(status=400 , data={'message':'your account is inactive, verify your email address or contact support'})
        else:
            return JsonResponse(status=400 , data={'message':'incorrect credentials provided, try again'})