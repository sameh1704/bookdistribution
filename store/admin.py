from django.contrib import admin
from .models import Stage, ClassLevel, Classroom, Student, Book, Supplier, BookDistribution , AcademicYear , SchoolBooklet , SchoolSupplies  , NotebookDelivery  , BookDepreciation , BookletDepreciation , NotebookDepreciation , BookOutstore 
from .models import BookletOutstore

class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('stage', 'name', 'academic_year')
    list_filter = ('stage', 'academic_year')
    search_fields = ['name']



class ClassroomAdmin(admin.ModelAdmin):  
    list_display = ('name', 'stage' ,'class_levels')
    list_filter = ('name', 'class_levels')
    search_fields = ['name']

class StageAdmin(admin.ModelAdmin):
    list_display = ['stage']
    list_filter = ['stage']
    search_fields = ['stage']

######################################################################################################################3
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_id', 'stage', 'class_level', 'section', 'academic_year', 'phone_number')
    list_filter = ('stage', 'class_level', 'section')
    search_fields = ('name', 'national_id', 'stage__stage', 'class_level__name', 'section__name', 'phone_number')
    autocomplete_fields = ['stage', 'class_level', 'section']

    def save_model(self, request, obj, form, change):
        if not change:
            academic_year, created = AcademicYear.objects.get_or_create(year='2023')
            obj.academic_year = academic_year
        super().save_model(request, obj, form, change)

######################################################################################################################3

class SchoolBookletAdmin(admin.ModelAdmin):
    list_display = ('title', 'booklet_edition','description', 'source', 'supplier', 'stage', 'class_level', 'term', 'received_date', 'quantity', 'live_quantity')
    list_filter = ('source', 'stage', 'class_level', 'term', 'received_date')
    search_fields = ('title', 'source', 'supplier__name', 'stage__stage', 'class_level__name',  'term')

######################################################################################################################3
class SchoolSuppliesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'source', 'supplier',  'term', 'received_date', 'in_quantity', 'live_quantity')
    list_filter = ('source',  'term', 'received_date')
    search_fields = ('title', 'source', 'supplier__name',  'term')

######################################################################################################################3

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'supplier', 'stage', 'class_level', 'term', 'received_date', 'received_quantity', 'available_quantity')
    list_filter = ('source', 'stage', 'class_level', 'term', 'received_date')
    search_fields = ('title', 'source', 'supplier__name', 'stage__stage', 'class_level__name',  'term')

######################################################################################################################3
from django.contrib import admin
from .models import NotebookType, NotebookAssignment

class NotebookTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'source', 'supplier', 'in_quantity', 'live_quantity',  'received_date', 'size']
    list_filter = ['source',  'received_date']
    search_fields = ['name', 'description', 'size']

class NotebookAssignmentAdmin(admin.ModelAdmin):
    list_display = ['grade', 'notebook', 'quantity_assignment', 'term', 'year', 'assigned_date']
    list_filter = ['grade', 'year', 'assigned_date']
    search_fields = ['notebook__name']

admin.site.register(NotebookType, NotebookTypeAdmin)
admin.site.register(NotebookAssignment, NotebookAssignmentAdmin)

###########################################################################################################################################
from django.http import JsonResponse

class BookDistributionAdmin(admin.ModelAdmin):
    list_display = ('get_books_titles','get_notebooks_titles','get_booklets_titles', 'student', 'stage', 'class_level', 'section', 'receipt_number', 'recipient_name',  'delivery_date', 'distribution_status')
    #list_filter = ('student',  'stage', 'class_level', 'section', 'receipt_number')
    #search_fields = ('student__name',  'stage__stage', 'class_level__name', 'section__name', 'receipt_number')




admin.site.register(BookOutstore)

admin.site.register(NotebookDepreciation)


admin.site.register(BookletDepreciation)
admin.site.register(Stage, StageAdmin)

admin.site.register(ClassLevel, ClassLevelAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(AcademicYear)
admin.site.register(Student, StudentAdmin)
admin.site.register(Supplier)
admin.site.register(Book, BookAdmin)
admin.site.register(BookDistribution, BookDistributionAdmin)
admin.site.register(SchoolBooklet , SchoolBookletAdmin)
admin.site.register(SchoolSupplies , SchoolSuppliesAdmin)

admin.site.register(NotebookDelivery)
admin.site.register(BookDepreciation)


admin.site.register(BookletOutstore)