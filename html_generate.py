import logging
import os
from os import listdir
from os.path import isfile, join

logging.basicConfig(filename='html_generation.log', filemode='w', level=logging.DEBUG)

def write_log(log):
  logging.info(log)
  
  
def generateSelectOption(line):
    name = line.split('_')[0]
    email = line.split('_')[1]
    return "<option value=\"" + email.strip() + "\">" + name.strip() + "</option>"


def generateSelectionList():
    names = open("txt/employees.txt", 'r')
    name_lines = names.readlines()
    html = """
        <label for="employeeName">Please select your name:</label>
        <select name="employeeName" id="empName">
        <option value =""></option>
    """
    for line in name_lines:
      html += generateSelectOption(line)
    
    html += "</select>\n\n"
    return html

def generateNewTable():
    table = """<form method="POST" action="/submit">"""
    table += generateSelectionList()
    table += """
      <br>
      <br>
      <table>
      <tr>
      <th>
      Item Code
      </th>
      <th>
      Item Description 
      </th>
      <th>
      Location
      </th>
      <th>
      Count
      </th>
      </tr> 
    """
    return table


def endNewTable():
    end = """
        </tr>
        </table>
        <div class="btn-group" style="float:left;">
            <input type="submit" name="save" value="SAVE">
        </div>
        <div class="btn-group" style="float:left; padding-right: 30px; padding-left:700px;">
            <input type="submit" name="submit" value="SUBMIT">
        </div>
        </form>
    """
    return end


def populateTable(line):
    output = ""
    item = line.split()[0]  
    if len(item) == 1:
        return ""     
    location = ""
    if len(line.split("|")) > 1:  
        location = line.split("|")[1]
        
    output += "<tr>\n"
    output += "  <td>" + item + "</td>\n"
    item_description = ""
    for part in line.split():
        if part == line.split()[0]:
            continue
        if part == '|':
            break
        item_description += part + " " 
    output += "  <td>" + item_description + "</td>\n"
    output += "  <td>" + location.strip() + "</td>\n"
    output += "  <td><input type=\"text\" size=\"14\" name=" + item + "/></td>\n"
    output += "</tr>\n"
    
    return output


output = ""
start = """
    <html>
        <head>
        <style>
            table, th, td {
              border: 1px solid black;
            }
            .btn-group input {
                font-size: 16px;
                border: 1px solid black;
                padding: 10px 24px;
                style: float:left;
            }
        </style>
        </head>
        <body>     
"""
endFile = '</body></html>'


def generatePageTitle(title):
    html = "<h2>Bayonet Inventory - " + title + "</h2>"
    html += "<br>"
    return html


def main():
    files = [f for f in listdir("/home/ubuntu/inv/txt/data") if isfile(join("/home/ubuntu/inv/txt/data", f))]
    print("Files detected:" + str(files))
    for file in files:
        print("Starting file: " + file)
        file_open = open("/home/ubuntu/inv/txt/data/" + file, 'r')
        file_lines = file_open.readlines()
        file_content = start
        file_content += generatePageTitle(file.split(".")[0])
        file_content += generateNewTable()
        for line in file_lines:
            file_content += populateTable(line)
        
        file_content += endNewTable()
        file_content += endFile
        
        html_file = open("/home/ubuntu/inv/static/inventory/" + file.split(".")[0] + ".html", 'wt')
        html_file_content = html_file.write(file_content)
        html_file.close()
        print('Wrote HTML File for ' + file)

main()
  