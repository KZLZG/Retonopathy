from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from PIL import Image as PILImage, ImageDraw
import io
import onnxruntime as ort
from PIL import ImageChops, Image
import matplotlib.pyplot as plt


# Initialize ONNX runtime session
session = ort.InferenceSession('unet.onnx')
input_name = session.get_inputs()[0].name


def overlay_masks(image, masks, threshold=160):

    mask_normalized = (masks - masks.min()) / (masks.max() - masks.min())
    color_mask = plt.get_cmap('jet')(mask_normalized) 
    color_mask = (color_mask * 255).astype(np.uint8)

    composite_mask = np.copy(np.array(image))
    for i in range(14):
    # Создание маски, где предсказания превышают порог
        mask_above_threshold = color_mask[i] > threshold
    
    # Применение маски: выбор новых значений там, где маска выше порога
        for j in range(3):  # для каждого из каналов RGB
            channel = composite_mask[:, :, j]
            new_values = np.maximum(channel, color_mask[i][:, :, j])
            channel[mask_above_threshold[:, :, j]] = new_values[mask_above_threshold[:, :, j]]
            composite_mask[:, :, j] = channel
    composite_image = Image.fromarray(composite_mask, 'RGB')
    combined = ImageChops.multiply(image, composite_image)
    return combined


@csrf_exempt
def model_inference(request):
    if request.method == 'POST':
        try:
            file = request.FILES['image']
            img = PILImage.open(file).convert('RGB')

            # Resize image and prepare for model input
            img = img.resize((512, 512))
            img_array = np.array(img).astype('float32')
            img_array = np.transpose(img_array, [2, 0, 1])
            img_array = np.expand_dims(img_array, axis=0)

            # Run model inference
            result = session.run(None, {input_name: img_array})
            img = overlay_masks(img, result[0][0])

            # Convert image back to byte array and return as response
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return HttpResponse(img_byte_arr, content_type='image/png')
        except Exception as e:
            print("Error processing the image:", str(e))
            return HttpResponse('Error processing image', status=500)

    return HttpResponse('Only POST method is accepted', status=400)
