As far as my tests can tell, the capstone.py program contains all of the features outlined within the assignment. 
To provide a bit of context on how I built it out:
    - In an effor to cut down on scrolling through numerous lines of code, I tried to consolidate a lot of generic
    processes into the index.py and utility.py files. If you so desire to look through my code, it wouldn't be a bad idea
    to start with those two files real quick so you have some reference to what's going on whenever those functions are called.
    - The first third of what you will likely see are just menus - particularly what a Manager would be able to interact with.
    To that end, there are two main menu functions, user_terminal() - anything relating to users, and compass() - competencies & 
    assessments. From there, it's what I considered to be all the baseline functions, with the more 'process' heavy functions 
    below them.
    - Regarding CSV files: you can find the option to import assessment results via CSV through the compass() menu. Just keep 
    following 'Assessment' related prompts until you see the correct option. The two files I chose to provide export functionality
    to were the individual User Competency and Assessment Reports, as that function is then accessible by both managers as well as
    generic users. I do believe I made the export function general enough that it wouldn't be all that complicated to support the 
    larger report for a given competency, but my brain died hours ago, so I kept it simple. *** When entering any file name, just
    don't forget to tag ".csv" on to the end.

And honestly, that's all I can really think about at the moment. To help test the code, I made a default generic manager that you 
can also use to login and interact with the Competency Database. From there, feel free to play around and see if you can break anything.
As exhausted as I am, I've no doubt I probably missed something somewhere!

Login: mainmanager@dev.com
Password: 'wasd'

Cheers!
