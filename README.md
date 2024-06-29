# cheftap-recipe-export
Super easy and hacky cheftap scraper to export the source URLs from the recipes since the export from Cheftap itself only dumps the recipe text, no images or source URL.
I wanted a list of source URLs to let Tandoor scrape them again.

## Usage

* Login on the Cheftap website with Chrome
* Go to https://cheftap.com/recipes/
* Open Network tools (F12) and switch to the Network tab
* Choose a random recipe
* Click on the first GET request, on the right side scroll down to request headers
* Right mouseclick on the Cookie: and Copy the value

It should look something like this:

```
__stripe_sid=9a82d7d9-dfs33-4fc2-9e8a-cc6dfghfghfg570462; __stripe_mid=aasd-8e7d-sdfsd-8457-asdasdfg; wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_fac84fddfc2asdadagf48354ac6b=username%7C1719851168%sdfaasasf%sdfsdfsvcxvxcvxcv; wfwaf-authcookie-sdfsdfsdfsdfsdfxcvxcvxcv=154946%7Cother%7Cupload_files%2Cpublish_posts%2Cedit_posts%2Cread%xcvxcvsdfas789798789321654968746346
```

* Run the script like this:
```
python scraper.py "username" "__stripe_sid=9a82d7d9-dfs33-4fc2-9e8a-cc6dfghfghfg570462; __stripe_mid=aasd-8e7d-sdfsd-8457-asdasdfg; wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_fac84fddfc2asdadagf48354ac6b=username%7C1719851168%sdfaasasf%sdfsdfsvcxvxcvxcv; wfwaf-authcookie-sdfsdfsdfsdfsdfxcvxcvxcv=154946%7Cother%7Cupload_files%2Cpublish_posts%2Cedit_posts%2Cread%xcvxcvsdfas789798789321654968746346"
```

It will create a `urls.txt` with the URLs on newlines