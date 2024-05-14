import cloudinary
from rest_framework import serializers

from ecommerceapp.models import User, Store, Product, OrderDetail, Order, Comment


class StoreField(serializers.RelatedField):
    def to_representation(self, value):
        if value:
            return {"id": value.id, "name": value.name, "address": value.address, "active": value.active}
        else:
            return None


class UserSerializier(serializers.ModelSerializer):
    store = StoreField(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'store']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializier(read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'user', 'active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'store']

    def create(self, validated_data):
        validated_data['store'] = self.context['request'].user.store
        return super().create(validated_data)


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        exclude = ['active']


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)
    user = UserSerializier(read_only=True)

    class Meta:
        model = Order
        exclude = ['active']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializier()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user']