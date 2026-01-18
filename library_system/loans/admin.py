from django.contrib import admin
from .models import Student, Loan

admin.site.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id')

admin.site.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    # This makes the columns visible in the list view
    list_display = ('student', 'amount', 'status', 'created_at')
    # This adds a filter sidebar
    list_filter = ('status',)
