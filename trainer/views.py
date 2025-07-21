from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingJob
from .tasks import process_training_job

def training_view(request):
    if request.method == 'POST':

        dataset_zip = request.FILES.get('dataset_zip')
        selected_model = request.POST.get('selected_model')
        epochs = int(request.POST.get('epochs', 10))

        if not dataset_zip:
            # Hata yönetimi
            return render(request, 'trainer/training_form.html', {'error': 'Lütfen bir veri seti dosyası yükleyin.'})

 
        job = TrainingJob.objects.create(
            dataset_zip=dataset_zip,
            selected_model=selected_model,
            epochs=epochs,
        )
        

        process_training_job.delay(job.id)
        
  
        return redirect('trainer:job_status', job_id=job.id)

    model_choices = TrainingJob.MODEL_CHOICES
    return render(request, 'trainer/training_form.html', {'model_choices': model_choices})


def job_status_view(request, job_id):
    job = get_object_or_404(TrainingJob, id=job_id)
    results_summary = job.get_results_summary() if job.status == 'COMPLETED' else None
    
    refresh_header = "30" if job.status in ['PENDING', 'RUNNING'] else None

    context = {
        'job': job,
        'results': results_summary,
        'refresh_header': refresh_header
    }
    return render(request, 'trainer/job_status.html', context)

def list_jobs_view(request):
    jobs = TrainingJob.objects.all().order_by('-created_at')
    return render(request, 'trainer/job_list.html', {'jobs': jobs})