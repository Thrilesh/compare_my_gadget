from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gadget = models.ForeignKey('Gadget', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gadget.name} ({self.rating}/5)"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gadget = models.ForeignKey('Gadget', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.gadget.name}"


class Gadget(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True,
                             null=True)  # New brand field
    category = models.CharField(
        max_length=50,
        choices=[('mobiles', 'Mobiles'), ('tab', 'Tablets'),
                 ('laptop', 'Laptops'), ('computers', 'Computers')]
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)  # New price field
    ram = models.CharField(max_length=20, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    reviews_count = models.PositiveIntegerField(default=0)
    comparisons_count = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    release_date = models.DateField(blank=True, null=True)

    # Adding Image Field
    image = models.ImageField(
        upload_to='gadget_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.name}" if self.brand else self.name


class Review(models.Model):
    gadget = models.ForeignKey(
        Gadget, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.gadget.name}"
