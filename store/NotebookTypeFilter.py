import django_filters
from django import forms
from .models import NotebookType, Supplier

import django_filters
from django import forms
from .models import NotebookType, Supplier

class NotebookTypeFilter(django_filters.FilterSet):
    name = django_filters.ChoiceFilter(
        field_name='name',
        label='نوع الكراسة',
        choices=[(notebook.name, notebook.name) for notebook in NotebookType.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    size = django_filters.ChoiceFilter(
        field_name='size',
        label='حجم الكراسة',
        choices=[(notebook.size, notebook.size) for notebook in NotebookType.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    source = django_filters.ChoiceFilter(
        field_name='source',
        choices=NotebookType.SOURCE_CHOICES,
        label='مصدر التوريد',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    supplier = django_filters.ModelChoiceFilter(
        field_name='supplier',
        queryset=Supplier.objects.all(),
        label='المورد',
        widget=forms.Select(attrs={'class': 'form-control'})
    )



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
        model = NotebookType
        fields = ['name', 'size', 'source', 'supplier',  'received_date__gte', 'received_date__lte']
