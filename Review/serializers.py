from rest_framework import serializers
from .models import Category, Product, Review , FavoriteProduct , ReviewVote
from django.db.models import Avg
from accounts.models import UserProfile

# ---------------------------
# 1. Category Serializer
# ---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        fields = ['id', 'name', 'slug', 'is_active']
        read_only_fields = ['id', 'slug'] 

# ---------------------------
# 2. Review Serializer
# ---------------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')
    product_image = serializers.ReadOnlyField(source='product.image.url')
    
    class Meta:
        model = Review
        fields = ['review_id', 'user', 'product_name', 'comment', 'product_image', 'rating', 'created_at']
        read_only_fields = ['review_id', 'created_at','user', 'product_name','product_image']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def validate(self, attrs):
        request = self.context.get('request')
        view = self.context.get('view')
        
        if request and view and request.method == 'POST':
            product_id = view.kwargs.get('product_id')
            user = request.user
            if Review.objects.filter(product__product_id=product_id, user=user).exists():
                raise serializers.ValidationError("You have already reviewed this product!")
        
        return attrs

# ---------------------------
# 3. Product Serializer
# ---------------------------
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'product_id', 'user', 'category', 'category_name', 
            'name', 'description', 'price', 'image', 
            'average_rating', 'reviews_count', 'created_at' 
        ]
        
        read_only_fields = ['product_id', 'user', 'created_at', 'average_rating', 'reviews_count' ]

    def get_average_rating(self, obj):

        avg = obj.reviews_product.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0 

    def get_reviews_count(self, obj):
        return obj.reviews_product.count()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product" , "created_at"]  
        read_only_fields = ["id", "user", "product" , "created_at"] 

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data.get("product") 
        if not product:
            raise serializers.ValidationError("Product is required.")
        
        favorite, created = FavoriteProduct.objects.get_or_create(
            user=user, 
            product=product,
            defaults={"user": user, "product": product}
        )
        return favorite

class ReviewVoteSerializer(serializers.ModelSerializer):
    upvotes_count = serializers.SerializerMethodField()
    downvotes_count = serializers.SerializerMethodField()

    class Meta:
        model = ReviewVote
        fields = ['is_upvote', 'created_at' , 'upvotes_count', 'downvotes_count']
        read_only_fields = ['created_at' , 'upvotes_count', 'downvotes_count']

    def get_upvotes_count(self, obj):
        return obj.votes.filter(is_upvote=True).count()

    def get_downvotes_count(self, obj):
        return obj.votes.filter(is_upvote=False).count()