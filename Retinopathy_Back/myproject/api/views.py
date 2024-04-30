from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image as PILImage
import io

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        file = request.FILES['image']
        # Open the image file with Pillow, without saving it
        img = PILImage.open(file)

        # Save the image to a bytes buffer instead of disk, keeping it in RGB
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Return the image directly in the response
        return HttpResponse(img_byte_arr, content_type='image/png')
    return HttpResponse('Only POST method is accepted.', status=400)
