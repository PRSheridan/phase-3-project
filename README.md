# Typewell | Phase-3 Project
Typewell is a **competetive typing-based game** located entirely in the command prompt. The purpose of the game is to type a given sentence **as quickly and as accurately as possible**. Users tests are saved to their unique profile, and are compared to other users in the leaderboard.

https://github.com/PRSheridan/phase-3-project/assets/142257140/c296d3dd-6e5f-4f1e-8926-d0e7de4d7137

## Setup:
Install termcolor, then run the script from the shell:

```
> python3 -m pip install --upgrade termcolor
> pipenv shell  
> python lib/cli.py
```

## Features:
From the main menu, there are five options: **Test, Leaderboard, Profile, Logout, and Quit**.  

**1. Test** gives the options to begin a new test, view a list of all possible sentences, and add new sentences to that list. Beginning a new test will give the user a countdown, then prompt them with a random sentence to copy. After entering an answer, the user will be shown their speed, accuracy, and score. The score is calculated by dividing the accuracy by the time, then given a weight based on the length of the sentence.  

**2. Leaderboard** shows all registered users average scores and sorts them from best to worst. New users will have a score of zero until their first test is completed.  

**3. Profile** shows the user all of their averaged statistics, and the amount of tests they have taken. There are three options within the Profile page: Change username, Reset statistics, and Delete profile. When statistics are reset, or a profile is deleted, there is no way to recover the lost data.  

**0. Logout** returns the user to the login screen and prompts them to login or create a new profile.  

**00. Quit** closes the application.  

## Future plans:
- Make the application executable.
- Create a more visually interesting testing format (show errors in real time).

Contact Me:  
[PRSheridan (github.com)](https://github.com/PRSheridan)  
[philrsheridan@gmail.com](mailto:philrsheridan@gmail.com)
