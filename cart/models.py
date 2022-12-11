from django.db import models
from website.models import Product

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma


class Transaksi(models.Model):
    Status=(
        ('Baru', 'Baru'),
        ('Lunas' , 'Lunas'),
    )

    no_transaksi = models.CharField(max_length=200, blank=False, null=True)
    nama_depan = models.CharField(max_length=200, blank=False, null=True)
    nama_belakang = models.CharField(max_length=200, blank=False, null=True)
    alamat = models.TextField(max_length=200, blank=False, null=True)
    provinsi = models.CharField(max_length=200, blank=False, null=True)
    kabupaten = models.CharField(max_length=200, blank=False, null=True)
    kecamatan = models.CharField(max_length=200, blank=False, null=True)
    kode_post = models.CharField(max_length=200, blank=False, null=True)
    email = models.CharField(max_length=200, blank=False, null=True)
    whatsapp = models.CharField(max_length=200, blank=False, null=True)
    total_transaksi = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=200, default="Baru", blank=True, null=True, choices=Status)
    date_created= models.DateTimeField(auto_now_add=True, null=True,blank=True)
    tanggal_kirim= models.DateTimeField(auto_now_add=False, null=True, blank=False)

    @property
    def tanggal_pengiriman(self):
        if self.tanggal_kirim is None:
            tglkirim ="-"
        else:
            tglkirim = self.tanggal_kirim.strftime("%d %b %Y %H:%M:%S")
        return tglkirim

    class Meta:
        ordering = ('-no_transaksi', )

    def __str__(self):
         return f"{self.nama_depan}-{self.no_transaksi}-({self.total_transaksi})" 
    class Meta:
        verbose_name_plural ="Transaksi"
    @property
    def total_pemabayaran(self):
        hargavalid = str(self.total_transaksi).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"
        return fikharga
    def nama_lengkap(self):
        if self.nama_belakang == "":
            nama = f"{self.nama_depan}"
        else:
            nama = f"{self.nama_depan}  {self.nama_belakang}"
        return nama
class DetailTransaksi(models.Model):
    no_transaksi = models.CharField(max_length=200, blank=False, null=True)
    product = models.ForeignKey(Product, null= True, on_delete=models.SET_NULL)
    jumlah = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ('-no_transaksi', )

    def __str__(self):
         nilai = str(self.product.setela_diskon)
         hargavalid = (nilai.replace(".0",""))
         return f"No Transaksi: {self.no_transaksi} Produk: ({self.product}) Jumlah: ({self.jumlah})  Harga: ({hargavalid})" 

    @property
    def harga(self):
        total = self.product.setela_diskon 
        

        hargavalid = str(total).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"


        return fikharga
    @property
    def sub_total(self):
        total = self.product.setela_diskon * self.jumlah

        
        hargavalid = str(total).replace('.0','')
        hargafik = int(hargavalid)
        hargarupiah = intcomma(hargafik)
        fikharga =  f"Rp. {str(hargarupiah)}"


        return fikharga
    class Meta:
        verbose_name_plural ="Detail Transaksi"
