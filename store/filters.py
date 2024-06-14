import django_filters
from django_filters import DateFromToRangeFilter
from .models import AcademicYear, ClassLevel, Classroom, Stage, Student, Supplier
from django_filters import DateRangeFilter
from django_filters.widgets import RangeWidget
from django_filters import DateFromToRangeFilter
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat
from django_filters.widgets import DateRangeWidget
from django import forms
from django.utils.translation import gettext_lazy as _
from store.forms import StudentForm


class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='اسم الطالب')
    stage = django_filters.ModelChoiceFilter(
        field_name='stage', 
        queryset=Stage.objects.all(), 
        label='المرحلة الدراسية',
        widget=forms.Select(attrs={'id': 'id_stage'})
    )
    class_level = django_filters.ModelChoiceFilter(
        field_name='class_level', 
        queryset=ClassLevel.objects.all(), 
        label='الصف الدراسي',
        widget=forms.Select(attrs={'id': 'id_class_level'})
    )
    section = django_filters.ModelChoiceFilter(
        field_name='section', 
        queryset=Classroom.objects.all(), 
        label='الفصل الدراسي',
        widget=forms.Select(attrs={'id': 'id_section'})
    )
    academic_year = django_filters.ModelChoiceFilter(
        field_name='academic_year', 
        queryset=AcademicYear.objects.all(), 
        label='السنة الدراسية'
    )
    national_id = django_filters.CharFilter(field_name='national_id', lookup_expr='exact', label='الرقم القومي')

    class Meta:
        model = Student
        fields = ['academic_year', 'name', 'national_id', 'stage', 'class_level', 'section']


# filters.py

import django_filters
from .models import Supplier
from django import forms

class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = ['name', 'phone']

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='اسم المورد',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    phone = django_filters.CharFilter(
        field_name='phone',
        lookup_expr='icontains',
        label='رقم تليفون المورد',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
