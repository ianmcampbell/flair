import shutil

import pytest
from torch.optim import SGD
from torch.optim.adam import Adam

import flair.datasets
from flair.data import Sentence, MultiCorpus
from flair.embeddings import (
    WordEmbeddings,
    FlairEmbeddings,
)
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

turian_embeddings = WordEmbeddings("turian")
flair_embeddings = FlairEmbeddings("news-forward-fast")


@pytest.mark.integration
def test_load_use_tagger():
    loaded_model: SequenceTagger = SequenceTagger.load("ner")

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])
    del loaded_model

    sentence.clear_embeddings()
    sentence_empty.clear_embeddings()

    loaded_model: SequenceTagger = SequenceTagger.load("pos")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])
    del loaded_model


@pytest.mark.integration
def test_load_use_tagger_keep_embedding():
    loaded_model: SequenceTagger = SequenceTagger.load("ner")

    sentence = Sentence("I love Berlin")
    loaded_model.predict(sentence)
    for token in sentence:
        assert len(token.embedding.cpu().numpy()) == 0

    loaded_model.predict(sentence, embedding_storage_mode="cpu")
    for token in sentence:
        assert len(token.embedding.cpu().numpy()) > 0

    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger(results_base_path, tasks_base_path):
    corpus = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=2,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, tag_dictionary, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger_empty_tags(results_base_path, tasks_base_path):
    corpus = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 2: "ner"}
    )
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=2,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, tag_dictionary, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger_large(results_base_path, tasks_base_path):
    corpus = flair.datasets.UD_ENGLISH().downsample(0.05)
    tag_dictionary = corpus.make_tag_dictionary("pos")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="pos",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=32,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, tag_dictionary, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger_flair_embeddings(results_base_path, tasks_base_path):
    corpus = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=flair_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=2,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, tag_dictionary, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger_adam(results_base_path, tasks_base_path):
    corpus = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus, optimizer=Adam)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=2,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, tag_dictionary, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_load_use_tagger_multicorpus(results_base_path, tasks_base_path):
    corpus_1 = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    corpus_2 = flair.datasets.NER_GERMAN_GERMEVAL(base_path=tasks_base_path)

    corpus = MultiCorpus([corpus_1, corpus_2])
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        results_base_path,
        learning_rate=0.1,
        mini_batch_size=2,
        max_epochs=2,
        shuffle=False,
    )

    del trainer, tagger, corpus
    loaded_model: SequenceTagger = SequenceTagger.load(
        results_base_path / "final-model.pt"
    )

    sentence = Sentence("I love Berlin")
    sentence_empty = Sentence("       ")

    loaded_model.predict(sentence)
    loaded_model.predict([sentence, sentence_empty])
    loaded_model.predict([sentence_empty])

    # clean up results directory
    shutil.rmtree(results_base_path)
    del loaded_model


@pytest.mark.integration
def test_train_resume_tagger(results_base_path, tasks_base_path):
    corpus_1 = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    corpus_2 = flair.datasets.NER_GERMAN_GERMEVAL(base_path=tasks_base_path)

    corpus = MultiCorpus([corpus_1, corpus_2])
    tag_dictionary = corpus.make_tag_dictionary("ner")

    model: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    trainer = ModelTrainer(model, corpus)
    trainer.train(results_base_path, max_epochs=2, shuffle=False, checkpoint=True)

    del trainer, model
    trainer = ModelTrainer.load_checkpoint(results_base_path / "checkpoint.pt", corpus)

    trainer.train(results_base_path, max_epochs=2, shuffle=False, checkpoint=True)

    # clean up results directory
    shutil.rmtree(results_base_path)
    del trainer


@pytest.mark.integration
def test_find_learning_rate(results_base_path, tasks_base_path):
    corpus = flair.datasets.ColumnCorpus(
        data_folder=tasks_base_path / "fashion", column_format={0: "text", 3: "ner"}
    )
    tag_dictionary = corpus.make_tag_dictionary("ner")

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=64,
        embeddings=turian_embeddings,
        tag_dictionary=tag_dictionary,
        tag_type="ner",
        use_crf=False,
    )

    # initialize trainer
    trainer: ModelTrainer = ModelTrainer(tagger, corpus, optimizer=SGD)

    trainer.find_learning_rate(results_base_path, iterations=5)

    # clean up results directory
    shutil.rmtree(results_base_path)
    del trainer, tagger, tag_dictionary, corpus

