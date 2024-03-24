

<div align="center">
  <img src="artworker/onca_prev_ui.png" width="250">
  <p><strong>Parda:</strong> a Tool for data scientists</p>
</div>



The Parda (Parser Dataset) is a versatile and powerful Python library designed to simplify the process of loading, processing, and managing various datasets. Aimed at researchers, data scientists, and developers working with large and complex datasets, this tool provides a seamless and intuitive way to handle data across different formats and structures.

## Key Features

- **Flexible Dataset Definitions**: Define your datasets with an easy-to-understand syntax that allows for detailed configurations including directory structures, file types, and custom transformations.

- **Automated Data Loading**: Automatically load data from specified directories, with support for filtering by file extensions and applying custom preprocessing steps.

- **Transformation Pipelines**: Apply a series of transformations to your data on-the-fly, making it easier to work with images, text, and other data types in their desired formats.

- **Concurrency for Efficiency**: Utilize multithreading to efficiently load and process data, significantly reducing the time required to prepare your datasets for analysis or training machine learning models.

- **Customizable Data Handling**: Whether you need batch processing, shuffling, or splitting datasets into training and validation sets, this module has you covered.

# Getting Started

## Installation

Clone this repository and include the module in your Python project.

```bash
  git clone https://github.com/CaioWing/Parda.git
```
    
Define Your Dataset: Use the provided syntax to create a definition for your dataset, specifying its structure and any transformations.

Load and Process: Utilize the module's functions to load your dataset according to the definition, ready for analysis or model training.


## Installation

To use PardaLoader, you need to have Python installed. You can install the required dependencies using pip:

```
pip install numpy pillow
```

## Usage

To use PardaLoader, you need to create an instance of the `PardaLoader` class and provide a dataset definition as a string. The dataset definition follows a specific syntax to define the structure and properties of the dataset.

### Dataset Definition

The dataset definition is a string that describes the structure and properties of the dataset. It uses the following keywords and syntax:

- `dataset`: Specifies the name of the dataset. It is followed by the dataset name in double quotes.
- `source_dir`: Specifies the source directory where the dataset files are located. It is followed by the directory path in double quotes.
- `structure`: Defines the structure of the dataset using nested subdirectories, tag directories, and label directories.
  - `subdir`: Represents a subdirectory in the dataset. It is followed by the subdirectory name in double quotes.
  - `tagdir`: Represents a tag directory within a subdirectory. It is followed by the tag directory name in double quotes.
  - `labeldir`: Represents a label directory within a tag directory. It is followed by the label directory name in double quotes. The `isd` keyword can be added to include subdirectories.
  - `files`: Specifies the file extensions to include in a directory. It is followed by the file extensions in double quotes.
- `output_format`: Specifies the output format of the loaded data. It is followed by the format name in double quotes (e.g., "numpy").
- `transformations`: Specifies the transformations to apply to the loaded data. It is followed by the transformation names in double quotes (e.g., "resize", "grayscale").

Here's an example dataset definition:

```python
dataset_definition = '''
dataset "my_dataset" {
    source_dir = "my_dataset"
    structure {
        subdir "images" {
            tagdir "train" {
                labeldir "label1" isd {
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
```

### Loading the Dataset

To load the dataset, create an instance of the `PardaLoader` class and provide the dataset definition:

```python
loader = PardaLoader(dataset_definition)
loader.parse()
```

You can then load the dataset using the `load_dataset` method:

```python
dataset = loader.load_dataset(generator=True, batch_size=4, shuffle=True, num_workers=4, max_files_per_dir=100)
```

The `load_dataset` method accepts the following arguments:
- `generator` (bool): If True, returns a generator that yields batches of data. If False, returns the entire dataset as a dictionary.
- `batch_size` (int): The number of samples per batch when using the generator.
- `shuffle` (bool): If True, shuffles the order of the files.
- `num_workers` (int): The number of worker threads to use for loading and preprocessing the data.
- `max_files_per_dir` (int): The maximum number of files to load from each directory. If None, loads all files.

### Getting Dataset Information

You can retrieve information about the loaded dataset using the `get_dataset_info` method:

```python
info = loader.get_dataset_info()
print("Dataset Information:")
print(info)
```

## Contributing

Contributions are welcome! If you have suggestions for improving this module, feel free to fork the repository and submit a pull request.


## Authors

- [@CaioWing](https://github.com/CaioWing)

