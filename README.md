# The hackathon roulette

## Overview

A cli application designed to foster cross-community collaboration during hackathons.  
Users select a pool of participant communities (e.g., FinOps, Python, Frontend, Data, etc.), and an LLM generates 6 tailored project ideas that specifically require members from those communities to work together.  
Users can then launch a choice wheel to randomly choosing one of the 6 projects.

## Tech Stack

- **Language:** Python 3.13+
- **Manager:** `uv` (for project management and running)
- **UI:** Pygame
- **LLM:** DeepSeek Chat (via `openai`)

## Functional Requirements

1.  **Community Pool Selection:**
    - Predefined list of communities: Python, API, FinOps, Frontend, Data Science, DevOps, UX/UI, Security.
    - CheckboxGroup or Dropdown to define the current "pool".
2.  **LLM Prompting:**
    - Request 6 project ideas.
    - Constraints: Each project must involve 1-2 people from at least two of the selected communities.
    - Response format: Strictly JSON for programmatic parsing.
3.  **The Wheel Experience:**
    - Once ideas are generated, display them in a spinning wheel
    - The spinning wheel randomly selects one of the 6 ideas with a visual animation.
4.  **Simple Execution:**
    - Must be runnable via a single command: `uv run app.py`

## Technical Snippets

### 1. `uv` Inline Metadata

To ensure the project is self-contained, use `uv` inline script metadata at the top of `app.py`:

```python
# /// script
# dependencies = [
#   "pygame>=2.6.1",
# ]
# ///
```

### 2. LLM Prompt Example

```python
prompt = f"""
Generate 6 hackathon project ideas based on these communities: {selected_communities}.
Each project must require exactly 1-2 people from each involved community.
Return the result as a JSON list of objects with:
- title: string
- description: string
- involved_communities: list of strings
- team_size: string (e.g., '1 Python, 1 FinOps')
"""
```

### 3. Data Model (Pydantic)

```python
from pydantic import BaseModel
from typing import List

class ProjectIdea(BaseModel):
    title: str
    description: str
    involved_communities: List[str]
    team_size: str

class ProjectList(BaseModel):
    projects: List[ProjectIdea]

```
