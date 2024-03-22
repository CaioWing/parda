import os
import re
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class DatasetLoader:
    def __init__(self, dataset_definition):
        self.dataset_definition = dataset_definition
        self.dataset_name = ""
        self.source_dir = ""
        self.structure = []
        self.output_format = ""
        self.transformations = []

    def parse(self):
        lines = self.dataset_definition.split("\n")
        parsing_structure = False
        structure_lines = []
        brace_count = 0  # Initialize a counter to track the depth of nested structures

        for line in lines:
            line = line.strip()
            # print(line)
            if line.startswith("dataset"):
                self.dataset_name = re.findall(r'"(.+?)"', line)[0]
                brace_count = 1

            elif line.startswith("source_dir"):
                self.source_dir = re.findall(r'"(.+?)"', line)[0]

            elif line.startswith("structure"):
                parsing_structure = True
                brace_count += 1  # Start of structure, set brace count to 1

            elif line.startswith("output_format"):
                self.output_format = re.findall(r'"(.+?)"', line)[0]

            elif line.startswith("transformations"):
                self.transformations = [t.strip() for t in re.findall(r'"(.+?)"', line)]

            elif parsing_structure:
                if line.startswith("{") or line.endswith("{"):
                    brace_count += 1  # Increment brace count for each opening brace
                elif line.startswith("}") or line.endswith("}"):
                    brace_count -= 1  # Decrement brace count for each closing brace
                    if brace_count == 0:
                        parsing_structure = False  # End of structure when brace count returns to 0
                        # print("estrutura:", structure_lines)
                        self.parse_structure(structure_lines)
                        structure_lines = []  # Reset structure_lines for potential future structures
                        continue  # Skip appending the closing brace of the structure to lines
                structure_lines.append(line)
            

    def parse_structure(self, lines):
        context_stack = []  # Stack to keep track of the current context: subdir, tagdir, or labeldir

        for line in lines:
            line = line.strip()
            if not line or line == "}":  # Ignore empty lines or lines that only close a context
                if line == "}" and context_stack:
                    context_stack.pop()  # Exit the current context
                continue

            # Extract the type (key) and name (value) of the current element
            key, value = re.match(r"(\w+)\s+\"(.+?)\"", line).groups()
            value = value.strip('"')

            if key == "subdir":
                current_subdir = {"name": value, "type": "subdir", "tagdirs": [], "files": []}
                if not context_stack:  # If the stack is empty, this subdir is top-level
                    self.structure.append(current_subdir)
                else:
                    context_stack[-1]["tagdirs"].append(current_subdir)  # Add to the last context in the stack
                context_stack.append(current_subdir)  # Push the current context onto the stack
            elif key == "tagdir":
                current_tagdir = {"name": value, "type": "tagdir", "labeldirs": [], "files": []}
                context_stack[-1]["tagdirs"].append(current_tagdir)  # Add to the last context in the stack
                context_stack.append(current_tagdir)  # Push the current context onto the stack
            elif key == "labeldir":
                current_labeldir = {"name": value, "type": "labeldir", "files": []}
                context_stack[-1]["labeldirs"].append(current_labeldir)  # Add to the last context in the stack
                context_stack.append(current_labeldir)  # Push the current context onto the stack
            elif key == "files":
                file_extensions = re.findall(r'"(.+?)"', line)
                context_stack[-1]["files"].extend(file_extensions)  # Add to the last context in the stack

    def load_dataset(self, generator=False, batch_size=32, shuffle=False, num_workers=1, max_files_per_dir=None):
        self.num_workers = num_workers
        dataset = {}

        def process_files(dir_path, extensions):
            file_list = []
            for file in os.listdir(dir_path):
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(dir_path, file)
                    file_list.append(file_path)

            if shuffle:
                np.random.shuffle(file_list)

            if max_files_per_dir is not None:
                file_list = file_list[:max_files_per_dir]

            if generator:
                def batch_generator():
                    for i in range(0, len(file_list), batch_size):
                        batch_files = file_list[i:i+batch_size]
                        batch_data = self.load_and_preprocess_files(batch_files)
                        yield batch_data
                return batch_generator()
            else:
                return self.load_and_preprocess_files(file_list)

        def process_structure(structure, parent_dir, parent_dataset):
            for item in structure:
                item_name = item["name"]
                item_path = os.path.join(parent_dir, item_name)
                item_type = item["type"]

                if item_type == "subdir":
                    parent_dataset[item_name] = {}
                    process_structure(item["tagdirs"], item_path, parent_dataset[item_name])
                    if "files" in item:
                        parent_dataset[item_name]["files"] = process_files(item_path, item["files"])
                elif item_type == "tagdir":
                    parent_dataset[item_name] = {}
                    process_structure(item["labeldirs"], item_path, parent_dataset[item_name])
                    if "files" in item:
                        parent_dataset[item_name]["files"] = process_files(item_path, item["files"])
                elif item_type == "labeldir":
                    parent_dataset[item_name] = process_files(item_path, item["files"])

        process_structure(self.structure, self.source_dir, dataset)
        return dataset

    def load_and_preprocess_files(self, file_list):
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            data = list(executor.map(self.load_and_preprocess_file, file_list))
        return data

    def load_and_preprocess_file(self, file_path):
        if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            image = self.load_image(file_path)
            return image
        elif file_path.lower().endswith((".txt", ".csv")):
            text = self.load_text(file_path)
            return text
        # Add more file types and preprocessing steps as needed

    def load_image(self, file_path):
        image = Image.open(file_path)
        image = self.apply_transformations(image)
        return np.array(image)

    def load_text(self, file_path):
        with open(file_path, "r") as file:
            text = file.read()
        return text

    def apply_transformations(self, image):
        for transformation in self.transformations:
            if transformation == "resize":
                image = image.resize((256, 256))  # Example resizing to 256x256
            elif transformation == "grayscale":
                image = image.convert("L")
            # Add more transformations as needed
        return image

    def get_dataset_info(self):
        info = {
            "dataset_name": self.dataset_name,
            "source_directory": self.source_dir,
            "output_format": self.output_format,
            "transformations": self.transformations,
            "structure": self.structure
        }
        return info

    def visualize_dataset(self, num_samples=5):
        dataset = self.load_dataset()
        print(f"Dataset: {self.dataset_name}")
        print(f"Source Directory: {self.source_dir}")
        print(f"Output Format: {self.output_format}")
        print(f"Transformations: {self.transformations}")
        print("Dataset Structure:")
        self.visualize_structure(dataset, num_samples)

    def visualize_structure(self, dataset, num_samples, indent_level=0):
        for key, value in dataset.items():
            indent = "    " * indent_level
            if isinstance(value, dict):
                print(f"{indent}{key}:")
                self.visualize_structure(value, num_samples, indent_level + 1)
            elif isinstance(value, list):
                print(f"{indent}{key}: {len(value)} files")
                if len(value) > 0 and indent_level < 2:
                    print(f"{indent}  Samples:")
                    for i in range(min(num_samples, len(value))):
                        print(f"{indent}    {value[i]}")
            else:
                print(f"{indent}{key}: {value}")

    def split_dataset(self, split_ratio=0.8, shuffle=True):
        dataset = self.load_dataset(shuffle=shuffle)
        train_dataset = {}
        val_dataset = {}

        def split_data(data, split_ratio):
            split_index = int(len(data) * split_ratio)
            return data[:split_index], data[split_index:]

        def split_structure(structure, parent_dataset, split_ratio):
            for key, value in structure.items():
                if isinstance(value, dict):
                    parent_dataset[key] = {}
                    split_structure(value, parent_dataset[key], split_ratio)
                elif isinstance(value, list):
                    train_data, val_data = split_data(value, split_ratio)
                    parent_dataset[key] = train_data
                    val_dataset[key] = val_data

        split_structure(dataset, train_dataset, split_ratio)
        return train_dataset, val_dataset

    def get_class_weights(self):
        dataset = self.load_dataset()
        class_counts = {}

        def count_classes(structure):
            for key, value in structure.items():
                if isinstance(value, dict):
                    count_classes(value)
                elif isinstance(value, list):
                    if key not in class_counts:
                        class_counts[key] = 0
                    class_counts[key] += len(value)

        count_classes(dataset)
        total_samples = sum(class_counts.values())
        class_weights = {cls: total_samples / count for cls, count in class_counts.items()}
        return class_weights

    def get_file_paths(self):
        file_paths = []

        def collect_file_paths(structure):
            for key, value in structure.items():
                if isinstance(value, dict):
                    collect_file_paths(value)
                elif isinstance(value, list):
                    file_paths.extend(value)

        dataset = self.load_dataset()
        collect_file_paths(dataset)
        return file_paths


if __name__ == '__main__':
    # Example usage
    dataset_definition = '''
    dataset "my_dataset" {
        source_dir = "my_dataset"
        
        structure {
            subdir "images" {
                tagdir "train" {
                    labeldir "label1" {
                        files ".jpg" ".png" ".jpeg"
                    }
                    labeldir "label2" {
                        files ".jpg" ".png" ".jpeg"
                    }
                }
                tagdir "test" {
                    files ".jpg" ".png"
                }
            }
            subdir "annotations" {
                files ".txt"
            }
        }
        
        output_format = "numpy"
        transformations = "resize" "grayscale"
    }
    '''

    loader = DatasetLoader(dataset_definition)
    loader.parse()

    # Load the dataset
    dataset = loader.load_dataset(generator=False, batch_size=32, shuffle=True, num_workers=4, max_files_per_dir=100)
    # Get dataset information
    info = loader.get_dataset_info()
    print("Dataset Information:")
    print(info)

    # Visualize the dataset structure
    print("\nDataset Structure:")
    loader.visualize_dataset(num_samples=3)