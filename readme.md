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
15 - Switch to WpCoolForm
16 - Switch to Automated Cart Abandonment Campaign for WP eCommerce with Pre-built Emails
17 - Switch to Post Shortcode
18 - Switch to Semantic Shortcode
19 - Switch to Exclude Category Widget                                                                                                                          
20 - Switch to Push Notifications for WordPress (Lite)
21 - Switch to Slimpack - Lightweight Jetpack
22 - Switch to Push Notifications for WordPress (Lite)
23 - Switch to Author Details
24 - Switch to Master Currency WP
25 - Switch to search-into-subcategories
[...]
```
Every switch means that the reject procedure works without problems!

# Install
 
```pip install marionette_client```

Get the Firefox nightly, set in about:config:
```
marionette.defaultPrefs.enabled -> true
marionette.defaultPrefs.port -> 2828
```

Start Firefox nightly and create a `config.ini` file and execute the script.

# Credits

Thanks to Manel Rhaiem for the example code for Marionette
