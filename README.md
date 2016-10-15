# Wazir

## Features

All of these are todos unless crossed out.

- filter by:
  - recency
  - whether or not the game was rated
  - whether or not the opponent was human
- given a game-prefix, show:
  - ~~number of games~~
  - ~~responses (with percentages and counts)~~
  - link to games
- ~~walk up and down a game tree~~

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
