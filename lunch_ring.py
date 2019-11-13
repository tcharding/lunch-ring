#!/usr/bin/python3
import sys
import datetime
import smtplib

from email.message import EmailMessage

"""
Lunch Ring

Maintains a ring of the CoBloX devs.  If today is notification_day emails
whomever is at the head of the list to notify them that it is their turn
to pick the lunch spot.  Rotates list head to tail.

Requires an SMTP server to be running on host machine.
Suggested usage: Run this script daily i.e., as a cron job.
"""



ring_path = "./ring.txt"        # The file holding the current lunch ring.
log_file = "./lunch_ring.log"
notification_day = "Wednesday"

# CoBloX hackers listed in alphabetical order.
address_book = [("Daniele", "daniele@coblox.tech"), ("Franck", "franck@coblox.tech"), ("Lucas", "lucas@coblox.tech"), ("Philipp", "philipp@coblox.tech"), ("Thomas", "thomas@coblox.tech"), ("Tobin", "tobin.harding@tenx.tech")]
author = "Tobin"

def main():
   today = day()
   if today == notification_day:
      send_notification()


def day():
   """Returns the current day i.e., Monday"""
   days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
   day = datetime.datetime.today().weekday()
   return days[day]



def send_notification():
   """Reads ring file and sends a notification to the head of the list"""
   who = rotate_ring_file(ring_path)
   notify(who)


def rotate_ring_file(filename):
   """Reads ring file into memory and writes it back to file putting the
   head of the list at the end.  Returns the head of the list"""

   return "Tobin"
   
   f = open(filename, 'r')
   ring = f.readlines()
   f.close()

   who = ring[0]                # Head of the list.
   who = who[:len(who)-1]       # Remove trailing newline.

   ring = ring[1:] + ring[:1]   # Rotate the list.

   f = open(filename, 'w')
   f.writelines("%s" % item for item in ring)
   
   return who


def notify(who):
   """Sends an notification to 'who'"""
   body = "Yo %s,\n\nIts your turn to pick the team lunch venue!  Please choose a place and book if necessary.  If we need to leave early to get there please notify the team - we like to eat at 12.\n\nThanks, you rule.\n" % who
   send_email_to(body, address_of(who))


def address_of(who):
   for (name, address) in address_book:
      if name == who:
         return address
                 
   err("failed to get email address for: " + who)


def send_email_to(body, address):
   msg = EmailMessage()
   msg.set_content(body)
   msg['Subject'] = ""
   msg['From'] = "no-reply@lunch-ring.bot"
   msg['To'] = address

   s = smtplib.SMTP('localhost')
   s.send_message(msg)
   s.quit()

   log("sent email to: %s\n" % address)


def err(msg):
   """logs 'msg' and sends an email to the script author"""
   print("error: %s" % msg)
   log(msg)
   sys.exit(1)


def log(msg):
   """Appends 'msg' to end of log file"""
   date = datetime.datetime.today()

   f = open(log_file, 'a')
   f.write("%s: %s" % (date, msg))
   
   
if __name__ == "__main__":
    main()
     
