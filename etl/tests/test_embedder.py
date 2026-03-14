# tests/test_embedder.py
import pytest
from unittest.mock import patch, MagicMock
from embedder import embed_texts, EmbedderConfig, OLLAMA_DIM, OPENAI_DIM


def test_ollama_returns_correct_dimension():
    mock_embedding = [0.1] * OLLAMA_DIM
    with patch("embedder.ollama.embeddings") as mock_ollama:
        mock_ollama.return_value = {"embedding": mock_embedding}
        cfg = EmbedderConfig(backend="ollama")
        result = embed_texts(["test text"], cfg)
    assert len(result) == 1
    assert len(result[0]) == OLLAMA_DIM


def test_embed_multiple_texts():
    mock_embedding = [0.1] * OLLAMA_DIM
    with patch("embedder.ollama.embeddings") as mock_ollama:
        mock_ollama.return_value = {"embedding": mock_embedding}
        cfg = EmbedderConfig(backend="ollama")
        result = embed_texts(["text one", "text two", "text three"], cfg)
    assert len(result) == 3
    assert mock_ollama.call_count == 3


def test_openai_fallback_uses_correct_dim():
    mock_embedding = [0.2] * OPENAI_DIM
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=mock_embedding)]
    with patch("embedder.openai.OpenAI") as mock_client_class:
        mock_client = MagicMock()
        mock_client.embeddings.create.return_value = mock_response
        mock_client_class.return_value = mock_client
        cfg = EmbedderConfig(backend="openai", openai_api_key="test-key")
        result = embed_texts(["test"], cfg)
    assert len(result[0]) == OPENAI_DIM


def test_raises_on_unknown_backend():
    cfg = EmbedderConfig(backend="unknown")  # type: ignore
    with pytest.raises(ValueError, match="Unknown backend"):
        embed_texts(["test"], cfg)
