# Wazir

## Features

All of these are todos unless crossed out.

- ~~Interactively explore a game database by walking up and down the "game tree."~~
  - At any node, show:
    - ~~Responses (with percentages and counts)~~
    - Links to games
- Filter by:
  - Recency
  - Whether or not the game was rated
  - Whether or not the opponent was human
  - Time control

## Input language

    [X] (algebraic move) = go down
    [X] (nothing)        = go down to most common move
    [X] 0                = go down to most common move
    [X] 1                = go down to most second common move
    [X] .                = go up one
    [ ] ...              = go up three
    [X] /                = go to root
    [ ] h                = toggle human
    [ ] r                = toggle rated
    [ ] 3d               = recency filter at 3 days
    [ ] 7m
    [ ] 2y
    [ ] g                = show games (paginated)
    [ ] n                = next page of games
    [ ] 4n

## Other todos

- Figure out what's wrong with `size`
