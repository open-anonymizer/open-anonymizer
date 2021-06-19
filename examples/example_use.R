# install.packages("reticulate")

library(reticulate)

use_virtualenv("/Users/mnutz/Library/Caches/pypoetry/virtualenvs/open-anonymizer-KkKdYzNH-py3.7")

source_python('open_anonymizer/utils.py')
source_python('open_anonymizer/anon.py')

nlp <- init_pipeline(model_name="xlm-roberta-large-finetuned-conll03-german")

sample_text <- "Hallo mein Name ist Herr Meiner. Ich komme aus Wuppertal und habe 24566465 indische Elefanten aus Indien. Meine Mail ist: test@wupper.tal. Meine Frau, Anne, ist Bäckerin in Nierdersachsen, wohnt aber genau wie ich in Wuppertal."

anonymize(
    text=sample_text,
    pipeline=nlp,
    entities=c("PER", "LOC", "ORG", "DATE", "PHONE", "NUMBER", "EMAIL"),
    flag_replace_address=TRUE
)