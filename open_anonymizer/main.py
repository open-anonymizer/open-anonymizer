import math
import time
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

import pandas as pd
import typer
from tqdm import tqdm

from open_anonymizer.anon import anonymize
from open_anonymizer.model_utils import clean_entities
from open_anonymizer.regex_rules import (regex_clean_date, regex_clean_email,
                                         regex_clean_number, regex_clean_phone)
from open_anonymizer.utils import (fix_strlist_value, init_pipeline,
                                   remove_context)

app = typer.Typer()


@app.callback()
def callback():
    """
    Anonymize your texts
    """


@app.command()
def init():

    model_name = "xlm-roberta-large-finetuned-conll03-german"

    typer.echo("=======================================")
    typer.echo(f"Checking if {model_name} is available.")
    typer.echo(f"{model_name} will be downloaded from Huggingface Model Hub otherwise.")
    typer.echo("This might take some minutes.")

    init_pipeline(model_name)

    typer.echo("=======================================")
    typer.echo(f"{model_name} is now available on your machine!")


@app.command()
def text(
    text: str = typer.Argument(..., help="Text to anonymize"),
    entity: List[str] = typer.Option(
        ["PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"],
        prompt="Select the entities you want to anonymize",
    ),
    no_context: bool = typer.Option(False),
):
    """
    Clean a single text, useful for testing and comparing models
    """

    entity = fix_strlist_value(entity)
    entities = list(set(entity))

    cleaned_text = deepcopy(text)

    # moved this block up, otherwise email-deanon does not work: markus@obi.de -> markus @ORG_1.de which is not picked up by mail-deanon.
    if "DATE" in entities:
        cleaned_text = regex_clean_date(cleaned_text)
    if "PHONE" in entities:
        cleaned_text = regex_clean_phone(cleaned_text)
    if "NUMBER" in entities:
        cleaned_text = regex_clean_number(cleaned_text, True)
    if "EMAIL" in entities:
        cleaned_text = regex_clean_email(cleaned_text)

    if any([e in ["PER", "LOC", "ORG"] for e in entities]):

        flag_replace_adress = typer.confirm(
            "Do you want to remove terms of address, like Herr or Frau?", default=True
        )

        # use large one as a default
        model_name = "xlm-roberta-large-finetuned-conll03-german"

        typer.echo("=======================================")
        typer.echo(f"Initializing {model_name}, this might take a few seconds")

        nlp = init_pipeline(model_name)
        cleaned_text = clean_entities(
            text=cleaned_text, pipeline=nlp, entities=entities, replace_address=flag_replace_adress
        )

    if no_context:
        cleaned_text = remove_context(cleaned_text)

    typer.echo("=======================================")
    typer.echo(cleaned_text)


@app.command()
def batch(
    input: Path = typer.Option(None, prompt="Path to your original file", exists=True),
    col: List[str] = typer.Option(None, prompt="Which columns do you want to anonymize?"),
    output: Path = typer.Option("results.csv", prompt="Path to anonymized file"),
    entity: List[str] = typer.Option(
        ["PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"],
        prompt="Select the entities you want to anonymize",
    ),
    replace_address: bool = typer.Option(
        True, prompt="Do you want to remove terms of address, like Herr or Frau?"
    ),
    no_context: bool = typer.Option(False, prompt="Do you want to remove the context?"),
):
    """
    Clean one or multiple columns in a csv file. 
    """

    start_ts = time.time()

    col = fix_strlist_value(col)
    cols = list(set(col))

    if not cols:
        typer.echo("No columns specified. Exiting.")
        raise typer.Exit()

    entity = fix_strlist_value(entity)
    entities = list(set(entity))

    typer.echo("=======================================")
    nlp = None
    if any([e in ["PER", "LOC", "ORG"] for e in entities]):

        model_name = "xlm-roberta-large-finetuned-conll03-german"
        typer.echo(f"Initializing {model_name}, this might take a few seconds")
        nlp = init_pipeline(model_name)

    typer.echo("=======================================")
    typer.echo("Loading your data")
    df = pd.read_csv(input)

    typer.echo("=======================================")
    typer.echo("Start anonymizing your data")
    tqdm.pandas()
    for c in cols:
        df[c] = df.progress_apply(
            lambda x: anonymize(
                text=x[c], pipeline=nlp, entities=entities, flag_replace_address=replace_address
            ),
            axis=1,
        )

    if no_context:
        typer.echo("=======================================")
        typer.echo("Removing context from data")
        for c in cols:
            df[c] = df.progress_apply(lambda x: remove_context(text=x[c]), axis=1)

    typer.echo("=======================================")
    typer.echo("Writing results")
    df.to_csv(output, index=False)

    time_taken = time.time() - start_ts
    time_taken_min = math.floor(time_taken / 60)
    time_taken_sec = time_taken - time_taken_min * 60
    typer.echo(f"All done in {time_taken_min} minutes and {time_taken_sec:.0f} seconds")
