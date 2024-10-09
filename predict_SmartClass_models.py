import os
from ultralytics import YOLO

model_folder = 'C:\\path\\to\\models_folder'  
image_folder = 'C:\\path\\to\\images_folder'  
output_base_folder = 'C:\\path\\to\\output_folder'  

os.makedirs(output_base_folder, exist_ok=True)
model_paths = [os.path.join(model_folder, model_name) for model_name in os.listdir(model_folder) if model_name.endswith('.pt')]
input_folder = image_folder 

for model_index, model_path in enumerate(model_paths):
    model_name = os.path.basename(model_path)
    print(f'Loading model: {model_path}')
    
    model = YOLO(model_path)
    model_output_folder = os.path.join(output_base_folder, model_name.replace('.pt', ''))
    os.makedirs(model_output_folder, exist_ok=True)

    # Perform inference on each image in the input folder
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)
        print(f'Processing image: {image_path} with model {model_name}')
        
        results = model(image_path, show=False)  
        
        if results:
            first_result = results[0]  
            
            if first_result.boxes and len(first_result.boxes) > 0: 
                print(f'Predictions for {image_name}: {first_result.boxes}') 
                
                # Save images with predictions
                output_image_path = os.path.join(model_output_folder, image_name)  
                first_result.plot(save=True, filename=output_image_path)  
            else:
                print(f'No detections for image: {image_name}')
        else:
            print(f'No results for image: {image_name}')
    
    input_folder = model_output_folder 

print("Inference completed for all images and SmartClass models.")
