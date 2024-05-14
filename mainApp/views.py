from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *


def index(request):
    return redirect('dorilar')


class DorilarView(View):
    def get(self, request):
        miqdor_query = request.GET.get('miqdor')
        dori_query = request.GET.get('dori')
        if miqdor_query is not None and dori_query is not None:
            dori = Dori.objects.get(id=dori_query)
            dori.miqdor += 1
            dori.save()
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


class DoriConfirmDeleteView(View):
    def get(self, request, id):
        dori = Dori.objects.get(id=id)
        context = {
            'dori': dori
        }
        return render(request, 'tasdiqlash.html', context)


class DoriDeleteView(View):
    def get(self, request, id):
        Dori.objects.filter(id=id).delete()
        return redirect('dorilar')


class TopDorilarView(View):
    def get(self, request):
        dorilar = {}
        for sotuv in Sotuv.objects.all():
            if sotuv.dori.id in dorilar:
                dorilar[sotuv.dori.id] += sotuv.summa
            else:
                dorilar[sotuv.dori.id] = sotuv.summa
        dorilar = sorted(dorilar.items(), key=lambda x: x[1], reverse=True)

        data = []
        for dori in dorilar:
            d = Dori.objects.get(id=dori[0])
            data.append({
                'nom': d.nom,
                'brend': d.ishlab_chiqaruvchi,
                'narx': dori[1]
            })

        return render(request, 'top-dorilar.html', context={'dorilar': data})


class TavsiyaView(View):
    def get(self, request):
        dorilar = Dori.objects.filter(miqdor__lt=10)
        return render(request, 'tavsiya.html', {'dorilar': dorilar})

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
        sotuvlar = Sotuv.objects.order_by('-id')
        if search is not None:
            sotuvlar = sotuvlar.filter(
                Q(dori__nom__icontains=search) |
                Q(dori__ishlab_chiqaruvchi__icontains=search) |
                Q(dori__turi__icontains=search)
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
        sotuv = Sotuv.objects.create(
            dori=dori,
            miqdor=miqdor,
            # summa=request.POST.get('summa'),
            sana=request.POST.get('sana')
        )
        sotuv.summa = sotuv.miqdor * sotuv.dori.narx
        sotuv.save()
        dori.miqdor -= miqdor
        dori.save()
        return redirect('sotuvlar')


def handler404(request, exception):
    return render(request, '404.html', status=404)
