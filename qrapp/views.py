from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import QRForm
import qrcode
from PIL import Image
from io import BytesIO
import base64
from .models import QRCode

def home(request):
    qr_data_uri = None

    if request.method == "POST":
        form = QRForm(request.POST, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data['data']
            fill = form.cleaned_data.get('fill_color') or '#000000'
            back = form.cleaned_data.get('back_color') or '#ffffff'
            box = form.cleaned_data.get('box_size') or 10
            logo_file = form.cleaned_data.get('logo')

            # --- إنشاء رمز QR مع منطقة فارغة للشعار ---
            qr_img = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=box,
                border=4
            )
            qr_img.add_data(data)
            qr_img.make(fit=True)
            img = qr_img.make_image(fill_color=fill, back_color=back).convert('RGB')

            if logo_file:
                logo = Image.open(logo_file)
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')

                qr_width, qr_height = img.size
                factor = 4  # الشعار حوالي 1/4 من حجم QR
                logo_size = (qr_width // factor, qr_height // factor)
                logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

                # إنشاء مستطيل فارغ باللون الخلفي
                pos = ((qr_width - logo_size[0]) // 2, (qr_height - logo_size[1]) // 2)
                mask_bg = Image.new('RGB', logo_size, back)
                img.paste(mask_bg, pos)

                # ضع الشعار على المنطقة الفارغة
                img.paste(logo, pos, mask=logo)

            # تحويل الصورة إلى base64 للعرض في HTML
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_b64 = base64.b64encode(buffer.getvalue()).decode()
            qr_data_uri = f"data:image/png;base64,{img_b64}"

            # --- حفظ الرمز في قاعدة البيانات وزيادة العدادات ---
            QRCode.objects.create(
                data=data,
                fill_color=fill,
                back_color=back,
                box_size=box,
                logo=logo_file
            )

    else:
        form = QRForm()

    return render(request, "qrapp/index.html", {'form': form, 'qr_data_uri': qr_data_uri})

# عرض تفاصيل الرمز وزيادة عدد الزيارات
def qr_detail(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)
    qr.views_count += 1
    qr.save(update_fields=['views_count'])
    return render(request, 'qr_detail.html', {'qr': qr})

# تحميل رمز QR وزيادة عدد التحميلات
def download_qr(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)
    qr.downloads_count += 1
    qr.save(update_fields=['downloads_count'])

    # تحويل رمز QR إلى صورة للتحميل
    qr_img = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr.box_size,
        border=4
    )
    qr_img.add_data(qr.data)
    qr_img.make(fit=True)
    img = qr_img.make_image(fill_color=qr.fill_color, back_color=qr.back_color).convert('RGB')

    if qr.logo:
        logo = Image.open(qr.logo.path)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        qr_width, qr_height = img.size
        factor = 4
        logo_size = (qr_width // factor, qr_height // factor)
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        pos = ((qr_width - logo_size[0]) // 2, (qr_height - logo_size[1]) // 2)
        mask_bg = Image.new('RGB', logo_size, qr.back_color)
        img.paste(mask_bg, pos)
        img.paste(logo, pos, mask=logo)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="qantresso_qr.png"'
    return response


def about(request):
    return render(request, 'qrapp/about.html')

def contact(request):
    if request.method == "POST":
        # هنا يمكن لاحقاً إضافة منطق إرسال الرسالة بالبريد أو تخزينها
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # حاليا سنعيد فقط صفحة شكراً بعد الإرسال (يمكن تحسينها لاحقاً)
        return render(request, 'qrapp/contact.html', {'success': True})

    return render(request, 'qrapp/contact.html')