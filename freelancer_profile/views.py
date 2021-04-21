
import re

from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup


from .models import Freelancer
from .forms import FreelancerForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = FreelancerForm(request.POST)
        if form.is_valid():
            data = form.save()
            messages.success(
                request, 'Data of  {} has been added!'.format(data.name))
    else:
        form = FreelancerForm()

    context = {
        'freelancers': Freelancer.objects.all(),
        'form': form,


    }
    return render(request, 'freelancer_profile/index.html', context=context)


def search_data(request):
    search = request.POST.get("search")
    form = FreelancerForm()
    try:
        freelancers = Freelancer.objects.filter(name__icontains=search)
    except:
        freelancers = None

    context = {
        'freelancers': freelancers,
        'form': form,
    }
    return render(request, 'freelancer_profile/search.html', context=context)


def get_behance_images(request, id):

    user = get_object_or_404(Freelancer, pk=id)
    html = urlopen(user.url)
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src': re.compile('.jpg')})
    img_urls = []
    print(images)
    for image in images:
        img_urls.append(image['src'])
        
        print(image['src']+'\n')

    context = {
        'freelancer': user,
        'all_images': img_urls,
    }
    return render(request, 'freelancer_profile/get_images.html', context=context)
