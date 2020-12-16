# Bayonet_Inventory
Flask web-app for generating dynamic web forms.

Bayonet Inventory is a system I created quickly to generate dynamic web forms utilizing input from text files (which were created from data taken off of Excel files). It also requires a text file of names and emails in the form of: [Name] _ [Email]

The idea is you seperate your data into a text file: ITEM_CODE [space] ITEM_DESCRIP [delimiter] ITEM_LOCATION, the html generation module then detects all your text files and creates html pages with tables that your employees can use to perform an inventory count.

The system supports "saving" of a form, via a button at the end of the form. When saved, a new html page is generated, importing the data from the current form onto the new form. An email is then sent to the employee containing the link to their saved form.

When a user "submits" their form, a XLSX file is generated using the data from the form. A email is also sent to the user containing a copy of their XLSX file. These XLSX files can then be further manipulated to get total counts, or whatever you want/need.

Current known issue: refreshing a form erases all data entered (unless its a saved page it seems), html generate module gets called twice on flask run (not the end of the world but is an issue).

This is in no way a perfect Flask app, but is very minimal and lightweight. Can be easily ran from AWS EC2, simply create a virtual enviornment and import all required files from this repo into it.
