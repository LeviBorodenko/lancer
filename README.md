# Lancer
Ever heard of [Black](https://github.com/psf/black)? This is similar.
A tool to turn your clean python code into a hideous (working) mess.

## Features
1. Turn all comments into Pitbull lyrics 💃 (or optionally, something safe for work)
2. Turn all your variable names into a mixture of animal sounds and horribly similar looking characters like "bark_bark_0OO0O". 🐶
3. Add irritating white spaces.
4. Add new, totally redundant comments.
5. Code still runs after all these _improvements_! 👷


## Example
Before:
```python


# Function that finds the sum of a list of numbers
def get_sum(nums: List[int]) -> int:

    sum = 0

    # Find the sum
    for num in nums:
        sum += num

    # Return the sum
    return sum

if __name__ == '__main__':
    sum = get_sum([1, 3])
    print(f"Sum of 1 and 3 is {sum}")

```

After:
```python


# Hey baby, givin' it your all when you're dancin' on me
def oink_oink_oink_IlΙlll (ribbit_ααaαα :List [int ])->int :

    # Setting value of sum
    sum =0

    # Bada bing, bada boom
    for num in ribbit_ααaαα :
        sum +=num

        # there's nothing like Miami's heat
    return sum

if __name__ =='__main__':
    # Setting value of sum
    sum =oink_oink_oink_IlΙlll ([1 ,3 ])
    print (f"Sum of 1 and 3 is {sum}")

```

## Installation and Usage
Simply run `pip install py-lancer` and then use the `lance` command line tool.

```
usage: lance [-h] [--version] -f ./FILE_PATH.py [-s][-y]

Ever heard of Black? This is the opposite.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f ./FILE_PATH.py, --file ./FILE_PATH.py
                        Python file to be lance'd.
  -s, --sfw             Generate comments that are safe for work.
  -y, --yolo            Overwrite original file, lol.
```

So if you have a python file at `./test.py`, you simply run `lance -f ./test.py`

## How does it work
The key tool we use it the `tokenizer` standard module in python. It allows us to tokenize any python script which then in turn makes substituting comments and variable names fairly simple.
Check out the source code for more details.

## Contribute
Bug reports, fixes and additional features are always welcome! Make sure to run the tests with `python setup.py test` and write your own for new features. Thanks.
