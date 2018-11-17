from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from .models import HouseModel, Property
from .forms import SearchForm, PropertyForm
from .utils import paginate, search_by


class HouseView(TemplateView):
    template_name = 'houses.html'
    limit = 10
    search_fields = ['house_name', 'house_city', 'house_neighborhood', 'house_id']

    def get(self, request):
        queryset = HouseModel.objects.all().order_by('house_name')
        search_form = SearchForm(request.GET)
        has_house = queryset.exists()
        search_found = has_house

        if search_form.is_valid():
            queryset = search_by(request, queryset, self.search_fields)
            search_found = queryset.exists()
        
        house = paginate(request, queryset, self.limit)

        return render(request, self.template_name, {'house': house, 'search_form': search_form,
            'search_found': search_found, 'has_house': has_house})


def home(request):
    photo = Property.objects.all()
    return render(request, 'home.html', { 'photo': photo })

def success(request):
    return render(request, 'success.html')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def form_photo_upload(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PropertyForm()
    return render(request, 'form_photo_upload.html', {
        'form': form
    })

def service(request):
    return render(request, 'service.html')
