
import django_filters

from store import forms
from .models import SchoolBooklet
from .models import Stage, ClassLevel, Supplier


import django_filters
from django import forms
from .models import SchoolBooklet, Stage, ClassLevel, Supplier

class SchoolBookletFilter(django_filters.FilterSet):
   # title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='عنوان البوكليت')
    title = django_filters.ChoiceFilter(
        field_name='title',
        label='عنوان البوكليت',
        choices=[(booklet.title, booklet.title) for booklet in SchoolBooklet.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    source = django_filters.ChoiceFilter(field_name='source', choices=SchoolBooklet.SOURCE_CHOICES, label='مصدر التوريد', widget=forms.Select(attrs={'class': 'form-control'}))
    supplier = django_filters.ModelChoiceFilter(field_name='supplier', queryset=Supplier.objects.all(), label='اسم المورد', widget=forms.Select(attrs={'class': 'form-control'}))
    stage = django_filters.ModelChoiceFilter(field_name='stage', queryset=Stage.objects.all(), label='اسم المرحلة الدراسية', widget=forms.Select(attrs={'class': 'form-control'}))
    class_level = django_filters.ModelChoiceFilter(field_name='class_level', queryset=ClassLevel.objects.all(), label='اسم الصف الدراسي', widget=forms.Select(attrs={'class': 'form-control'}))
    term = django_filters.ChoiceFilter(choices=SchoolBooklet.TERM_CHOICES, label='الترم الدراسي', widget=forms.Select(attrs={'class': 'form-control'}))
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
        model = SchoolBooklet
        fields = ['title', 'source', 'supplier', 'stage', 'class_level', 'term', 'received_date__gte', 'received_date__lte']


