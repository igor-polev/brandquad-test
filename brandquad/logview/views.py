from django.shortcuts import render
from django.http import HttpResponse

# Main page
def index(request):
    return HttpResponse("Nothing here yet.")
