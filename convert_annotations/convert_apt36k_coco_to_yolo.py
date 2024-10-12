import json
import os
import shutil

def convert_coco_to_yolo(coco_json_path, image_dir, output_image_dir, output_label_dir, class_mapping):
    with open(coco_json_path) as f:
        data = json.load(f)
    
    images = {image['id']: image for image in data['images']}
    annotations = data['annotations']
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    
    for ann in annotations:
        category_id = ann['category_id']
        
        if category_id not in class_mapping:
            continue
        
        new_class_id = class_mapping[category_id]
        
        image_id = ann['image_id']
        bbox = ann['bbox']
        
        image_info = images[image_id]
        img_width = image_info['width']
        img_height = image_info['height']
        
        # YOLO format calculation (x_center, y_center, width, height)
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        width = bbox[2] / img_width
        height = bbox[3] / img_height
        
        yolo_annotation = f"{new_class_id} {x_center} {y_center} {width} {height}\n"
        
        original_file_path = image_info['file_name']
        relative_file_path = original_file_path.split('AP-36k-patr1\\')[1]
        linux_relative_file_path = relative_file_path.replace('\\', '/')
        
        # Extracting the folder name and image name to include in the final name
        image_folder = os.path.dirname(linux_relative_file_path)
        image_filename = os.path.splitext(os.path.basename(linux_relative_file_path))[0]
        final_image_name = f"apt36k_{image_folder.replace('/', '_')}_{image_filename}"
        
        # Output path for annotations
        os.makedirs(output_label_dir, exist_ok=True)
        output_file = os.path.join(output_label_dir, f"{final_image_name}.txt")
        
        # Saving the converted annotation
        with open(output_file, 'a') as f_out:
            f_out.write(yolo_annotation)
        
        # Copying the corresponding image to the new directory with the 'apt36k_' prefix and the adjusted name
        src_image_path = os.path.join(image_dir, linux_relative_file_path)
        new_image_name = f"{final_image_name}.jpg"
        dest_image_path = os.path.join(output_image_dir, new_image_name)
        
        os.makedirs(output_image_dir, exist_ok=True)
        shutil.copy2(src_image_path, dest_image_path)
        print(f"Processed: {new_image_name}")

# Updated class mapping
class_mapping = {
    3: 1,
    2: 2,
    4: 3,
    30: 4,
    28: 5,
    14: 6,
    13: 7,
    18: 8
}

convert_coco_to_yolo(
    '/homeLocal/julianaquin/datasets/ap36k/apt36k_annotations.json',  # Path to the COCO annotations file
    '/homeLocal/julianaquin/datasets/ap36k/AP-36k-patr1',            # Directory where the images are stored
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all',  # Directory to save the copied images
    '/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all',  # Directory to save the converted annotations
    class_mapping                                                    # Updated class mapping
)
