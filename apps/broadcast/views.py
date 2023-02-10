from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .forms import BroadcastForm
from .classifier import predict_sentiment
from .models import Broadcast
from .serializer import BroadcastSerializer


def broadcast(request):
    if request.method == 'POST':
        form = BroadcastForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.cleaned_data['message']
            classifier_msg = predict_sentiment(message)
            # send message to all users
            context = {
                'status': 'ok',
                'message': message,
                'classification': classifier_msg
            }
            return JsonResponse(context)

    else:
        form = BroadcastForm(user=request.user)
    return render(request, 'broadcast/broadcast.html', {'form': form})


class BroadcastApiView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, email):
        try:
            broadcast = Broadcast.objects.get(email=email)
            # only return the all messages
            messages = BroadcastSerializer(broadcast).data
            return Response(messages, status=200)
        except Broadcast.DoesNotExist:
            return JsonResponse({'message': 'The broadcast does not exist'}, status=404)

    def post(self, request, email):
        if email != 'create':
            return Response({'message': 'Invalid request.'}, status=400)

        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')

        try:
            broadcast = Broadcast.objects.get(email=email)
            return Response({'message': 'Broadcast already exists.'}, status=400)
        except Broadcast.DoesNotExist:
            classification = predict_sentiment(message)
            broadcast = Broadcast.objects.create(
                name=name,
                email=email,
                message=message,
                classification=classification,
            )
            messages = {
                'success': 'Data created successfully.',
                'data': {
                    'name': broadcast.name,
                    'email': broadcast.email,
                    'message': broadcast.message,
                    'classification': broadcast.classification,
                },
            }
            return Response(messages, status=201)

    def put(self, request, email):
        try:
            broadcast = Broadcast.objects.get(email=email)
        except Broadcast.DoesNotExist:
            message = {
                'status': 'error',
                'message': 'Broadcast does not exist.',
                'note': 'Please create a broadcast first.',
                'url': 'api/broadcast/create/',
                'method': 'POST',
                'data': {
                    'name': 'string',
                    'email': 'string',
                    'message': 'string',
                }
            }
            return Response(message, status=400)
        name = broadcast.name
        email = broadcast.email
        message = request.data.get('message')
        classification = predict_sentiment(message)
        data = {
            'name': name,
            'email': email,
            'message': message,
            'classification': classification,
        }
        serializer = BroadcastSerializer(data=data)
        if serializer.is_valid():
            serializer.update(broadcast, serializer.validated_data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


def api_docs(request):
    return render(request, 'broadcast/api_docs.html')