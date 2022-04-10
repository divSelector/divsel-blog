Title: Ternary Operator Abuse
Date: 2020-05-14
Slug: ternary-abuse
  
If you're new to Python you might not be aware that the language has a ternary conditional operator. This is an operator that takes three inputs: a Boolean statement evaluating to one of two possible values in the events of true and false. In traditional computer languages, this would be expressed as `condition ? 0 : 1`, however in Python, we say,

```python
0 if condition else 1
```

These ternaries are used frequently in other programming languages but Python typically aims at being a more readable language. And yet, after writing Python for however long its been since you learned what a ternary is, it's very tempting to use every opportunity to avoid this:

```python
if condition:
  x = 0
else:
  x = 1
```

But consider what happens when your code becomes full of assignment statements like 

```python
from pathlib import Path

def get_pics(path: Path):
  file_dir = path if path.exists() else print("Bad Path")
  if file_dir.is_dir():
    originals = [Path(pic) for pic in file_dir.iterdir() if pic.is_file()]
    saving = [f"ha/{f.name}" for f in originals]
    return [
      (str(o), str(s)) for o, s in zip(originals, saving)
    ] if originals and saving else print("Failed to Get Pics")
```

In these examples of ternary abuse, what is the value of `file_dir`, or the return value of `get_pics()`, if the condition is false? Because the return value of `print()` is `None`, then the value is `None`. And if the value is `None`, what happens when we try to call `.is_dir()` on None?

```py
AttributeError: 'NoneType' object has no attribute 'is_dir'
```

Fail. You cannot use a ternary operator to assign values in this manner; or, rather, you shouldn't. Using a print statement as the example is fairly excessive in bad code smell, but it illustrates that when the ternary is used for assignment, the values should most likely be of comparable type.

Lets clean this up.

```python
def get_pics(path: Path):
  try:
    if path.is_dir():
      originals = [Path(pic) for pic in path.iterdir() if pic.is_file()]
      saving = [f"ha/{f.name}" for f in originals]
      return [(str(o), str(s)) for o, s in zip(originals, saving)]
  except AttributeError:
    print(f"{path} is not a Path object")
```
      
The ternary operator is a footnote in the Pythonic religion because we often do not need it. Instead of using a conditional statement at all, we use try/except block to handle what happens if `path` is not a `Path` object.

In the former example, we were also using a ternary to nullify the return value if the the `originals` and `saving` listcomps were unable to form.

While it may not seem like it will become excessive at first, using the ternary conditional to avoid verbose typing will often clutter up your codebase and make it significantly less readable. Often, there is a more Pythonic way to write these evaluations.
