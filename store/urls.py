from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views    


app_name = 'store'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('home/', views.home, name='home'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('allstudent/', views.allstudent, name='allstudent'),
    path('add/', add_student, name='add_student'),
    path('import/', import_students, name='import_students'),
    path('export/', export_students, name='export_students'),
    path('students/', studentListView.as_view(), name='student_list'),
    path('export_Student_excel/', export_Student_excel, name='export_Student_excel'),
    ##################################################################
    path('bookstore/', views.bookstore, name='bookstore'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('booktypes/add_delivery/', add_BookDelivery, name='add_book_delivery'),
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('books/export_excel/', export_book_excel, name='export_book_excel'),
    path('add_notebook_type/', add_notebook_type, name='add_notebook_type'),
    ##################################################################
    path('note/', views.note, name='note'),
    path('notebooktypes/', NotebookTypeListView.as_view(), name='notebooktype_list'),
    path('notebooktypes/add_delivery/', add_notebook_delivery, name='add_notebook_delivery'),
    path('edit_notebook_type/<int:pk>/', edit_notebook_type, name='edit_notebook_type'),
    path('notebooktypes/export_excel/', export_notebooktype_excel, name='export_notebooktype_excel'),
    path('add_notebook_assignment/', add_notebook_assignment, name='add_notebook_assignment'),
    path('notebook-assignments/', NotebookAssignmentListView.as_view(), name='notebook_assignment_list'),
    path('edit_notebook_assignment/<int:pk>/', edit_notebook_assignment, name='edit_notebook_assignment'),
    ##################################################################
    path('booklet/', views.booklet, name='booklet'),
    path('add_school_booklet/', views.add_school_booklet, name='add_school_booklet'),
    path('add_booklet_delivery/', add_BookletDelivery, name='add_booklet_delivery'),
    path('edit_school_booklet/<int:pk>/', edit_school_booklet, name='edit_school_booklet'),
    path('school_booklets/', SchoolBookletListView.as_view(), name='school_booklet_list'),
    path('school_booklets/export_excel/', export_school_booklet_excel, name='export_school_booklet_excel'),
    
    path('get_class_levels/', views.get_class_levels, name='get_class_levels'),
    path('get_class_student/', views.get_class_student, name='get_class_student'),
    path('add_school_supplies/', views.add_school_supplies, name='add_school_supplies'),
    ################################################################################
    path('book_distribution/', BookDistributionCreateView.as_view(), name='book_distribution'),
    path('search_student/', views.search_student, name='search_student'),
    path('get_selected_student/', views.get_selected_student, name='get_selected_student'),  # الإضافة الجديدة
    path('get_student_info/', views.get_student_info, name='get_student_info'),
    path('get_available_books/', views.get_available_books, name='get_available_books'),
    path('get_available_notebooks/', views.get_available_notebooks, name='get_available_notebooks'),
    path('get_available_booklets/', views.get_available_booklets, name='get_available_booklets'),
    path('book-distribution/', BookDistributionListView.as_view(), name='book_distribution_list'),
    
    path('book-distribution/<int:pk>/update/', BookDistributionUpdateView.as_view(), name='book_distribution_update'),
    path('book-distribution/<int:pk>/delete/', BookDistributionDeleteView.as_view(), name='book_distribution_delete'),
    path('export_to_excel/', export_to_excel, name='export_to_excel'),
   
    path('search_students/', views.student_distribution_search, name='search_students'),
    path('export_students/', export_students_to_excel, name='export_students_to_excel'),

############################################################################################
    path('create_supplier/', create_supplier, name='create_supplier'),
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('export_supplier_excel/', export_supplier_excel, name='export_supplier_excel'),
    path('suppliers/edit/<int:pk>/', edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:pk>/', delete_supplier, name='delete_supplier'),
    


    path('migrate-students/', migrate_students_view, name='migrate_students'),
                            ####الاهلاكات #######

                            

    path('depreciations/', views.depreciations, name='depreciations'),
    path('depreciation/create/', BookDepreciationCreateView.as_view(), name='depreciation-create'),
    path('depreciation/', BookDepreciationListView.as_view(), name='depreciation-list'),
    
    path('depreciationbooklet/', BookletDepreciationCreateView.as_view(), name='depreciationbooklet'),
    path('depreciationbooklit-list/', BookletDepreciationListView.as_view(), name='depreciationbooklit-list'),



    path('depreciationnotebook/', NotebooDepreciationCreateView.as_view(), name='depreciationnotebook'),
    path('depreciationnotebook-list/', NotebooDepreciationListView.as_view(), name='depreciationnotebook-list'),

     #####صرق خارج الطلبة######
    path('outlet/', views.outlet, name='outlet'),
    
    

   path('bookoutlet/', BookOutstoreCreateView.as_view(), name='bookoutlet'),
   path('bookoutlet_list/', BookOutstoreListView.as_view(), name='bookoutlet_list'),
   
   path('bookletoutlet/', BookletOutstoreCreateView.as_view(), name='bookletoutlet'),
   path('bookletoutlet_list/', BookletOutstoreListView.as_view(), name='bookletoutlet_list'),

   path('get_books/', get_books, name='get_books'),
   path('get_booklets/', views.get_booklets, name='get_booklets'),

    #path('stock-report/', views.stock_report_view, name='stock_report'),
    #path('load-class-levels/', views.load_class_levels, name='load_class_levels'),
    #path('generate-report/', views.generate_report, name='generate_report'),   
  
   path('required_resources/', required_resources_view, name='required_resources'),
   path('notebook_request/', views.notebook_request_view, name='notebook_request'),
   path('ajax/load_class_levels/', views.load_class_levels, name='load_class_levels'),



   

]




