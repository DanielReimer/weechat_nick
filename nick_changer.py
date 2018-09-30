#!/usr/bin/python3

import weechat, re

# Globals
SCRIPT_NAME = "rc_nick"

# Initialize
weechat.register("rc_nick", "pigs", "1.0", "MIT", "Rocket Chat name changer", "", "")
weechat.config_set_plugin("nick_format", "%s")

# :nickname!name@192.168.1.1 PRIVMSG #channel :this is a message
def get_nick(string):
    return string[1:string.index('!')]

def get_message(string):
    return ' '.join(string.split(' ')[3:])[1:]

def get_channel(string):
    return string.split(' ')[2]

def get_server(string):
    return string.split(' ')[0][string.index('!'):][1:]

def build_privmsg(nick, server, channel, message):
    return ":%s!%s PRIVMSG %s :%s" % (nick, server, channel, message)
    
def modifier_cb(data, modifier, modifier_data, string):
    nick = get_nick(string)
    message = get_message(string)
    channel = get_channel(string)
    server = get_server(string)

    # Ignore messages that are not from rc
    if nick != "rc":
        return string
    
    # Switch the nicks
    rc_nick = re.match(r"^<\w+_rc> ", message)
    if rc_nick:
        unformatted_nick = rc_nick.group(0)[1:][:-5]
        nick = weechat.config_string(weechat.config_get("plugins.var.python." + SCRIPT_NAME + ".nick_format")) % (unformatted_nick)
    else:
        return string
        
    # Remove the nick in message
    message = re.sub(r"^<\w+_rc> ", "", message)
    
    return build_privmsg(nick, server, channel, message)

def config_cb(data, option, value):
    weechat.config_set_plugin("nick_format", weechat.config_string(weechat.config_get("plugins.var.python." + SCRIPT_NAME + ".nick_format")))
    return weechat.WEECHAT_RC_OK

# Hooks
weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*", "config_cb", "")
weechat.hook_modifier("irc_in_privmsg", "modifier_cb", "")
