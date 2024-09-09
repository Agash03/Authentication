from rest_framework import serializers
from authapp.models import MyUser
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password', 'write_only': True})

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # These methods should be inside the class, indented correctly
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'password2': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        # Remove password2 from validated_data
        del validated_data['password2']
        return MyUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    class Meta:
        model = MyUser
        fields = ['email', 'password']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['name','email','phone']
        
class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only= True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only= True)
    class Meta:
        model = MyUser
        fields = ['password','password2'] 
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and confim Password does not match')
        user.set_password(password)
        user.save()
        return attrs
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields =['email']
        
    def  validate(self, attrs):
        email = attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID:',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link = 'http://localhost:2000/api/user/resetpass/',uid+'/'+token  
            print('password reset link',link)
            link = str(link)  # Convert to string if it's not already
            body = 'Click the following link to reset your password' + link
            
            data = {
                'subject': 'Reset your password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            
            
            return attrs      
        else:  
            raise serializers.ValidationError('you are not a registered user')
        
        
class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only= True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only= True)
    class Meta:
        model = MyUser
        fields = ['password','password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token= self.context.get('token')
        if password != password2:
            raise serializers.ValidationError('password and confim Password does not match')
        id = smart_str(urlsafe_base64_decode(uid))
        user = MyUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('invalid token')
        user.set_password(password)
        user.save()
        return attrs