

import django_filters
from .models import Book

from django import forms
from .models import Book, Stage, ClassLevel, Supplier

import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        label='المادة الدراسية',
        lookup_expr='icontains',  # للبحث الجزئي غير الحساس لحالة الأحرف
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المادة'})
    )    
    source = django_filters.ChoiceFilter(field_name='source', choices=Book.SOURCE_CHOICES, label='مصدر التوريد', widget=forms.Select(attrs={'class': 'form-control'}))
    supplier = django_filters.ModelChoiceFilter(field_name='supplier', queryset=Supplier.objects.all(), label='اسم المورد', widget=forms.Select(attrs={'class': 'form-control'}))
    stage = django_filters.ModelChoiceFilter(field_name='stage', queryset=Stage.objects.all(), label='اسم المرحلة الدراسية', widget=forms.Select(attrs={'class': 'form-control'}))
    class_level = django_filters.ModelChoiceFilter(field_name='class_level', queryset=ClassLevel.objects.all(), label='اسم الصف الدراسي', widget=forms.Select(attrs={'class': 'form-control'}))
    term = django_filters.ChoiceFilter(choices=Book.TERM_CHOICES, label='الترم الدراسي', widget=forms.Select(attrs={'class': 'form-control'}))
    received_date__gte = django_filters.DateFilter(
        field_name='received_date',
        lookup_expr='gte',
        label='تاريخ الاستلام (من)',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    received_date__lte = django_filters.DateFilter(
        field_name='received_date',
        lookup_expr='lte',
        label='تاريخ الاستلام (إلى)',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'received_quantity': ['exact', 'gte', 'lte'],
            'available_quantity': ['exact', 'gte', 'lte'],
            'term': ['exact'],
            'received_date': ['exact', 'gte', 'lte'],
            
        }
