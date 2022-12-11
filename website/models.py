from django.db import models
from PIL import Image
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

class Kategori(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    aktif = models.BooleanField(default=True)
    banner_satu = ResizedImageField(size=[800, 200], quality=80, crop=['middle', 'center'] , upload_to='gambar/banner', blank=True, null=True, verbose_name="Gambar (575 x 200 pixel)")
    banner_dua = ResizedImageField(size=[800, 200], quality=80, crop=['middle', 'center'] , upload_to='gambar/banner', blank=True, null=True, verbose_name="Gambar (575 x 200 pixel)")
   
    slug = models.SlugField(max_length=200, null=False, unique=True)
    @property
    def get_products(self):
        return Product.objects.filter(kategori__nama=self.nama)
    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Kategori"

    
class Product(models.Model):
    KETERANGAN=(
        ('Baru', 'Baru'),
        ('Lama' , 'Lama'),
       
    )

    kategori = models.ForeignKey(Kategori, null=True, blank=True, related_name="produks", on_delete=models.SET_NULL)
    nama_produk = models.CharField(max_length=200, blank=True, null=True, unique=True)
    gambar = ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=False, null=True, verbose_name="Gambar (270 x 250 pixel)")
    gambar_satu = ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=True, null=True, verbose_name="Gambar (270 x 250 pixel)")
    gambar_dua = ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=True, null=True, verbose_name="Gambar (270 x 250 pixel)")
    gambar_tiga = ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=True, null=True, verbose_name="Gambar (270 x 250 pixel)")
    gambar_empat = ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=True, null=True, verbose_name="Gambar (270 x 250 pixel)")
    gambar_lima= ResizedImageField(size=[270, 250], quality=80, crop=['middle', 'center'] , upload_to='gambar/product', blank=True, null=True, verbose_name="Gambar (270 x 250 pixel)")
    slug = models.SlugField(max_length=200, unique=True)
    keterangan = RichTextField(blank=True, null=True)
    harga = models.PositiveIntegerField(blank=True, null=True)
    no_whatsup = models.PositiveBigIntegerField(blank=True, null=True,)
    tanggal_upload= models.DateTimeField(auto_now_add=True, null=True)
    diskon = models.IntegerField(default=0,  blank=True, null=True, verbose_name="Diskon (%)")
    dibeli = models.IntegerField(default=0,  blank=True, null=True)
    keterangan_barang = models.CharField(max_length=200, null=True, choices=KETERANGAN)
    @property
    def setela_diskon(self):
        if self.diskon == 0 :
            nilai_diskon = self.harga
        else:
            jml = self.diskon / 100
            nilai_diskon = self.harga - (jml * self.harga)
        return nilai_diskon


    def __str__(self):
        return self.nama_produk
    class Meta:
        verbose_name_plural ="Product"
    
class Slide(models.Model):
    teks_awal = models.CharField(max_length=200, blank=False, null=True,verbose_name="Teks satu (<span>Text</span> Merah)")
    teks_dua = models.CharField(max_length=200, blank=False, null=True)
    teks_tiga = models.CharField(max_length=200, blank=False, null=True, verbose_name="Teks dua (<span>Text</span> Merah)")
    gambar_slide = models.ImageField(upload_to='gambar/slide', blank=False, null=True, verbose_name="Gambar (475 x 880 pixel)")
    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.teks_dua
    class Meta:
        verbose_name_plural ="Slide"
    def save(self, *args, **kwargs):
        super(Slide, self).save(*args, **kwargs)

        img = Image.open(self.gambar_slide.path)

        if img.height > 475 or img.width > 880:
            output_size = (475,880)
            img.thumbnail(output_size)
            img.save(self.gambar_slide.path)
class Kontak(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    no_whatsup = models.PositiveBigIntegerField(blank=True, null=True,)
    email = models.EmailField(max_length=200,blank=False, null=True)
    subject = models.CharField(max_length=200, blank=False, null=True)
    isi = models.TextField(max_length=200, blank=False, null=True)

    def __str__(self):
        
        return '%s, %s' % (self.nama, self.email) 
    class Meta:
        verbose_name_plural ="Kontak"


class Profil(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    keterangan = RichTextField(blank=True, null=True)
    gambar = models.ImageField(upload_to='gambar/profil', blank=False, null=True, verbose_name="Gambar (1920 x 1200 pixel)")
    tanggal_upload= models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Profil"
    def save(self, *args, **kwargs):
        super(Profil, self).save(*args, **kwargs)

        img = Image.open(self.gambar.path)

        if img.height > 1200 or img.width > 1900:
            output_size = (1200,1900)
            img.thumbnail(output_size)
            img.save(self.gambar.path)
class Statis(models.Model):
    alamat_kami = models.TextField(max_length=200, blank=False, null=True)
    telpon = models.CharField(max_length=200, blank=False, null=True)
    email = models.EmailField(max_length=200, blank=False, null=True)
   

    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural ="Statis"