# Hackathon Roulette - Project Specifications

## Overview

A CLI application that generates cross-community hackathon project ideas and randomly selects one via a spinning wheel interface.

## Core Features

### 1. Community Selection

- **Available Communities**: Python, API, FinOps, Frontend, Data Science, DevOps, UX/UI, Security
- **Selection Methods**:
  - Command-line arguments: `uv run app.py Python Frontend`
  - "all" keyword: Selects all 8 communities
  - Minimum requirement: At least 2 communities
- **Validation**: Invalid communities are skipped with warning messages

### 2. Project Generation

- **Quantity**: Always generates exactly 6 project ideas
- **Constraints**: Each project involves 1-2 people from at least 2 selected communities
- **Mock Data**: Uses template-based generation (no LLM integration in POC)
- **Project Structure**:
  ```python
  {
    "title": "Full descriptive title",
    "slug": "Shortened version for wheel display (max ~30 chars)",
    "description": "Detailed project description",
    "involved_communities": ["Community1", "Community2"],
    "team_size": "1 Community1, 1 Community2"
  }
  ```

### 3. Spinning Wheel Interface

- **Technology**: Pygame 2.6.1+
- **Display**:
  - Color-coded wheel slices (8 distinct colors)
  - Shortened project slugs displayed on wheel
  - Pointer arrow at 3 o'clock position
  - Winner announcement with visual feedback
- **Controls**:
  - SPACE: Spin the wheel
  - D: Toggle project details view
  - ESC: Exit application
- **Physics**:
  - Random initial spin velocity (15-25 units)
  - Friction coefficient: 0.992
  - Minimum speed threshold: 0.1
  - Smooth angular deceleration

### 4. User Interface Flow

1. **Console Output**:
   - Lists all 6 generated projects with full details
   - Shows both full title and wheel slug
   - Displays communities and team size
2. **Wheel Interface**:
   - Launches automatically after console display
   - Shows spinning animation
   - Announces winner
   - Optional details view (press D)
3. **Final Output**:
   - Returns to console with selected project
   - Displays complete project details
   - Exit message

## Technical Specifications

### File Structure

```
.
├── app.py                    # Main application (CLI + Pygame)
├── pyproject.toml           # Project configuration
├── SPECS.md                 # This specifications document
├── README.md               # User documentation
├── AGENTS.md               # Development guidelines
└── scripts/
    └── spinning-wheel.py    # Original wheel prototype
```

### Dependencies

```toml
# pyproject.toml
dependencies = [
    "pygame>=2.6.1",
    "openai>=2.15.0"  # For future LLM integration
]
```

### Execution

```bash
# Installation & Run
uv run app.py <community1> <community2> ...

# Examples
uv run app.py Python Frontend
uv run app.py Python DevOps Security
uv run app.py all
uv run app.py  # Shows help
```

### Code Architecture

#### Main Components

1. **CLI Parser** (`parse_communities()`):
   - Validates input communities
   - Handles "all" keyword
   - Enforces minimum 2 communities

2. **Project Generator** (`generate_mock_projects()`):
   - Creates 6 projects from templates
   - Ensures cross-community collaboration
   - Generates shortened slugs for wheel display

3. **Console Display** (`display_projects()`):
   - Formatted output of all projects
   - Shows both title and slug

4. **Wheel Engine** (`run_spinning_wheel()`):
   - Pygame-based visualization
   - Physics simulation
   - Winner selection algorithm
   - Interactive controls

#### Key Functions

- `wrap_text()`: Text wrapping for wheel display
- `get_winner()`: Determines winning slice based on angle
- `draw_wheel()`: Renders wheel with wrapped text

## Design Decisions

### 1. Simplicity First

- **Mock Data**: Uses templates instead of LLM for POC
- **No Configuration Files**: All settings in code
- **Minimal Dependencies**: Only Pygame required

### 2. User Experience

- **Progressive Disclosure**: Basic info in console, details in wheel
- **Clear Feedback**: Visual and textual confirmation
- **Error Tolerance**: Skips invalid inputs with warnings

### 3. Visual Design

- **Color Palette**: 8 distinct, high-contrast colors
- **Text Hierarchy**: Larger fonts for titles, smaller for details
- **Animation**: Smooth spinning with realistic physics

## Future Enhancements

### Phase 2: LLM Integration

- Integrate DeepSeek/OpenAI API
- Dynamic project generation based on communities
- JSON response parsing with Pydantic models

### Phase 3: Enhanced UI

- Community selection via Pygame checkboxes
- Project editing before wheel spin
- Save/load project lists

### Phase 4: Advanced Features

- Team size customization
- Project difficulty levels
- Time estimation for projects
- Export to markdown/JSON

## Quality Requirements

### Performance

- Wheel renders at 60 FPS
- Instant project generation
- Smooth animations

### Reliability

- Handles invalid inputs gracefully
- No crashes on API failures (future)
- Consistent random selection

### Usability

- Clear instructions
- Intuitive controls
- Accessible color scheme

## Testing Scenarios

### Core Functionality

1. Valid community selection (2+ communities)
2. "all" keyword functionality
3. Invalid community handling
4. Wheel spin and winner selection
5. Details toggle (D key)

### Edge Cases

1. Single community input (should fail)
2. No input (should show help)
3. Mixed valid/invalid communities
4. Wheel exit before spin completion

## Development Guidelines

### Code Style

- Follow AGENTS.md conventions
- Type hints for all functions
- Google-style docstrings
- 88 character line limit

### Testing

- Unit tests for core logic
- Integration tests for full flow
- Manual testing of Pygame UI

### Documentation

- Keep SPECS.md updated
- Maintain clear README.md
- Code comments for complex logic

## Success Metrics

### Functional

- ✅ Generates 6 projects from selected communities
- ✅ Displays projects in readable format
- ✅ Spins wheel and selects random project
- ✅ Shows project details on demand
- ✅ Handles invalid inputs gracefully

### Technical

- ✅ Single command execution
- ✅ No external dependencies beyond Pygame
- ✅ Clean code structure
- ✅ Type-safe implementation

### User Experience

- ✅ Clear instructions and feedback
- ✅ Engaging visual interface
- ✅ Intuitive keyboard controls
- ✅ Fast response times

---

_Last Updated: 2026-01-19_  
_Version: 1.0.0 (POC)_  
_Status: ✅ Complete and Functional_
