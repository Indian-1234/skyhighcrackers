from django import forms
from .models import similarCrackers

class CrackForm(forms.ModelForm):
    class Meta:
        model = similarCrackers
        fields = ['name', 'image', 'similarname', 'actual_price', 'discount_price', 'content']
