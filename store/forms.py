from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from .models import AcademicYear, BookDepreciation, BookOutstore, BookletOutstore, ClassLevel, Classroom, NotebookDepreciation, Stage, Student, Supplier, Book, BookDistribution
from .models import BookDistribution
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import BookDistribution, Book, NotebookType, SchoolBooklet, Stage, ClassLevel, Classroom , BookletDepreciation
from django.forms import ValidationError
from django import forms
from .models import NotebookType
from django import forms
from .models import NotebookAssignment
from .models import SchoolBooklet
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import SchoolSupplies
##########################################################################################################
class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['name', 'stage', 'academic_year']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('يرجى إدخال اسم الصف.')
        if not name.strip().replace(" ", "").isalpha():
            raise forms.ValidationError('اسم الصف يجب أن يحتوي على أحرف فقط.')
        return name

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'class_levels']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('يرجى إدخال اسم الفصل.')
        return name

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage']

    def clean(self):
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        academic_year = cleaned_data.get('academic_year')

        if stage and academic_year:
            if stage == 'رياض الأطفال' and academic_year.year != 1:
                raise forms.ValidationError('خطأ: رياض الأطفال يجب أن يكون الصف الوحيد في السنة الدراسية الأولى.')

        return cleaned_data

#######################################################
from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone']
        labels = {
            'name': 'اسم المورد',
            'phone': 'رقم تليفون المورد',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
##############################################################################################################################
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'national_id', 'phone_number', 'stage', 'class_level', 'section', 'academic_year']

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if not national_id.isdigit():
            raise forms.ValidationError('الرقم القومي يجب أن يحتوي على أرقام فقط.')
        return national_id
######################################################################################################################

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')
        return phone
###################################################################################################################################3

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'source', 'received_quantity', 'supplier', 'stage', 'class_level', 'term']

    def clean_received_date(self):
        received_date = self.cleaned_data['received_date']
        if received_date < timezone.now().date():
            raise ValidationError('لا يمكنك تحديد تاريخ في الماضي.')
        return received_date

    def clean(self):
        super().clean()
        stage = self.cleaned_data.get('stage')
        class_level = self.cleaned_data.get('class_level')
        if stage and class_level:
            # التحقق من أن الصف الدراسي المحدد يتناسب مع المرحلة
            if not class_level.stage == stage:
                raise ValidationError('الصف الدراسي المحدد لا يتناسب مع المرحلة المحددة.')
        #######################################################################################################
from .models import BookDelivery

class BookDeliveryForm(forms.ModelForm):
    class Meta:
        model = BookDelivery
        fields = ['book_type', 'quantity', 'received_date']
        widgets = {
            'book_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


###########################################################################################################################33


class NotebookTypeForm(forms.ModelForm):
    class Meta:
        model = NotebookType
        fields = ['name', 'size', 'description', 'source', 'supplier', 'in_quantity']


######################################################################################################3


class NotebookAssignmentForm(forms.ModelForm):
    class Meta:
        model = NotebookAssignment
        fields = ['stage', 'grade', 'notebook', 'quantity_assignment', 'term', 'year']

    def clean(self):
        cleaned_data = super().clean()
        notebook = cleaned_data.get('notebook')
        quantity_assignment = cleaned_data.get('quantity_assignment')
        if notebook and quantity_assignment:
            if quantity_assignment > notebook.live_quantity:
                raise forms.ValidationError('الكمية المخصصة أكبر من الكمية المتاحة للكراسة.')
        return cleaned_data
##############################################################################

from django import forms
from .models import NotebookDelivery

class NotebookDeliveryForm(forms.ModelForm):
    class Meta:
        model = NotebookDelivery
        fields = ['notebook_type', 'quantity', 'received_date']
        widgets = {
            'notebook_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


####################################################################################################################################3



class SchoolBookletForm(forms.ModelForm):
    class Meta:
        model = SchoolBooklet
        fields = ['title', 'booklet_edition', 'description', 'source', 'supplier', 'stage', 'class_level', 'quantity', 'term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'stage' in self.data:
            try:
                stage_id = int(self.data.get('stage'))
                self.fields['class_level'].queryset = ClassLevel.objects.filter(stage_id=stage_id)
            except (ValueError, TypeError):
                pass  # يتم تجاهل أي خطأ هنا


    
    
from django import forms
from .models import BookletDelivery

class BookletDeliveryForm(forms.ModelForm):
    class Meta:
        model = BookletDelivery
        fields = ['booklet_type', 'quantity', 'received_date']
        widgets = {
            'booklet_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

####################################################################################################################################3
    


class SchoolSuppliesForm(forms.ModelForm):
    class Meta:
        model = SchoolSupplies
        fields = ['name', 'description', 'source', 'supplier', 'in_quantity', 'term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        term = cleaned_data.get('term')

        if name and description:
            # التحقق من عدم تكرار تسجيل الأدوات
            if SchoolSupplies.objects.filter(name=name, description=description).exists():
                raise forms.ValidationError('هذه الأداة المدرسية مسجلة بالفعل.')

        # التحقق من الكمية
        in_quantity = cleaned_data.get('in_quantity')
        if in_quantity < 0:
            raise forms.ValidationError('الكمية يجب أن تكون أكبر من الصفر.')

        return cleaned_data



####################################################################################################################################3





# فورم البحث عن الطالب
class StudentSearchForm(forms.Form):
    student_name = forms.CharField(label='اسم الطالب', max_length=255)

    def __init__(self, *args, **kwargs):
        super(StudentSearchForm, self).__init__(*args, **kwargs)
        self.fields['student_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ادخل اسم الطالب'})
        
# فورم اختيار الطالب
class StudentSelectForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')  # استخراج الطلاب من الوسيطة
        super(StudentSelectForm, self).__init__(*args, **kwargs)
        # إعداد اختيار الطالب المحدد لاستخدامه في القائمة المنسدلة
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].queryset = students

    # إضافة دالة clean لتحديث حقول المرحلة والصف والفصل بالقيم الصحيحة عند اختيار الطالب
    def clean(self):
        cleaned_data = super().clean()
        selected_student = cleaned_data.get('name')
        if selected_student:
            cleaned_data['stage'] = selected_student.stage
            cleaned_data['class_level'] = selected_student.class_level
            cleaned_data['section'] = selected_student.section

# فورم توزيع الكتب والكراسات والبوكليتات

class BookDistributionForm(forms.ModelForm):
    search_student = forms.CharField(label='ابحث عن الطالب', max_length=255, required=True)
    receipt_number = forms.CharField(label='رقم ايصال الدفع', required=True)

    # تحديد حقول الكتب والكراسات والبوكليتات غير ملزمة
    books = forms.ModelMultipleChoiceField(queryset=Book.objects.all(), widget=forms.SelectMultiple, required=False)
    notebooks = forms.ModelMultipleChoiceField(queryset=NotebookType.objects.all(), widget=forms.SelectMultiple, required=False)
    booklets = forms.ModelMultipleChoiceField(queryset=SchoolBooklet.objects.all(), widget=forms.SelectMultiple, required=False)
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), required=True, label='المرحلة الدراسية')
    class_level = forms.ModelChoiceField(queryset=ClassLevel.objects.all(), required=True, label='الصف الدراسي')
    section = forms.ModelChoiceField(queryset=Classroom.objects.all(), required=True, label='الفصل الدراسي')
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}), required=True, label='تاريخ التوزيع')

 
    def __init__(self, *args, **kwargs):
        super(BookDistributionForm, self).__init__(*args, **kwargs)
        self.fields['delivery_date'].initial = timezone.now().date()

    def clean_receipt_number(self):
        receipt_number = self.cleaned_data.get('receipt_number')
        student = self.cleaned_data.get('student')

        if not receipt_number:
            raise forms.ValidationError('يرجى إدخال رقم ايصال الدفع')

        # قائمة الأرقام التي يمكن تكرارها
        exceptions = ['111', '222', '333']

        # تحقق مما إذا كان رقم الإيصال موجود بالفعل لنفس الطالب
        existing_records = BookDistribution.objects.filter(
            receipt_number=receipt_number,
            student=student
        ).exclude(receipt_number__in=exceptions)

        # إذا كان هناك سجلات موجودة
        if existing_records.exists():
            raise forms.ValidationError('رقم الإيصال موجود بالفعل لهذا الطالب')

        return receipt_number

    def clean_student(self):
        student = self.cleaned_data.get('student')
        if not student:
            raise forms.ValidationError('يرجى تحديد الطالب')
        return student

    class Meta:
        model = BookDistribution
        fields = ['search_student', 'student', 'stage', 'class_level', 'section', 'receipt_number', 'books', 'notebooks', 'booklets', 'recipient_name', 'distribution_status', 'delivery_date']

#################################################################################################################################


from django import forms
from .models import Stage, ClassLevel

class SearchForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), required=True, label='المرحلة الدراسية')
    class_level = forms.ModelChoiceField(queryset=ClassLevel.objects.all(), required=True, label='الصف الدراسي')
    distribution_status = forms.ChoiceField(
        choices=[('all', 'جميع الحالات'), ('جزئي', 'تسليم جزئي'), ('غير مستلم', 'غير مستلم')],
        required=True,
        label='حالة التوزيع'
    )

#################################################################################################################################

from .models import Student, Stage, ClassLevel


class StudentMigrationForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), label='المرحلة الدراسية', required=False)
    class_level = forms.ModelChoiceField(queryset=ClassLevel.objects.none(), label='الصف الدراسي', required=False)
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.none(), label='الطلاب', widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(StudentMigrationForm, self).__init__(*args, **kwargs)
        if 'stage' in self.data:
            try:
                stage_id = int(self.data.get('stage'))
                self.fields['class_level'].queryset = ClassLevel.objects.filter(stage_id=stage_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('stage'):
            self.fields['class_level'].queryset = self.initial['stage'].classlevel_set.order_by('name')

        if 'class_level' in self.data:
            try:
                class_level_id = int(self.data.get('class_level'))
                self.fields['students'].queryset = Student.objects.filter(class_level_id=class_level_id).order_by('name')
            except (ValueError, TypeError):
                pass

    def save(self):
        students = self.cleaned_data['students']
        for student in students:
            student.migrate_to_next_level()
            student.save()
##########################################################################################################

class BookDepreciationForm(forms.ModelForm):
    class Meta:
        model = BookDepreciation
        fields = ['book', 'quantity', 'cause']
##########################################################################################################

class BookletDepreciationForm(forms.ModelForm):
    class Meta:
        model = BookletDepreciation
        fields = ['booklet', 'quantity', 'cause']



##########################################################################################################

class NotebookDepreciationForm(forms.ModelForm):
    class Meta:
        model = NotebookDepreciation
        fields = ['notebook', 'quantity', 'cause']

##########################################################################################################

class BookOutstoreForm(forms.ModelForm):
    class Meta:
        model = BookOutstore
        fields = ['name', 'book', 'quantity', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

##########################################################################################################

class BookletOutstoreForm(forms.ModelForm):
    class Meta:
        model = BookletOutstore
        fields = ['name', 'booklet', 'quantity', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

