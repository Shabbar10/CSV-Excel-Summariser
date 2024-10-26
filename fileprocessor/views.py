from time import sleep

from django.contrib import messages

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FileUploadForm
from .models import FileUpload
from .utils import process_file, send_summary_email


def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = FileUpload.objects.create(
                file=request.FILES["file"], name=form.cleaned_data["name"]
            )

            file_path = upload.file.path
            summary = process_file(file_path)
            upload.summary = summary
            upload.save()

            try:
                send_summary_email(summary, upload.name)
                messages.success(request, "File processed and sent successfully")
                print("File processed and sent successfully")
            except Exception as e:
                messages.warning(
                    request, f"File processed but email not sent - {str(e)}"
                )

            sleep(5)
            return redirect(reverse("fileprocessor:summary_view", args=[upload.pk]))
    else:
        form = FileUploadForm()

    return render(request, "fileprocessor/upload.html", {"form": form})


def summary_view(request, pk):
    upload = get_object_or_404(FileUpload, pk=pk)
    return render(request, "fileprocessor/summary.html", {"upload": upload})
