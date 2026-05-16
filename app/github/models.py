"""Pydantic models for GitHub webhook event payloads."""

from typing import Any

from pydantic import BaseModel


class GitHubUser(BaseModel):
    login: str
    id: int


class GitHubRepository(BaseModel):
    id: int
    full_name: str
    default_branch: str = "main"


class GitHubInstallation(BaseModel):
    id: int


class GitHubIssue(BaseModel):
    number: int
    title: str
    body: str | None = None
    user: GitHubUser
    labels: list[dict[str, Any]] = []


class GitHubPullRequest(BaseModel):
    number: int
    title: str
    body: str | None = None
    user: GitHubUser


class IssueEvent(BaseModel):
    action: str
    issue: GitHubIssue
    repository: GitHubRepository
    installation: GitHubInstallation


class PullRequestEvent(BaseModel):
    action: str
    pull_request: GitHubPullRequest
    repository: GitHubRepository
    installation: GitHubInstallation


class IssueCommentEvent(BaseModel):
    action: str
    issue: GitHubIssue
    comment: dict[str, Any]
    repository: GitHubRepository
    installation: GitHubInstallation
