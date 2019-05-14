#!/usr/bin/python
import ConfigParser, time
from marionette_driver.marionette import Marionette
from marionette_driver import By, Wait
import subprocess
import argparse
import urllib
import cgi

def sendmessage(title, message):
    subprocess.Popen(['notify-send', title, message])
    return

# Detect if user is logged
def logged_in(init):
    try:
        return client.find_element(By.CSS_SELECTOR, 'body.logged-in')
    except:
        try:
            val = int(init)
        except:
            init = 0
            if init < 5:
                init += 1
                return logged_in(init)
            else:
                return True


#  Detect if action have success
def gp_success(init):
    try:
        return client.find_element(By.CSS_SELECTOR, 'div.gp-js-success')
    except:
        try:
            val = int(init)
        except:
            init = 0
            if init < 5:
                init += 1
                return gp_success(init)
            else:
                return True

parser = argparse.ArgumentParser(description='Bulk Reject translations on GlotPress with Firefox')
parser.add_argument('--search', dest='search', help='The term with problems', required=True, type=str)
parser.add_argument('--remove', dest='remove', help='The wrong translation to remove', required=True, type=str)
parser.add_argument('--replace', dest='replace', help='The new translation to submit', required=False, type=str)
parser.add_argument('--lang', dest='lang', help='The locale, eg: it', default="it")
args = parser.parse_args()
# Load configuration
config = ConfigParser.RawConfigParser()
config.readfp(open('config.ini'))
print "Connection in progress to Firefox"
client = Marionette(host='127.0.0.1', port=28288)
client.start_session()
print "Connection to Firefox Done"
# Detect if already logged
try:
    client.find_element(By.CSS_SELECTOR, 'body.logged-in')
    client.navigate("https://translate.wordpress.org/wp-login.php?action=logout&redirect_to=https%3A%2F%2Ftranslate.wordpress.org%2F&_wpnonce=583839252e")
except:
    pass
# Login
client.navigate("https://login.wordpress.org/?redirect_to=https%3A%2F%2Ftranslate.wordpress.org%2F")
try:
    #Log In Form
    usernameLogin = client.find_element(By.ID, 'user_login')
    usernameLogin.click()
    usernameLogin.send_keys(config.get('Login', 'user'))
    passwordLogin = client.find_element(By.ID, 'user_pass')
    passwordLogin.click()
    passwordLogin.send_keys(config.get('Login', 'pass'))
    # Click on the Log in button to connect
    client.find_element(By.ID, 'wp-submit').click()
    time.sleep(1)
    Wait(client).until(logged_in)
except:
    print "Already logged"
# Move to the term
term = args.search
# encode the term and change the space ('%20') in a '+'
term = urllib.quote_plus(term, safe='')

client.navigate("https://translate.wordpress.org/consistency?search=" + term + "&set=" + args.lang + "%2Fdefault")
# Remove the strings different from our
removeOtherStrings = "var right = document.querySelectorAll('table td:nth-child(2) .string');for (var i=0; i<right.length; i++){if(right[i].innerHTML!=='" + cgi.escape(args.remove.replace("'","\\'")) + "') {td = right[i].parentNode;tr = td.parentNode;tr.outerHTML=''}}"
result = client.execute_script(removeOtherStrings)
# Force to open the link in another tab with a little hack in js
addTarget = "var anchors = document.querySelectorAll('table td:nth-child(2) .meta a');for (var i=0; i<anchors.length; i++){anchors[i].setAttribute('target', '_blank');}"
result = client.execute_script(addTarget)
# Open all the links
openPages = client.find_elements(By.CSS_SELECTOR, 'table td:nth-child(2) .meta a')
print('Find ' + str(len(openPages)) + ' wrong strings for ' + args.search + ' with -> ' + args.remove)
i = 0
j = 0
for openPage in openPages:
    original_window = client.current_window_handle
    openPage.click()
    # Wait page load, glotpress is very slow
    time.sleep(1.5)
    all_tab = client.window_handles
    if all_tab[-1] != original_window:
        # Switch to the tab opened
        client.switch_to_window(all_tab[-1])
        Wait(client).until(logged_in)
        i += 1
        print(str(i) + ' - Switch to ' + client.find_element(By.CSS_SELECTOR, '.breadcrumb li:nth-child(3)').text)
        try:
            client.find_element(By.CSS_SELECTOR, 'button.reject').click()
            # Reject the translation
            time.sleep(1)
            Wait(client).until(gp_success)
            # If a replacing translation is set, submit it
            if args.replace:
                try:
                    client.find_element(By.CSS_SELECTOR, '.action.edit').click();
                    time.sleep(1)
                    client.find_element(By.CSS_SELECTOR, 'textarea.foreign-text').clear()
                    client.find_element(By.CSS_SELECTOR, 'textarea.foreign-text').send_keys(args.replace)
                    client.find_element(By.CSS_SELECTOR, 'button.translation-actions__save.with-tooltip').click()
                    Wait(client).until(gp_success)
                    j += 1
                except:
                    print(str(i) + ' - Not possible submit new string on ' + client.find_element(By.CSS_SELECTOR, '.breadcrumb li:nth-child(3)').text)
        except:
            print(str(i) + ' - Not possible reject on ' + client.find_element(By.CSS_SELECTOR, '.breadcrumb li:nth-child(3)').text)

        client.close()
        client.switch_to_window(original_window)
        # Repeat the process
# Force a logout
client.navigate("https://translate.wordpress.org/wp-login.php?action=logout")
print('Finished!')
if args.replace is None:
    sendmessage('Finished Translate.WP.org bulk rejection', args.search + ' on ' + args.remove + ' with ' + str(i) + ' removals')
else:
    sendmessage('Finished Translate.WP.org bulk rejection', args.search + ' on ' + args.remove + ' with ' + str(j) + ' replaces')
