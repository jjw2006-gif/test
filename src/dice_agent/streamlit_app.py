"""Streamlit user interface for the dice agent.

Run the app with::

    streamlit run src/dice_agent/streamlit_app.py

The UI exposes a single button to roll a six‑sided dice and displays whether
the resulting number is prime.
"""

from __future__ import annotations

import streamlit as st

from .agent import is_prime, roll_dice


def main() -> None:
    """Render the interactive Streamlit application."""

    # Page title and short description so users know what to expect.
    st.title("Dice Roller")
    st.write(
        "Click the button below to roll a six-sided dice. We'll also tell you"
        " if the number is prime."
    )

    # The button returns True only when clicked in the current rerun.  When
    # this happens we use the LangChain tools to roll the dice and check
    # primality.
    if st.button("Roll the dice"):
        # ``roll_dice`` expects a string input but ignores the value.  Passing
        # an empty string keeps the interface simple.
        value = roll_dice.invoke("")
        st.write(f"The dice shows **{value}**.")

        # ``is_prime`` also expects string input.  Cast the integer before
        # invoking the tool.
        prime = is_prime.invoke(str(value))
        if prime:
            st.success("It's a prime number!")
        else:
            st.warning("It's not a prime number.")


if __name__ == "__main__":  # pragma: no cover - UI entry point
    main()

