import datetime
import os


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


def generate_item_list(file):
    rfile = open(file, 'r')
    return rfile.readlines()

    
def generate_table_line(item_code, item_name, item_value):
    output = ''
    output += "<tr>\n"
    output += "<td>" + item_code + "</td>\n"
    output += "<td>" + item_name + "</td>\n"
    output += "<td><input type=\"text\" size = \"14\" name=" + item_code + " value=" + item_value.replace('/', '') + "></td>\n"
    output += "</tr>\n"
    return output
  
def generateSelectionList(email):
    html = """
        <label for="employeeName">Please select your name:</label>
        <select name="employeeName" id="empName">
    """
    html += "<option value=\"" + email.strip() + "\">" + email.strip() + "</option>"
    html += "</select>\n\n"
    return html
  
        
def generateNewTable(email):
    table = """<form method="POST" action="/submit">"""
    table += generateSelectionList(email)
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
    
    
def generatePageTitle(title):
    html = "<h2>Bayonet Inventory - " + title + " Saved Page</h2>"
    html += "<br>"
    return html
    
    
def save_employee_progress(d, email, save_code, type, from_save):
    new_page = start
    new_page += generatePageTitle(email)
    new_page += generateNewTable(email)
    items = 0
    items = open("txt/data/" + type + ".txt", 'r')
    
    clean_dict = {}
    new_key = 0
    
    for key in d:
        new_key = key.replace('/', '')
        clean_dict[new_key] = d[key]
    
    item_lines = items.readlines()
    
    for line in item_lines:
        if len(line.split()) == 1:
            continue
        item_code = line.split()[0]
        if item_code in clean_dict:
            item_value = clean_dict[item_code]
            item_name = line.partition(' ')[2].strip()
            new_page += generate_table_line(item_code, item_name, item_value)
            
    new_page += endNewTable()
    new_page += endFile
    
    save_code_file = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + "_" + str(save_code)
    
    if os.path.exists("/home/ubuntu/inv/static/save/" + type) == False:
        os.mkdir("/home/ubuntu/inv/static/save/" + type)
    
    new_page_save = open("static/save/" + type + '/' + str(save_code_file) + ".html", 'wt')
    f = new_page_save.write(new_page)
    new_page_save.close()
    
    return "http://inventory.bayonetchat.com/save/" + type + "/" + save_code_file
    
    