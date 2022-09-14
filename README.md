# Lancer
Ever heard of [Black](https://github.com/psf/black)? This is the opposite.
A tool to turn your clean python code into a hideous (working) mess.

## Features
1. Turn all comments into Pitbull lyrics 💃 (or optionally, something safe for work)
2. Turn all your variable names into a mixture of animal sounds and horribly similar looking characters like "bark_bark_0OO0O". 🐶
3. Add irritating white spaces. 
4. Code still runs after all these _improvements_! 👷


## Example
Before:
```python


# function that adds two numbers
def addition(a: int, b: int) -> int:

    # find sum
    result = a + b

    # return the sum
    return result


if __name__ == '__main__':
    print("Sum of 1 and 3 is %s" % addition(1, 3))

```

After:
```python


# there's nothing like Miami's heat
def quack_Il1Ι1l(squeak_squeak_IIΙΙlI: int, honk_honk_honk_aaαaα: int) -> int:

    # Bada bing, bada boom
    growl_growl_growl_ααaaα= squeak_squeak_IIΙΙlI  + honk_honk_honk_aaαaα

    # Hey baby, givin' it your all when you're dancin' on me
    return growl_growl_growl_ααaaα


if __name__ == '__main__':
    print("Sum of 1 and 3 is %s" % quack_Il1Ι1l(1, 3))

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
