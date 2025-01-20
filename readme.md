# Readme

# Welcome to the Casino my friend

This is a repo for my attempt at the une ai competition that was held from Dec 2024 -
Jan 2025.

## What it does

The idea for this project is to take in multiple datastreams for 100's of assests,
do some math on their raw data and calculate the risk it should take in the market.
That's the theory... this idea would take quite some time to build, so in practice...

Currently this project takes real time data from only the bitcoin asset and uses
a neural network on some engineered features to determine if it should buy or sell depending 
on the current position of the users account (bybit) and the output it calculates.

When I started this project, the idea was so simple in my head... I started writting
the first few modules, the database, the neural net, the features... then the scope
creep kicked in and all of a sudden it turned into some kind of mash of duct tape
and rubber bands in an attempt to just get all the basic functionality in. I hope to remedy some of the
poor design choice I choose to use along the way. This project taught
me more about what not to do instead of what to do, but learning is learning.
<br>
UPDATE: Feels less like rubber bands and duct tape just 4 days later, 
still structual problems that can be fixed with a little more time and refactoring
<br>
UPDATE: Feels like the greatest ball of duct taped rubber bands to ever exist 2 days later...
<br>
UPDATE: Refactored some core elements.... everything is under control.
<br>

## How it does what it does

Initially a user is asked for credentials to trade i.e an api key and the secret, if they
have already provided one, the program will automatically read the .env file, otherwise they will have 
to fill out the api information. The program will then read the user log file (or create one if one with default values if it doesn't exist) 
for the strategy writtin within and send that to the database. The strategy is a timeframe that 
the market trades on i.e 1minute, 5minute, 1hour, Day, etc. The database then either creates a 
file for that strategy/timeframe or reads it in if it already exists. The database compares the last
record it has to the realtime market and if the time stamps don't match, then it downloads
the missing data to complete its records. 

This database file is then used to create a set of features for the neural net to 
train on. Once trained the program then executes a prediction on the current market 
data and returns either a buy or sell event. Depending on if the event agrees or 
disagrees with what the users account is currently doing, it will then either 
1. Do nothing (agrees)
2. Closes trade and opens another on the opposide side of the market(disagrees)
3. Or opens a trade as there is currently no trade active.

All of this is controlled by the program and the neural net, the user doesn't have to 
do anything. The user can choose to change which ever strategy is being used to trade
though, currently only high and low risk straties exist. Each has subtle differences. 
Low risk looks at the daily time frame and can really only make one trade a day, it 
also uses a smaller percentage of the users account per trade. High risk looks at 
the 1minute time frame... yes thats right, in glorious conditions it could technically
execute 1440 trades a day... at a higher percentage of the users account. In the future
I would probably have the NN control which strategy it's using depending on the volitility
and past performance of the market. 

UPDATE: AUTOMATION IS NOW ACTIVE<br>
You can also select to turn on automation, this will have the NN update the database,
retrain and make a new prediction for each time period that passes that matches the 
current strategy... I know, sounds confusing, but it's simple. If you current have high
risk strategy selected, then that corresponds to make a decision each minute, meaning 
the NN will also retrain and make a decision each minute, this is true for any other 
time frame. As of writting this only low and high risk with time frames of 1 day and 1 minute
exist. To exit automation mode all you have to do is hit the enter key. 

That's it, the project is far from perfect, there are alot of problems to fix, modules 
to refactor and features to add. Feedback is very welcome, i'm new to developing programs, 
using machine learning... computer science in general, the whole reason I entered this 
competition was to see where I was at after one year of studying. Enjoy. 
<br>
UPDATE: Extra features like force closing a position & reviewing current position 
are now available.
<br>

## How to run

- Open up a terminal
- Navigate to a directory you are happy cloning the project too
- Type or copy & paste everything on the below line <br>
git clone https://github.com/Mokoto-K/une-ai-competition.git une-ai-competition-winning-entry
- After the repo is cloned successfully you'll want to set up a virtual environment for python, you can do this in the terminal 
by typing:<br> python -m venv .venv <br>
you may need to use python3 instead of python. f you have any trouble running the python command, 
visit python.org for more information on how to update your python distribution on your selected system.
- To activate the environment you then need to run <br>
Linux/Mac: source .venv/bin/activate <br>
Windows(depends on your shell):   .\\.venv\Scripts\activate.bat <br>
Apparently this doesn't work for vscode if you're into that kind of thing...
- Next you will need to install the requirements, you can do this with one of the following
commands. <br>
pip install -r requirements.txt
pip3 install -r requirements.txt
- Now just run python main.py or python3 main.py
- To run the real account function (which is running on testnet) you will have to enter an api key and secret the first time when are prompted, below I have provided one for the purpose of the competition:<br>
api key = ZJvzXJ4WEpphUlVTiw<br>
secret = NuvY5NftCiBlZuoWPmi7ozyxI2I8lugrY4vx<br>
Don't worry it's just a test account for the competition, these keys arn't important.
There is one risk with sharing an api for this contest and that is the program will 
probably exhibit some weird behaviour if multiple people start running it with the 
same key. There is no fix for this as multiple people should not have your api key 
and secret. This is a known risk that is necessary for the contest and the contest only<br>
If you wish to make your own test account you can do so here: <br>
https://testnet.bybit.com/en/ <br>
Just remember to request currency to fund your account before trying to use the account with this program.
<br>
If you wish to view the account that is connected to the program you can go here and log in using these details:<br>
https://testnet.bybit.com/trade/usdt/BTCUSDT <br>
Email: une.ai.competition@gmail.com <br>
Password: Uneaicompetition1<br>

- Welcome to losing your retirement... house... family, everything really<br>
You'll have nothing, and you'll be happy.

## Why bitcoin and why bybit

- Bitcoin trades 24/7 so for a competition where I have no idea when someone may run
the program, I need it to be able to produce results. Normal markets have open and 
close times as well as are only open monday to friday. I'm only using bitcoin for 
simplicities sake as a proof of concept, pulling this idea off at scale would be
a very expensive task requiring access to many different assets and platforms which
often require strict barriers of to entry.
- Bybit is a simple exchange that can do everything I need for this project, they store 
all historical data (for the last 1000 time periods of your choice) it's free to 
start an account and use the data, no barrier to entry and a fully functional api 
to build products off. These arn't commonly free things in the world of finance.
- These are the main reasons why i've chosen to scale down my original idea and use
just this one asset and this one exchange for the project.

## Known problems

- The entire project, it's one giant problem that weighs me down at night...
- There is a market security mechanism on bybits end which stops market orders for executing
against resting orders if it would cause too much slippage in the order book. This is due 
to running the program on a testnet which has significantly less trading activity and
users, this probelem does not exist in the real market.
This problem sometimes has the effect of not fully closing a position when the NN desires too. 
We have no control over this and you can't force an order through, this is a protection
on bybits end. So sometimes a full position wont get closed and will close the next time
the nn makes a decision.

## Extra Information
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

## Programming log

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

#### 12th of January, 2025
Discovered some pretty critial bugs relating to the inner workings of trade calculations 
nothing that's not fixable in time, but i currently am strapped for time to continue
working on this project, I do have other things i've been putting off to do and an 
exam to revise for. If it wasn't for this competition, at this point I would just 
start the process of refactoring the parts that are bloated and not concise instead 
of trying to patch a leaky ship... so with this in mind I might not try to patch 
this leaky ship for the time being and if im able to get the fixes done in time then
all good, and if not... well oh well, the project is far from being 100% completed 
anyway and it currently is completely functional which is all that is needed. I made 
big design mistakes at the start that im paying for now, its ok, lessons learnt.

#### 13th of January, 2025
Busy day elsewhere, inside the project though, I made some small ground on the technical
debt i've created in the main . py module in an attempt to just get a solution. It's 
slow going as I build a somewhat jenga construction of functions to get this baby
to work.

#### 15th of January, 2025
Didn't write in the log yesterday, was too busy filling other information in the 
readme. Yesterday I added automation to the program, today I tried to add some 
more features and tune the NN.... alas, it is impossible to just "tune" an NN into
being a rpofitable trader, a lot more research is needed to find an edge for it 
to use. This is probably the big glaring hole in this project... this and main.py..
that place sucks right now, incredibly unhappy how much short cutting and ducktape
i've used to bring that together. Iwill refactor this project, but I dont have the 
time to do it before the dealine. Anyway, today was more refinement and trying to 
fix small bugs that pop up everywhere. Probably finished at this point, perhaps just
some small decisions, we will see what tomorrow brings, hopefully the end to this.:w

#### 16th of January, 2025
Each time I try to slim down main.... it expands!! It's not entirely my fault though,
what started as splitting up functionality of bigger functions turned into bug finding.
Bybit is under traffic today, probably due to the trump inaguration coming up and 
markets in general experiencing heavy traffic. Anyway, this caused a whole slue of 
new bugs not seen before. I simultansously decided to adfd acouple of new features 
like force closing orders. I digress.... I think im done for the main branch of this 
project and now i will pivot to working on fixes in main on a different branch. If 
im able to rework it before the deadline, i can ship it, else I just keep the Project
where it is at!

#### 17th of January, 2025
Well well well... the day finally came when I put down the refactor of a century..
Main has been reworked and now isn't a complete dumpster fire. Minor changes elsewhere,
mostly just catching strage edge cases that crop up. At the current moment, barring 
any critical bugs that appear in the next two days while it runs non stop trading..
this project is at a place where it can be judged and no new features will be going
in until after next week. So... after 12 days, 70+ hrs (not ashamed admitting that).

#### 19th of January, 2025
A few minor display changes implemented after getting some "non tech savy" people 
to try run the program.... we call that... r n d bby. Other than that, just slight 
changes to the documentation and writing up the 500 word  description. I will submit
it tomorrow in its current form.
