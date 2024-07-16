from datetime import date, datetime
import pandas as pd
import xlsxwriter
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, user_passes_test

from store import serializers
from store.utils import calculate_required_resources

from .forms import (
    BookDepreciationForm, BookOutstoreForm, BookletDepreciationForm,
    BookletOutstoreForm, NotebookDepreciationForm, StudentForm,
    BookDistributionForm, StudentSearchForm, StudentSelectForm,
    SchoolBookletForm, SchoolSuppliesForm, NotebookTypeForm,
    BookForm, NotebookAssignmentForm, SupplierForm,
    BookDeliveryForm, NotebookDeliveryForm, BookletDeliveryForm,
    StudentMigrationForm, SearchForm, NotebookRequestForm
)
from .models import (
    AcademicYear, Book, BookDepreciation, BookDistribution,
    BookOutstore, BookletDepreciation, BookletOutstore, ClassLevel,
    Classroom, NotebookAssignment, NotebookDepreciation, NotebookType,
    SchoolBooklet, Stage, Student, Supplier, BookDelivery,
    NotebookDelivery, BookletDelivery, SchoolBooklet, BookDistribution
)

from .NotebookTypeFilter import NotebookTypeFilter
from store.SchoolBookletFilter import SchoolBookletFilter
from .Bookfilter import BookDistributionFilter
from .filters import SupplierFilter
from .filters import StudentFilter
from .BOOK_LIST import BookFilter



from accounts.decorators import custom_permission_required, CustomPermissionMixin







#############################################################################################




##############################################################################33
@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def home(request):

    return render(request, 'home.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def list(request):

    return render(request, 'list.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def Dashboard(request):

    return render(request, 'Dashboard.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')

def allstudent(request):

    return render(request, 'student.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def bookstore(request):

    return render(request, 'bookstore.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def note(request):

    return render(request, 'note.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')
def booklet(request):

    return render(request, 'booklet.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')

def depreciations(request):

    return render(request, 'depreciations.html')

@login_required
@custom_permission_required('is_admin', 'is_editor', 'is_viewer')

def outlet(request):

    return render(request, 'outlet.html')

################################################################33

@login_required
@custom_permission_required('is_admin', 'is_editor')
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')  # استبدل 'supplier_list' باسم العرض الذي يعرض قائمة الموردين
    else:
        form = SupplierForm()
    return render(request, 'create_supplier.html', {'form': form})

################################################



class SupplierListView(CustomPermissionMixin, FilterView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = Supplier
    template_name = 'supplier_list.html'
    filterset_class = SupplierFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['supplier_list'] = page_obj
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())

        return context

@login_required
@custom_permission_required('is_admin', 'is_editor')
def export_supplier_excel(request):
    # تحديد اسم الملف مع تضمين التاريخ الحالي
    filename = f"supplier_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # إنشاء ملف Excel وورقة عمل
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # تحضير العناوين
    headers = [
        'ترقيم',
        'اسم المورد',
        'رقم التليفون',
        'الكتب الدراسية',
        'البوكليتات المدرسية',
        'أنواع الكراسات',
    ]

    # كتابة العناوين في الصف الأول في الملف
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # استرجاع البيانات المصفاة
    queryset = Supplier.objects.all()

    for row, supplier in enumerate(queryset, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, supplier.name)
        worksheet.write(row, 2, supplier.phone)

        # جمع الكتب الدراسية
        books = Book.objects.filter(supplier=supplier)
        books_data = '\n'.join([f"{book.title} - العدد {book.available_quantity} - التاريخ {book.received_date}" for book in books])
        worksheet.write(row, 3, books_data)

        # جمع البوكليتات المدرسية
        booklets = SchoolBooklet.objects.filter(supplier=supplier)
        booklets_data = '\n'.join([f"{booklet.title} - العدد {booklet.live_quantity} - التاريخ {booklet.received_date}" for booklet in booklets])
        worksheet.write(row, 4, booklets_data)

        # جمع أنواع الكراسات
        notebooks = NotebookType.objects.filter(supplier=supplier)
        notebooks_data = '\n'.join([f"{notebook.name} - العدد {notebook.live_quantity} - التاريخ {notebook.received_date}" for notebook in notebooks])
        worksheet.write(row, 5, notebooks_data)

    # إغلاق ملف Excel وإرسال الاستجابة
    workbook.close()
    return response


###################################################################


@login_required
@custom_permission_required('is_admin', 'is_editor')

def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('store:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form, 'supplier': supplier})

@login_required
@custom_permission_required('is_admin', 'is_editor')

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('store:supplier_list')
    return render(request, 'delete_supplier.html', {'supplier': supplier})


################################################################33

@login_required
@custom_permission_required('is_admin', 'is_editor')

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة الطالب بنجاح.')
            return redirect('store:Dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@login_required
@custom_permission_required('is_admin', 'is_editor')
def import_students(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'الملف يجب أن يكون بصيغة Excel (xlsx).')
            return redirect('import_students')
        
        df = pd.read_excel(excel_file, names=['name', 'national_id', 'stage', 'class_level', 'section', 'phone_number', 'academic_year'])
        
        for index, row in df.iterrows():
            try:
                class_level = ClassLevel.objects.get(name=row['class_level'], stage__stage=row['stage'])
                section = Classroom.objects.get(name=row['section'], class_levels=class_level)
                academic_year = AcademicYear.objects.get(year=row['academic_year'])
                student = Student(
                    name=row['name'],
                    national_id=row['national_id'],
                    phone_number=row['phone_number'],
                    stage=class_level.stage,
                    class_level=class_level,
                    section=section,
                    academic_year=academic_year
                )
                student.save()
            except ClassLevel.DoesNotExist:
                messages.error(request, f"الصف '{row['class_level']}' غير موجود في المرحلة '{row['stage']}'")
            except Classroom.DoesNotExist:
                messages.error(request, f"الفصل '{row['section']}' غير موجود في الصف '{row['class_level']}'")
            except AcademicYear.DoesNotExist:
                messages.error(request, f"السنة الدراسية '{row['academic_year']}' غير موجودة.")

        messages.success(request, 'تم استيراد الطلاب بنجاح.')
        return redirect('store:add_student')
    return render(request, 'import_students.html')

import pandas as pd

@login_required
@custom_permission_required('is_admin', 'is_editor')
def export_students(request):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"طلاب_{timestamp}.xlsx"

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    students = Student.objects.all()
    data = {
        'اسم الطالب': students.values_list('name', flat=True),
        'الرقم القومي': students.values_list('national_id', flat=True),
        'المرحلة الدراسية': students.values_list('stage__stage', flat=True),
        'الصف الدراسي': students.values_list('class_level__name', flat=True),
        'الفصل الدراسي': students.values_list('section__name', flat=True),
        'رقم الهاتف': students.values_list('phone_number', flat=True),
        'السنة الدراسية': students.values_list('academic_year__year', flat=True),
    }
    df = pd.DataFrame(data)
    df.to_excel(response, index=False)

    return response


############################################################################################

@login_required
@custom_permission_required('is_admin', 'is_editor')
def get_class_student(request):
    stage_id = request.GET.get('stage_id')
    class_level_id = request.GET.get('class_level_id')

    data = {}

    if stage_id:
        stage = Stage.objects.get(pk=stage_id)
        class_levels = ClassLevel.objects.filter(stage=stage).prefetch_related(
            Prefetch('classroom_set', queryset=Classroom.objects.all())
        )
        data['class_levels'] = [
            {
                'id': class_level.id,
                'name': class_level.name,
                'sections': [
                    {'id': section.id, 'name': section.name}
                    for section in class_level.classroom_set.all()
                ]
            }
            for class_level in class_levels
        ]
        # Clear sections data when changing stage
        data['sections'] = []

    elif class_level_id:
        class_level = ClassLevel.objects.get(pk=class_level_id)
        sections = class_level.classroom_set.all()
        data['sections'] = [
            {'id': section.id, 'name': section.name}
            for section in sections
        ]

    return JsonResponse(data)

##########################################################################################################################



class studentListView(CustomPermissionMixin, FilterView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = Student
    template_name = 'Student_list.html'
    filterset_class = StudentFilter
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['Student_list'] = page_obj
        context['filter'] = self.filterset

        return context

    



 #######################################################################################################33
@login_required
@custom_permission_required('is_admin', 'is_editor')
def export_Student_excel(request):
    # تحديد اسم الملف مع تضمين التاريخ الحالي
    filename = f"Student_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # إنشاء ملف Excel وورقة عمل
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # تحضير العناوين
    headers = [
        'ترقيم',
        'اسم الطالب',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الفصل الدراسي',
        'الرقم القومي',
        'رقم التليفون',
        ' السنة الدراسية',   
    ]

    # كتابة العناوين في الصف الأول في الملف
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # استرجاع البيانات المصفاة وكتابتها في ملف Excel
    queryset = StudentFilter(request.GET, queryset=Student.objects.all()).qs

    for row, student in enumerate(queryset, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, student.name)
        worksheet.write(row, 2, str(student.stage))
        worksheet.write(row, 3, str(student.class_level))
        worksheet.write(row, 4, str(student.section))
        worksheet.write(row, 5, student.national_id)
        worksheet.write(row, 6, student.phone_number)
        worksheet.write(row, 7, student.class_level.academic_year.year if student.class_level.academic_year else '')

    # إغلاق ملف Excel وإرسال الاستجابة
    workbook.close()
    return response

########################################################3
@login_required
@custom_permission_required('is_admin', 'is_editor')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:bookstore') 
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def edit_book(request, pk):
    

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث  بنجاح.')
            return redirect('store:bookstore')      
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})
###############################################

class BookListView(CustomPermissionMixin, FilterView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = Book
    template_name = 'book_list.html'
    filterset_class = BookFilter
    paginate_by = 10

    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        
        filterset.filters['source'].extra['choices'] = [(book.source, book.source) for book in Book.objects.all()]
        return filterset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['title'] = 'قائمة الكتب'
        context['page_obj'] = page_obj

        # تطبيق الفلترة على الكتب
        filterset = self.get_filterset(self.filterset_class)
        filtered_books = filterset.qs

        # استعلام لجلب التوريدات المرتبطة بالكتب المفلترة
        deliveries = BookDelivery.objects.filter(book_type__in=filtered_books)

        # تضمين تفاصيل التوريدات في السياق
        context['deliveries'] = deliveries
        return context

#####################################################################
# دالة لإضافة توريد كتاب
@login_required
@custom_permission_required('is_admin', 'is_editor')

def add_BookDelivery(request):
    if request.method == 'POST':
        form = BookDeliveryForm(request.POST)
        if form.is_valid():
            book_delivery = form.save(commit=False)
            book_delivery.save()

            # تحديث الكمية المتاحة في Book
            book = book_delivery.book_type
            book.available_quantity += book_delivery.quantity
            book.save()

            messages.success(request, 'تم إضافة تفاصيل التوريد بنجاح.')
            return redirect('store:bookstore')   # تعديل إلى اسم العرض الصحيح
    else:
        form = BookDeliveryForm()
    return render(request, 'add_book_delivery.html', {'form': form})



@login_required
@custom_permission_required('is_admin', 'is_editor')
# تعديل export_book_excel
def export_book_excel(request):
    filename = f"book_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    headers = [
        'ترقيم',
        'اسم المادة الدراسية',
        'مصدر التوريد',
        'اسم المورد',
        'الكمية الواردة',
        'الكمية المتاحة',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الترم الدراسي',
        'تاريخ الاستلام',
        'تفاصيل التوريد'
    ]

    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    queryset = BookFilter(request.GET, queryset=Book.objects.all()).qs

    row = 1
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    for book in queryset:
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, book.get_title_display())
        worksheet.write(row, 2, book.source)
        worksheet.write(row, 3, book.supplier.name if book.supplier else '')
        worksheet.write(row, 4, book.received_quantity)
        worksheet.write(row, 5, book.available_quantity)
        worksheet.write(row, 6, str(book.stage))
        worksheet.write(row, 7, str(book.class_level))
        worksheet.write(row, 8, book.term)
        worksheet.write_datetime(row, 9, book.received_date, date_format)

        col = 10  # بدء عمود تفاصيل التوريد

        deliveries = BookDelivery.objects.filter(book_type=book)
        for delivery in deliveries:
            worksheet.write(row, col, delivery.quantity)
            worksheet.write_datetime(row, col + 1, delivery.received_date, date_format)
            col += 2

        row += 1

    workbook.close()
    return response
    


######################################################################################
@login_required
@custom_permission_required('is_admin', 'is_editor')

def add_notebook_type(request):
    if request.method == 'POST':
        form = NotebookTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة نوع الكراسة بنجاح.')
            return redirect('store:note')
    else:
        form = NotebookTypeForm()
    return render(request, 'add_notebook_type.html', {'form': form})

@login_required
@custom_permission_required('is_admin', 'is_editor')
def add_notebook_delivery(request):
    if request.method == 'POST':
        form = NotebookDeliveryForm(request.POST)
        if form.is_valid():
            notebook_delivery = form.save(commit=False)
            notebook_delivery.save()
            
            # تحديث الكمية الحالية في NotebookType
            notebook = notebook_delivery.notebook_type
            notebook.live_quantity += notebook_delivery.quantity
            notebook.save()
            
            messages.success(request, 'تم إضافة تفاصيل التوريد بنجاح.')
            return redirect('store:note')
    else:
        form = NotebookDeliveryForm()
    return render(request, 'add_notebook_delivery.html', {'form': form})

@login_required
@custom_permission_required('is_admin', 'is_editor')
def edit_notebook_type(request, pk):
    notebook = get_object_or_404(NotebookType, pk=pk)

    if request.method == 'POST':
        form = NotebookTypeForm(request.POST, instance=notebook)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الكراسة بنجاح.')
            return redirect('store:note')  # تعديل إلى اسم العرض الصحيح
    else:
        form = NotebookTypeForm(instance=notebook)

    return render(request, 'edit_notebook_type.html', {'form': form, 'notebook': notebook})

#############################################################


class NotebookTypeListView(CustomPermissionMixin, FilterView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = NotebookType
    template_name = 'notebooktype_list.html'
    filterset_class = NotebookTypeFilter
    paginate_by = 10

    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        filterset.filters['name'].extra['choices'] = [(notebook.name, notebook.name) for notebook in NotebookType.objects.all()]
        filterset.filters['size'].extra['choices'] = [(notebook.size, notebook.size) for notebook in NotebookType.objects.all()]
        return filterset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'قائمة أنواع الكراسات'
        filterset = self.get_filterset(self.filterset_class)
        filtered_notebooks = filterset.qs
        deliveries = NotebookDelivery.objects.filter(notebook_type__in=filtered_notebooks)
        context['deliveries'] = deliveries
   
        return context
    
@login_required
@custom_permission_required('is_admin', 'is_editor')
def export_notebooktype_excel(request):
    filename = f"NotebookType_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    headers = [
        'ترقيم',
        'نوع الكراسة',
        'حجم الكراسة',
        'وصف الكراسة',
        'مصدر التوريد',
        'اسم المورد',
        'الكمية الواردة',
        'الكمية الحالية',
        'تاريخ الاستلام'
    ]

    # كتابة العناوين
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    queryset = NotebookTypeFilter(request.GET, queryset=NotebookType.objects.all()).qs

    row = 1
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    max_deliveries = 0
    # Determine the maximum number of deliveries
    for notebook in queryset:
        deliveries_count = NotebookDelivery.objects.filter(notebook_type=notebook).count()
        if deliveries_count > max_deliveries:
            max_deliveries = deliveries_count

    # Add headers for delivery details
    for i in range(max_deliveries):
        worksheet.write(0, 10 + i*2, f'الكمية المستلمة {i+1}')
        worksheet.write(0, 11 + i*2, f'تاريخ التوريد {i+1}')

    for notebook in queryset:
        worksheet.write(row, 0, row)
        worksheet.write(row, 1, notebook.name)
        worksheet.write(row, 2, notebook.size)
        worksheet.write(row, 3, notebook.description)
        worksheet.write(row, 4, notebook.source)
        worksheet.write(row, 5, notebook.supplier.name if notebook.supplier else '')
        worksheet.write(row, 6, notebook.in_quantity)
        worksheet.write(row, 7, notebook.live_quantity)
        worksheet.write_datetime(row, 8, notebook.received_date, date_format)

        col_offset = 9  # بدء عمود تفاصيل التوريد

        deliveries = NotebookDelivery.objects.filter(notebook_type=notebook)
        for delivery in deliveries:
            worksheet.write(row, col_offset, delivery.quantity)
            worksheet.write_datetime(row, col_offset + 1, delivery.received_date, date_format)
            col_offset += 2

        row += 1

    workbook.close()
    return response
#####################################################################################3
@login_required
@custom_permission_required('is_admin', 'is_editor')

def add_notebook_assignment(request):
    if request.method == 'POST':
        form = NotebookAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:note')  
    else:
        form = NotebookAssignmentForm()
    return render(request, 'add_notebook_assignment.html', {'form': form})

def get_class_levels(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id).order_by('name')
    return render(request, 'class_levels_options.html', {'class_levels': class_levels})

class NotebookAssignmentListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = NotebookAssignment
    template_name = 'notebook_assignment_list.html'  
    context_object_name = 'assignments' 
    paginate_by = 10  

@login_required
@custom_permission_required('is_admin', 'is_editor')
def edit_notebook_assignment(request, pk):
    assignment = get_object_or_404(NotebookAssignment, pk=pk)
    if request.method == 'POST':
        form = NotebookAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('store:note')  # يمكنك تعديل هذا المسار حسب احتياجاتك
    else:
        form = NotebookAssignmentForm(instance=assignment)
    return render(request, 'edit_notebook_assignment.html', {'form': form, 'assignment': assignment})

###############################################################################################

@login_required
@custom_permission_required('is_admin', 'is_editor')
def add_school_booklet(request):
    if request.method == 'POST':
        form = SchoolBookletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:booklet')
    else:
        form = SchoolBookletForm()
    return render(request, 'add_school_booklet.html', {'form': form})

def get_class_levels(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id)
    data = [{'id': class_level.id, 'name': class_level.name} for class_level in class_levels]

    return JsonResponse(data, safe=False)

@login_required
@custom_permission_required('is_admin', 'is_editor')
def edit_school_booklet(request, pk):
    booklet = get_object_or_404(SchoolBooklet, pk=pk)

    if request.method == 'POST':
        form = SchoolBookletForm(request.POST, instance=booklet)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث البوكليت بنجاح.')
            return redirect('store:booklet')  # تأكد من تعديل المسار إلى اسم العرض الصحيح
    else:
        form = SchoolBookletForm(instance=booklet)

    return render(request, 'edit_school_booklet.html', {'form': form, 'booklet': booklet})
##################################################



class SchoolBookletListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = SchoolBooklet
    template_name = 'school_booklet_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['title'] = 'قائمة البوكليتات المدرسية'
        context['page_obj'] = page_obj

        # تمرير الفلتر إلى القالب
        booklet_filter = SchoolBookletFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = booklet_filter

        # استعلام للحصول على تفاصيل التوريد
        booklet_deliveries = BookletDelivery.objects.filter(booklet_type__in=booklet_filter.qs)
        context['deliveries'] = booklet_deliveries

        return context
@login_required
@custom_permission_required('is_admin', 'is_editor')

def add_BookletDelivery(request):
    if request.method == 'POST':
        form = BookletDeliveryForm(request.POST)
        if form.is_valid():
            booklet_delivery = form.save(commit=False)
            booklet_delivery.save()
            
            # تحديث الكمية الحالية في SchoolBooklet
            booklet = booklet_delivery.booklet_type
            booklet.live_quantity += booklet_delivery.quantity
            booklet.save()
            
            messages.success(request, _('تم إضافة تفاصيل التوريد بنجاح.'))
            return redirect('store:booklet')  # تعديل إلى اسم العرض الصحيح
    else:
        form = BookletDeliveryForm()
    return render(request, 'add_booklet_delivery.html', {'form': form})

    
@login_required
@custom_permission_required('is_admin', 'is_editor')
def export_school_booklet_excel(request):
    filename = f"school_booklet_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    headers = [
        'ترقيم',
        'عنوان البوكليت',
        'إصدار الكتاب',
        'وصف البوكليت',
        'مصدر التوريد',
        'اسم المورد',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الكمية الواردة',
        'الكمية الحالية',  # إضافة حقل "الكمية الحالية"
        'الترم الدراسي',
        'تاريخ الاستلام',
    ]

    # Get the queryset and calculate the maximum number of deliveries
    queryset = SchoolBookletFilter(request.GET, queryset=SchoolBooklet.objects.all()).qs
    max_deliveries = 0
    for booklet in queryset:
        deliveries_count = BookletDelivery.objects.filter(booklet_type=booklet).count()
        if deliveries_count > max_deliveries:
            max_deliveries = deliveries_count

    # Add headers for delivery details
    for i in range(max_deliveries):
        headers.extend([f'الكمية المستلمة {i+1}', f'تاريخ التوريد {i+1}'])

    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    row = 1
    for booklet in queryset:
        worksheet.write(row, 0, row)
        worksheet.write(row, 1, booklet.title)
        worksheet.write(row, 2, booklet.booklet_edition)
        worksheet.write(row, 3, booklet.description)
        worksheet.write(row, 4, booklet.source)
        worksheet.write(row, 5, booklet.supplier.name if booklet.supplier else '')
        worksheet.write(row, 6, str(booklet.stage))
        worksheet.write(row, 7, str(booklet.class_level))
        worksheet.write(row, 8, booklet.quantity)
        worksheet.write(row, 9, booklet.live_quantity)  # كتابة "الكمية الحالية"
        worksheet.write(row, 10, booklet.term)
        worksheet.write(row, 11, booklet.received_date.strftime('%Y-%m-%d'))

        # Write delivery details
        col_offset = 12  # تعيين بداية عمود تفاصيل التوريد
        deliveries = BookletDelivery.objects.filter(booklet_type=booklet)
        for delivery in deliveries:
            worksheet.write(row, col_offset, delivery.quantity)
            worksheet.write(row, col_offset + 1, delivery.received_date.strftime('%Y-%m-%d'))
            col_offset += 2

        row += 1

    workbook.close()
    return response


###############################################################################################

@login_required
@custom_permission_required('is_admin', 'is_editor')
def add_school_supplies(request):
    if request.method == 'POST':
        form = SchoolSuppliesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:list')  # يمكن تغيير الوجهة بحسب الحاجة
    else:
        form = SchoolSuppliesForm()
    return render(request, 'add_school_supplies.html', {'form': form})
##################################################################################################################################



class BookDistributionCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookDistribution
    form_class = BookDistributionForm
    template_name = 'book_distribution_form.html'
    success_url = reverse_lazy('store:home')

    def form_valid(self, form):
        # تحقق من رقم الإيصال هنا أيضًا لضمان صحة البيانات
        receipt_number = form.cleaned_data['receipt_number']
        student = form.cleaned_data['student']
        
        # قائمة الأرقام التي يمكن تكرارها
        exceptions = ['111', '222', '333']

        existing_records = BookDistribution.objects.filter(
            receipt_number=receipt_number,
            student=student
        ).exclude(receipt_number__in=exceptions)

        if existing_records.exists():
            form.add_error('receipt_number', 'رقم الإيصال موجود بالفعل لهذا الطالب')
            return self.form_invalid(form)

        book_distribution = form.save(commit=False)
        book_distribution.student = form.cleaned_data['student']
        book_distribution.stage = form.cleaned_data['stage']
        book_distribution.class_level = form.cleaned_data['class_level']
        book_distribution.section = form.cleaned_data['section']
        book_distribution.save()

        # Save many-to-many fields
        book_distribution.books.set(form.cleaned_data['books'])
        book_distribution.notebooks.set(form.cleaned_data['notebooks'])
        book_distribution.booklets.set(form.cleaned_data['booklets'])

        return super().form_valid(form)
        
        ###################################################


def search_student(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            students = Student.objects.filter(
                Q(name__icontains=query)
            )[:10]
            student_data = serializers.serialize('json', students)  # تحويل QuerySet إلى JSON
            return JsonResponse({'students': student_data}, content_type='application/json; charset=utf-8')
    return JsonResponse({'students': []})



####################################3

def get_selected_student(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student_id = request.GET.get('student_id')
        try:
            selected_student = Student.objects.get(id=student_id)
            data = {
                'id': selected_student.id,
                'name': selected_student.name,
                'stage': selected_student.stage,
                'class_level': selected_student.class_level.name,
                'section': selected_student.section.name,
            }
            
            # Print the retrieved selected student data for debugging
            print("Retrieved selected student data:", data)
            
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({})

#####################################3

# الحصول على الكتب المتاحة

def get_current_term():
    today = date.today()
    if today.month in [9, 10, 11, 12]:  # من سبتمبر إلى ديسمبر
        return 'الترم الأول'
    elif today.month in [1, 2, 3, 4, 5, 6, 7, 8]:  # من يناير إلى أبريل
        return 'الترم الثاني'
    else:
        return None  # خارج نطاق التوزيع

def get_available_books(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage

        # استبعاد الكتب التي تم تسليمها بالفعل للطالب
        delivered_books = BookDistribution.objects.filter(
            student=student
        ).values_list('books', flat=True)

        # الحصول على الترم الحالي
        current_term = get_current_term()

        if not current_term:
            return JsonResponse({'books': []})  # لا يوجد توزيع في هذه الفترة

        # جلب الكتب المتاحة للترم الحالي
        current_term_books = Book.objects.filter(
            stage=stage,
            class_level=class_level,
            term=current_term,
            available_quantity__gt=0
        ).exclude(id__in=delivered_books)

        # إذا كان الترم الثاني، جلب الكتب التي لم يتم استلامها من الترم الأول
        if current_term == 'الترم الثاني':
            previous_term_books = Book.objects.filter(
                stage=stage,
                class_level=class_level,
                term='الترم الأول',
                available_quantity__gt=0
            ).exclude(id__in=delivered_books)
        else:
            previous_term_books = Book.objects.none()

        # جمع الكتب المتاحة للترم الحالي والكتب التي لم يتم استلامها من الترم السابق
        combined_books = current_term_books | previous_term_books

        data = []
        for book in combined_books:
            book_data = {
                'id': book.id,
                'title': book.title 
            }
            data.append(book_data)
        return JsonResponse({'books': data})
    return JsonResponse({})




##########################################################################3


def get_available_notebooks(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage

        # استبعاد الكراسات التي تم تسليمها بالفعل للطالب
        delivered_notebooks = BookDistribution.objects.filter(
            student=student
        ).values_list('notebooks', flat=True)

        # الحصول على الترم الحالي
        current_term = get_current_term()

        if not current_term:
            return JsonResponse({'notebooks': []})  # لا يوجد توزيع في هذه الفترة

        # جلب الكراسات المتاحة للترم الحالي
        current_term_notebooks = NotebookAssignment.objects.filter(
            stage=stage,
            grade=class_level,
            term=current_term
        ).exclude(notebook__id__in=delivered_notebooks)

        # إذا كان الترم الثاني، جلب الكراسات التي لم يتم استلامها من الترم الأول
        if current_term == 'الترم الثاني':
            previous_term_notebooks = NotebookAssignment.objects.filter(
                stage=stage,
                grade=class_level,
                term='الترم الأول'
            ).exclude(notebook__id__in=delivered_notebooks)
        else:
            previous_term_notebooks = NotebookAssignment.objects.none()

        # جمع الكراسات المتاحة للترم الحالي والكراسات التي لم يتم استلامها من الترم السابق
        combined_notebooks = current_term_notebooks | previous_term_notebooks

        data = []
        for notebook_assignment in combined_notebooks:
            notebook_data = {
                'id': notebook_assignment.notebook.id,
                'name': notebook_assignment.notebook.name,
                'quantity_assignment': notebook_assignment.quantity_assignment  # إضافة الكمية المخصصة
            }
            data.append(notebook_data)
        return JsonResponse({'notebooks': data})
    return JsonResponse({})



#################################################################################



# الحصول على البوكليتات المتاحة
def get_available_booklets(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage

        # جلب تاريخ آخر عملية صرف للبوكليتات للطالب المحدد
        last_delivery_date = BookDistribution.objects.filter(
            student=student
        ).order_by('-delivery_date').first()

        # الحصول على الترم الحالي
        current_term = get_current_term()

        if not current_term:
            return JsonResponse({'booklets': []})  # لا يوجد توزيع في هذه الفترة

        if last_delivery_date:
            # استبعاد البوكليتات التي تم تسليمها بالفعل للطالب قبل التاريخ الأخير للصرف
            delivered_booklets = last_delivery_date.booklets.all()
        else:
            delivered_booklets = []

        # جلب البوكليتات المتاحة للترم الحالي
        current_term_booklets = SchoolBooklet.objects.filter(
            stage=stage,
            class_level=class_level,
            term=current_term,
            live_quantity__gt=0
        ).exclude(id__in=delivered_booklets)

        # إذا كان الترم الثاني، جلب البوكليتات التي لم يتم استلامها من الترم الأول
        if current_term == 'الترم الثاني':
            previous_term_booklets = SchoolBooklet.objects.filter(
                stage=stage,
                class_level=class_level,
                term='الترم الأول',
                live_quantity__gt=0
            ).exclude(id__in=delivered_booklets)
        else:
            previous_term_booklets = SchoolBooklet.objects.none()

        # جمع البوكليتات المتاحة للترم الحالي والبوكليتات التي لم يتم استلامها من الترم السابق
        combined_booklets = current_term_booklets | previous_term_booklets

        data = []
        for booklet in combined_booklets:
            booklet_data = {
                'id': booklet.id,
                'title': booklet.title
            }
            data.append(booklet_data)
        return JsonResponse({'booklets': data})
    return JsonResponse({})




####################################3


def get_student_info(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student_id = request.GET.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            stage = student.stage.stage if student.stage else None
            class_level = student.class_level.name if student.class_level else None
            section = student.section.id if student.section else None
            data = {
                'stage': stage,
                'class_level': class_level,
                'section': section,
                
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({})

#########################################################################################################


class BookDistributionUpdateView(CustomPermissionMixin, UpdateView):
    permissions = ['is_admin', 'is_editor']
    model = BookDistribution
    fields = ['student', 'stage', 'class_level', 'section', 'receipt_number', 'books', 'notebooks', 'booklets', 'delivery_date', 'distribution_status', 'recipient_name']
    template_name = 'book_distribution_update.html'
    success_url = reverse_lazy('store:book_distribution_list')




class BookDistributionDeleteView(CustomPermissionMixin, DeleteView):
    permissions = ['is_admin', 'is_editor']
    model = BookDistribution
    success_url = reverse_lazy('store:home')
    template_name = 'book_distribution_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "تم حذف توزيع الكتب والكراسات والبوكليتات بنجاح.")
        return HttpResponseRedirect(success_url)

########################################################################################################


class BookDistributionListView(CustomPermissionMixin, FilterView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    filterset_class = BookDistributionFilter
    queryset = BookDistribution.objects.all()
    template_name = 'book_distribution_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['title'] = 'قائمة توزيع الكتب والكراسات والبوكليتات'
        context['page_obj'] = page_obj
        return context
    

@login_required
@custom_permission_required('is_admin', 'is_editor')

def export_to_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="book_distribution.xlsx"'

    # إنشاء ملف Excel وورقة عمل
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # تحضير العناوين
    headers = [
        '#',
        'اسم الطالب',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الفصل الدراسي',
        'رقم الإيصال',
        'اسم المستلم',
        'تاريخ التوزيع',
        'حالة التوزيع',
        'الكتب المسلمة',
        'الكراسات المسلمة',
        'البوكليتات المسلمة',
    ]

    # كتابة العناوين في الصف الأول في الملف
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # استرجاع البيانات المصفاة وكتابتها في ملف Excel
    queryset = BookDistributionFilter(request.GET, queryset=BookDistribution.objects.all()).qs

    for row, distribution in enumerate(queryset, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, distribution.student.name)
        worksheet.write(row, 2, str(distribution.stage))
        worksheet.write(row, 3, str(distribution.class_level))
        worksheet.write(row, 4, str(distribution.section))
        worksheet.write(row, 5, distribution.receipt_number)
        worksheet.write(row, 6, distribution.recipient_name)
        worksheet.write(row, 7, distribution.delivery_date)
        worksheet.write(row, 8, distribution.get_distribution_status_display())
        worksheet.write(row, 9, distribution.get_books_titles())
        worksheet.write(row, 10, distribution.get_notebooks_titles())
        worksheet.write(row, 11, distribution.get_booklets_titles())

    # إغلاق ملف Excel وإرسال الاستجابة
    workbook.close()
    return response




########################################################################################################
@login_required
@custom_permission_required('is_admin', 'is_editor')

def migrate_students_view(request):
    if request.method == 'POST':
        form = StudentMigrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:Dashboard')
    else:
        form = StudentMigrationForm()
    return render(request, 'migrate_students.html', {'form': form})


####################################################################################################################


@login_required
@custom_permission_required('is_admin', 'is_editor')

def student_distribution_search(request):
    form = SearchForm(request.POST or None)
    students = []
    stage = class_level = distribution_status = None

    if request.method == 'POST' and form.is_valid():
        stage = form.cleaned_data['stage']
        class_level = form.cleaned_data['class_level']
        distribution_status = form.cleaned_data['distribution_status']

        request.session['stage'] = stage.id
        request.session['class_level'] = class_level.id
        request.session['distribution_status'] = distribution_status

        return redirect(request.path_info)

    elif request.method == 'GET':
        stage_id = request.session.get('stage')
        class_level_id = request.session.get('class_level')
        distribution_status = request.session.get('distribution_status')

        if stage_id and class_level_id and distribution_status:
            try:
                stage = Stage.objects.get(id=stage_id)
                class_level = ClassLevel.objects.get(id=class_level_id)
            except Stage.DoesNotExist:
                stage = None
            except ClassLevel.DoesNotExist:
                class_level = None

            if stage and class_level:
                if distribution_status == 'جزئي':
                    partial_distributions = BookDistribution.objects.filter(
                        stage=stage, 
                        class_level=class_level, 
                        distribution_status=BookDistribution.PARTIAL_DISTRIBUTION
                    )
                    student_ids = partial_distributions.values_list('student', flat=True)
                    students = Student.objects.filter(id__in=student_ids)

                    for student in students:
                        distribution = partial_distributions.get(student=student)
                        student.delivered_books = distribution.get_books_titles()
                        student.undelivered_books = distribution.get_undelivered_books_titles()
                        student.delivered_booklets = distribution.get_booklets_titles()
                        student.undelivered_booklets = distribution.get_undelivered_booklets_titles()
                elif distribution_status == 'غير مستلم':
                    distributed_students = BookDistribution.objects.filter(
                        stage=stage, 
                        class_level=class_level
                    ).values_list('student', flat=True)
                    students = Student.objects.filter(
                        stage=stage, 
                        class_level=class_level
                    ).exclude(id__in=distributed_students)
                else:  # حالة 'جميع الحالات'
                    students = Student.objects.filter(stage=stage, class_level=class_level)
                    distributions = BookDistribution.objects.filter(stage=stage, class_level=class_level)
                    for student in students:
                        try:
                            distribution = distributions.get(student=student)
                            student.delivered_books = distribution.get_books_titles()
                            student.undelivered_books = distribution.get_undelivered_books_titles()
                            student.delivered_booklets = distribution.get_booklets_titles()
                            student.undelivered_booklets = distribution.get_undelivered_booklets_titles()
                        except BookDistribution.DoesNotExist:
                            student.delivered_books = ""
                            student.undelivered_books = ""
                            student.delivered_booklets = ""
                            student.undelivered_booklets = ""

    paginator = Paginator(students, 30)  # عدد العناصر في كل صفحة
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)

    if request.GET.get('export'):
        return export_students_to_excel(students)

    return render(request, 'student_distribution_search.html', {'form': form, 'students': students_page})


#############################################################################
@login_required
@custom_permission_required('is_admin', 'is_editor')

def export_students_to_excel(students):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    headers = [
        '#',
        'اسم الطالب',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الفصل الدراسي',
        'الكتب المسلمة',
        'الكتب غير المسلمة',
        'البوكليتات المسلمة',
        'البوكليتات غير المسلمة'
    ]

    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row, student in enumerate(students, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, student.name)
        worksheet.write(row, 2, str(student.stage))  # تحويل الكائن إلى نص
        worksheet.write(row, 3, str(student.class_level.name))  # تحويل الكائن إلى نص
        worksheet.write(row, 4, str(student.section.name if student.section else ''))  # تحويل الكائن إلى نص
        worksheet.write(row, 5, getattr(student, 'delivered_books', ''))
        worksheet.write(row, 6, getattr(student, 'undelivered_books', ''))
        worksheet.write(row, 7, getattr(student, 'delivered_booklets', ''))
        worksheet.write(row, 8, getattr(student, 'undelivered_booklets', ''))

    workbook.close()
    return response

###############################################################################################################################


class BookDepreciationCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookDepreciation
    form_class = BookDepreciationForm
    template_name = 'book_depreciation_form.html'
    success_url = reverse_lazy('store:depreciations')

class BookDepreciationListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = BookDepreciation
    template_name = 'book_depreciation_list.html'
    context_object_name = 'depreciations'

###############################################################################################################################

class BookletDepreciationCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookDepreciation
    form_class = BookletDepreciationForm
    template_name = 'booklet_depreciation_form.html'
    success_url = reverse_lazy('store:depreciations')


class BookletDepreciationListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = BookletDepreciation
    template_name = 'booklet_depreciation_list.html'
    context_object_name = 'depreciations'

###############################################################################################################################


class NotebooDepreciationCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookletDepreciation
    form_class = NotebookDepreciationForm
    template_name = 'notebook_depreciation_form.html'
    success_url = reverse_lazy('store:depreciations')


class NotebooDepreciationListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor', 'is_viewer']
    model = NotebookDepreciation
    template_name = 'notebook_depreciation_list.html'
    context_object_name = 'depreciations'

###############################################################################################################################



class BookOutstoreCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookOutstore
    form_class = BookOutstoreForm
    template_name = 'BookOutstore_form.html'
    success_url = reverse_lazy('store:outlet')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stages'] = Stage.objects.all()
        context['class_levels'] = ClassLevel.objects.all()
        return context

def get_books(request):
    if request.method == 'GET':
        stage_id = request.GET.get('stage_id')
        class_level_id = request.GET.get('class_level_id')

        data = {}

        if stage_id:
            stage = Stage.objects.get(pk=stage_id)
            class_levels = ClassLevel.objects.filter(stage=stage)
            data['class_levels'] = [
                {
                    'id': class_level.id,
                    'name': class_level.get_name_display()  # استخدم get_name_display() للحصول على القيمة المقابلة للاختيار
                }
                for class_level in class_levels
            ]
            # امسح بيانات الكتب عند تغيير المرحلة
            data['books'] = []

        if stage_id and class_level_id:
            # الحصول على الترم الحالي
            current_term = get_current_term()

            if not current_term:
                data['books'] = []  # لا يوجد توزيع في هذه الفترة
            else:
                # جلب الكتب المتاحة للترم الحالي
                current_term_books = Book.objects.filter(
                    stage_id=stage_id,
                    class_level_id=class_level_id,
                    term=current_term,
                    available_quantity__gt=0
                )

                # إذا كان الترم الثاني، جلب الكتب التي لم يتم استلامها من الترم الأول
                if current_term == 'الترم الثاني':
                    previous_term_books = Book.objects.filter(
                        stage_id=stage_id,
                        class_level_id=class_level_id,
                        term='الترم الأول',
                        available_quantity__gt=0
                    )
                else:
                    previous_term_books = Book.objects.none()

                # جمع الكتب المتاحة للترم الحالي والكتب التي لم يتم استلامها من الترم السابق
                combined_books = current_term_books | previous_term_books

                data['books'] = [
                    {
                        'id': book.id,
                        'title': book.title
                    }
                    for book in combined_books
                ]

        return JsonResponse(data)
    return JsonResponse({})
#########################################

class BookOutstoreListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor']
    model = BookOutstore
    form_class = BookOutstoreForm
    template_name = 'BookOutstore_list.html'
 
###############################################################################################################################


class BookletOutstoreCreateView(CustomPermissionMixin, CreateView):
    permissions = ['is_admin', 'is_editor']
    model = BookletOutstore
    form_class = BookletOutstoreForm
    template_name = 'BookletOutstore_form.html'
    success_url = reverse_lazy('store:outlet')
def get_booklets(request):
    if request.method == 'GET' and 'stage_id' in request.GET and 'class_level_id' in request.GET:
        stage_id = request.GET.get('stage_id')
        class_level_id = request.GET.get('class_level_id')

        # الحصول على الترم الحالي
        current_term = get_current_term()

        if not current_term:
            return JsonResponse({'booklets': []})  # لا يوجد توزيع في هذه الفترة

        # جلب البوكليتات المتاحة للترم الحالي
        current_term_booklets = SchoolBooklet.objects.filter(
            stage_id=stage_id,
            class_level_id=class_level_id,
            term=current_term,
            live_quantity__gt=0
        )

        # إذا كان الترم الثاني، جلب البوكليتات التي لم يتم استلامها من الترم الأول
        if current_term == 'الترم الثاني':
            previous_term_booklets = SchoolBooklet.objects.filter(
                stage_id=stage_id,
                class_level_id=class_level_id,
                term='الترم الأول',
                live_quantity__gt=0
            )
        else:
            previous_term_booklets = SchoolBooklet.objects.none()

        # جمع البوكليتات المتاحة للترم الحالي والبوكليتات التي لم يتم استلامها من الترم السابق
        combined_booklets = current_term_booklets | previous_term_booklets

        data = []
        for booklet in combined_booklets:
            booklet_data = {
                'id': booklet.id,
                'title': booklet.title
            }
            data.append(booklet_data)
        return JsonResponse({'booklets': data})
    return JsonResponse({})

#########################################

class BookletOutstoreListView(CustomPermissionMixin, ListView):
    permissions = ['is_admin', 'is_editor']
    model = BookletOutstore
    form_class = BookletOutstoreForm
    template_name = 'bookletoutlet_list.html'




###############################################################################################

@login_required
@custom_permission_required('is_admin', 'is_editor')

def required_resources_view(request):
    required_resources = calculate_required_resources()

    context = {
        'required_books': required_resources['books'],
       
        'required_booklets': required_resources['booklets'],
    }
    return render(request, 'required_resources.html', context)



###############################################################################################################3


def load_class_levels(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id).order_by('name')
    data = [{'id': class_level.id, 'name': class_level.name} for class_level in class_levels]

    return JsonResponse(data, safe=False)


@login_required
@custom_permission_required('is_admin', 'is_editor')
def notebook_request_view(request):
    form = NotebookRequestForm()
    results = []

    if request.method == 'POST':
        form = NotebookRequestForm(request.POST)
        if form.is_valid():
            stage = form.cleaned_data['stage']
            class_levels = form.cleaned_data['class_levels']
            notebook_type = form.cleaned_data['notebook_type']
            quantity_per_student = form.cleaned_data['quantity_per_student']

            student_count = Student.objects.filter(stage=stage, class_level__in=class_levels).count()
            required_quantity = (quantity_per_student * student_count) - notebook_type.live_quantity

            results.append({
                'stage': stage.stage,
                'class_levels': ", ".join([class_level.name for class_level in class_levels]),
                'notebook_type': notebook_type.name,
                'required_quantity': max(0, required_quantity)
            })

    return render(request, 'notebook_request.html', {'form': form, 'results': results})


