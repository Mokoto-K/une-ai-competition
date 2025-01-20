# Readme

# Welcome to the Casino my friend

This is a repo for my attempt at the une ai competition that was held from Dec 2024 -
Jan 2025.

## What it does 

The idea for this project is to take in multiple datastreams for 100's of assests,
do some math on their raw data, assess current market conditions, calculate the 
risk it should take and execute real trades using the user connected account to 
essentially manage their assets/retriement instead of paying a super fund, investment
firm, or any other middle man. 

That's the theory atleast... this idea in total would take quite some time to build, 
and the price of the data would be very expensive to buy for a competition, 
so as a proof of concept this project
currently takes real time data from only the bitcoin asset and uses a neural network
on some engineered features to determine if it should buy or sell depending 
on the current position of the users account (which is connected to a real exchange
making trades) and the output it calculates. It then executes trades in real time,
tracking it's own performance as it goes. 

When the program starts the user is either prompted to input api information for Bybit
(the exchange used for this project, the api key and secret used for this project 
can be found in the readme of the git repo under the 'how to use' section, copy and 
paste from there) or they are greeted with a choice of commands to make if they already
have an account and api connected.

Users have the choice to enter a trade or change the current risk level (strategy) that is 
deployed in the market which currently supports two extreme levels of high ((decide per minute)
yes thats right, in glorious conditions it could technically
execute 1440 trades a day... at a higher percentage of the users account)
and low (decide per day). In the future I would probably have the 
NN control which strategy it's using depending on the volitility and past performance 
of the market. Anyway, if you choose this option the program will take the risk level 
you chose and query the exchange in realtime to either create a database of time periods
split according to the risk level, (price data for each minute, day, etc) or update one 
if it already exists. It does this by comparing the time of the last record stored 
with current market time to determine how many records it needs to download to be 
up to date. After this the data is processed, features are created and fed into a neural 
network which then determines if it should buy or sell using binary classification.
The program then pulls real user account data to compare against the neural networks 
decision and either closes a trade, opens a trade or does nothing depending on what 
trade the user is already in. 

You can also choose to automate this process to have it running 24/7, updating according
to the risk level selected, which you can change at any time. If you want to turn it off,
there is functionality to force close trades so you are no longer at risk as well as
a simulation mode to view the performance of the neural net on the market for the 
last x decisions (currently hard set to 500 for the purpose of the competition)

When I started this project, the idea was so simple in my head... I started writting
the first few modules, the database, the neural net, the features... then the scope
creep kicked in and all of a sudden it turned into some kind of mash of duct tape
and rubber bands in an attempt to just get all the basic functionality in. I hope to remedy some of the
poor design choice I choose to use along the way. This project taught
me more about what not to do instead of what to do, but learning is learning.
<br><br>
UPDATE: Feels less like rubber bands and duct tape just 4 days later, 
still structual problems that can be fixed with a little more time and refactoring
<br><br>
UPDATE: Feels like biggest ball of duct taped rubber bands to ever exist 2 days later...
<br><br>
UPDATE: Refactored some core elements.... everything is under control.
<br>

## How to run

- Open up a terminal
- Navigate to a directory you are happy cloning the project too
- Type or copy & paste everything on the below line:<br>
git clone https://github.com/Mokoto-K/une-ai-competition.git une-ai-competition-winning-entry
- After the repo is cloned successfully you'll want to set up a virtual environment 
for python, you can do this in the terminal by typing:<br> 
python -m venv .venv <br>
You may need to use python3 instead of python depending on how your system is set up. 
If you have any trouble running the python command, visit python.org for more information 
on how to update your python distribution on your selected system.
- To activate the environment you then need to run: <br>
Linux/Mac: source .venv/bin/activate <br>
Windows(depends on your shell):   .\\.venv\Scripts\activate.bat <br>
Apparently this doesn't work for vscode if you're into that kind of thing...
- Next you will need to install the requirements, you can do this with one of the following
commands: <br>
pip install -r requirements.txt
pip3 install -r requirements.txt
- Now just run python main.py or python3 main.py
- To run the real account function (which is running on testnet) you will have to 
enter an api key and secret the first time when are prompted, below I have provided 
one for the purpose of the competition:<br>
api key = ZJvzXJ4WEpphUlVTiw<br>
secret = NuvY5NftCiBlZuoWPmi7ozyxI2I8lugrY4vx<br>
Don't worry it's just a test account for the competition, these keys arn't important.
<br><br>
There is one risk with sharing an api for this contest and that is the program will 
probably exhibit some weird behaviour if multiple people start running it with the 
same key. There is no fix for this as multiple people should not have your api key 
and secret. This is a known risk that is necessary for the contest and the contest only
and I don't think it will cause any serious issues with the programs functionality...<br><br>
If you wish to make your own test account you can do so here: <br>
https://testnet.bybit.com/en/ <br>
Just remember to request currency to fund your account before trying to use the 
account with this program  as well as apply for an api... it's slightly annoying 
to do so that's why one has been provided for the competitions judges.
<br><br>
If you wish to view the account that is connected to the program you can go here
and log in using these details:<br>
Login page: https://testnet.bybit.com/en/login <br>
Email: une.ai.competition@gmail.com <br>
Password: Uneaicompetition1<br>
Trading Page: https://testnet.bybit.com/trade/usdt/BTCUSDT <br>

- Welcome to losing your retirement... house... family, everything really<br>
You'll have nothing, and you'll be happy.

## Why bitcoin and why bybit

- Bitcoin trades 24/7 so for a competition where I have no idea when someone may run
the program, I need it to be able to produce results. Normal markets have open and 
close times as well as mostly only open monday to friday. I'm only using bitcoin for 
simplicities sake as a proof of concept, pulling this idea off at scale would be
a very expensive task requiring access to many different assets and platforms which
often require strict barriers of entry and with market data fetching high prices.
- Bybit is a simple exchange that can do everything I need for this project, they store 
all historical data (for the last 1000 time periods of your choice) it's free to 
start an account and use the data, no barrier to entry and a fully functional api 
to build products off. These arn't commonly free things in the world of finance. 
Bybit also has a testnet with a fully intergrated api (even though it does have its flaws)
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

## Extra Information (redundant information at this point)
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

## Future features 

I have alot of ideas on how to make this program alot better, i'm not sure on the 
validity of them all or just how possible they are, i'd need to learn more about 
neural nets and markets to know the full scope of what I could achieve. That being 
said, the program files are littered with TODOs and ideas that I didn't get around 
to fixing/finishing/implementing. Some main ones are:

- Strategy control decided by Neural net using performance and volitility to decide 
with more flexibility on how much risk and when to deploy it.
- Using CNNs and RNNs to process sentiment online such as bloomberg terminal
updates, news outlets and X to better understand what is happening in the market 
as well as time series processing of our data (cuz ya know... what happened a minute 
ago is probably important for the next minute)
- Processing not only multiple assets but also asset classes for better control 
and management of finances, this would greatly reduce the risks that are currently 
taken.
- Extra order features like take profits and stop losses to maximise potential 
profits and minimize losses, or atleast better define the risk.
- Ability to connect to multiple exchanges, this idea is kind of a work in progress
because... why not just be the gateway, this is tricky because you esseentially 
are just becoming the middle man. But really what i'm saying is, a user connects 
their money to your service, that has access to all these markets and has a NN 
making decisions for them... Not exactly what currently exist in the traditional 
finance world, but also not exactly what exists in the new defi world. I don't know 
I haven't thought about it enough.
- Better history logging or all trades instead of leaning on the exchanges history
- More features to train on such as more staple market proven indicators like MACD,
RSI, insider trading, all your favourites. No but seriously more research into 
what makes markets tick to take more of the randomness out of this process.:w
 
<hr>

## Programming log

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

#### 20th of January, 2025
Alright, 12ish solid days of work, one idea... kinda executed... Just fixing typos 
and minor display problems/differences... and editing the readme.
