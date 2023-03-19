from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'supchik': {
        'бульон, л': 2,
        'картофель, кг': 0.3,
        'морковь, кг': 0.2,
        'лапша, кг': 0.4,
        'лавровый лист, шт': 1,
    }
}


def recipe(request):
    context = {
        'recipes': [meal for meal in DATA]
    }
    return render(request, 'calculator/recipes.html', context)


def omlet(request):
    servings = int(request.GET.get('servings', 1))
    recipe = {product: amount * servings for product, amount in DATA.get('omlet').items()}
    context = {
        'recipe': recipe,
    }
    return render(request, 'calculator/index.html', context)


def pasta(request):
    servings = int(request.GET.get('servings', 1))
    recipe = {product: amount * servings for product, amount in DATA.get('pasta').items()}
    context = {
        'recipe': recipe,
    }
    return render(request, 'calculator/index.html', context)


def buter(request):
    servings = int(request.GET.get('servings', 1))
    recipe = {product: amount * servings for product, amount in DATA.get('buter').items()}
    context = {
        'recipe': recipe,
    }
    return render(request, 'calculator/index.html', context)


def supchik(request):
    servings = int(request.GET.get('servings', 1))
    recipe = {product: amount * servings for product, amount in DATA.get('supchik').items()}
    context = {
        'recipe': recipe,
    }
    return render(request, 'calculator/index.html', context)
