import json
import datetime
import urllib.request
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Kategori, Kontak, Profil, Slide, Statis
from cart.models import Transaksi, DetailTransaksi
from django.db.models import Count
from django.views.generic import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from cart.forms import CartAddProductForm
from django.db.models import Q 
from cart.keranjang import Cart

def beranda(request):
    kategori = Kategori.objects.filter(aktif=True).order_by('-id')
    slider = Slide.objects.filter(aktif=True).order_by('-id')
    jumlahkategori = Kategori.objects.all().annotate(product_count=Count('produks')).order_by('-id')
    trending = Product.objects.order_by('-dibeli')
    cart_product_form = CartAddProductForm()
    context = {
            "kategori" : kategori,
            "judul": "Halaman Beranda",
            "jumlahkategori":jumlahkategori,
            "slide": slider,
            "trending":trending,
            "cart_product_form": cart_product_form,

    }
    return render(request, 'beranda.html', context)

def product(request, kategori_slug, slug):
    produk = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(kategori=produk.kategori.id)
    jml = related.count()
    cart_product_form = CartAddProductForm()
    current_site = get_current_site(request)
    context = {
         "judul": "Halaman Product",
         "produk":produk,
         "related":related,
         "jml":jml,
         "cart_product_form": cart_product_form,
         "domain": current_site.domain,
    }
    return render(request, 'product.html', context)

def kategori(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    produk =  kategori.produks.order_by('-id')
    cart_product_form = CartAddProductForm()
    halaman_tampil = Paginator(produk, 8)
    halaman_url = request.GET.get('halaman',1)
    halaman_produk = halaman_tampil.get_page(halaman_url)
    if halaman_produk.has_previous():
        url_previous = f'?halaman={halaman_produk.previous_page_number()}'
    else:
        url_previous = ''

    if halaman_produk.has_next():
        url_next = f'?halaman={halaman_produk.next_page_number()}'
    else:
        url_next = ''
    context = {
         "judul": "Halaman Kategori",
         "detailkategori": kategori,
         "produk" : halaman_produk,
         "previous" : url_previous,
          "next" : url_next,
          "cart_product_form": cart_product_form,
    }
   
    return render(request, 'kategori.html', context)


class KontakView(View):
    def get(self, request):
        context = {
        'judul': 'Halaman Kontak',
       }
        return render(request, 'kontak.html', context)
       
    def post(self, request):
        context = {
            'judul': 'Halaman Kontak',
            'data': request.POST,
            'has_error': False
        }
        nama = request.POST.get('nama')
        no_whatsup = request.POST.get('whatsapp')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        pesan = request.POST.get('pesan')
        if nama=="":
           messages.error(request, 'Nama Masih kosong')
           context['has_error'] = True

        if no_whatsup=="":
               messages.error(request, 'No whatsapp Masih kosong')
               context['has_error'] = True

        if subject=="":
               messages.error(request, 'Subject Masih kosong')
               context['has_error'] = True

        if pesan=="":
               messages.error(request, 'Pesan Masih kosong')
               context['has_error'] = True

        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        # print(result['success'])
        if result['success']== False:
            messages.error(request, 'CaptCaha Masih Belum dicentang')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'kontak.html', context, status=400)

        kontak = Kontak.objects.create(nama = nama, email = email, no_whatsup=no_whatsup, subject = subject,  isi = pesan )
        kontak.save()
        context = {
                    'judul': 'Halaman Kontak',
                    'data': "",
                    'has_error': False
        }
        messages.success(request, 'Pesan sudah terkirim, silakan tunggu respon selanjutnya!')
        return render(request, 'kontak.html', context, status=400)


def profil(request):
    profil = Profil.objects.all().order_by('-id')[:1]
    context = {
        "judul": "Halaman Profil",
        "profil":profil,
    }
    return render(request, 'profil.html', context)


class CheckoutView(View):
    def get(self, request):
        context = {
        'judul': 'Halaman Checkout',
       }
        return render(request, 'checkout.html', context)
       
    def post(self, request):
        context = {
            'judul': 'Halaman checkout',
            'data': request.POST,
            'has_error': False
        }
        grantotal = request.POST.get('grantotal')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        alamat = request.POST.get('alamat')
        provinsi = request.POST.get('provinsi')
        kabupaten = request.POST.get('kabupaten')
        kecamatan = request.POST.get('kecamatan')
        kode_post = request.POST.get('kode_post')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        no_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if grantotal == "0" :
           messages.error(request, 'Anda belum berbelanja, Silakan belanja terlebih dahulu')
           context['has_error'] = True
        if nama_depan=="":
               messages.error(request, 'Nama Depan Masih kosong')
               context['has_error'] = True

       

        if alamat=="":
               messages.error(request, 'Alamat Masih kosong')
               context['has_error'] = True 

        if provinsi=="":
               messages.error(request, 'Provinsi Masih kosong')
               context['has_error'] = True
        if kabupaten=="":
               messages.error(request, 'Kabupaten Masih kosong')
               context['has_error'] = True
        if kecamatan=="":
               messages.error(request, 'Kecamatan Masih kosong')
               context['has_error'] = True
        if kode_post=="":
               messages.error(request, 'Kode Post Masih kosong')
               context['has_error'] = True
        if whatsapp=="":
               messages.error(request, 'Whatsapp Masih kosong')
               context['has_error'] = True
       
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        # print(result['success'])
        if result['success']== False:
            messages.error(request, 'CaptCaha Masih Belum dicentang')
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'checkout.html', context, status=400)

        transaksi = Transaksi.objects.create(no_transaksi = no_transaksi, 
                                              nama_depan = nama_depan,
                                              nama_belakang=nama_belakang, 
                                              alamat = alamat,
                                              provinsi = provinsi,
                                              kabupaten = kabupaten,
                                              kecamatan = kecamatan,
                                              kode_post = kode_post,
                                              email = email,
                                              whatsapp = whatsapp,
                                              total_transaksi = grantotal )
        transaksi.save()
        keranjang = Cart(request)
       
        # print(keranjang)
        for r in keranjang:
            
            instance_detail= DetailTransaksi(
                no_transaksi = no_transaksi,
                product = r['product'],
                jumlah = r['quantity'],
            )
            instance_detail.save()

            dibeliupdate=Product.objects.get(nama_produk=r['product'])
            dibeliupdate.dibeli+=int(r['quantity'])
            dibeliupdate.save()
            
           
            # .update(
            #     dibeli =+ int(r['quantity']),



        keranjang.clear()
        context = {
                    'judul': 'Halaman checkout',
                    'data': "",
                    'has_error': False
        }
        messages.success(request, 'Pesanan Anda akan segera diproses, silakan tunggu akan ada respon selanjutnya!')
        return render(request, 'checkout.html', context, status=400)



def cari(request):
    datakategori=request.GET.get('kategori')
    datakata=request.GET.get('kata')
    if datakategori == "all":
        hasilcari = Product.objects.filter(Q(nama_produk__icontains=datakata)).order_by('-id')
    else:
        hasilcari = Product.objects.filter(Q(nama_produk__icontains=datakata) & Q(kategori__id__exact=datakategori)).order_by('-id')
        
    cart_product_form = CartAddProductForm()
    jmlproduk = hasilcari.count()
    context = {
        "judul": "Halaman Cari",
        "cart_product_form": cart_product_form,
        "hasilcari": hasilcari,
        "jmlproduk":jmlproduk
    }
    print(hasilcari)
    return render(request, 'cari.html', context)

def kategoriberanda(request):
    kategori = Kategori.objects.filter(aktif=True).order_by('-id')
    return {'kategori':kategori}


def modalberita(request):
    modalproduk = Product.objects.order_by('-id')
    return {'modalproduk':modalproduk}


def statisweb(request):
    statis = Statis.objects.get(id=1)
    return {'statis':statis}