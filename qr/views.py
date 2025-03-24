from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Sum

import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from PIL import Image
from io import BytesIO
import base64
import json
import os
import tempfile
import svglib.svglib
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import datetime

from .models import QRCode, UserPreference

def index(request):
    context = {}
    qr_id = None
    
    if request.method == "POST":
        qr_text = request.POST.get("qr_text", "")
        
        # Get customization options
        foreground_color = request.POST.get("foreground_color", "#000000")
        background_color = request.POST.get("background_color", "#FFFFFF")
        box_size = int(request.POST.get("box_size", 10))
        border = int(request.POST.get("border", 4))
        
        # Create QR code with customization
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        
        # Create the QR code image
        qr_image = qr.make_image(fill_color=foreground_color, back_color=background_color)
        
        # Convert to base64 for display
        stream = BytesIO()
        qr_image.save(stream, format='PNG')
        qr_image_data = stream.getvalue()
        qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
        
        # Save QR code in database if user is authenticated and chose to save it
        if request.user.is_authenticated and request.POST.get("save_qr_code") == "on":
            qr_name = request.POST.get("qr_name", "")
            qr_code = QRCode.objects.create(
                user=request.user,
                content=qr_text,
                name=qr_name,
                foreground_color=foreground_color,
                background_color=background_color,
                box_size=box_size,
                border=border
            )
            qr_id = qr_code.id
            messages.success(request, _("QR code saved successfully!"))
        
        # Prepare the context with the generated QR code
        context = {
            'qr_image_base64': qr_image_base64,
            'variable': qr_text,
            'qr_text': qr_text,
            'foreground_color': foreground_color,
            'background_color': background_color,
            'box_size': box_size,
            'border': border,
            'qr_id': qr_id
        }
    
    return render(request, 'index.html', context=context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default preferences
            UserPreference.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, _("Account created successfully!"))
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_qr_codes = QRCode.objects.filter(user=request.user).order_by('-created_at')
    total_downloads = user_qr_codes.aggregate(Sum('download_count'))['download_count__sum'] or 0
    total_shares = user_qr_codes.aggregate(Sum('share_count'))['share_count__sum'] or 0
    
    context = {
        'user': request.user,
        'user_qr_codes': user_qr_codes,
        'total_downloads': total_downloads,
        'total_shares': total_shares,
    }
    return render(request, 'profile.html', context)

@login_required
def qr_history(request):
    user_qr_codes = QRCode.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'qr_history.html', {'qr_codes': user_qr_codes})

@login_required
def qr_detail(request, qr_id):
    qr_code = get_object_or_404(QRCode, id=qr_id, user=request.user)
    
    # Increment view count
    qr_code.increment_view_count()
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_code.box_size,
        border=qr_code.border,
    )
    qr.add_data(qr_code.content)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=qr_code.foreground_color, back_color=qr_code.background_color)
    
    # Convert to base64 for display
    stream = BytesIO()
    qr_image.save(stream, format='PNG')
    qr_image_data = stream.getvalue()
    qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
    
    context = {
        'qr_code': qr_code,
        'qr_image_base64': qr_image_base64,
    }
    
    return render(request, 'qr_detail.html', context)

@login_required
def user_preferences(request):
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preferences.language = request.POST.get('language', 'en')
        preferences.default_qr_foreground = request.POST.get('default_qr_foreground', '#000000')
        preferences.default_qr_background = request.POST.get('default_qr_background', '#FFFFFF')
        preferences.save()
        
        messages.success(request, _("Preferences updated successfully!"))
        return redirect('user_preferences')
    
    context = {
        'preferences': preferences,
    }
    return render(request, 'user_preferences.html', context)

def download_qr(request):
    qr_id = request.GET.get('id')
    format = request.GET.get('format', 'png')
    
    # If qr_id is provided, get from database
    if qr_id and request.user.is_authenticated:
        qr_code = get_object_or_404(QRCode, id=qr_id, user=request.user)
        qr_content = qr_code.content
        foreground_color = qr_code.foreground_color
        background_color = qr_code.background_color
        box_size = qr_code.box_size
        border = qr_code.border
        
        # Increment download count
        qr_code.increment_download_count()
    else:
        # Use session data for anonymous users
        qr_content = request.session.get('qr_content', 'QR Code')
        foreground_color = request.session.get('foreground_color', '#000000')
        background_color = request.session.get('background_color', '#FFFFFF')
        box_size = request.session.get('box_size', 10)
        border = request.session.get('border', 4)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    # Create response based on requested format
    if format == 'svg':
        # SVG format
        factory = qrcode.image.svg.SvgImage
        img = qr.make_image(image_factory=factory, fill_color=foreground_color, back_color=background_color)
        stream = BytesIO()
        img.save(stream)
        response = HttpResponse(stream.getvalue(), content_type='image/svg+xml')
        response['Content-Disposition'] = 'attachment; filename="qr_code.svg"'
    elif format == 'pdf':
        # PDF format
        img = qr.make_image(fill_color=foreground_color, back_color=background_color)
        stream = BytesIO()
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img.save(tmp_file, format='PNG')
            tmp_filename = tmp_file.name
        
        # Create PDF with the image
        c = canvas.Canvas(stream)
        c.drawImage(tmp_filename, 100, 100)
        c.save()
        
        # Clean up the temporary file
        os.unlink(tmp_filename)
        
        response = HttpResponse(stream.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="qr_code.pdf"'
    else:
        # Default PNG format
        img = qr.make_image(fill_color=foreground_color, back_color=background_color)
        stream = BytesIO()
        img.save(stream, format="PNG")
        response = HttpResponse(stream.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
    
    return response

@login_required
@require_POST
def track_download(request):
    data = json.loads(request.body)
    qr_id = data.get('qr_id')
    
    if qr_id:
        qr_code = get_object_or_404(QRCode, id=qr_id, user=request.user)
        qr_code.increment_download_count()
    
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def track_share(request):
    data = json.loads(request.body)
    qr_id = data.get('qr_id')
    
    if qr_id:
        qr_code = get_object_or_404(QRCode, id=qr_id, user=request.user)
        qr_code.increment_share_count()
    
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def delete_qr(request, qr_id):
    qr_code = get_object_or_404(QRCode, id=qr_id, user=request.user)
    qr_code.delete()
    messages.success(request, _("QR code deleted successfully!"))
    return redirect('qr_history')

# API views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import QRCodeSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_qr_api(request):
    serializer = QRCodeSerializer(data=request.data)
    if serializer.is_valid():
        # Set the user before saving
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_qr_api(request):
    qr_codes = QRCode.objects.filter(user=request.user)
    serializer = QRCodeSerializer(qr_codes, many=True)
    return Response(serializer.data)

def api_docs(request):
    return render(request, 'api_docs.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')
