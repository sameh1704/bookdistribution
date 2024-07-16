from .models import Student, Book, NotebookType, SchoolBooklet, ClassLevel

def calculate_required_resources():
    resources = {
        'books': [],
        'notebooks': [],
        'booklets': [],
    }

    class_levels = ClassLevel.objects.all()

    for class_level in class_levels:
        stage = class_level.stage

        # حساب عدد الطلاب في الصف الدراسي المحدد
        student_count = Student.objects.filter(stage=stage, class_level=class_level).count()

        # حساب الكميات المطلوبة من الكتب
        for book in Book.objects.filter(stage=stage, class_level=class_level):
            required_quantity = student_count - book.available_quantity
            resources['books'].append({
                'stage': stage.stage,
                'class_level': class_level.name,
                'title': book.title,
                'required_quantity': max(0, required_quantity)  # تأكد من أن الكمية المطلوبة غير سالبة
            })

        # حساب الكميات المطلوبة من البوكليتات
        for booklet in SchoolBooklet.objects.filter(stage=stage, class_level=class_level):
            required_quantity = student_count - booklet.live_quantity
            resources['booklets'].append({
                'stage': stage.stage,
                'class_level': class_level.name,
                'title': booklet.title,
                'required_quantity': max(0, required_quantity)  # تأكد من أن الكمية المطلوبة غير سالبة
            })

        # حساب الكميات المطلوبة من الكراسات
        for notebook in NotebookType.objects.all():
            quantity_per_student = 2  # هنا يمكنك تحديد الكمية لكل طالب حسب الحاجة
            required_quantity = (quantity_per_student * student_count) - notebook.live_quantity
            resources['notebooks'].append({
                'stage': stage.stage,
                'class_level': class_level.name,
                'title': notebook.name,
                'required_quantity': max(0, required_quantity)  # تأكد من أن الكمية المطلوبة غير سالبة
            })

    return resources
