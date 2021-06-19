import pandas as pd

from open_anonymizer.anon import anonymize
from open_anonymizer.utils import init_pipeline, remove_context

# initialize model
nlp = init_pipeline(model_name="xlm-roberta-large-finetuned-conll03-german")

# anonymize a single text
sample_text = """
    Hallo mein Name ist Herr Meiner. Ich komme aus Wuppertal und habe 24566465 indische Elefanten aus Indien. 
    Meine Mail ist: test@wupper.tal. 
    Meine Frau, Anne, ist Bäckerin in Nierdersachsen, wohnt aber genau wie ich in Wuppertal.
    """

res = anonymize(
    text=sample_text,
    pipeline=nlp,
    entities=["PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"],
    flag_replace_address=True,
)

print(f"anonymized: {res}")
print("####################################")

# if you want to remove the context just use
context_removed_res = remove_context(res)
print(f"context removed: {context_removed_res}")
print("####################################")


# you can also easily loop across multiple open texts
sample_texts = [
    "Hallo mein Name ist Herr Meiner. Ich komme aus Wuppertal und habe 24566465 indische Elefanten aus Indien.",
    "Meine Mail ist: test@wupper.tal.",
    "Meine Frau, Anne, ist Bäckerin in Nierdersachsen, wohnt aber genau wie ich in Wuppertal.",
]

res_multiple = []
for each in sample_texts:
    temp_res = anonymize(
        text=sample_text,
        pipeline=nlp,
        entities=["PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"],
        flag_replace_address=True,
    )
    res_multiple.append(temp_res)

print(f"multiple sentences anonymized: {res_multiple}")
print("####################################")

# or use it with pandas dataframes
res_dict = []
for each in sample_texts:
    temp_dict = {"text": each}
    res_dict.append(temp_dict)

res_df = pd.DataFrame(res_dict)

res_df["text_anon"] = res_df.apply(
    lambda x: anonymize(
        text=x["text"],
        pipeline=nlp,
        entities=["PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"],
        flag_replace_address=True,
    ),
    axis=1,
)

print("pandas dataframe anonymized:")
print(res_df.head())
