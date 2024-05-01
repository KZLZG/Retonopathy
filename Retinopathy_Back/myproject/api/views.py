from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from PIL import Image as PILImage, ImageDraw
import io
import onnxruntime as ort
import matplotlib.cm as cm  # for colormap


# Initialize ONNX runtime session
session = ort.InferenceSession('unet.onnx')
input_name = session.get_inputs()[0].name

def generate_color_map(n_colors):
    """
    Generate a list of distinct RGB colors.

    Args:
    n_colors (int): Number of distinct colors to generate.

    Returns:
    List of tuples: Each tuple contains three integers (R, G, B).
    """
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap('tab20')  # Using a matplotlib colormap that supports up to 20 unique colors
    colors = [cmap(i) for i in range(n_colors)]  # Generate colors
    # Convert colors from 0-1 range to 0-255 range and return as list of tuples
    return [(int(r*255), int(g*255), int(b*255)) for r, g, b, _ in colors]

def overlay_masks(image, masks, color=(255, 0, 0)):

    colors = generate_color_map(len(masks))
    output_image =  np.array(image.copy())
    image =  np.array(image)
    # Ensure color has three elements (R, G, B)
    if len(color) != 3:
        raise ValueError("Color must be a tuple of three integers (R, G, B).")
    
    # Loop through each mask
    for mask, color in zip(masks, colors):
        # Verify that the mask dimensions match the image dimensions
        if mask.shape != image.shape[:2]:
            raise ValueError("Mask shape does not match image dimensions.")

        # Apply the color to places where the mask is 1
        for i in range(3):  # Loop over color channels
            output_image[:, :, i] = np.where(mask>mask.max()/1.5, color[i], output_image[:, :, i])
    return PILImage.fromarray(output_image).convert('RGB')




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
