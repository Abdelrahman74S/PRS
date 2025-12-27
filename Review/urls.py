from django.urls import path
from .views import (
    ListCategoryAPIView,
    CreateCategoryAPIView,
    RetrieveUpdateDestroyCategoryAPIView,
    ListProductAPIView,
    CreateProductAPIView,
    ProductDetailAPIView,
    ListReviewAPIView,
    CreateReviewAPIView,
    RetrieveUpdateDestroyReviewAPIView,
    MyReviewedProductsListView,
    MyReviewsDetailListView,
    FavoriteProductView,
    ListFavoriteProductView,
    ReviewVoteView
)

urlpatterns = [
    # ---------------------------
    # Category URLs
    # ---------------------------
    path("categories/", ListCategoryAPIView.as_view(), name="category-list"),
    path("categories/create/", CreateCategoryAPIView.as_view(), name="category-create"),
    path(
        "categories/<slug:slug>/",
        RetrieveUpdateDestroyCategoryAPIView.as_view(),
        name="category-detail",
    ),
    # ---------------------------
    # Product URLs
    # ---------------------------
    path("products/", ListProductAPIView.as_view(), name="product-list"),
    path("products/create/", CreateProductAPIView.as_view(), name="product-create"),
    path(
        "products/<uuid:product_id>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # ---------------------------
    # Review URLs (nested under product)
    # ---------------------------
    path(
        "products/<uuid:product_id>/reviews/",
        ListReviewAPIView.as_view(),
        name="review-list",
    ),
    path(
        "products/<uuid:product_id>/reviews/create/",
        CreateReviewAPIView.as_view(),
        name="review-create",
    ),
    path(
        "reviews/<uuid:review_id>/",
        RetrieveUpdateDestroyReviewAPIView.as_view(),
        name="review-detail",
    ),
    path(
        "products/my-reviews/",
        MyReviewedProductsListView.as_view(),
        name="my-reviewed-products",
    ),
    path(
        "reviews/my-reviews/",
        MyReviewsDetailListView.as_view(),
        name="my-reviews-detail",
    ),
    # ---------------------------
    # favorite URLs 
    # ---------------------------
    path("products/<uuid:product_id>/favorite/", FavoriteProductView.as_view()),
    path("favorites/", ListFavoriteProductView.as_view(), name="favorite-list"),
    # ---------------------------
    # vote URLs 
    # ---------------------------
    path(
        "reviews/<uuid:review_id>/vote/", ReviewVoteView.as_view(), name="review-vote"
    ),
]