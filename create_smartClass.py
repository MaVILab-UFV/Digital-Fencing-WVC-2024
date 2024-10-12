import os
import shutil

# Defining the classes for each dataset
datasets = {
    "apt36k": {"cat", "dog", "horse", "sheep", "cow", "elephant", "zebra", "giraffe"},
    "cows2021": {"cow"},
    "coco": {"person", "cat", "dog", "horse", "sheep", "cow", "elephant", "zebra", "giraffe"},
    "nrec": {"person"}
}

# A dictionary to store intersections and their corresponding datasets
intersection_results = {}

# Creating intersections and assigning SmartClass names
smart_class_count = 1
for dataset_name, dataset_classes in datasets.items():
    for other_dataset_name, other_dataset_classes in datasets.items():
        if dataset_name != other_dataset_name:
            # Intersection between the two datasets
            intersection = dataset_classes.intersection(other_dataset_classes)
            if intersection:
                # Sort to ensure the same set is always identified in the same way
                intersection_tuple = tuple(sorted(intersection))
                # If the intersection has not been recorded yet
                if intersection_tuple not in intersection_results:
                    intersection_results[intersection_tuple] = {dataset_name, other_dataset_name}  # Using set to avoid duplicates
                else:
                    intersection_results[intersection_tuple].update([other_dataset_name])

# Printing the results as SmartClass_1, SmartClass_2, ...
smart_classes = {}
for classes, datasets_involved in intersection_results.items():
    smart_class_name = f"SmartClass_{smart_class_count}"
    smart_classes[smart_class_name] = set(classes)
    print(f"{smart_class_name}: {', '.join(classes)} = {', '.join(sorted(datasets_involved))}")
    smart_class_count += 1

# Define the source and destination directories
image_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/images/all"
label_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/labels/all"
output_base_dir = "/homeLocal/julianaquin/datasets/digital-fence-dataset/"

# Mapping dictionary of IDs to class names
class_mapping = {
    0: "person",
    1: "cat",
    2: "dog",
    3: "horse",
    4: "sheep",
    5: "cow",
    6: "elephant",
    7: "zebra",
    8: "giraffe"
}

# Function to create the .txt file with SmartClass information, including class mapping
def create_smartclass_info_file(smart_class_name, class_mapping_new, datasets_involved):
    output_dir = os.path.join(output_base_dir, smart_class_name)
    info_file_path = os.path.join(output_dir, f"{smart_class_name}_info.txt")
    with open(info_file_path, 'w') as info_file:
        class_mapping_str = ", ".join([f"{orig_class} -> {new_class}" for orig_class, new_class in class_mapping_new.items()])
        info_file.write(f"{smart_class_name}: {class_mapping_str} = {', '.join(sorted(datasets_involved))}\n")
    print(f"Info file created for {smart_class_name} at {info_file_path}")

# Function to check if an annotation contains only the allowed classes for the SmartClass
def filter_annotation_by_class(annotation_path, allowed_classes, class_mapping_new):
    new_lines = []
    with open(annotation_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            class_id = int(line.split()[0])  # Assuming the first number in the line is the class ID
            class_name = class_mapping[class_id]  # Mapping the ID to the class name
            if class_name in allowed_classes:
                # Map the original class ID to the new SmartClass ID
                new_class_id = list(allowed_classes).index(class_name)
                new_line = line.replace(str(class_id), str(new_class_id), 1)
                new_lines.append(new_line)
    return new_lines if new_lines else None  # Return modified lines if valid, else None

# Main function to process each SmartClass
def process_smart_classes():
    for smart_class_name, allowed_classes in smart_classes.items():
        print(f"Processing {smart_class_name} for classes: {allowed_classes}")

        # Output directories
        output_image_dir = os.path.join(output_base_dir, smart_class_name, "images")
        output_label_dir = os.path.join(output_base_dir, smart_class_name, "labels")
        os.makedirs(output_image_dir, exist_ok=True)
        os.makedirs(output_label_dir, exist_ok=True)

        # Create a new class mapping for this SmartClass
        class_mapping_new = {class_name: idx for idx, class_name in enumerate(allowed_classes)}

        # Create the SmartClass info file
        datasets_involved = intersection_results[tuple(sorted(allowed_classes))]
        create_smartclass_info_file(smart_class_name, class_mapping_new, datasets_involved)

        # Process each annotation file
        for label_file in os.listdir(label_dir):
            if label_file.endswith('.txt'):
                label_path = os.path.join(label_dir, label_file)

                # Filter the annotation by allowed classes
                new_annotation = filter_annotation_by_class(label_path, allowed_classes, class_mapping_new)
                if new_annotation:
                    # Copy the annotation and corresponding image to the SmartClass folder
                    image_file = label_file.replace(".txt", ".png")  # Assuming the image extension is .png
                    image_path = os.path.join(image_dir, image_file)

                    # Check if the image exists and adjust if necessary
                    if not os.path.exists(image_path):
                        # Try with other extensions
                        for ext in ['.jpg', '.jpeg', '.bmp']:  # Add other extensions as needed
                            image_file = label_file.replace(".txt", ext)
                            image_path = os.path.join(image_dir, image_file)
                            if os.path.exists(image_path):
                                break

                    if os.path.exists(image_path):
                        # Write the new annotation with updated class IDs
                        with open(os.path.join(output_label_dir, label_file), 'w') as out_label_file:
                            out_label_file.writelines(new_annotation)
                        
                        # Copy the corresponding image
                        shutil.copy(image_path, os.path.join(output_image_dir, image_file))
                        print(f"Copied {label_file} and {image_file} for {smart_class_name}")
                    else:
                        print(f"Image {image_file} not found for {label_file}")

process_smart_classes()

