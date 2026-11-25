"""Canonical enumerations for the domain model (SPECS.md §2, §4, §6, §8, §9)."""

from __future__ import annotations

import enum


class ResourceType(str, enum.Enum):
    MODEL = "MODEL"
    SPACE = "SPACE"
    API_SERVICE = "API_SERVICE"
    MCP_SERVER = "MCP_SERVER"
    AGENT_SERVICE = "AGENT_SERVICE"
    DATASET = "DATASET"
    REPOSITORY = "REPOSITORY"


class InterfaceType(str, enum.Enum):
    HTTP_REST = "HTTP_REST"
    OPENAPI = "OPENAPI"
    GRADIO = "GRADIO"
    MCP = "MCP"
    A2A = "A2A"
    SDK = "SDK"
    EMBED = "EMBED"
    WEBHOOK = "WEBHOOK"
    CLI = "CLI"


class CapabilityStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    DISCOVERED = "DISCOVERED"
    CONTRACT_VERIFIED = "CONTRACT_VERIFIED"
    EVALUATED = "EVALUATED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    SUSPENDED = "SUSPENDED"
    DEPRECATED = "DEPRECATED"


class ExecutionStatus(str, enum.Enum):
    CREATED = "CREATED"
    POLICY_CHECK = "POLICY_CHECK"
    QUEUED = "QUEUED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STREAMING = "STREAMING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    DENIED = "DENIED"


class Decision(str, enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    ALLOW_WITH_LIMITS = "ALLOW_WITH_LIMITS"


class DataClass(str, enum.Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class EvidenceMark(str, enum.Enum):
    MEASURED = "MEASURED"
    REPORTED = "REPORTED"
    INFERRED = "INFERRED"


class Channel(str, enum.Enum):
    WEB = "WEB"
    TELEGRAM = "TELEGRAM"
    DISCORD = "DISCORD"
    TEAMS = "TEAMS"
    LINE = "LINE"
    SLACK = "SLACK"
    WHATSAPP = "WHATSAPP"


class EntityType(str, enum.Enum):
    PROVIDER = "PROVIDER"
    RESOURCE = "RESOURCE"
    INTERFACE = "INTERFACE"
    OPERATION = "OPERATION"
    TOOL = "TOOL"
    CAPABILITY = "CAPABILITY"
    CONTRACT = "CONTRACT"
    EVALUATION = "EVALUATION"
    HEALTH = "HEALTH"
    POLICY = "POLICY"
    EXECUTION = "EXECUTION"
    ARTIFACT = "ARTIFACT"
    RECIPE = "RECIPE"
    APP = "APP"
    DEPLOYMENT = "DEPLOYMENT"