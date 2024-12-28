# Quickmaths

Quickmaths is a pygame based game allowing to sharpen arithmetic skills and math creativity using two fun playing modes: time trial and countdown.

<img src="https://github.com/user-attachments/assets/098baad5-7b62-4f81-bde7-c367433f6ffc" alt="Time trial" width="600"/>

## Time trial

Compete with your friends in time trial mode and become the human calculator. 

In the menu choose the preferable operation, number of digits in the number and the amount of equations required to finish challange. You can also turn on the flash mode: equation will diseappear after short time to ensure the calculations are done in the head! 

Save your best runs and become the first in the ranking!

<img src="https://github.com/user-attachments/assets/4032f686-b8f1-43ae-b241-f109eab1be99" alt="Time trial menu" width="600"/>



## Countdown

This mode originates from the numbers game in the british game show called Countdown.

Players, using four basic operators (+, -, x, /) and the tiled numbers try to get as close as possible to the randomly generated target.

<img src="https://github.com/user-attachments/assets/f6b5ac03-cd9f-482b-b936-8ee8fe08f3a4" alt="Countdown" width="600"/>

The official rules are: 

- There are four numbers in the large set { 25 , 50 , 75 , 100 }

- There are twenty numbers in the small set, two each of the numbers 1-10  
  { 1 , 1 , 2 , 2 , 3 , 3 , 4 , 4 , 5 , 5 , 6 , 6 , 7 , 7 , 8 , 8 , 9 , 9 , 10 , 10 }

- One contestant selects as many numbers as desired 
  (unseen) from the large set (between none and all four), and the balance
   are pulled from the small set to make six numbers in total.

- A random three-digit *target* number is then chosen by a computer

- The contestants are given 30 seconds to get as close
   as possible to the chosen target by using just the four basic 
  arithmetic operators + - × ÷

- Not all the digits need to be used.

- Concatenation of the digits is not allowed (You can’t use a “2” and “2” to make “22”).

- At no intermediate step in the process can the current running total become negative or involve a fraction.

- Each numbered tile can only be used once in the calculation.

- 10 points are awarded for correctly getting the exact solution.

- 7 points are awarded for getting within 5 of the required solution.

- 5 points are awarded for getting within 10 points of the required solution.

## Installation

### Clone and enter the repository

```
git clone git@github.com:MarcinKadziolka/quick-maths.git
cd quick-maths
```

### Create virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install required packages

```
pip install -r requirements.txt
```

### Run the program

```
python3 main.py
```
