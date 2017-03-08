import sqlite3, os, io
import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw() #use to hide tkinter window

currdir = os.getcwd()
appDir = os.getenv('APPDATA') + r'\Skype'
print appDir
tempDir = tkFileDialog.askdirectory(parent=root, initialdir=appDir, title='Select your Skype user directory')
if len(tempDir) > 0:
    print "You chose %s" % tempDir
    inFile = tempDir
else:
    exit(0)
tempDir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Select your output directory')
if len(tempDir) > 0:
    print "You chose %s" % tempDir
    outFile = tempDir
else:
    exit(0)

con = sqlite3.connect(inFile + r'\main.db')
c= con.cursor()
c.execute('SELECT DISTINCT author FROM messages')
uniqueFroms = list(c.fetchall())
for author in uniqueFroms:
    print "making history file for " + author[0] + "..."
    c.execute('SELECT datetime(timestamp, \'unixepoch\', \'localtime\'), body_xml FROM messages WHERE author = ? ORDER BY timestamp DESC', author)
    result = c.fetchall()
    newFile = outFile + '\\' + author[0] + ".txt"
    dir = os.path.dirname(newFile)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with io.open(newFile, mode='w+', encoding='utf-8') as f:
        for row in result:
            f.write(row[0] + ": ")
            if row[1] is not None:
                f.write(row[1])
            f.write(u"\n")
        


### this is for more advance grouping if I can figure it out. for now just group by author
#c.execute("SELECT DISTINCT convo_id FROM messages")
#uniqueChats = list(c.fetchall())
#print uniqueChats
#for convoID in uniqueChats:
#    c.execute('SELECT participants FROM chats WHERE conv_dbid = ?', convoID)
#    print "Convo ID: " + str(convoID) + str(c.fetchone())
