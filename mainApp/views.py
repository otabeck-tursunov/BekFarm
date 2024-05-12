from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *


class DorilarView(View):
    def get(self, request):
        search = request.GET.get('search')
        dorilar = Dori.objects.order_by('nom')
        if search is not None:
            dorilar = Dori.objects.filter(
                Q(nom__icontains=search) |
                Q(ishlab_chiqaruvchi__icontains=search) |
                Q(turi__icontains=search)
            )
        context = {
            'dorilar': dorilar
        }
        return render(request, 'dorilar.html', context)

    def post(self, request):
        Dori.objects.create(
            nom=request.POST.get('nom'),
            ishlab_chiqaruvchi=request.POST.get('ishlab_chiqaruvchi'),
            turi=request.POST.get('turi'),
            narx=request.POST.get('narx'),
            miqdor=request.POST.get('miqdor'),
            kelgan_sana=request.POST.get('kelgan_sana'),
            muddat=request.POST.get('muddat')
        )
        return redirect('dorilar')


class SotuvlarView(View):
    def get(self, request):
        search = request.GET.get('search')
        sotuvlar = Sotuv.objects.all()
        if search is not None:
            sotuvlar = sotuvlar.filter(
                Q(dori__nom__icontains=search) |
                Q(dori__ishlab_chiqaruvchi__icontains=search)
            )
        dorilar = Dori.objects.all()
        context = {
            'sotuvlar': sotuvlar,
            'dorilar': dorilar
        }
        return render(request, 'sotuvlar.html', context)

    def post(self, request):
        dori = Dori.objects.get(pk=request.POST.get('dori'))
        miqdor = int(request.POST.get('miqdor'))
        if miqdor > dori.miqdor:
            return HttpResponse("""            <p>Kiritilgan miqdorda dori mavjud emas</p>            """)
        Sotuv.objects.create(
            dori=dori,
            miqdor=miqdor,
            summa=request.POST.get('summa'),
            sana=request.POST.get('sana')
        )
        dori.miqdor -= miqdor
        dori.save()
        return redirect('sotuvlar')


from django.shortcuts import render


def handler404(request, exception):
    return render(request, '404.html', status=404)
