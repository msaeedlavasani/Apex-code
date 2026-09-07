"""Bounded product provider/model catalog for the local Apex MVP.

This module contains non-secret product metadata only. Credential material is
resolved by the desktop broker and exists in the Python service only in
memory for the selected runtime configuration.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


class ProviderConfigurationError(ValueError):
    """A provider or model selection is not supported by the bounded catalog."""


@dataclass(frozen=True)
class ModelDefinition:
    model_id: str
    display_name: str


@dataclass(frozen=True)
class ProviderDefinition:
    provider_id: str
    display_name: str
    credential_env: str
    models: tuple[ModelDefinition, ...]


@dataclass(frozen=True)
class ModelSelection:
    provider_id: str
    model_id: str

    @property
    def model_reference(self) -> str:
        return f"{self.provider_id}/{self.model_id}"


PROVIDERS: tuple[ProviderDefinition, ...] = (
    ProviderDefinition(
        "openai",
        "OpenAI",
        "OPENAI_API_KEY",
        (
            ModelDefinition("gpt-4o-mini", "GPT-4o mini"),
            ModelDefinition("gpt-4.1-mini", "GPT-4.1 mini"),
        ),
    ),
    ProviderDefinition(
        "anthropic",
        "Anthropic",
        "ANTHROPIC_API_KEY",
        (
            ModelDefinition("claude-3-5-haiku-20241022", "Claude 3.5 Haiku"),
            ModelDefinition("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet"),
        ),
    ),
    ProviderDefinition(
        "openrouter",
        "OpenRouter",
        "OPENROUTER_API_KEY",
        (
            ModelDefinition("openai/gpt-4o-mini", "OpenAI GPT-4o mini"),
            ModelDefinition("anthropic/claude-3.5-sonnet", "Anthropic Claude 3.5 Sonnet"),
        ),
    ),
)


def provider_definition(provider_id: str) -> ProviderDefinition:
    for provider in PROVIDERS:
        if provider.provider_id == provider_id:
            return provider
    raise ProviderConfigurationError("provider is not supported")


def validate_selection(provider_id: str, model_id: str) -> ModelSelection:
    provider = provider_definition(provider_id)
    if not isinstance(model_id, str) or not model_id.strip():
        raise ProviderConfigurationError("model is required")
    if not any(model.model_id == model_id for model in provider.models):
        raise ProviderConfigurationError("model is not supported for the selected provider")
    return ModelSelection(provider.provider_id, model_id)


def catalog_records(
    selection: ModelSelection | None = None,
    configured_provider_id: str | None = None,
) -> list[dict[str, object]]:
    """Return a renderer-safe catalog with no credential material."""
    records: list[dict[str, object]] = []
    for provider in PROVIDERS:
        records.append(
            {
                "provider_id": provider.provider_id,
                "display_name": provider.display_name,
                "configured": provider.provider_id == configured_provider_id,
                "models": [asdict(model) for model in provider.models],
                "catalog_strategy": "CURATED_STATIC_MVP",
                "credential_status": "CONFIGURED" if provider.provider_id == configured_provider_id else "NOT_CONFIGURED",
            }
        )
    return records
