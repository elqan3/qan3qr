from django import forms

class QRForm(forms.Form):
    data = forms.CharField(
        label='النص أو الرابط',
        widget=forms.Textarea(attrs={'rows':2, 'placeholder':'اكتب الرابط أو النص هنا...'})
    )
    fill_color = forms.CharField(
        label='لون المربع',
        initial='black',
        required=False
    )
    back_color = forms.CharField(
        label='لون الخلفية',
        initial='white',
        required=False
    )
    box_size = forms.IntegerField(
        label='حجم المربع',
        initial=10,
        min_value=1,
        max_value=40
    )
    logo = forms.ImageField(
        label='شعار (اختياري)',
        required=False
    )
