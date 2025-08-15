"""Dice rolling agent package.

This package exposes the core tools used throughout the project.  Importing
from :mod:`dice_agent` gives convenient access to the helper functions without
having to dive into the submodules.
"""

from .agent import create_agent, roll_dice, is_prime

# Re-export the public functions so ``from dice_agent import create_agent``
# works as expected.
__all__ = ["create_agent", "roll_dice", "is_prime"]
