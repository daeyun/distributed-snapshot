# Programming Assignment 1
## CS 425 Distributed Systems Spring  2014

### Group members:
* Joon Young Seo (jmseo2)
* Daeyun Shin (dshin11)

### Algorithm

We used two invariants: widgets and money. The master process (main.py) launches n processes, and each process initializes the
RNG seed with its ID and randomly sends either widgets or money. When they send or receive messages, they update their corresponding
invariants accordingly.

### Usage

./bin/mp1 [number of processes] [number of snapshots]

Requirement: python3

Execute `mp1` in ./bin folder. For example,

cd bin
./mp1 4 5

#### Search Utility

To search for lines containing the string "snapshot 0",

./snapshots/search-all.py "snapshot 0"
