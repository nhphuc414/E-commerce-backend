from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, parsers, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ecommerceapp import serializers, perms, paginators
from ecommerceapp.models import User, Store, Product, Order, OrderDetail, Comment, Like


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializier
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action in ['current_user', 'get_orders']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializier(request.user).data)

    @action(methods=['get'], url_path='orders', detail=False)
    def get_orders(self, request):
        orders = Order.objects.filter(user=request.user)
        # Serialize the orders
        serializer = serializers.OrderViewSerializer(orders, many=True)
        return Response(serializer.data)


class StoreViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer

    def get_permissions(self):
        if self.action in ['get_inactive', 'confirm', 'reject']:
            return [perms.StaffOrSuperUserAuthenticated()]

        return [permissions.IsAuthenticated()]

    @action(methods=['get'], url_path='inactive-store', url_name='inactive-store', detail=False)
    def get_inactive(self, request):
        inactive_stores = Store.objects.filter(active=False)
        serializer = serializers.StoreSerializer(inactive_stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='products', url_name='products', detail=True)
    def products(self, request, pk):
        products = self.get_object().products.filter(active=True).all()

        return Response(serializers.ProductSerializer(products, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='confirm-store', url_name='confirm-store', detail=True)
    def confirm(self, request, pk):
        store = self.get_object()
        store.active = True
        store.save()
        return Response({'message': 'Store confirmed successfully'}, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='reject-store', url_name='reject-store', detail=True)
    def reject(self, request, pk):
        store = self.get_object()
        store.delete()
        return Response({'message': 'Store rejected and deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.UpdateAPIView, generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny()]
    parser_classes = [parsers.MultiPartParser]
    pagination_class = paginators.ProductsPaginator

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [perms.StoreOwnerAuthenticated()]
        if self.action in ['add_comment', 'rating']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        address = self.request.query_params.get('address', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if address:
            queryset = queryset.filter(store__address__icontains=address)

        return queryset

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, product=self.get_object(), content=request.data.get('content'))
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], url_path='comments', url_name='comments', detail=True)
    def comments(self, request, pk):
        comments = self.get_object().comment_set.filter(active=True).all()

        return Response(serializers.CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class PlaceOrderViewSet(viewsets.ViewSet, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PlaceOrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order_details_data = request.data.pop('order_details')
        order_data = request.data
        serializer = serializers.OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            # Validate and create OrderDetails within the transaction
            for detail_data in order_details_data:
                detail_serializer = serializers.OrderDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save(Order=order, product_id = detail_data["product_id"])
                else:
                    transaction.set_rollback(True)
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.OwnerAuthenticated]

    def get_permissions(self):
        if self.action in ['like']:
            return [permissions.IsAuthenticated()]

        return [perms.OwnerAuthenticated()]

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, comment=self.get_object())
        if not created:
            like.active = not like.active
            like.save()
        return Response(serializers.LessonDetailsSerializer(self.get_object(), context={'request': request}).data,
                        status=status.HTTP_200_OK)