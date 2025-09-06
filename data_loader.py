import os
from utils.change_background_gemini import change_background_to_black


base_dir = os.path.dirname(os.path.abspath(__file__))

def process_directory_in_place(directory, white_threshold=220):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                output_path = os.path.join(root, file)
                change_background_to_black(image_path, output_path, white_threshold=white_threshold)

# Set your dataset paths
train_dir = os.path.join(base_dir, 'data')

# Process train and val sets
process_directory_in_place(train_dir)