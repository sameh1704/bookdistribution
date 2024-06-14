# BookDistributionfilter.py
import django_filters
from .models import BookDistribution

class BookDistributionFilter(django_filters.FilterSet):
    student_name = django_filters.CharFilter(field_name='student__name', lookup_expr='icontains', label='اسم الطالب')
    receipt_number = django_filters.CharFilter(lookup_expr='exact', label='رقم الإيصال')
    recipient_name = django_filters.CharFilter(lookup_expr='icontains', label='اسم المستلم')
    delivery_date__gte = django_filters.DateFilter(field_name='delivery_date', lookup_expr='gte', label='تاريخ التوزيع من')
    delivery_date__lte = django_filters.DateFilter(field_name='delivery_date', lookup_expr='lte', label='تاريخ التوزيع إلى')
    distribution_status = django_filters.ChoiceFilter(choices=BookDistribution.DISTRIBUTION_CHOICES, label='حالة التوزيع')
    

    class Meta:
        model = BookDistribution
        fields = []

