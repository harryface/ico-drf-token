from rest_framework import serializers

from .models import Bid, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    
class BidSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bid
        exclude = ['created_at', 'user', 'unit_price']
        
    def validate(self, data):
        """
        Check that the number_of_tokens is greater than bidding_price.
        """
        if data['number_of_tokens'] > data['bidding_price']:
            raise serializers.ValidationError("Number of tokens cannot be greater than Bidding price!")
        return data
        
        
class ExternalBidPopulateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bid
        exclude = ['unit_price']
        
    def validate(self, data):
        """
        Check that the number_of_tokens is greater than bidding_price.
        """
        if data['number_of_tokens'] > data['bidding_price']:
            raise serializers.ValidationError("Number of tokens cannot be greater than Bidding price!")
        return data