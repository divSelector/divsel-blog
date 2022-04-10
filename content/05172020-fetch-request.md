Title: Anything From the Client Side is User Input
Date: 2020-05-17
Slug: client-side-user-input
  
User input is dangerous. One of the first things you probably learn is that its necessary to not only validate what a user types into a form, but due to drastic variations in what a user can submit, you also have to sanitize it.

If you make a calculator that runs `eval()` on the raw string `'4 + 3 - 7'` that was put to the program via an `input()` prompt, you open a vector for a user to execute code in your program, and by extension, on the system that is running the program.

This is programming 101. When you make your first web form, you learn to validate and sanitize everything that the user sends you.


## Let's talk about JavaScript
Imagine that we have created a little JavaScript UX for creating a character on our website for an online game. Maybe the game will be played in the browser or maybe it won't. It doesn't matter because either way, when the character creation experience is over, we have to send the data to the server so that we can save it.

When the user clicks submit, the character object is sent as a byte string in a POST request.

```js
submitBtn.addEventListener('click', function() {
  fetch('/character-submit', {
    method: 'POST',
    body: JSON.stringify(character)
    }).then(function (response) {
      return response.text();
    }).then(function (text) {
      console.log(`POST response: ${text}`)
      })
    })
```

This is where it will be received, at our Flask app on a remote host running our website and our database.

```python
@users.route('/character-submit', methods=['POST'])
@login_required
def character_submit():
  if request.method == 'POST':
    print('Incoming..')
    j = json.loads(request.get_data())
    
    commit_character_to_database(j)
    
    return 'OK', 200
```

But what is missing here? What do we have to do before we commit this data?

## JavaScript that is sent to a server IS user input.

In the average browser, a user can press `CTRL + SHIFT + I` and open the console. They can look at the code and find the contextual value of `character`, which we sent in the body of the fetch request.

This is what that character object might look like after its assembled in out character maker interface.

```js
character = {
    meat: 6,
    leet: 5,
    street: 1,
    honesty: -1,
    loadout: ["85.44 GB Wordlist", 
              "Samurai Sword"]
}
```

But all a user has to do is write over this object, perhaps with their own properties, put directly in the console just before they click on our submit button. JavaScript occurs literally inside the user's browser. We have no control of what goes on there really. That's why they call it the client-side. 

In the least horrible scenario, your user is starting the game with 99999 hp. In the worst, you have opened a vector for SQL Injection the moment that you save this to the database.

In any case, the certain outcome of treating JSON from a user's browser as something to take lightly is that things on the server will break.

## So how do we deal with this?

Let's define the aforementioned function from our Flask view:

```python
def commit_character_to_database(j):
    if len(j) != 5:
        return 'OBJECT TOO LONG', 403

    meat, leet, street = attrs = j['meat'], j['leet'], j['street']
    try:
        for attr in attrs:
            if not 1 <= attr <= 7:
                return 'BAD ATTR VALUE', 403
    except TypeError:
        return 'ATTR SHOULD BE INT', 403
            
    honesty = j['honesty']
    if not honesty == 1 and not honesty == -1:
        return 'HONESTY IS DISHONEST', 403
    
    loadout = j['loadout']
    if len(loadout) != 2:
        return 'BAD LOADOUT QUANTITY', 403
    
    loadout_items = ["Samurai Sword", "85.44 GB Wordlist",
                        "Stolen Cyberdeck", "Fake Work Visa"]
    
    for item in loadout:
        if item not in loadout_items:
            return "BAD LOADOUT ITEM", 403
        
    stats = dict(meat=meat, leet=leet, street=street,
                 honesty=honesty, loadout=loadout)
    
    new_character = CharacterSheet(player_id=current_user.id, stats=stats)
    db.session.add(new_character)
    db.session.commit()

```

And that is still code that probably needs another round of sanitation and review.
