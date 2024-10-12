import os
import shutil
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(voc_dir, output_image_dir, output_label_dir, dataset_type):
    class_mapping = {
        "person-part": 0,
        "person": 0
    }

    def process_directory(directory):
        print(f"Processing directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            print(f"Walking into directory: {root}")
            if not any(os.path.isdir(os.path.join(root, d)) for d in dirs):
                print(f"No subdirectories in {root}. Processing files...")
                for file in files:
                    if file.endswith('.xml'):
                        xml_file = os.path.join(root, file)
                        print(f"Processing file: {xml_file}")
                        tree = ET.parse(xml_file)
                        root_elem = tree.getroot()

                        image_width = int(root_elem.find("size/width").text)
                        image_height = int(root_elem.find("size/height").text)

                        annotations_for_txt = []
                        for obj in root_elem.iter('object'):
                            category = obj.find('name').text
                            if category not in class_mapping:
                                continue

                            category_id = class_mapping[category]

                            bbox = obj.find('bndbox')
                            xmin = float(bbox.find('xmin').text)
                            ymin = float(bbox.find('ymin').text)
                            xmax = float(bbox.find('xmax').text)
                            ymax = float(bbox.find('ymax').text)
                            x_center = (xmin + xmax) / 2.0 / image_width
                            y_center = (ymin + ymax) / 2.0 / image_height
                            w = (xmax - xmin) / image_width
                            h = (ymax - ymin) / image_height

                            bbox_info = f"{category_id} {x_center} {y_center} {w} {h}"
                            annotations_for_txt.append(bbox_info)

                        # Generate file names with the "nrec" prefix and "train" or "val"
                        original_filename = root_elem.find("filename").text
                        base_filename = os.path.splitext(original_filename)[0]
                        new_filename = f"nrec_{dataset_type}_{base_filename}"

                        # Path for the annotation file (YOLO format)
                        txt_path = os.path.join(output_label_dir, f"{new_filename}.txt")
                        with open(txt_path, 'w') as txt_file:
                            txt_file.write("\n".join(annotations_for_txt))

                        # Now look for the corresponding image in the "Images" subfolder
                        image_dir = os.path.join(os.path.dirname(xml_file), "../Images")
                        image_file = os.path.join(image_dir, base_filename + ".png")

                        if os.path.exists(image_file):
                            # Copy the corresponding PNG image to the destination directory and rename it
                            new_image_path = os.path.join(output_image_dir, f"{new_filename}.png")
                            shutil.copy(image_file, new_image_path)
                            print(f"Copied image {image_file} to {new_image_path}")
                        else:
                            print(f"Image not found for: {base_filename} in {image_dir}")

            for sub_dir in dirs:
                process_directory(os.path.join(root, sub_dir))

    process_directory(voc_dir)

# Define output directories
output_image_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all"
output_label_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all"

# Usage
convert_voc_to_yolo(
    "/homeLocal/julianaquin/datasets/NREC/val/positive", 
    output_image_dir, 
    output_label_dir, 
    "val"
)
convert_voc_to_yolo(
    "/homeLocal/julianaquin/datasets/NREC/train/positive", 
    output_image_dir, 
    output_label_dir, 
    "train"
)
convert_voc_to_yolo(
    "/homeLocal/julianaquin/datasets/NREC/test/positive", 
    output_image_dir, 
    output_label_dir, 
    "train"
)
