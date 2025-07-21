from django.contrib import admin
from .models import TrainingJob

@admin.register(TrainingJob)
class TrainingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'selected_model', 'status', 'created_at', 'epochs')
    list_filter = ('status', 'selected_model')
    readonly_fields = ('created_at', 'dataset_path', 'results_path')