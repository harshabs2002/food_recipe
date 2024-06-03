from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from  django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name
PREDEFINED_CATEGORIES=[
    "Appetizers and Snacks",
    "Main Dishes",
    "Bread and Baked Goods",
    "Desserts",
    "Salads and Sides",
    "Soups and Stews",
    "Pasta and Pizza",
    "Drinks",
    "Chinese",
    "Healthy Options",
    "Cakes",
    "Not Specified"
]
@receiver(post_migrate)
def check_categories(sender,**kwargs):
    if Category.objects.count() == 0:
        for category_name in PREDEFINED_CATEGORIES:
            Category.objects.create(name=category_name)

class Recipe(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='receipe_image',default='default_recipe_image.svg',blank=True,null=True)
    description=models.TextField()
    cook_time = models.CharField(max_length=100)
    serving = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='instructions')
    step_number = models.PositiveIntegerField()
    instruction_text = models.TextField()

    class Meta:
        ordering=['step_number']

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

    GRAMS = 'GRAMS'
    KILOGRAMS ='KILOGRAMS'
    LITERS ='LITERS'
    TEASPOONS='TEASPOONS'
    TABLESPOONS='TABLESPOONS'
    CUPS ='CUPS'
    OUNCES='OUNCES'
    POUNDS='POUNDS'
    PIECES='PIECES'
    DEFAULT='NOT SPECIFIED'

    METRIC_CHOICES =[
        (GRAMS , 'GRAMS'),
        (KILOGRAMS ,'KILOGRAMS'),
        (LITERS ,'LITERS'),
        (TEASPOONS,'TEASPOONS'),
        (TABLESPOONS,'TABLESPOONS'),
        (CUPS ,'CUPS'),
        (OUNCES,'OUNCES'),
        (POUNDS,'POUNDS'),
        (PIECES,'PIECES'),
        (DEFAULT,'NOT SPECIFIED'),
    ]
    metric = models.CharField(max_length=20,choices=METRIC_CHOICES,default=DEFAULT)

    def __str__(self) :
        return f"{self.quantity}{self.get_metric_dispaly()}of {self.name}"