# Overview
This project is a single-file pygame simulation where squares move, bounce, flee larger neighbors, chase smaller neighbors, and display FPS on screen.

The code in `main.py` is already functional and reasonably organized, but it still has a few beginner-friendly refactoring opportunities:
- The `Square.update()` method mixes jitter, interaction math, speed control, and boundary handling in one long block.
- The flee and chase calculations repeat very similar distance and vector logic.
- Speed normalization uses two branches that do almost the same thing.
- Some variable names and inline comments can be made more explicit for first-year readers.

This plan keeps behavior the same and focuses on small, safe improvements.

# Refactoring Goals
- Make `Square.update()` easier to read by splitting it into small helper methods.
- Reduce duplicated math and repeated scaling logic.
- Improve naming so the movement rules are easier to follow.
- Keep the current chase, flee, jitter, bounce, and FPS behavior unchanged.
- Ensure the final refactored code uses short inline comments that explain what changed and why.

# Step-by-Step Refactoring Plan
## Step 1: Extract the interaction math into small helper methods
What to do:
- Move the flee calculation into a helper such as `_compute_flee_vector(all_squares)`.
- Move the chase calculation into a helper such as `_compute_chase_vector(all_squares)`.
- Return `(x, y)` force components from each helper and add them in `Square.update()`.

Why it helps:
- This separates “calculate influence” from “apply movement.”
- Beginners can understand one rule at a time instead of reading a long loop.

Inline comment instruction for final code:
- Add short comments in the helpers explaining that one computes escape force and the other computes pursuit force.

## Step 2: Extract boundary correction into a bounce helper
What to do:
- Move the left/right and top/bottom wall checks into a helper such as `_bounce_within_bounds()`.
- Keep the same clamping and velocity inversion behavior.

Why it helps:
- The main update method becomes shorter and focuses on motion logic.
- Boundary rules become easier to find and test.

Inline comment instruction for final code:
- Add a concise comment in the helper explaining that clamping plus velocity inversion keeps squares inside the screen and creates bounce behavior.

## Step 3: Simplify the speed normalization branch
What to do:
- Replace the two almost identical speed-scaling branches with one clear block.
- Keep the same effect: if the current speed differs from the target speed, scale `vx` and `vy` once.

Why it helps:
- Removes repeated code and makes the size-based speed rule easier to spot.
- Reduces the chance of one branch being changed while the other is forgotten.

Inline comment instruction for final code:
- Add one short inline comment explaining that the scaling keeps speed aligned with the size-based target.

## Step 4: Improve coordinate variable names
What to do:
- Rename the center-point variables to something more explicit, such as `self_center_x_pos` and `self_center_y_pos`.
- Keep the names simple and consistent with the existing style.

Why it helps:
- Clear names make the distance math easier to understand.
- New readers can see that these values are positions measured from the center of each square.

Inline comment instruction for final code:
- Add a short comment near the center-point calculation explaining that the values are used for distance-based interaction math.

## Step 5: Clarify the initialization comments
What to do:
- Keep the random setup the same, but tighten comments around size, position, velocity, and color initialization.
- Make the comments describe why the constraints exist, not just what the assignment does.

Why it helps:
- Comments become more useful for students learning why bounds matter.
- This keeps the constructor readable without changing behavior.

Inline comment instruction for final code:
- Use concise comments that explain the purpose of each initialization rule, such as staying inside the screen or keeping speed in a safe range.

## Step 6: Verify behavior after each small change
What to do:
- After each step, run `python main.py` and confirm:
- Squares still move and bounce.
- Flee and chase behavior still work.
- FPS text still renders.
- No new errors appear.

Why it helps:
- Incremental testing catches regressions early.
- This is the safest way to refactor beginner code.

Inline comment instruction for final code:
- No special runtime comment is needed for this step, but keep any comments added during refactoring short and relevant.

# Final Output Requirements (Mandatory)
When this plan is executed, the output must:
- Contain only the refactored code.
- Include concise inline comments explaining what changed and why it improves readability, maintainability, or correctness.
- Preserve the current gameplay behavior, including chase, flee, jitter, speed normalization, bouncing, and FPS display.
- Avoid advanced design patterns or heavy abstractions.

# Key Concepts for Students
- Separation of concerns: split one large method into focused helper methods.
- DRY: do not repeat the same math or scaling logic in multiple places.
- Behavioral preservation: change the structure without changing what the program does.
- Naming clarity: choose variable names that describe the data clearly.
- Incremental testing: check behavior after each small edit.

# Safety Notes
- Do not change gameplay constants unless you are intentionally testing a different feel.
- Keep each refactoring step small so bugs are easy to trace.
- If behavior changes unexpectedly, undo only the last step and test again.
- Keep inline comments short; too many comments can make the code harder to read.