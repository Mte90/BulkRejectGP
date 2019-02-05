# Bulk Reject GP
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)   

The Consistency tool of GlotPress is very useful to find string approved and in our case to find wrong approved strings.  
The annoying part that they are all the same but it is a manual procedure, so you need to open every string and reject manually.  
That script use Firefox Nightly with Marionette that is a framework to control Firefox.  
After the execution, search on consistence the string, open all the link with that string and reject the string.  
A little example of output:
```
Find 31 wrong strings                                                                                                                                           
1 - Switch to Any Hostname                                                                                                                                      
2 - Switch to Social Media Trifecta                                                                                                                             
3 - Switch to NIP24 for WooCommerce                                                                                                                             
4 - Switch to Carts Guru                                                                                                                                        
5 - Switch to Minutemailer Subscribe                                                                                                                            
6 - Switch to Mixcloud Shortcode                                                                                                                                
7 - Switch to Energ1zer                                                                                                                                         
8 - Switch to Hidden content post wordpress
9 - Switch to hiWeb Memory Usage
10 - Switch to User Shortcodes Plus
11 - Switch to OBOP
12 - Switch to Little Hippo
13 - Switch to Add-custom-page-template
14 - Switch to Mandrill WP - Email Form Under Post
[...]
```
Every switch means that the reject procedure works without problems!

## Install

Marionette installation is mandatory 
```
pip install marionette_driver
```

Get the Firefox Nightly/Dev Edition, set in about:config tab:
```
marionette.enabled -> true
marionette.port -> 28288
```

Create a `config.ini` file, starting from `config-sample.ini`, and put the username and password for wp.org of a PTE.

## Execute

```./bulkrejectgp.py --search="Delete" --remove="cancella" --replace="Elimina" --lang="it"```

Please note that the `replace` is optional! It is intended to be used when you don't only want to reject the string, but you also want to suggest a new one.

## Massive Bulk Rejection
### Use case
Bulk reject is really good to clear/replace **ONE** string, but consider the following case as example.

The Italian polyglots team decide to unify the translation of the string "_Sorry, but nothing matched your search terms. Please try again with some different keywords._".

That was the situation, according to the Consistency:
![Consistency screenshot](./images/consistency.png)

Good luck feeding the command terminal 16 or 17 times to launch the bulkreject command!!!

Wouldn't be awesome to fill in a simple text file and then launch a huge bulk reject?!? (_One command to clear them all!_)

### One text file to clear them all!
The sample text file is the `string-sample.json` one. Keep it untouched for further reference and create a copy named `strings.json`.

Set your language using your locale code
````json
"lang": "it"
````
Then fill in the `commands` property, which contains the single commands.
````json
"commands": [
        {
            "search": "String to be fixed",
            "remove": "String to be removed",
            "replace": "String to be replaced"
        },
        {
            "search": "String to be fixed",
            "remove": "String to be removed",
            "replace": "String to be replaced"
        }
]
````
Add more commands by simple copy-paste the `search`, `remove` and `replace` array element. Remember to separate each single command property with a colon ( _,_ ).

If you don't want to replace a string, just leave the property empty.
````json
"replace": ""
````

### Execute!
```./massive-bulkrejectgp.py```

## Credits

Thanks to Manel Rhaiem for the example code for Marionette.

Thanks to [G. Allegretta](https://github.com/gAllegr) for the replace option and the massive bulkrejection option.
