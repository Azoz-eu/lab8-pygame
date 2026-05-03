small simulation about multiple squares on screen, continuous movement, visible interaction rules

randomize each square's size, start position (inside bounds), initial velocity direction and magnitude, and color

add believable motion with tiny randomness at each update step, apply small jitter to velocity.
without it, the movement can look too mechanical. with too much jitter, motion looks noisy and unstable.

smaller squares flee larger ones
- compare each square against others
- if another square is larger and nearby, move away from it

tie speed to size
- smaller squares are faster
- larger squares are slower

added frame rate counter.


what to add next:
bigger squares chase smaller ones
- compare each square against others
- if another square is smaller and nearby, chase towards it