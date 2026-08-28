# AI-Based Mobile Recommendation System

An AI-powered Python package that recommends mobile phones based on user preferences such as budget, camera quality, RAM, storage, battery, and screen size. It validates natural-language requests, filters and scores a mobile phone dataset, and explains the recommendation using Ollama.

## Features

- Accepts mobile phone requirements in natural language
- Uses an Ollama model to validate and extract requirements
- Cleans and refines mobile phone data
- Filters phones using required specifications
- Scores results according to the user's priorities
- Recommends the best matching phones and explains the result

## Requirements

- Python 3.10 or newer
- Ollama installed and running
- Access to the `gpt-oss:120b-cloud` Ollama model

Install Ollama from [ollama.com/download](https://ollama.com/download), then sign in and make the model available:

```bash
ollama signin
ollama pull gpt-oss:120b-cloud
```

## Install From PyPI

The package distribution name is `mobile_phone_recommendation_system`. Install the latest published version in an activated virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the package and its declared Python dependencies:

```bash
python -m pip install mobile_phone_recommendation_system
```

Run the application as a module:

```bash
python -m mobile_phone_recommendation_system
```

The package name used by `pip` and the module name used by Python are the same in this project. In general, Python module names must use underscores rather than hyphens.

## Install In Editable Mode

Editable installation is intended for development. It makes the local source code importable in the environment, so changes to Python files are available without rebuilding and reinstalling the package.

First, download the Git repository to your local machine and open the repository root, the directory containing `pyproject.toml`.

Then run:

```bash
python -m pip install -e .
```

Run the local package with:

```bash
python -m mobile_phone_recommendation_system
```

Editable mode is recommended when you plan to update the code. A regular install is more appropriate when you only want to use a published release.

## Updating A Local Development Install

After changing the source code, run the package again. No reinstall is normally required:

```bash
python -m mobile_phone_recommendation_system
```

If you change `pyproject.toml`, add or remove dependencies, or change package metadata, reinstall the editable package:

```bash
python -m pip install -e . --upgrade
```

To update to a newer published release instead:

```bash
python -m pip install --upgrade mobile_phone_recommendation_system
```

## Use From The Repository

Clone the repository and enter its root directory:

```bash
git clone https://github.com/iamsouradeepsarkar/Mobile_Phone_Recommendation_System.git
cd Mobile_Phone_Recommendation_System
```

Create a virtual environment, activate it, and install the package in editable mode:

```bash
python -m pip install -e .
```

Then run:

```bash
python -m mobile_phone_recommendation_system
```

The package should be run from the module entry point rather than by executing an individual source file. This allows Python to resolve the package's relative imports correctly.

## Project Structure

```text
Mobile_Phone_Recommendation_System/
├── pyproject.toml
├── README.md
├── requirements.txt
├── LICENSE
└── src/
    └── mobile_phone_recommendation_system/
        ├── __init__.py
        ├── __main__.py
        ├── main.py
        ├── ai_response_generator.py
        ├── data_cleaner.py
        ├── filter_mobiles_based_on_user_inputs.py
        ├── unique_company_ratings.py
        ├── unique_model_ratings.py
        ├── unique_processor_ratings.py
        ├── instructions/
        ├── mobile_data/
        ├── refined_mobile_data/
        └── ratings_files/
```

The package data includes the AI instruction files, the source mobile dataset, the refined dataset, and the generated company, model, and processor ratings.

## How It Works

1. The application asks for a mobile phone request.
2. Ollama validates the request and extracts its requirements.
3. The dataset is cleaned if a refined version is not available.
4. Company, model, and processor ratings are generated when required.
5. Phones are filtered using strict requirements.
6. Matching phones are scored according to the requested priorities.
7. The highest-scoring phone is displayed with an AI-generated explanation.

## Runtime Notes

- Ollama must be installed, running, and authenticated for AI features to work.
- The application uses the `gpt-oss:120b-cloud` model.
- The package currently uses bundled data files and generated rating files.
- If no phone matches the strict requirements, the application reports that no matching result was found.

## License

This project is licensed under the MIT License.

## Links

- [Homepage](https://github.com/iamsouradeepsarkar/Mobile_Phone_Recommendation_System)
- [Issue tracker](https://github.com/iamsouradeepsarkar/Mobile_Phone_Recommendation_System/issues)
