import os
import zipfile
from io import BytesIO
from django.http import HttpResponse, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from docx import Document
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import zipfile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from PIL import Image
from docx2pdf import convert
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PyPDF2 import PdfMerger  # For PDF merging
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings
import os
import zipfile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings
from docx2pdf import convert
from PIL import Image
from PyPDF2 import PdfMerger
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings
from moviepy.editor import VideoFileClip
from PIL import Image
from PyPDF2 import PdfMerger
from docx2pdf import convert
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image


def debug_templates(request):
    return HttpResponse(f"Template dirs: {settings.TEMPLATES[0]['DIRS']}")

def index_view(request):
    return render(request, 'converter/index.html')

def about_view(request):
    return render(request, 'converter/about.html')  

def service_view(request):
    return render(request, 'converter/service.html') 

def why_view(request):
    return render(request, 'converter/why.html')  

def team_view(request):
    return render(request, 'converter/team.html')

def inddex_view(request):
    return render(request, 'converter/index.html')

def convert_view(request):
    return render(request, 'convert.html')

def index_view(request):
    return render(request, 'convert.html')

def convert_view(request):
    return render(request, 'converter/convert.html')  

def index_view(request):
    return render(request, 'converter/index.html')

def about_view(request):
    return render(request, 'converter/about.html')  

def service_view(request):
    return render(request, 'converter/service.html') 

def why_view(request):
    return render(request, 'converter/why.html')  

def team_view(request):
    return render(request, 'converter/team.html') 



from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from django.conf import settings
from docx2pdf import convert
from PyPDF2 import PdfMerger
from PIL import Image
import zipfile
import os

def convert_view(request):
    result_url = None  
    error = None       
    fs = FileSystemStorage()  

    
    converted_files_dir = os.path.join(settings.MEDIA_ROOT, 'converted_files')
    os.makedirs(converted_files_dir, exist_ok=True)

    if request.method == 'POST':
        conversion_type = request.POST.get('conversion_type')

        try:
            
            if conversion_type == 'compress_document':
                files = request.FILES.getlist('files')
                compressed_file_name = 'compressed_files.zip'
                compressed_file_path = os.path.join(converted_files_dir, compressed_file_name)

                
                with zipfile.ZipFile(compressed_file_path, 'w') as zipf:
                    for file in files:
                        file_path = fs.save(file.name, file)  
                        zipf.write(fs.path(file_path), arcname=file.name)  

                
                result_url = fs.url(os.path.join('converted_files', compressed_file_name))

            # Handle Word to PDF conversion
            elif conversion_type == 'word_to_pdf':
                if 'file' not in request.FILES:
                    return HttpResponseBadRequest("No file uploaded")

                word_file = request.FILES['file']
                if not word_file.name.endswith('.docx'):
                    return HttpResponseBadRequest("Uploaded file is not a Word document")

                
                file_path = fs.save(word_file.name, word_file)
                temp_file_path = fs.path(file_path)

               
                pdf_name = word_file.name.replace('.docx', '.pdf')
                pdf_path = os.path.join(converted_files_dir, pdf_name)

                # Convert the Word document to PDF
                try:
                    convert(temp_file_path, pdf_path)
                except Exception as e:
                    return HttpResponseBadRequest(f"Error during conversion: {e}")

                
                os.remove(temp_file_path)

                
                result_url = fs.url(os.path.join('converted_files', pdf_name))

            # Handle JPEG to pdf conversion
            elif conversion_type == 'jpg_to_pdf':
                if 'files' not in request.FILES:
                    return HttpResponseBadRequest("No file uploaded for JPG to PDF conversion.")

                image_files = request.FILES.getlist('files')

                pdf_name = 'images.pdf'
                pdf_path = os.path.join(converted_files_dir, pdf_name)

   
                c = canvas.Canvas(pdf_path, pagesize=A4)

   
                for img_file in image_files:
                    img = Image.open(img_file)
                    img_width, img_height = img.size

       
                    aspect_ratio = img_width / img_height
                    a4_width, a4_height = A4

        
                    if aspect_ratio > 1:  
                        new_width = a4_width
                        new_height = new_width / aspect_ratio
                    else:  
                        new_height = a4_height
                        new_width = new_height * aspect_ratio

       
                    x_offset = (a4_width - new_width) / 2
                    y_offset = (a4_height - new_height) / 2

       
                    img_reader = ImageReader(img)

                    c.drawImage(img_reader, x_offset, y_offset, new_width, new_height)

                    c.showPage()


                c.save()

                result_url = fs.url(os.path.join('converted_files', pdf_name))

            # Handle JPG to PDF conversion
            elif conversion_type == 'jpg_to_png':
                 image_files = request.FILES.getlist('files')
                 images = []

                 for img_file in image_files:
                    img = Image.open(img_file)
                    img = img.convert('RGB')
                    images.append(img)

                 pdf_path = os.path.join(converted_files_dir, 'images.pdf')
                 images[0].save(pdf_path, save_all=True, append_images=images[1:])
                 result_url = fs.url(pdf_path)

                 result_url = fs.url(os.path.join('converted_files', pdf_name))


            # Handle PDF merging
            elif conversion_type == 'merge_pdfs':
                pdf_files = request.FILES.getlist('files')
                merger = PdfMerger()

                for pdf_file in pdf_files:
                    pdf_path = fs.save(pdf_file.name, pdf_file)
                    merger.append(fs.path(pdf_path))

                merged_pdf_name = 'merged.pdf'
                merged_pdf_path = os.path.join(converted_files_dir, merged_pdf_name)
                merger.write(merged_pdf_path)
                merger.close()

                result_url = fs.url(os.path.join('converted_files', merged_pdf_name))

            # Handle image resizing
            elif conversion_type == 'resize_image':
                if 'file' not in request.FILES:
                    return HttpResponseBadRequest("No file uploaded for image resizing.")

                image_file = request.FILES['file']
                width = int(request.POST.get('width', 100))
                height = int(request.POST.get('height', 100))
                img = Image.open(image_file)
                resized_image_name = 'resized_image.png'
                resized_image_path = os.path.join(converted_files_dir, resized_image_name)
                img = img.resize((width, height), Image.LANCZOS)
                img.save(resized_image_path)

                result_url = fs.url(os.path.join('converted_files', resized_image_name))

           
            elif conversion_type == 'video_to_audio':
                if 'file' not in request.FILES:
                    return HttpResponseBadRequest("No file uploaded for Video to Audio conversion.")

                video_file = request.FILES['file']
                if not video_file.name.endswith(('.mp4', '.avi', '.mov')):
                    return HttpResponseBadRequest("Uploaded file is not a valid video format.")

              
                file_path = fs.save(video_file.name, video_file)
                temp_file_path = fs.path(file_path)

               
                audio_name = video_file.name.rsplit('.', 1)[0] + '.mp3'  
                audio_path = os.path.join(converted_files_dir, audio_name)

                # Convert Video to Audio
                try:
                  
                    from moviepy.editor import VideoFileClip
                    with VideoFileClip(temp_file_path) as video:
                        audio = video.audio
                        audio.write_audiofile(audio_path)
                except Exception as e:
                    return HttpResponseBadRequest(f"Error during conversion: {e}")

            
                os.remove(temp_file_path)

               
                result_url = fs.url(os.path.join('converted_files', audio_name))

            else:
                error = "Invalid conversion type selected."

        except Exception as e:
            error = str(e)

    return render(request, 'converter/convert.html', {'result_url': result_url, 'error': error})


def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'converted', file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    else:
        return HttpResponseNotFound("File not found")


def convert_file(request):
    if request.method == "POST":
        conversion_type = request.POST.get('conversion_type')
        files = request.FILES.getlist('files') if 'files' in request.FILES else None
        result_url = None
        error = None

        try:
            if conversion_type == 'jpg_to_pdf':
                result_url = "path/to/converted/file.pdf"
            elif conversion_type == 'jpeg_to_png':
                result_url = "path/to/converted/file.png"
            elif conversion_type == 'merge_pdfs':
                
                result_url = "path/to/merged/file.pdf"
            elif conversion_type == 'resize_image':
                
                result_url = "path/to/resized/file.jpg"
            elif conversion_type == 'compress_document':
                
                result_url = "path/to/compressed/file.zip"
            elif conversion_type == 'word_to_pdf':
                
                result_url = "path/to/converted/file.pdf"
        except Exception as e:
            error = str(e)

        return render(request, 'convert.html', {'result_url': result_url, 'error': error})

    return render(request, 'convert.html')

