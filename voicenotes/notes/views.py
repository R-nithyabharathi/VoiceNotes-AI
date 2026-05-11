from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Note
import speech_recognition as sr
from moviepy import VideoFileClip
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'index.html', {"notes": notes})
@login_required
def save_note(request):
    if request.method == "POST":
        text = request.POST.get("text")
        Note.objects.create(content=text)
        return JsonResponse({"status":"saved"})
@login_required
def delete_note(request, id):
    Note.objects.get(id=id).delete()
    return redirect("/")

@login_required

def video_to_text(request):
    if request.method == "POST" and request.FILES.get("video"):
        video = request.FILES["video"]
        fs = FileSystemStorage(location="media")
        filename = fs.save(video.name, video)
        filepath = fs.path(filename)

        # Extract audio from video
        clip = VideoFileClip(filepath)
        audio_path = "media/audio.wav"
        clip.audio.write_audiofile(audio_path)

        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
        except:
            text = "Could not understand audio"

        Note.objects.create(content="VIDEO NOTE: " + text)
        return redirect("/")
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

from django.http import HttpResponse

def download_notes(request):
    notes = Note.objects.all().order_by('-created_at')

    content = ""
    for note in notes:
        content += f"{note.created_at} : {note.content}\n\n"

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=voice_notes.txt'
    return response