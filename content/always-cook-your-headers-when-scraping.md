Title: Always Cook Your Headers When Scraping!
Date: 03/08/2022
Status: Published
Slug: always-cook-your-headers-when-scraping

I&#8217;m going to try to make a habit of sharing snippets I end up using a&nbsp;lot.

<p>This is a pretty basic snippet where you should start when you&#8217;re sending web requests from the command line and you need the output to be reflecting of what you would be looking at from a&nbsp;browser.</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">fake_useragent</span> <span class="kn">import</span> <span class="n">UserAgent</span>
<span class="kn">import</span> <span class="nn">requests</span>

<span class="k">def</span> <span class="nf">get_headers</span><span class="p">()</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
    <span class="k">return</span> <span class="p">{</span>
        <span class="s2">&quot;User-Agent&quot;</span><span class="p">:</span> <span class="n">UserAgent</span><span class="p">()</span><span class="o">.</span><span class="n">random</span><span class="p">,</span>
        <span class="s2">&quot;Accept-Language&quot;</span><span class="p">:</span> <span class="s2">&quot;en-gb&quot;</span><span class="p">,</span>
        <span class="s2">&quot;Accept-Encoding&quot;</span><span class="p">:</span> <span class="s2">&quot;br,gzip,deflate&quot;</span><span class="p">,</span>
        <span class="s2">&quot;Accept&quot;</span><span class="p">:</span> <span class="s2">&quot;test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8&quot;</span><span class="p">,</span>
        <span class="s2">&quot;Referer&quot;</span><span class="p">:</span> <span class="s2">&quot;http://www.google.com&quot;</span>
    <span class="p">}</span>

<span class="k">def</span> <span class="nf">get_response</span><span class="p">(</span><span class="n">url</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
    <span class="n">html</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">url</span><span class="p">,</span> <span class="n">headers</span><span class="o">=</span><span class="n">get_headers</span><span class="p">())</span>
    <span class="n">html</span><span class="o">.</span><span class="n">raise_for_status</span><span class="p">()</span>  <span class="c1"># This is simple HTTP error handling.</span>
    <span class="k">return</span> <span class="n">html</span><span class="o">.</span><span class="n">content</span>
</code></pre></div>


<p>One thing to keep in mind when writing scrapers is that the <code>User-Agent</code> sent from the requests python3 module could potentially receive a response with different elements that have different attributes than the ones you are looking at in your browser as you are trying to figure out how to write&nbsp;selectors.</p>
<hr>
<p>Don&#8217;t forget to install <a href="https://docs.python-requests.org/en/latest/">requests</a> and <a href="https://pypi.org/project/fake-useragent/">fake-useragent</a> using <code>pip install requests fake-useragent</code></p>