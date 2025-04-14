from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from renter.forms import ClothPostForm


@login_required
def property_form_view(request):
    if request.method == "POST":
        # breakpoint()
        form = ClothPostForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Property Created Successfully!"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = ClothPostForm()
    return render(request, "property_form.html", {"form": form})