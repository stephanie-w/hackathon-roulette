# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pygame>=2.6.1",
# ]
# ///

"""
Hackathon Roulette - CLI application for generating cross-community project ideas.
"""

import math
import random
import sys
from typing import Any

import pygame


AVAILABLE_COMMUNITIES = [
    "Python",
    "API",
    "FinOps",
    "Frontend",
    "Data Science",
    "DevOps",
    "UX/UI",
    "Security",
]


def parse_communities(community_args: list[str]) -> list[str]:
    """Parse community arguments from command line."""
    selected = []
    for arg in community_args:
        if arg.lower() == "all":
            return AVAILABLE_COMMUNITIES
        # Check if it's a valid community
        for community in AVAILABLE_COMMUNITIES:
            if arg.lower() == community.lower():
                selected.append(community)
                break
        else:
            print(f"Warning: '{arg}' is not a valid community. Skipping.")

    if len(selected) < 2:
        print("Error: You must select at least 2 communities.")
        print(f"Available communities: {', '.join(AVAILABLE_COMMUNITIES)}")
        sys.exit(1)

    return selected


def generate_mock_projects(communities: list[str]) -> list[dict[str, Any]]:
    """Generate 6 mock project ideas based on selected communities."""
    projects = []

    # Project templates that combine different community skills
    templates = [
        {
            "title_template": "AI-Powered {comm1} Analytics Dashboard",
            "desc_template": "Build a dashboard that uses {comm1} for data processing and {comm2} for the frontend interface.",
        },
        {
            "title_template": "{comm1} and {comm2} Collaboration Platform",
            "desc_template": "Create a platform that facilitates collaboration between {comm1} and {comm2} teams.",
        },
        {
            "title_template": "Secure {comm1} Application with {comm2} Integration",
            "desc_template": "Develop a secure application using {comm1} principles with {comm2} integration.",
        },
        {
            "title_template": "Automated {comm1} Pipeline with {comm2} Monitoring",
            "desc_template": "Implement an automated pipeline for {comm1} with monitoring using {comm2} tools.",
        },
        {
            "title_template": "{comm1} Data Visualization with {comm2} UX",
            "desc_template": "Create interactive data visualizations using {comm1} with {comm2} user experience design.",
        },
        {
            "title_template": "API-First {comm1} Solution with {comm2} Security",
            "desc_template": "Build an API-first solution for {comm1} with {comm2} security best practices.",
        },
    ]

    for _i, template in enumerate(templates):
        # Randomly select 2 different communities for each project
        selected_comms = random.sample(communities, min(2, len(communities)))

        # Create title and slug
        title = template["title_template"].format(
            comm1=selected_comms[0],
            comm2=selected_comms[1] if len(selected_comms) > 1 else selected_comms[0],
        )

        # Create a shorter slug for wheel display
        # Remove common prefixes and keep it concise
        slug = title
        # Remove common prefixes
        for prefix in ["AI-Powered ", "Secure ", "Automated ", "API-First "]:
            if slug.startswith(prefix):
                slug = slug[len(prefix) :]
                break

        # Truncate if still too long
        if len(slug) > 30:
            words = slug.split()
            slug = ""
            for word in words:
                if len(slug + " " + word) <= 30:
                    slug = slug + " " + word if slug else word
                else:
                    slug += "..."
                    break

        project = {
            "title": title,
            "slug": slug.strip(),
            "description": template["desc_template"].format(
                comm1=selected_comms[0],
                comm2=selected_comms[1]
                if len(selected_comms) > 1
                else selected_comms[0],
            ),
            "involved_communities": selected_comms,
            "team_size": f"1 {selected_comms[0]}, 1 {selected_comms[1]}"
            if len(selected_comms) > 1
            else f"2 {selected_comms[0]}",
        }
        projects.append(project)

    return projects


def display_projects(projects: list[dict[str, Any]]) -> None:
    """Display generated projects in console."""
    print("\n" + "=" * 60)
    print("GENERATED HACKATHON PROJECT IDEAS")
    print("=" * 60)

    for i, project in enumerate(projects, 1):
        print(f"\n{i}. {project['title']}")
        print(f"   Wheel display: {project['slug']}")
        print(f"   Description: {project['description']}")
        print(f"   Communities: {', '.join(project['involved_communities'])}")
        print(f"   Team Size: {project['team_size']}")

    print("\n" + "=" * 60)
    print("Launching spinning wheel to select a project...")
    print("=" * 60 + "\n")


def run_spinning_wheel(projects: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Run the Pygame spinning wheel with project titles."""
    # Extract slugs for the wheel (shorter display)
    options = [project["slug"] for project in projects]

    # Also keep mapping from slug to full project
    slug_to_project = {project["slug"]: project for project in projects}

    # Pygame configuration
    WIDTH, HEIGHT = 800, 800
    FPS = 60
    FRICTION = 0.992
    MIN_SPEED = 0.1

    # Colors for wheel slices
    COLORS = [
        (231, 76, 60),  # Red
        (52, 152, 219),  # Blue
        (155, 89, 182),  # Purple
        (46, 204, 113),  # Green
        (241, 196, 15),  # Yellow
        (230, 126, 34),  # Orange
        (52, 73, 94),  # Dark blue
        (26, 188, 156),  # Teal
    ]

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hackathon Roulette - Project Selector")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    small_font = pygame.font.SysFont("Arial", 14, bold=True)
    winner_font = pygame.font.SysFont("Arial", 36, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 24, bold=True)

    def wrap_text(text: str, max_width: float) -> list[str]:
        """Wrap text to fit within max_width pixels."""
        words = text.split()
        lines: list[str] = []
        current_line: list[str] = []

        for word in words:
            # Test if adding this word would exceed max width
            test_line = " ".join([*current_line, word])
            test_surface = font.render(test_line, True, (255, 255, 255))
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        # If text is still too long, truncate and add ellipsis
        if len(lines) > 2:
            lines = lines[:2]
            if len(lines[1]) > 3:
                lines[1] = lines[1][:10] + "..."

        return lines

    def draw_wheel(surface: pygame.Surface, angle: float) -> None:
        center_x, center_y = float(WIDTH // 2), float(HEIGHT // 2)
        radius = 300
        num_options = len(options)
        slice_angle = 360 / num_options
        max_text_width = radius * 0.8  # Maximum width for text in slice

        for i in range(num_options):
            start_deg = angle + (i * slice_angle)
            end_deg = angle + ((i + 1) * slice_angle)

            # Draw the colored slice
            points = [(center_x, center_y)]
            start_rad = math.radians(start_deg)
            end_rad = math.radians(end_deg)
            steps = int(slice_angle) if int(slice_angle) > 2 else 2

            for step in range(steps + 1):
                theta = start_rad + (end_rad - start_rad) * (step / steps)
                px = center_x + radius * math.cos(theta)
                py = center_y - radius * math.sin(theta)
                points.append((px, py))

            pygame.draw.polygon(surface, COLORS[i % len(COLORS)], points)

            # Draw text label with wrapping
            mid_angle = math.radians(start_deg + slice_angle / 2)
            text_distance = radius * 0.5

            # Wrap the text
            wrapped_lines = wrap_text(options[i], max_text_width)

            # Draw each line of text
            line_height = 20
            total_height = len(wrapped_lines) * line_height
            start_y_offset = -total_height / 2 + line_height / 2

            for line_idx, line in enumerate(wrapped_lines):
                # Calculate position for this line
                line_y_offset = start_y_offset + line_idx * line_height
                text_x = center_x + text_distance * math.cos(mid_angle)
                text_y = center_y - text_distance * math.sin(mid_angle) + line_y_offset

                # Create and rotate text surface
                if len(wrapped_lines) > 1 and line_idx > 0:
                    text_surf = small_font.render(line, True, (255, 255, 255))
                else:
                    text_surf = font.render(line, True, (255, 255, 255))

                # Rotate text to align with slice
                rotation_angle = -(start_deg + slice_angle / 2)
                text_surf = pygame.transform.rotate(text_surf, rotation_angle)
                text_rect = text_surf.get_rect(center=(text_x, text_y))
                surface.blit(text_surf, text_rect)

    def get_winner(angle: float) -> tuple[str, int]:
        num_options = len(options)
        slice_angle = 360 / num_options
        normalized_angle = (-angle) % 360
        winner_index = int(normalized_angle / slice_angle)
        return options[winner_index], winner_index

    # Main game loop
    current_angle = 0.0
    speed = 0.0
    spinning = False
    winner_text = ""
    show_details = False
    selected_project = None

    run = True
    while run:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif not spinning:
                    if event.key == pygame.K_SPACE:
                        speed = random.uniform(15, 25)
                        spinning = True
                        winner_text = ""
                        show_details = False
                    elif event.key == pygame.K_d and winner_text:
                        show_details = not show_details

        # Update physics
        if spinning:
            current_angle += speed
            speed *= FRICTION

            if speed < MIN_SPEED:
                speed = 0
                spinning = False
                winner_slug, _winner_index = get_winner(current_angle)
                winner_text = winner_slug
                selected_project = slug_to_project[winner_slug]

        # Draw wheel
        draw_wheel(screen, current_angle)

        # Draw pointer
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            [
                (WIDTH // 2 + 310, HEIGHT // 2),
                (WIDTH // 2 + 340, HEIGHT // 2 - 20),
                (WIDTH // 2 + 340, HEIGHT // 2 + 20),
            ],
        )

        # Draw instructions or winner
        if winner_text:
            res = winner_font.render(f"SELECTED: {winner_text}", True, (255, 255, 0))
            screen.blit(res, (WIDTH // 2 - res.get_width() // 2, 50))

            if show_details and selected_project:
                project = selected_project
                y_offset = 100

                # Draw full title
                title_surf = instruction_font.render(
                    f"Full Title: {project['title']}", True, (255, 255, 200)
                )
                screen.blit(
                    title_surf,
                    (WIDTH // 2 - title_surf.get_width() // 2, y_offset),
                )

                # Draw project details
                desc_lines = []
                words = project["description"].split()
                line = ""
                for word in words:
                    if len(line + " " + word) < 60:
                        line += " " + word if line else word
                    else:
                        desc_lines.append(line)
                        line = word
                if line:
                    desc_lines.append(line)

                for i, line in enumerate(desc_lines):
                    desc_surf = instruction_font.render(line, True, (200, 200, 200))
                    screen.blit(
                        desc_surf,
                        (
                            WIDTH // 2 - desc_surf.get_width() // 2,
                            y_offset + 40 + i * 30,
                        ),
                    )

                comm_surf = instruction_font.render(
                    f"Communities: {', '.join(project['involved_communities'])}",
                    True,
                    (200, 200, 200),
                )
                screen.blit(
                    comm_surf,
                    (
                        WIDTH // 2 - comm_surf.get_width() // 2,
                        y_offset + 40 + len(desc_lines) * 30 + 10,
                    ),
                )

                team_surf = instruction_font.render(
                    f"Team Size: {project['team_size']}", True, (200, 200, 200)
                )
                screen.blit(
                    team_surf,
                    (
                        WIDTH // 2 - team_surf.get_width() // 2,
                        y_offset + 40 + len(desc_lines) * 30 + 40,
                    ),
                )

                detail_instr = instruction_font.render(
                    "Press D to hide details | ESC to exit", True, (150, 150, 150)
                )
                screen.blit(
                    detail_instr,
                    (WIDTH // 2 - detail_instr.get_width() // 2, HEIGHT - 80),
                )
                screen.blit(
                    title_surf,
                    (WIDTH // 2 - title_surf.get_width() // 2, y_offset),
                )

                # Draw project details
                desc_lines = []
                words = project["description"].split()
                line = ""
                for word in words:
                    if len(line + " " + word) < 60:
                        line += " " + word if line else word
                    else:
                        desc_lines.append(line)
                        line = word
                if line:
                    desc_lines.append(line)

                for i, line in enumerate(desc_lines):
                    desc_surf = instruction_font.render(line, True, (200, 200, 200))
                    screen.blit(
                        desc_surf,
                        (
                            WIDTH // 2 - desc_surf.get_width() // 2,
                            y_offset + 40 + i * 30,
                        ),
                    )

                comm_surf = instruction_font.render(
                    f"Communities: {', '.join(project['involved_communities'])}",
                    True,
                    (200, 200, 200),
                )
                screen.blit(
                    comm_surf,
                    (
                        WIDTH // 2 - comm_surf.get_width() // 2,
                        y_offset + 40 + len(desc_lines) * 30 + 10,
                    ),
                )

                team_surf = instruction_font.render(
                    f"Team Size: {project['team_size']}", True, (200, 200, 200)
                )
                screen.blit(
                    team_surf,
                    (
                        WIDTH // 2 - team_surf.get_width() // 2,
                        y_offset + 40 + len(desc_lines) * 30 + 40,
                    ),
                )

                detail_instr = instruction_font.render(
                    "Press D to hide details | ESC to exit", True, (150, 150, 150)
                )
                screen.blit(
                    detail_instr,
                    (WIDTH // 2 - detail_instr.get_width() // 2, HEIGHT - 80),
                )
            else:
                instr = instruction_font.render(
                    "Press SPACE to spin again | D for details | ESC to exit",
                    True,
                    (200, 200, 200),
                )
                screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, HEIGHT - 80))
        elif not spinning:
            instr = instruction_font.render(
                "Press SPACE to spin the wheel | ESC to exit", True, (200, 200, 200)
            )
            screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

    # Return the selected project
    return selected_project


def main() -> None:
    """Main entry point for the application."""
    if len(sys.argv) < 2:
        print("Hackathon Roulette - Cross-Community Project Generator")
        print("=" * 60)
        print("\nUsage: uv run app.py <community1> <community2> ...")
        print("\nAvailable communities:")
        for community in AVAILABLE_COMMUNITIES:
            print(f"  - {community}")
        print("\nExamples:")
        print("  uv run app.py Python Frontend")
        print("  uv run app.py Python API DevOps")
        print("  uv run app.py all")
        print("\nNote: You need at least 2 communities.")
        sys.exit(1)

    # Parse communities from command line
    communities = parse_communities(sys.argv[1:])
    print(f"Selected communities: {', '.join(communities)}")

    # Generate mock projects
    projects = generate_mock_projects(communities)

    # Display projects in console
    display_projects(projects)

    # Run spinning wheel
    selected_project = run_spinning_wheel(projects)

    # Display final result
    if selected_project:
        print("\n" + "=" * 60)
        print("SELECTED PROJECT FOR YOUR HACKATHON!")
        print("=" * 60)
        print(f"\nTitle: {selected_project['title']}")
        print(f"Description: {selected_project['description']}")
        print(f"Communities: {', '.join(selected_project['involved_communities'])}")
        print(f"Team Size: {selected_project['team_size']}")
        print("\n" + "=" * 60)
        print("Happy hacking! 🚀")
        print("=" * 60)


if __name__ == "__main__":
    main()
