# Capture the forge

# Requirements

- A big number of user should be able to register
- An admin should be able to add and delete puzzles dynamically
- The users should be able to solve a puzzle, upload the answer and win points
- There should be a scoreboard for the users
- The users should be able to form teams for the team scoreboard
- Teams should be able to mersh

# Webpages

## home
It's the home page, nothing more nothing less

## login and register
In this pages the user enter their credentials, the login
returns a authentication cookie and redirects to /play
to start puzzling, meanwhile register just redirects to
/login once done entering the credentials.

## play
This page, once the user request it, makes the server get
the list of puzzles and generates a website displaying them.

## Scoreboard
This page, once the user request it, makes the server get
the list of users in order of score and then renders a website
displaying them.

# Code's objects

## Puzzles

A puzzle is a singular problem given to the user, every puzzle contains

- Name
- Description
- Link
- Files: path to all the files required to solve the puzzle
- Difficulty
- Flag's 256Hash

but that is a _puzzle_ instance, a _puzzles_ object is double linked list, 
the list of puzzles should be displayed in order fast, for the website's performance.
But also should allow for fast insertion and deletion, given that the number of
puzzles is not that big, the slowed search performance should not be an issue.


## User

An user has the following properties:

- Username
- Password's SHA256 hash
- Team
- Score
- Problems solved

## Scoreboard

This is a tree ordered by user score, this allows for fast insertion and deletion
as for fast traversing. Perfect for the scoreboard, given the potentially big number
of users, changing the position of a user in the board should be quite fast.
