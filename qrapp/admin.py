from django.contrib import admin
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_data', 'views_count', 'downloads_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('data',)

    def short_data(self, obj):
        # عرض أول 30 حرف من النص أو الرابط لتسهيل التعرف على الرمز
        return obj.data[:30]
    short_data.short_description = 'النص / الرابط'
