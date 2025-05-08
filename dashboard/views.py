from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .forms import CSVUploadForm
from .models import SalesData
import matplotlib.pyplot as plt
import io
import urllib
import base64
import csv
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .forms import CSVUploadForm
from django.contrib import messages
from django.core.paginator import Paginator



# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded)

        try:
            headers = next(reader)
            rows = [list(map(str, row)) for row in reader]
            request.session['csv_headers'] = headers
            request.session['csv_data'] = rows
            messages.success(request, "Plik CSV został przesłany poprawnie.")
        except Exception:
            messages.error(request, "Błąd podczas przetwarzania pliku.")
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def dashboard(request):
    headers = request.session.get('csv_headers', [])
    rows = request.session.get('csv_data', [])
    graph = None

    # Obsługa wykresu
    if request.method == 'POST' and 'generate_chart' in request.POST:
        x_col = request.POST.get('x_column')
        y_col = request.POST.get('y_column')

        if x_col and y_col and rows:
            df = pd.DataFrame(rows, columns=headers)
            # Oczyszczanie danych z nadmiarowych spacji i zamiana przecinków na kropki
            df = df.applymap(lambda x: x.strip().replace(',', '.') if isinstance(x, str) else x)
            # Próbujemy przekonwertować y_col do liczby
            df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
            # Usuwamy wiersze z brakami
            df = df.dropna(subset=[x_col, y_col])
            try:
                df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
                df = df.dropna(subset=[x_col, y_col])
                grouped = df.groupby(x_col)[y_col].sum()

                # Po grupowaniu
                if len(grouped) > 20:
                    grouped = grouped.sort_values(ascending=False).head(20)

                plt.figure(figsize=(10, 4))
                grouped.plot(kind='bar', color="#7c3aed")
                plt.title(f'{y_col} wg {x_col}')
                plt.xticks(rotation=45)
                plt.tight_layout()

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                graph = base64.b64encode(image_png).decode('utf-8')
                plt.close()
            except Exception as e:
                messages.error(request, f'Błąd podczas generowania wykresu: {e}')

    # paginacja
    paginator = Paginator(rows, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/dashboard.html', {
        'headers': headers,
        'rows': rows,
        'page_obj': page_obj,
        'graph': graph
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja zakończona sukcesem.")
            return redirect('dashboard')
        else:
            messages.error(request, "Błąd w formularzu. Spróbuj ponownie.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})