from django.http import HttpResponseRedirect
from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Category,Recipe,Ingredient,Instruction
from .forms import RecipeForm,IngredientForm,InstructionForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.
@login_required
def view_user_recipes(request):
        recipes =Recipe.objects.filter(created_by = request.user)
        return render(request,'recipe/view_user_recipes.html',{
           'title':'My recipes',
           'recipes' :   recipes ,
        })




@login_required
def view_recipes(request):
    query=request.GET.get('query','')
    category_id = request.GET.get('category',0)
    categories = Category.objects.all()
    recipes = Recipe.objects.all()

    if category_id :
       recipes = recipes.filter(category_id=category_id)

    if query:
        recipes = recipes.filter(Q(name__icontains = query) | Q(description__icontains = query))
    return render(request,'recipe/view_recipes.html',{
      'title':'Recipe',
      'recipes':recipes,
      'categories': categories,
    })
@login_required
def recipe_detail(request,recipe_primary_key):
    recipe = get_object_or_404(Recipe,pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
    return render(request,'recipe/recipe_detail.html',{
        'title':'Recipe Detail',
        'recipe':recipe,
        'ingredients':ingredients,
        'instructions':instructions,
    })
@login_required
def view_recipe_detail(request,recipe_primary_key):
    recipe = get_object_or_404(Recipe,pk=recipe_primary_key)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_primary_key)
    instructions = Instruction.objects.filter(recipe_id=recipe_primary_key)
    return render(request,'recipe/view_recipe_detail.html',{
        'title':'Recipe Detail',
        'recipe':recipe,
        'ingredients':ingredients,
        'instructions':instructions,
    })

@login_required
def create_recipe(request):
    if request.method == 'POST':
       form = RecipeForm(request.POST,request.FILES)

       if form.is_valid():
           recipe = form.save(commit=False)
           recipe.created_by = request.user
           recipe.save()
           messages.success(request,'Recipe created sucessfully')
       else:
           messages.error(request,'Failed to create ')
           
    else:
        form = RecipeForm()
    return render(request,'recipe/form.html',{
      'title':'Create Recipe',
      'form' : form ,
    })
@login_required
def update_recipe(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!!")
            
        
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipe/form.html', {
        'title': "Update Recipe",
        'form': form,
    })

@login_required
def delete_recipe(request,recipe_primary_key):
    recipe = get_object_or_404(Recipe,pk=recipe_primary_key,created_by =request.user)
    recipe.delete()

    messages.success(request,'Recipe deleted sucessfully')
    return redirect('core:home')

@login_required
def create_ingredient(request,recipe_primary_key):
    if request.method == 'POST':
       form = IngredientForm(request.POST)

       if form.is_valid():
           ingredient = form.save(commit=False)
           ingredient.recipe_id = recipe_primary_key
           ingredient.save()
           messages.success(request,'ingredient created sucessfully')
       else:
           messages.error(request,'Failed to create ingredient.')
           
    else:
        form =IngredientForm()
    return render(request,'recipe/form.html',{
       'title' : "Create Recipe Ingredient ",
       'form' : form
    })
@login_required
def update_ingredient(request,recipe_primary_key,ingredient_primary_key):
    recipe = get_object_or_404(Recipe,pk=recipe_primary_key,created_by =request.user)
    ingredient = get_object_or_404(Ingredient,pk=ingredient_primary_key,recipe=recipe)
    
    if request.method == 'POST':
       form = IngredientForm(request.POST,instance=ingredient)
       if form.is_valid():
            form.save()
            messages.success(request,"ingredient updated sucessfully!!")
       else:
            messages.error(request,"Failed to update")
    else:   
        form =IngredientForm(instance=ingredient)
    return render(request,'recipe/form.html',{
       'title' : "Update Recipe Ingredient ",
       'form' : form
    })
@login_required
def delete_ingredient(request, recipe_primary_key, ingredient_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_primary_key, recipe=recipe)
    ingredient.delete()

    messages.success(request, 'Ingredient deleted successfully')
    return HttpResponseRedirect(reverse('recipe:view_recipe_detail', args=(recipe_primary_key,)))

@login_required
def create_instruction(request, recipe_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            instruction = form.save(commit=False)
            instruction.recipe = recipe
            instruction.save()
            messages.success(request, 'Instruction created successfully')
        else:
            messages.error(request, 'Failed to create instruction')
    else:
        form = InstructionForm()
    return render(request, 'recipe/form.html', {
        'title': 'Create Instruction',
        'form': form,
    })

@login_required
def update_instruction(request, recipe_primary_key, instruction_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instruction = get_object_or_404(Instruction, pk=instruction_primary_key, recipe=recipe)
    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instruction updated successfully')
        else:
            messages.error(request, 'Failed to update instruction')
    else:
        form = InstructionForm(instance=instruction)
    return render(request, 'recipe/form.html', {
        'title': 'Update Instruction',
        'form': form,
    })

@login_required
def delete_instruction(request, recipe_primary_key, instruction_primary_key):
    recipe = get_object_or_404(Recipe, pk=recipe_primary_key, created_by=request.user)
    instruction = get_object_or_404(Instruction, pk=instruction_primary_key, recipe=recipe)
    instruction.delete()
    messages.success(request, 'Instruction deleted successfully')
    return HttpResponseRedirect(reverse('recipe:view_recipe_detail', args=(recipe_primary_key,)))