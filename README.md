# Open Anonymizer

Open Anonymizer is a natural language processing software that anonymizes German texts. Open Anonymizer uses a XLM-RoBERTa model for anonymizing `persons/names`, `locations`, `organizations` and a rule-based approach for anonymizing `dates`, `phone numbers`, `other numbers` and `emails`.

![Screenshot CLI](screenshot_cli_text.png?raw=true)


## Installing this library

For using this code and repository, besides a Python installation you should have poetry (https://python-poetry.org/docs/#installation) installed. 

We suggest that you clone this repo and initialize it with `poetry shell` and install all dependencies via `poetry install`. 

## Usage in your own script

You can use the library as shown in the **examples** folder in your own scripts.

## Usage via the command line interface

Or if you want to use the command line interface, follow these steps. 

* Clone this repo.
* Run `poetry shell`.
* and install all dependencies with `poetry install`.
* if you want to anonymize a single text, run `anonymize text 'Hallo ich bin Markus'` and follow the instructions.
* if you want to anonymize a comma seperated filee run `anonymize batch` and folllow the prompts, e.g. with example data that can be found in `./examples`.

## Further information

Open Anonymizer is a part of our Master Thesis for the Mannheim Master of Applied Data Science & Measurement written by Dimitri Epp and Markus Nutz.

## License 

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
