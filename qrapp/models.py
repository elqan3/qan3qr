from django.db import models

class QRCode(models.Model):
    data = models.TextField(verbose_name="النص أو الرابط")
    fill_color = models.CharField(max_length=7, default="#000000", verbose_name="لون المربعات")
    back_color = models.CharField(max_length=7, default="#ffffff", verbose_name="لون الخلفية")
    box_size = models.PositiveIntegerField(default=10, verbose_name="حجم المربعات")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="الشعار (اختياري)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد الزيارات")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="عدد التحميلات")

    class Meta:
        verbose_name = "رمز QR"
        verbose_name_plural = "رموز QR"
        ordering = ['-created_at']  # الترتيب حسب الأحدث أولاً

    def __str__(self):
        # عرض أول 20 حرف من النص لسهولة التعرف على الرمز
        return f"QR {self.id} - {self.data[:20]}"
