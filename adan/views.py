#file: adan/views.py

from django.shortcuts import render

# Nézet a 'Adan' oldal megjelenítésére
# Ez a nézet rendereli az 'adan.html' sablont, amely az alapértelmezett szöveget tartalmazza
def adan_view(request):
    """
    Adan oldal betöltése. A nézet visszatéríti az 'adan.html' sablont, 
    amely az alkalmazás alapértelmezett szövegét tartalmazza.
    """
    return render(request, 'adan/adan.html')
