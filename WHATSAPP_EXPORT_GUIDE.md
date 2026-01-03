# How to Export WhatsApp Chat to Text File

WhatsApp has a built-in feature to export chats as text files. It's completely free and easy!

## 📱 On iPhone

### Method 1: Export Chat
1. Open WhatsApp
2. Go to the chat you want to export
3. Tap the contact/group name at the top
4. Scroll down and tap **"Export Chat"**
5. Choose **"Without Media"** (faster, smaller file) or **"Attach Media"** (includes images)
6. Select where to save:
   - **Mail** - Email it to yourself
   - **Files** - Save to iCloud Drive or local files
   - **AirDrop** - Send to your Mac
   - **Notes** - Save in Apple Notes

### Result:
You'll get a `.txt` file named like: `WhatsApp Chat with [Contact Name].txt`

---

## 📱 On Android

### Method 1: Export Chat
1. Open WhatsApp
2. Go to the chat you want to export
3. Tap the three dots (⋮) in the top right
4. Tap **"More"**
5. Tap **"Export chat"**
6. Choose **"Without media"** or **"Include media"**
7. Select where to save:
   - **Gmail** - Email it to yourself
   - **Google Drive** - Save to cloud
   - **Save to device** - Local storage

### Result:
You'll get a `.txt` file that you can access from your computer

---

## 💻 Transfer to Computer

### From iPhone:
- **AirDrop** to Mac (easiest)
- **Email** to yourself and download
- **iCloud Drive** - Access from any device
- **USB Cable** - Connect and use Finder/iTunes

### From Android:
- **Email** to yourself
- **Google Drive** - Access from any browser
- **USB Cable** - Connect and browse files
- **Cloud storage** (Dropbox, OneDrive, etc.)

---

## 📄 What the Export Looks Like

The exported file is a plain text file with format:
```
[DD/MM/YYYY, HH:MM:SS] Contact Name: Message text
[DD/MM/YYYY, HH:MM:SS] Your Name: Your message
[DD/MM/YYYY, HH:MM:SS] Contact Name: Another message
```

Example:
```
[15/05/2024, 09:30:15] John: I got 3 today!
[15/05/2024, 09:31:22] Mary: Nice! I got 4
[15/05/2024, 09:32:10] John: What about you Bob?
[15/05/2024, 09:33:45] Bob: 5 for me
```

---

## 🔧 Post-Processing the Export

Once you have the text file, you can:

### 1. Parse Wordle Scores
Create a Python script to extract scores:

```python
import re

def extract_wordle_scores(whatsapp_file):
    """Extract Wordle scores from WhatsApp export"""
    with open(whatsapp_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match Wordle scores (adjust as needed)
    # Looks for numbers 1-6 or "X" (failed)
    pattern = r'\[(\d{2}/\d{2}/\d{4}), \d{2}:\d{2}:\d{2}\] ([^:]+): .*?(\d|X)'
    
    matches = re.findall(pattern, content)
    
    for date, name, score in matches:
        print(f"{date} - {name}: {score}")

# Usage
extract_wordle_scores('WhatsApp Chat with Wordle Group.txt')
```

### 2. Convert to CSV
```python
import csv
import re

def whatsapp_to_csv(input_file, output_file):
    """Convert WhatsApp export to CSV"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Time', 'Name', 'Message'])
        
        for line in lines:
            match = re.match(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.+)', line)
            if match:
                date, time, name, message = match.groups()
                writer.writerow([date, time, name.strip(), message.strip()])

# Usage
whatsapp_to_csv('WhatsApp Chat.txt', 'chat_export.csv')
```

### 3. Search for Specific Content
```python
def search_messages(whatsapp_file, keyword):
    """Search for messages containing a keyword"""
    with open(whatsapp_file, 'r', encoding='utf-8') as f:
        for line in f:
            if keyword.lower() in line.lower():
                print(line.strip())

# Usage
search_messages('WhatsApp Chat.txt', 'wordle')
```

---

## 📊 Limitations

- **Maximum messages**: 40,000 messages per export (usually enough)
- **Media**: Images/videos are separate files if included
- **Deleted messages**: Won't appear in export
- **Formatting**: Plain text only, no formatting preserved

---

## 💡 Tips

1. **Export regularly** if you want to keep history (WhatsApp doesn't keep forever)
2. **Without media** is faster and creates smaller files
3. **Backup first** - Export doesn't delete anything from WhatsApp
4. **Privacy** - Be careful with exported files, they contain full chat history
5. **Encoding** - Files are UTF-8, which handles emojis and special characters

---

## 🔐 Privacy & Security

- Exported files are **not encrypted**
- Store them securely
- Don't share unless necessary
- Delete after processing if sensitive

---

## Alternative: Third-Party Tools

If you need more features:
- **WA Backup Extractor** (paid, more features)
- **iMazing** (iOS, paid)
- **Dr.Fone** (paid, data recovery)

But the built-in export is usually sufficient and completely free!