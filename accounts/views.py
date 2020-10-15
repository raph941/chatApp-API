from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
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
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models.functions import Concat
from django.db.models import Q
from django.db.models import Value as V

import json


class usersListView(ListCreateAPIView):
    '''gets a list of user, or create a new user''' 
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    

class searchUserView(ListAPIView):
    '''gets a list of user, or create a new user''' 
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        query = self.request.GET.get('query')
        if query is not None:
            or_lookup_name = (
                Q(username__icontains=query) |
                Q(fullname__icontains=query)
            )
            queryset = User.objects.filter(or_lookup_name)
            return queryset
            
        return User.objects.none() 


class userView(RetrieveUpdateDestroyAPIView):
    ''' View for managing specific user '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


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

        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # import pdb ; pdb.set_trace()
        # user = authenticate(username=username, password=password)

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