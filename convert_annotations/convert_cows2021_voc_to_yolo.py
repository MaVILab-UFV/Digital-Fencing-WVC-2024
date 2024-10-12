import json
import os
import shutil

def convert_coco_to_yolo(coco_json_path, image_dir, output_image_dir, output_label_dir, class_mapping, dataset_type):
    with open(coco_json_path) as f:
        data = json.load(f)
    
    images = {image['id']: image for image in data['images']}
    annotations = data['annotations']

    for ann in annotations:
        category_id = ann['category_id']
        
        # Check if the category is in the desired class mapping
        if category_id not in class_mapping:
            continue
        
        new_class_id = class_mapping[category_id]
        
        image_id = ann['image_id']
        bbox = ann['bbox']
        
        image_info = images[image_id]
        img_width = image_info['width']
        img_height = image_info['height']
        
        # YOLO calculation (x_center, y_center, width, height)
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        width = bbox[2] / img_width
        height = bbox[3] / img_height
        
        yolo_annotation = f"{new_class_id} {x_center} {y_center} {width} {height}\n"
        
        # Original image name without extension
        image_filename = os.path.splitext(image_info['file_name'])[0]
        
        # Add the prefix cows2021 and specify if it's train or val (for test)
        final_image_name = f"cows2021_{dataset_type}_{image_filename}"
        
        # Output path for the annotations
        os.makedirs(output_label_dir, exist_ok=True)
        output_file = os.path.join(output_label_dir, f"{final_image_name}.txt")
        
        # Save the converted annotation
        with open(output_file, 'a') as f_out:
            f_out.write(yolo_annotation)
        
        # Copy the corresponding image to the new directory with the cows2021_ prefix and adjusted name
        src_image_path = os.path.join(image_dir, image_info['file_name'])
        new_image_name = f"{final_image_name}.jpg"
        dest_image_path = os.path.join(output_image_dir, new_image_name)
        
        os.makedirs(output_image_dir, exist_ok=True)
        shutil.copy2(src_image_path, dest_image_path)
        print(f"Processed: {new_image_name}")

# Class mapping as per the table provided for WVC2024.yaml 
class_mapping = {
    1: 5
}

# Converting to the validation dataset (Test -> val)
convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Test/annotations/instances_val.json',  # Path to the COCO annotation file
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Test/images/val',                     # Directory where the images are located
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all',                                                     # Directory to save the copied images
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all',                                                     # Directory to save the converted annotations
    class_mapping,                                                                                                          # Class mapping
    dataset_type='val'                                                                                                      # Dataset identifier (val for test)
)

# Converting to the training dataset (Train -> val)
convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Train/annotations/instances_val.json',  # Path to the COCO annotation file
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Train/images/val',                      # Directory where the images are located
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all',                                                       # Directory to save the copied images
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all',                                                       # Directory to save the converted annotations
    class_mapping,                                                                                                            # Class mapping
    dataset_type='train'                                                                                                      # Dataset identifier (train)
)

# Converting to the training dataset (Train -> train)
convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Train/annotations/instances_train.json',  # Path to the COCO annotation file
    '/homeLocal/julianaquin/datasets/bd_cows2021/Sub-levels/Detection_and_localisation/Train/images/train',                      # Directory where the images are located
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all',                                                         # Directory to save the copied images
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all',                                                         # Directory to save the converted annotations
    class_mapping,                                                                                                              # Class mapping
    dataset_type='train'                                                                                                        # Dataset identifier (train)
)
