from .models import (
    Category, 
    Product, 
    Review, 
    FavoriteProduct,
    ReviewVote
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    FavoriteSerializer,
    ReviewVoteSerializer
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permission import IsAdminOrOwner
from rest_framework.pagination import PageNumberPagination
from .filterset import ProductFilter, ReviewFilter, CategoryFilter
from .throttling import ReviewCreateThrottle, ProductListThrottle
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

# Create your views here.

# ---------------------------
# Category Views
# ---------------------------
class ListCategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100
    filterset_class = CategoryFilter

    @method_decorator(cache_page(60 * 15, key_prefix="category_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time

        time.sleep(2) 
        return super().get_queryset()


class CreateCategoryAPIView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RetrieveUpdateDestroyCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated, IsAdminUser]


# ---------------------------
# Product Views
# ---------------------------
class ListProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    throttle_classes = [ProductListThrottle]
    pagination_class = PageNumberPagination
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 10

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreateProductAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_id"
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_update(self, serializer):
        serializer.save()


# ---------------------------
# Review Views
# ---------------------------
class ListReviewAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 10
    filterset_class = ReviewFilter
    throttle_classes = [ReviewCreateThrottle]

    @method_decorator(cache_page(60 * 15, key_prefix="Review_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return Review.objects.filter(product__product_id=product_id)


class CreateReviewAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, product_id=product_id)
        serializer.save(user=self.request.user, product=product)


class RetrieveUpdateDestroyReviewAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "review_id"
    permission_classes = [IsAuthenticated, IsAdminOrOwner]


class MyReviewedProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(reviews_product__user=user)


class MyReviewsDetailListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class FavoriteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = FavoriteSerializer(
            data={"product": product.product_id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        FavoriteProduct.objects.filter(user=request.user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFavoriteProductView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)


class ReviewVoteView(generics.CreateAPIView):
    serializer_class = ReviewVoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        user = self.request.user
        is_upvote = serializer.validated_data.get('is_upvote')

        existing_vote = ReviewVote.objects.filter(review=review, user=user).first()

        if existing_vote:
            if existing_vote.is_upvote == is_upvote:
                existing_vote.delete()
                raise ValidationError("Vote removed.") 
            else:
                existing_vote.is_upvote = is_upvote
                existing_vote.save()
                return 
        
        serializer.save(user=user, review=review)