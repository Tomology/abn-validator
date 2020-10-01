from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .utils import abn_validator, excel_style_letters
import pandas as pd

# Create your views here.


def upload_file(request, *args, **kwargs):
    return render(request, 'landing.html', {})


def data_preview(request, *args, **kwargs):
    if request.method == "POST":

        # Assign form data to variables
        orientation = request.POST.get("orientation")

        # Save uploaded file
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_location = fs.path(name)
        file_url = fs.url(name)

        # Initialise context variables
        headings = None
        values = None
        excel_letters_column = None
        excel_letters_row = None

        # Open workbook and assign values for preview
        if (orientation == 'columns'):
            wb = pd.read_excel(fs.path(name), header=None).fillna('')
            values = wb.values.tolist()[:10]
            if len(values) > 0:
                excel_letters_column = excel_style_letters(len(values[0]))
            else:
                excel_letters_column = None
        else:
            wb = pd.read_excel(fs.path(name), header=None).fillna('')
            values = []
            for arrays in wb.values.tolist():
                values.append(arrays[:10])
            if len(values) > 0:
                excel_letters_row = excel_style_letters(len(values[0]))
            else:
                excel_letters_row = None
    else:
        headings = None
        values = None
        excel_letters_row = None
        excel_letters_column = None
        file_location = None
        file_url = None
        orientation = None
    context = {
        'file_location': file_location,
        'file_url': file_url,
        "orientation": orientation,
        'excel_letters_column': excel_letters_column,
        'excel_letters_row': excel_letters_row,
        'headings': headings,
        'values': values
    }
    return render(request, 'data_preview.html', context)


def results(request, *args, **kwargs):
    if request.method == "POST":
        file_location = request.POST.get("file_location")
        file_url = request.POST.get("file_url")
        first_row_headings = request.POST.get("first_row_headings")
        orientation = request.POST.get("orientation")
        abn_index = request.POST.get("abn_index")
        abn_validator(file_location, first_row_headings,
                      orientation, abn_index)
    else:
        file_location = None
    return render(request, 'results.html', {'download_link': file_url})
