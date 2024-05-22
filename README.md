# Typewell | Phase-3 Project
Typewell is a **competetive typing-based game** located entirely in the command prompt. The purpose of the game is to type a given sentence **as quickly and as accurately as possible**. Users tests are saved to their unique profile, and are compared to other users in the leaderboard.

## Setup:
Install termcolor, then run the script from the shell:

```
> python3 -m pip install --upgrade termcolor
> pipenv shell  
> python lib/cli.py
```

## Features:
From the main menu, there are five options: **Test, Leaderboard, Profile, Logout, and Quit**.  

![testexample-ezgif com-video-to-gif-converter](https://github.com/PRSheridan/phase-3-project/assets/142257140/3ddd47a1-eafe-4d01-922a-f4bbda3f3db3)

**1. Test** gives the options to begin a new test, view a list of all possible sentences, and add new sentences to that list. Beginning a new test will give the user a countdown, then prompt them with a random sentence to copy. After entering an answer, the user will be shown their speed, accuracy, and words-per-minute (WPM). The value is calculated by the following formula:
(((string_length/5)/(test_time/60))*(accuracy/100))  


![menuexample-ezgif com-video-to-gif-converter](https://github.com/PRSheridan/phase-3-project/assets/142257140/34344656-1cd6-4a41-a991-bdc39379d3fb)

**2. Leaderboard** shows all registered users average scores and sorts them from best to worst. New users will have aan average WPM of zero until their first test is completed.  

**3. Profile** shows the user all of their averaged statistics, and the amount of tests they have taken. There are three options within the Profile page: Change username, Reset statistics, and Delete profile. When statistics are reset, or a profile is deleted, there is no way to recover the lost data.  

**0. Logout** returns the user to the login screen and prompts them to login or create a new profile.  

**00. Quit** closes the application.  

**Admin:** Allows an admin account to make changes to any user or test instance. This includes creating, viewing, editing, and deleting for all instances. Only accessible to accounts with the admin role which can be created by preceding the username with "adm_". 

## Future plans:
- Make the application executable.
- Create a more visually interesting testing format (show errors in real time).

Contact Me:  
[PRSheridan (github.com)](https://github.com/PRSheridan)  
[philrsheridan@gmail.com](mailto:philrsheridan@gmail.com)
