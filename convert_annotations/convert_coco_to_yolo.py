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
        
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        width = bbox[2] / img_width
        height = bbox[3] / img_height
        
        yolo_annotation = f"{new_class_id} {x_center} {y_center} {width} {height}\n"
        
        # Generate the new file name with coco_train or coco_val prefix
        image_filename = os.path.splitext(image_info['file_name'])[0]
        new_filename = f"coco_{dataset_type}_{image_filename}"

        # Path to save the YOLO annotation
        output_file = os.path.join(output_label_dir, f"{new_filename}.txt")
        with open(output_file, 'a') as f_out:
            f_out.write(yolo_annotation)

        # Copy the corresponding image and rename it
        original_image_path = os.path.join(image_dir, image_info['file_name'])
        if os.path.exists(original_image_path):
            new_image_path = os.path.join(output_image_dir, f"{new_filename}.jpg")
            shutil.copy(original_image_path, new_image_path)
            print(f"Copied image {original_image_path} to {new_image_path}")
        else:
            print(f"Image not found for: {image_filename}")

# Class mapping
class_mapping = {
    1: 0, 
    16: 1,
    17: 2,
    18: 3,
    19: 4,
    20: 5,
    21: 6,
    23: 7,
    24: 8
}

# Output directories
output_image_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all"
output_label_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all"

# Convert training annotations
convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/coco2017/annotations/instances_train2017.json',  # Path to the COCO annotations file
    '/homeLocal/julianaquin/datasets/coco2017/train2017',                 # Directory where the images are located
    output_image_dir,                                                     # Output directory to save images
    output_label_dir,                                                     # Output directory to save annotations
    class_mapping,                                                        # Class mapping
    "train"                                                               # Dataset type (train)
)

# Convert validation annotations
convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/coco2017/annotations/instances_val2017.json',  # Path to the COCO annotations file
    '/homeLocal/julianaquin/datasets/coco2017/val2017',                 # Directory where the images are located
    output_image_dir,                                                   # Output directory to save images
    output_label_dir,                                                   # Output directory to save annotations
    class_mapping,                                                      # Class mapping
    "val"                                                               # Dataset type (val)
)
