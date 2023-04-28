Title: Dynamically Rendering Content on Neocities Pages
Date: 2023-03-16
Slug: dynamic-render-content-neocities
Tags: neocities, webdev
  
A common question that I see coming from new [Neocities](https://neocities.org) webmasters:

### "Is there a way to edit all my navigation HTML at once or do I have to go through page by page updating all of them to add something to the menu?"

---

That is a great question and probably one of the first big questions you will have as you begin your journey into HTML and CSS. 

The solution that I'm going to give you is the *easiest* one to implement, but it is not necessarily the *best*. But since you are new, we'll start with this very flawed approach that will work on your personal Neocities page and serve to introduce you to the somewhat problematic, messy world of JavaScript.

I would strongly suggest that you not use this technique in a commercial website.

At the end of this tutorial, we'll look at some of the reasons you might want to consider doing this a better way once you learn more.

---

## Lets start by adding code to the following files:

## index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Dynamic Content Loading</title>
  </head>
  <body>
    <h1>Dynamic Content Loading</h1>
    <noscript>Unfortunately, this page cannot load without JS.</noscript>
    <nav></nav>
    <article>
        <h3>This is some dumb Content</h3>
        <p>Enjoy this terrible content. You're quite welcome!</p>
        <p>Perhaps you would enjoy some <a href="index2.html">Better Content</a>?</p>
    </article>
    <footer></footer>
        <script src="script.js"></script>
  </body>
</html>
```

This is just a basic starting template for an HTML page.

---

## index2.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Dynamic Content Loading</title>
  </head>
  <body>
    <h1>Dynamic Content Loading</h1>
    <noscript>Unfortunately, this page cannot load without JS.</noscript>
    <nav></nav>
    <article>
        <h3>This is some better Content</h3>
        <p>Enjoy this better content. You're quite welcome!</p>
        <p>Perhaps you would enjoy some <a href="index.html">Terrible Content</a>?</p>
    </article>
    <footer></footer>
        <script src="script.js"></script>
  </body>
</html>
```

For the purpose of demonstrating that this will work on any page, we copy a slightly alternate version of the first page into a second page.

---

## nav.html

```html
<ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Pictures</a></li>
    <li><a href="#">Links</a></li>
    <li><a href="#">Contact</a></li>
</ul>
```

This is a simple unordered list of imaginary links. We'll be inserting the HTML of this file into the empty `<nav></nav>` placeholder that we've left on our pages.

---

## foot.html

```html
<p>Copyright 2023 Your Mom</p>
```

To demonstrate that we could also do this with other pages and other elements, make this page as well, and we'll insert it into `<footer></footer>`.

---

## script.js

```js
function insertPageToElement(endpoint, selector) {
    const storageKey = "insertPageToElement-" + endpoint
    const insertHTML = (sel, htm) => document.querySelector(sel).innerHTML = htm;
    if (sessionStorage.getItem(storageKey) === null) {
        console.log(`Loading ${endpoint} via fetch`)
        fetch(endpoint)
            .then((response) => response.text())
            .then((html) => {
                sessionStorage.setItem(storageKey, html);
                insertHTML(selector, html)
            })
            .catch((error) => {
                console.warn(error);
            });
    } else {
        console.log(`Loading ${endpoint} from sessionStorage`)
        const html = sessionStorage.getItem(storageKey)
        insertHTML(selector, html)
    }
}

insertPageToElement("nav.html", "nav")
insertPageToElement("foot.html", "footer")
```

This last file is the meat and potatoes of the technique. It's the instruction that tells the page where to look for the content we want to insert into our pages and where we want to insert it. 

If you don't understand how this works, don't worry. We're going to go over it. For now just verify that you've made all the files listed above and that they have the correct code copied into them. Upload them to a folder on your Neocities site and verify that both pages load the menu links and the copyright notice.

---

## How Does This Work?

### Fetching the Resource

As stated above, the foundation is that every page we want to insert our menu into has to load `script.js`.  That is what we're doing when we say `<script src="script.js"></script>`.

In this script, we define a function that takes an endpoint (a url link) and a CSS selector. It fetches the contents of the page at the link and it inserts HTML into the placeholder element that is selected by the selector. 

```js
insertPageToElement("nav.html", "nav")
```

- `"nav.html"` is the endpoint (url link)
- `"nav"` is what selects the `<nav></nav>` element.

Note that if either the `nav.html` page does not exist or if the `<nav></nav>` element is not present, there will be an error, and the content will fail to load.

### Caching the Resource

One important element of this script is that it stores ("caches") the contents of what it fetched into the browser session. This means that if the user navigates to another page in the same tab, the script will not have to do another fetch request to get the `nav.html` markup. It will just reuse what it already fetched, saving time and energy. However if the user closes the tab, it will have to do the fetch again. This makes sure that your returning users are not pulling outdated resources from their cache.

### Adding Links to the Menu

Now you should be able to simply edit the `nav.html` file and it should update both pages -- or any number of pages -- if the following are true:

1. the page loads the script
2. the script calls `insertPageToElement`...
3. ...gives it a link to another page and
4. ...gives it an element that exists on the current page.

```html
<ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Pictures</a></li>
    <li><a href="#">Links</a></li>
    <li><a href="#">Contact</a></li>
    <li><a href="#">NEW LINK!!!</a></li>
</ul>
```

## How do I insert this into a specific div?

Let's say instead of `<nav></nav>` you have `<div id="nav"></div>`
Then in the `script.js` file, change it to `insertPageToElement("nav.html", "#nav")`

## But what if it's still not working?

The most likely thing is that it's having trouble fetching your menu page. It might help to change it to this

`insertPageToElement("https//yoursite.neocities.org/nav.html", "nav")`

If this does not fix it, try looking in the dev tools console. That's where you look for problems when you're working with JavaScript.

## Why is This Kinda Bad?

- **It's Not Very Secure**

I am assuming that you are making your first personal page on NeoCities. If you are doing this on the site where you are sending your customers to login and stuff like that, it is likely that malicious actors will possibly target your users with XSS attacks. That's kind of outside the scope of this tutorial, but it's worth pointing this out first and foremost.

- **It's Inefficient**

When we do something like this:

```js
insertPageToElement("nav.html", "nav")
insertPageToElement("foot.html", "footer")
insertPageToElement("header.html", "header")
```

...it brings the number of requests that have to go to the server before the page will load for the user to **a grand total of 5** (one for the page, one for the script file, and three for the nav, footer, and header). Frankly, that is ridiculous, especially since we know that at least one of those requests is for a single line of text that we will most likely never change.

Do we really need to slow the page down for the user to load something so simple? Maybe sometimes we do and sometimes we don't.

Even with the session caching, if you're using this technique to dynamically load things that do not need to be dynamically loaded, it's still wastefully silly.

*I would suggest that maybe you should only do this with things you know are going to change often and be used on many pages.*

- **It Does Not Work Without JavaScript**

If the user doesn't have JS enabled, the only thing we can do is inform them with `<noscript>` tags that they need to enable it, because without that, the page isn't going to load. A lot of modern websites rely on JavaScript to load and many times it's worth it for the convenience... But other times it's just plain lazy and badly designed.

As I said above, for the same reason:

*I would suggest that maybe you should only do this with things you know are going to change often and be used on many pages.*

## What Other Ways Exist to Solve This Problem?

- **Server Side Rendering**

If you were hosting this website somewhere other than Neocities, you would most likely be able to approach this problem in an infinitely better way using a server side language like PHP or Python.

- **Static Generated Website**

In my opinion, the best way to deal with this problem for a non-commercial, personal site is to start generating your site locally on your computer. I do that with this page using the [pelican](https://getpelican.com/) Python library.

This can be pretty hard to get set up and maybe isn't the best approach for your very first pages. But maybe one day you can look into this approach.

- **Build the menu HTML with JavaScript**

In this technique, we are loading a separate HTML page and write that HTML into the current page.

It would be nicer to build the menu HTML directly from the `script.js` file.

This is more advanced for basically the same effect at a lower number of requests, and the reason I didn't start with this method is because there is no easy way to plug and play whatever HTML you may have in your menu onto the page without learning some JavaScript yourself.


