from typing import Literal

from pydantic import BaseModel, Field


class RouteDecision(BaseModel):
    route: Literal["it_question", "small_talk"]


class EvidenceGrade(BaseModel):
    sufficient: Literal["yes", "no"] = Field(
        description="Can the context fully answer the question?"
    )
    reason: str


class GroundingGrade(BaseModel):
    grounded: Literal["yes", "no"]
    unsupported_claims: list[str] = []
