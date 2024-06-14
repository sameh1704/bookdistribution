from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_save
from django.db import transaction
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator


#######################################################################
class AcademicYear(models.Model):
    year = models.IntegerField(unique=True, verbose_name="السنة الدراسية")
    
    def __str__(self):
        return str(self.year)
    class Meta:
        verbose_name = 'السنة'
        verbose_name_plural = '  السنة الدراسية'


class Stage(models.Model):
    STAGE_CHOICES = [
        ('تمهيدى', 'تمهيدى'),
        ('رياض الأطفال', 'رياض الأطفال'),
        ('primry', 'primry'),
        ('الاعدادية', 'الاعدادية'),
        ('الثانوية', 'الثانوية'),
    ]
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, verbose_name='المرحلة الدراسية')
    

   
    def __str__(self):
        return f"{self.stage} "

    class Meta:
        unique_together = ['stage']
        verbose_name = 'المرحلة'
        verbose_name_plural = 'المراحل الدراسية'


    class Meta:
        unique_together = ['stage']
        verbose_name = 'المرحلة'
        verbose_name_plural = 'المراحل الدراسية'
    
    
class ClassLevel(models.Model):
    class_choices = [
        ('تمهيدى', 'تمهيدى'),
        ('KG1', 'KG1'),
        ('KG2', 'KG2'),
        ('PRIM 1', 'PRIM 1'),
        ('PRIM 2', 'PRIM 2'),
        ('PRIM 3', 'PRIM 3'),
        ('PRIM 4', 'PRIM 4'),
        ('PRIM 5', 'PRIM 5'),
        ('PRIM 6', 'PRIM 6'),
        ('PREP 1', 'الصف الاعدادى الأول'),
        ('PREP 2', 'الصف الثاني الاعدادى '),
        ('PREP 3', 'الصف الثالث الاعدادى '),
        ('SEC 1', 'الصف الأول الثانوي '),
        ('SEC 2', 'الصف الثاني الثانوي '),
        ('SEC 3', 'الصف الثالث الثانوي '),
    ]
    name = models.CharField(max_length=50, choices=class_choices, verbose_name='اسم الصف الدراسي')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['stage', 'name', 'academic_year']]
        verbose_name = 'الصف'
        verbose_name_plural = 'الصف الدراسي'


class Classroom(models.Model):
    name = models.CharField(max_length=2, verbose_name='الفصل الدراسي')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة')
    class_levels = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')

    def __str__(self):
        return f"{self.name} "

    class Meta:
        unique_together = [['class_levels', 'name']]
        verbose_name = 'ترقيم الفصول'
        verbose_name_plural = 'الفصل الدراسي'


##########################################################################################################################


from datetime import date, datetime

from datetime import datetime
from django.core.exceptions import ValidationError

class Student(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية", related_name="students")
    name = models.CharField(max_length=255, verbose_name='اسم الطالب')
    national_id = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message='يجب أن يحتوي الرقم القومي على 14 رقمًا بدقة.',
                code='invalid_national_id'
            )
        ],
        verbose_name='الرقم القومي'
    )
    phone_number = models.CharField(max_length=15, verbose_name='رقم الهاتف')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    section = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, verbose_name='الفصل الدراسي')

    def migrate_to_next_level(self):
        # استخراج قائمة الصفوف الدراسية الحالية في المرحلة الحالية
        current_stage_class_levels = list(self.stage.classlevel_set.all().order_by('id'))

        # التحقق من كون الطالب في الصف الأخير في المرحلة
        if self.class_level == current_stage_class_levels[-1]:
            # الترحيل إلى المرحلة التالية
            next_stage = Stage.objects.filter(id__gt=self.stage.id).order_by('id').first()
            if next_stage:
                next_class_level = next_stage.classlevel_set.first()  # الصف الدراسي الأول في المرحلة التالية
                self.stage = next_stage
                self.class_level = next_class_level
                # تعيين الفصل الدراسي الجديد بناءً على الاسم المشابه للفصل الحالي
                self.section = Classroom.objects.filter(stage=next_stage, class_levels=next_class_level, name=self.section.name).first()
                # زيادة العام الدراسي بمقدار واحد
                self.academic_year = AcademicYear.objects.get_or_create(year=self.academic_year.year + 1)[0]
        else:
            # الترحيل إلى الصف التالي في نفس المرحلة
            next_class_level = current_stage_class_levels[current_stage_class_levels.index(self.class_level) + 1]
            self.class_level = next_class_level
            # تعيين الفصل الدراسي الجديد بناءً على الاسم المشابه للفصل الحالي
            self.section = Classroom.objects.filter(stage=self.stage, class_levels=next_class_level, name=self.section.name).first()

    def save(self, *args, **kwargs):
        current_year = datetime.now().year
        current_month = datetime.now().month

        if not self.pk:
            academic_year, created = AcademicYear.objects.get_or_create(year=current_year)
            self.academic_year = academic_year  # تعيين العام الدراسي إلى العام الحالي
        else:
            if current_month > 7 and self.academic_year.year != current_year:  # إذا كان الشهر الحالي بعد يوليو ولم يكن العام الدراسي الحالي هو العام الحالي
                self.migrate_to_next_level()  # ترحيل الطالب
                self.academic_year = AcademicYear.objects.get_or_create(year=current_year)[0]  # تحديث العام الدراسي إلى العام الحالي
        super().save(*args, **kwargs)

    def clean(self):
        # التحقق من عدم تكرار الرقم القومي داخل السنة الدراسية نفسها
        students_with_same_national_id = Student.objects.filter(national_id=self.national_id, academic_year=self.academic_year).exclude(id=self.id)
        if students_with_same_national_id.exists():
            raise ValidationError({'national_id': 'هذا الرقم القومي موجود بالفعل في سجلات الطلاب.'})

        # التحقق من أن رقم الهاتف يحتوي على أكثر من 12 رقم وأنه يتكون من أرقام فقط
        if len(self.phone_number) < 11:
            raise ValidationError(_('رقم الهاتف يجب أن يحتوي على 11 رقم على الأقل.'))
        if not self.phone_number.isdigit():
            raise ValidationError(_('رقم الهاتف يجب أن يتكون من أرقام فقط.'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'الطالب'
        verbose_name_plural = 'اضافة الطلاب'




##########################################################################################################################

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المورد')
    phone = models.CharField(max_length=15, verbose_name='رقم تليفون المورد')

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = 'مورد'
        verbose_name_plural = 'الموردين'

#############################################################################################################################


class Book(models.Model):

    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]

    title = models.CharField(max_length=100, verbose_name='المادة الدراسية')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    received_quantity = models.PositiveIntegerField(verbose_name='الكمية الواردة', validators=[MinValueValidator(0)])
    available_quantity = models.PositiveIntegerField(verbose_name='الكمية المتاحة',)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    def save(self, *args, **kwargs):
        if not self.id:
            self.available_quantity = self.received_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.source} - {self.term} - Available Quantity: {self.available_quantity}'

    class Meta:
        verbose_name = 'كتاب دراسي'
        verbose_name_plural = 'المواد الدراسية'
        constraints = [
            UniqueConstraint(fields=['title', 'source', 'term', 'stage', 'class_level'], name='unique_book_per_class')
        ]

class BookDelivery(models.Model):
    book_type = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='المادة الدراسية')
    quantity = models.IntegerField(verbose_name='الكمية المستلمة')
    received_date = models.DateField(verbose_name='تاريخ التوريد', auto_now_add=False)

    def __str__(self):
        return f'{self.book_type.title} - {self.quantity} - {self.received_date}'

    class Meta:
        verbose_name = ' اضافة توريد كتب '
        verbose_name_plural = ' اضافة توريد كتب '

########################################################################################################

class SchoolBooklet(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        (' مدرسة المنار', 'مدرسة المنار'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='عنوان البوكليت')
    booklet_edition = models.CharField(max_length=20, verbose_name='إصدار الكتاب', blank=True, null=True)
    description = models.TextField(verbose_name='وصف البوكليت', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey('ClassLevel', on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة', validators=[MinValueValidator(0)])
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.source} - {self.term} - الكمية الحالية : {self.live_quantity}'

    class Meta:
        verbose_name = 'بوكليت مدرسي'
        verbose_name_plural = 'البوكليتات المدرسية'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'booklet_edition', 'stage', 'class_level'],
                name='unique_booklet'
            )
        ]


class BookletDelivery(models.Model):
    booklet_type = models.ForeignKey(SchoolBooklet, on_delete=models.CASCADE, verbose_name=_('نوع البوكليت'))
    quantity = models.IntegerField(default=0, verbose_name=_('الكمية المستلمة'), validators=[MinValueValidator(0)])
    received_date = models.DateField(verbose_name=_('تاريخ التوريد'), auto_now_add=False)

    def __str__(self):
        return f'{self.booklet_type.title} - {self.quantity} - {self.received_date}'

    class Meta:
        verbose_name = _('تفاصيل توريد البوكليت')
        verbose_name_plural = _('تفاصيل توريد البوكليت')

    ############################################################################################################


class SchoolSupplies(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]
    name = models.CharField(max_length=100, verbose_name='   الأداة المدرسية')
    description = models.TextField(verbose_name='وصف   الأداة المدرسية', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    in_quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة')
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')


    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.in_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ادوات   مدرسية'
        verbose_name_plural = 'الادوات المدرسية'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'description'],
                name='unique_school_supplies'
            )
        ]
#######################################################################################################3
class NotebookType(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]

    name = models.CharField(max_length=100, verbose_name='نوع الكراسة')
    size = models.CharField(max_length=50, verbose_name='حجم الكراسة')
    description = models.CharField(max_length=100, verbose_name='وصف الكراسة', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    in_quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة')
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    
    def decrement_quantity(self):
        if self.live_quantity > 0:
            self.live_quantity -= 1
            self.save()
        else:
            raise ValidationError("لا يوجد رصيد كافٍ لهذه الكراسة")
    
    def increment_quantity(self):
       self.live_quantity += 1
       self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.in_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.size}'

    class Meta:
        verbose_name = 'نوع كراسة'
        verbose_name_plural = 'أنواع الكراسات'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'size'],
                name='unique_notebook_type'
            )
        ]



class NotebookAssignment(models.Model):
    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    grade = models.ForeignKey('ClassLevel', on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    notebook = models.ForeignKey(NotebookType, on_delete=models.CASCADE, verbose_name='الكراسة')
    quantity_assignment = models.PositiveIntegerField(default=0, verbose_name='الكمية المخصصة')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية")
    assigned_date = models.DateField(auto_now_add=True, verbose_name='تاريخ التخصيص')
    

    def __str__(self):
        return f'{self.grade} - {self.notebook.name} - {self.quantity_assignment}- {self.term}'

    class Meta:
        verbose_name = 'تخصيص كراسة'
        verbose_name_plural = 'تخصيصات الكراسات'
        




#######################################################################################################################

class BookDistribution(models.Model):
    PARTIAL_DISTRIBUTION = 'جزئي'
    FULL_DISTRIBUTION = 'كامل'
    DISTRIBUTION_CHOICES = [
        (PARTIAL_DISTRIBUTION, 'توزيع جزئي'),
        (FULL_DISTRIBUTION, 'توزيع كامل'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='الطالب')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    section = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='الفصل الدراسي')
    receipt_number = models.CharField(max_length=20, verbose_name='رقم الإيصال')
    
    books = models.ManyToManyField(Book, verbose_name='الكتب المسلمة', blank=True)
    notebooks = models.ManyToManyField(NotebookType, verbose_name='الكراسات المسلمة', blank=True)
    booklets = models.ManyToManyField(SchoolBooklet, verbose_name='البوكليتات المسلمة', blank=True)

    delivery_date = models.DateField(auto_now_add=False, verbose_name='تاريخ التوزيع')
    distribution_status = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default=FULL_DISTRIBUTION, verbose_name='حالة التوزيع')
    recipient_name = models.CharField(max_length=100, verbose_name='اسم المستلم')

    def get_books_titles(self):
        return ", ".join([book.title for book in self.books.all()])

    def get_notebooks_titles(self):
        return ", ".join([notebook.name for notebook in self.notebooks.all()])
    
    def get_booklets_titles(self):
        return ", ".join([booklet.title for booklet in self.booklets.all()])
 

    def get_undelivered_books_titles(self):
        delivered_books = self.books.all()
        all_books = Book.objects.filter(stage=self.stage, class_level=self.class_level)
        undelivered_books = all_books.exclude(id__in=delivered_books)
        return ", ".join([book.title for book in undelivered_books])

    def get_undelivered_booklets_titles(self):
        delivered_booklets = self.booklets.all()
        all_booklets = SchoolBooklet.objects.filter(stage=self.stage, class_level=self.class_level)
        undelivered_booklets = all_booklets.exclude(id__in=delivered_booklets)
        return ", ".join([booklet.title for booklet in undelivered_booklets])

    def __str__(self):
        return f'{self.student.name} - {self.stage} - {self.class_level} - {self.receipt_number}'

    class Meta:
        verbose_name = 'توزيع الكتب والكراسات والبوكليتات'
        verbose_name_plural = 'توزيع الكتب والكراسات والبوكليتات'
        unique_together = ['student', 'delivery_date', 'receipt_number']
        
    def delete(self, *args, **kwargs):
        for book in self.books.all():
            book.available_quantity += 1
            book.save()

        for booklet in self.booklets.all():
            booklet.live_quantity += 1
            booklet.save()

        for notebook in self.notebooks.all():
            assignment = NotebookAssignment.objects.get(notebook=notebook, grade=self.class_level, stage=self.stage)
            notebook.live_quantity += assignment.quantity_assignment
            notebook.save()

        super().delete(*args, **kwargs)


  # إضافة استقبال لتغييرات البوكليتات
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(m2m_changed, sender=BookDistribution.books.through)
def update_books_quantity(sender, instance, action, **kwargs):
    if action == 'post_add':
        for book in instance.books.all():
            if book.available_quantity > 0:
                book.available_quantity -= 1
                book.save()
    elif action == 'post_remove':
        for book in instance.books.all():
            book.available_quantity += 1
            book.save()

@receiver(m2m_changed, sender=BookDistribution.booklets.through)
def update_booklets_quantity(sender, instance, action, **kwargs):
    if action == 'post_add':
        for booklet in instance.booklets.all():
            if booklet.live_quantity > 0:
                booklet.live_quantity -= 1
                booklet.save()
    elif action == 'post_remove':
        for booklet in instance.booklets.all():
            booklet.live_quantity += 1
            booklet.save()

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def get_current_term():
    today = date.today()
    if today.month in [9, 10, 11, 12]:  # من سبتمبر إلى ديسمبر
        return 'الترم الأول'
    elif today.month in [1, 2, 3, 4, 5, 6]:  # من يناير إلى أبريل
        return 'الترم الثاني'
    else:
        return None  # خارج نطاق التوزيع

@receiver(m2m_changed, sender=BookDistribution.notebooks.through)
def update_notebooks_quantity(sender, instance, action, **kwargs):
    current_term = get_current_term()
    if not current_term:
        raise ValidationError("التوزيع غير مسموح به في هذه الفترة.")

    if action == 'post_add':
        for pk in kwargs['pk_set']:
            notebook = NotebookType.objects.get(pk=pk)
            try:
                assignment = NotebookAssignment.objects.get(notebook=notebook, grade=instance.class_level, stage=instance.stage, term=current_term)
                if notebook.live_quantity >= assignment.quantity_assignment:
                    notebook.live_quantity -= assignment.quantity_assignment
                    notebook.save()
                else:
                    raise ValidationError(f"لا يوجد كمية كافية للكراسة {notebook.name}")
            except NotebookAssignment.DoesNotExist:
                raise ValidationError(f"لا يوجد تخصيص للكراسة {notebook.name} للترم الحالي.")
    elif action == 'post_remove':
        for pk in kwargs['pk_set']:
            notebook = NotebookType.objects.get(pk=pk)
            try:
                assignment = NotebookAssignment.objects.get(notebook=notebook, grade=instance.class_level, stage=instance.stage, term=current_term)
                notebook.live_quantity += assignment.quantity_assignment
                notebook.save()
            except NotebookAssignment.DoesNotExist:
                raise ValidationError(f"لا يوجد تخصيص للكراسة {notebook.name} للترم الحالي.")


#######################################################################################################################

from django.db import models
from .models import NotebookType

class NotebookDelivery(models.Model):
    notebook_type = models.ForeignKey(NotebookType, on_delete=models.CASCADE, verbose_name='نوع الكراسة')
    quantity = models.IntegerField(verbose_name='الكمية المستلمة')
    received_date = models.DateField(verbose_name='تاريخ التوريد', auto_now_add=False)  # قم بإزالة auto_now_add=True

    def __str__(self):
        return f'{self.notebook_type.name} - {self.quantity} - {self.received_date}'

    class Meta:
        verbose_name = 'توريد كراسة'
        verbose_name_plural = 'توريدات الكراسات'
#################################################################################################

class BookDepreciation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='الكتاب')
    quantity = models.PositiveIntegerField(verbose_name='الكمية المستهلكة', validators=[MinValueValidator(1)])
    cause = models.CharField(max_length=100, verbose_name='سبب الإهلاك')
    date = models.DateField(auto_now_add=True, verbose_name='تاريخ الإهلاك')

    def save(self, *args, **kwargs):
        if self.book.available_quantity < self.quantity:
            raise ValidationError("الكمية المستهلكة لا يمكن أن تتجاوز الكمية المتاحة")
        self.book.available_quantity -= self.quantity
        self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.book.title} - {self.quantity} - {self.date}'

    class Meta:
        verbose_name = 'إهلاك كتاب'
        verbose_name_plural = 'إهلاك الكتب'

#################################################################################################################
class BookletDepreciation(models.Model):
    booklet = models.ForeignKey(SchoolBooklet, on_delete=models.CASCADE, verbose_name='البوكليت')
    quantity = models.PositiveIntegerField(verbose_name='الكمية المستهلكة', validators=[MinValueValidator(1)])
    cause = models.CharField(max_length=100, verbose_name='سبب الإهلاك')
    date = models.DateField(auto_now_add=True, verbose_name='تاريخ الإهلاك')

    def save(self, *args, **kwargs):
        if self.booklet.live_quantity < self.quantity:
            raise ValidationError("الكمية المستهلكة لا يمكن أن تتجاوز الكمية المتاحة")
        self.booklet.live_quantity -= self.quantity
        self.booklet.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.booklet.title} - {self.quantity} - {self.date}'

    class Meta:
        verbose_name = 'إهلاك البوكليت'
        verbose_name_plural = 'إهلاك البوكليت'


#################################################################################################################
class NotebookDepreciation(models.Model):
    notebook = models.ForeignKey(NotebookType, on_delete=models.CASCADE, verbose_name='الكراسات')
    quantity = models.PositiveIntegerField(verbose_name='الكمية المستهلكة', validators=[MinValueValidator(1)])
    cause = models.CharField(max_length=100, verbose_name='سبب الإهلاك')
    date = models.DateField(auto_now_add=True, verbose_name='تاريخ الإهلاك')

    def save(self, *args, **kwargs):
        if self.notebook.live_quantity < self.quantity:
            raise ValidationError("الكمية المستهلكة لا يمكن أن تتجاوز الكمية المتاحة")
        self.notebook.live_quantity -= self.quantity
        self.notebook.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.notebook.title} - {self.quantity} - {self.date}'

    class Meta:
        verbose_name = 'إهلاك الكراسات'
        verbose_name_plural = 'إهلاك الكراسات'




#######################################################################################################################

class BookOutstore(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المستلم')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='الكتاب')
    quantity = models.PositiveIntegerField(verbose_name='الكمية ', validators=[MinValueValidator(1)])
    date = models.DateField(auto_now_add=False, verbose_name='تاريخ الصرف')
    
    def save(self, *args, **kwargs):
        if self.book.available_quantity < self.quantity:
            raise ValidationError("الكمية لا يمكن أن تتجاوز الكمية المتاحة")
        self.book.available_quantity -= self.quantity
        self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name.title} - {self.quantity} - {self.date}'

    class Meta:
        verbose_name = 'صرف كتاب'
        verbose_name_plural = 'صرف الكتب'
#######################################################################################################################

class BookletOutstore(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المستلم')
    booklet = models.ForeignKey(SchoolBooklet, on_delete=models.CASCADE, verbose_name='البوكليت')
    quantity = models.PositiveIntegerField(verbose_name='الكمية ', validators=[MinValueValidator(1)])
    date = models.DateField(auto_now_add=False, verbose_name='تاريخ الصرف')
    

    def save(self, *args, **kwargs):
        if self.booklet.live_quantity < self.quantity:
            raise ValidationError("الكمية المستهلكة لا يمكن أن تتجاوز الكمية المتاحة")
        self.booklet.live_quantity -= self.quantity
        self.booklet.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.booklet.title} - {self.quantity} - {self.date}'


    class Meta:
        verbose_name = 'صرف بوكليت'
        verbose_name_plural = 'صرف بوكليت'