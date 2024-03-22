
# Dataset Configuration Module

The Dataset Configuration Module is a versatile and powerful Python library designed to simplify the process of loading, processing, and managing various datasets. Aimed at researchers, data scientists, and developers working with large and complex datasets, this tool provides a seamless and intuitive way to handle data across different formats and structures.

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
## Usage/Examples

```python
from dataset_loader import DatasetLoader

# Define your dataset
dataset_definition = """
dataset "my_dataset" {
    source_dir = "path/to/your/dataset"
    
    structure {
        ...
    }
    
    output_format = "numpy"
    transformations = "resize" "grayscale"
}
"""

# Initialize the loader and load your dataset
loader = DatasetLoader(dataset_definition)
dataset = loader.load_dataset()
```


## Contributing

Contributions are welcome! If you have suggestions for improving this module, feel free to fork the repository and submit a pull request.


## Authors

- [@CaioWing](https://github.com/CaioWing)

