# Readme
repo for une ai competition

## Welcome to the Casino my friend

This is a repo for my attempt at the une ai competition that was held from Dec 2024 -
Jan 2025.

### What it does

The idea for this project is to take in multiple datastreams for 100's of assests,
do some math on their raw data and calculate the risk it should take in the market.
That's the theory... this idea would take quite some time to build, so in practice...

Currently this project takes real time data from only the bitcoin asset and makes
simple calculations on its raw data to determine if it should buy or sell depending 
on the current position of the users account (bybit) and the output it calculates.

To get this project from where it is to it's final form will be a project to completely 
finish at a later date. As of the 11th of January, 2025 the first version with bare minimum
of features is ready to be used.

When I first started this project, the idea was so simple in my head... I started writting
the first few modules, the database, the neural net, even the features... then the scope
creep kicked in and all of a sudden it turned into some kind of monster I lost control
of towards the end just get all the basic functionality in. I hope to remedy the
poor choice of design you may see scatter throughout the project. This project taught
me more about what not to do instead of what to do, learning is learning I guess.

### How to run

- Open up a terminal
- Navigate to a directory you are happy cloning the project too
- Type or copy & paste everything on the below line 
https://github.com/Mokoto-K/une-ai-competition.git une-ai-competition-winning-entry
- After the repo is cloned successfully type: python main.py or python3 main.py
- To run the real account function you will have to enter the:
api key = 
secret = 
Don't worry it's just a test account for the competition, these keys arn't important.
- Welcome to losing your retirement... house... family, everything really
You'll have nothing, and you'll be happy.

### Extra Information
I'll add more to this as I think of things

- The simulation is just the ai predicting over the last x days (set to 100 at the 
time of writting) in ideal conditions and isn't to be taken serious, it's more for an 
example too see what it does as if you are waiting for it to make decisions on the 
real time market, you would have to check daily at the longest and maybe 30 - 60
minutes at the shortest to see anything happening.

- The change strategy command just changes which database file the nn trains on.
So High risk is the one minute data stream, so technically it could be buying and 
selling every other minute. The low risk option is pointing the nn to train on 
the daily data stream which updates at 00:00 UTC each day.

- 

<hr>

### Programming log

<hr>

#### 5th of January, 2025
In an ideal world I would have more time to implement my idea(s) for this 
competition, I have three but I think that only one is achievable in two weeks
with my current knowledge of neural networks.

1. Traffic light control  - An AI that monitors traffic and changes lights
depending on conditions and volume of traffic/accidents/emergency vechiles, etc
2. Journaling app - A bit plain but essentially an everyday journal that would
train itself from your entries and recommend things or remind you or things you
keep mentioning and perhaps not doing, or sense when you are happy or sad and
help adjust, I don't know, seems complicated and a little intrusive, but that
is what a journal is i guess.
3. Financial management system - An AI that manages and adjusts your assets/
trading accounts/whatever by monitoring market conditions and implementing either
a predefined strategy or one it learns by itself. You could select how much
risk you are willing to take on and it can adjust for that in terms of different
assets, timeframes, etc. A literal self managed super fund essentially.

All three ideas are pretty much the same thing. Get realtime data, make a decision
on that data, run through logic to execute whatever aligns with that decision.
I think the financial management system is the easiest to implement at my current
skill level, as its basically just binary classification. A journaling app using 
NLP is something I haven't tried yet so I might be too tight on time and my 
favourite idea (traffic light control) seems kind of impossible as i'm not sure
if I can get access to real time traffic data and even if I could I would have 
to set up a model with a bunch of parameters and that seems like a daunting task.
So I think it's the financial management system for now.

#### 6th of January, 2025
Built alot today, made some decision, not happy with all of them, very happy with
how others turned out. Project is mostly complete in at this point, just have to
decide if im going to connect it to an actual exchange to trade for the competition 
or create a simulation to trade off the last couple hundred days with a fake balance
but real data... decide tomorrow, probably implement both and make a settings menu
or something. I'm tired, alot of messy code to clean up tomorrow, alot of converting
to classes i think.

#### 7th of January, 2025
Today I want to finish all main functionality off and have everything that has 
been made so far, presentable. I want to change the features module into a class 
so that it can run multiple csv, I could just implement a DB that stores it all 
but that might take longer and i'd ultimately still have to incorporate some way 
of dealing with each individual asset class, so this is good ground work to be built
on top of later. I'll try remember to check in as the day goes....

#### 8th of January, 2025
Today was rough, I rewrote the api to exchange like 4 different times due to getting
something different wrong each time... the auth killed me... so I thought, turned 
out bybit (the exchange we are going to use) handles paramters and urls a bit 
different to what I thought.

At a point of the project where all the pieces are there, it's about assembling
them in the right order or fashion.... haven't quite come to the conclusion on 
how that should be yet.

Maybe more tomorrow, or maybe some C while I mull over the decisions.

:wq

#### 9th of January, 2025
Mostly cleaning up some file and thinking of how to progress this from a series
of pieces into a program that gels... no good solutions so far beside the basic 
and obvious ones, may be doomed to be a boring piece of software tbh haha. Still 
lots to do like extra features for the nn to train on, i still haven't scaled the
data going in.... I know i know, also need to implement a test account and see if 
that is a feasable path to go down for the competition instead of me opening a 
real money account and providing acct details.... which im not going to do, so 
yeah. I'll figure it out in the coming downs, hopefully, long list of todo all 
through out the program to do.
:wq

#### 10th of January, 2025
Accomplished very little today, got stuck on alot of small tasks with logging trades,
environment variables, laoding api keys, etc. I am really unhappy with main.py right
now, it is an absolute mess! Currently the program is broken but im so tired, i'll be 
back tomorrow.:wq

#### 11th of January, 2025
Finally all main and basic functionality is in and working. Now I have to tune the 
nn, fix the 100 todos and then I can optimize the program. I don't know how much
more I get done on this project before the due date, and i'm really not happy in 
how it turned out, this became less about the ai and more about just getting all
the pieces for a system to make trades and monitor those trades... kind of a nightmare
to be honest. Back to C for a little bit to have a break from python!


