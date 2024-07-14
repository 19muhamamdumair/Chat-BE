# chat/views.py

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Conversation, Message, UserProfile
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from rest_framework_simplejwt.backends import TokenBackend
import jwt


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        access_token = self.request.headers.get('Authorization').split()[1]  # Extracting the JWT token
        try:
            decoded_access_token = jwt.decode(access_token, options={"verify_signature": False})
            user_id = decoded_access_token['user_id']

            queryset = Conversation.objects.filter(Q(therapist_id=user_id) | Q(parent_id=user_id))
            return queryset

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token is expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({"error": "Invalid token format"}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        try:
            access_token = self.request.headers.get('Authorization').split()[1]
            decoded_access_token = jwt.decode(access_token, options={"verify_signature": False})
            user_id = decoded_access_token['user_id']
            
            if 'parent' in serializer.validated_data:
                serializer.save(parent_id=user_id)
                print('Saved with parent_id:', user_id)
            elif 'therapist' in serializer.validated_data:
                serializer.save(therapist_id=user_id)
                print('Saved with therapist_id:', user_id)
            else:
                return Response({"error": "You must specify either parent_id or therapist_id"},
                                status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token is expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({"error": "Invalid token format"}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        access_token = self.request.headers.get('Authorization').split()[1]  # Extracting the JWT token
        decoded_access_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id = decoded_access_token['user_id']

        instance = self.get_object()
        print('therapist_id user_id update :>> ', user_id)

        if instance.parent_id == user_id or instance.therapist_id == user_id:
            print('therapist_id user_id update :>> ', user_id)
            serializer.save()
        else:
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        access_token = self.request.headers.get('Authorization').split()[1]  # Extracting the JWT token
        decoded_access_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id = decoded_access_token['user_id']

        if instance.parent_id == user_id or instance.therapist_id == user_id:
            instance.delete()
            return Response({"message": "Conversation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.none()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        print("conversation_id:>> ", conversation_id)
        if conversation_id:
            # queryset = Message.objects.all()
            queryset = Message.objects.filter(conversation_id=conversation_id)
        else:
            queryset = Message.objects.none()
        return queryset

    def perform_create(self, serializer):
        file = self.request.data.get('file')
        if file:
            serializer.save(file=file)
        else:
            serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if username:
        user = authenticate(username=username, password=password)
    elif email:
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None
    else:
        return Response({"error": "Username or email is required"}, status=status.HTTP_400_BAD_REQUEST)

    print('user', user)
    if user is not None:
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_details = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user_profile.role,
            }

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_details['access_token'] = access_token
            user_details['refresh_token'] = refresh_token


            return Response(user_details)
        except UserProfile.DoesNotExist:
            return Response({"error": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'User not found or invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_conversation_status(request):
    conversation_id = request.data.get('conversation_id')
    new_status = request.data.get('status')
    
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.status = int(new_status)  # Ensure it's cast to an integer
        conversation.save()
        
        return Response({"message": "Conversation status updated successfully"}, status=status.HTTP_200_OK)
    
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_therapists(request):
    therapists = UserProfile.objects.filter(role='therapist')
    therapist_details = [
        {
            'username': therapist.user.username,
            'email': therapist.user.email,
            'first_name': therapist.user.first_name,
            'last_name': therapist.user.last_name,
            'role': therapist.role,
        } for therapist in therapists
    ]
    return Response(therapist_details)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_parents(request):
    parents = UserProfile.objects.filter(role='parent')
    parent_details = [
        {
            'username': parent.user.username,
            'email': parent.user.email,
            'first_name': parent.user.first_name,
            'last_name': parent.user.last_name,
            'role': parent.role,
        } for parent in parents
    ]
    return Response(parent_details)
