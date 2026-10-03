# Git ופרסום ב־GitHub

שם המאגר המוצע: **ha-ps-playtime-companion**

תיאור קצר להדבקה ב־GitHub:

> Home Assistant PS4 playtime schedules, quotas, quiet-hour reminders and a Bubble dashboard with weekly/monthly statistics.

Topics מוצעים: `home-assistant`, `blueprint`, `ps4`, `goldhen`, `bubble-card`, `parental-controls`, `hdmi-cec`.

## יצירת המאגר

1. צרו ב־GitHub מאגר ריק בשם המוצע. בחרו Public אם רצונכם לשתף; אל תסמנו יצירת README או license כי הקבצים כבר בחבילה.
2. פתחו PowerShell **בתיקיית החבילה בלבד**, ולא בתיקיית העבודה שמכילה גיבויי הבית.
3. התקינו Git אם אינו זמין. הריצו:

   ```powershell
   git init -b main
   python -m pip install -r requirements-dev.txt
   python -m unittest discover -s tests -v
   git add README.md LICENSE CHANGELOG.md requirements-dev.txt .gitignore .github blueprints dashboard packages examples tools tests docs
   git diff --cached --stat
   git diff --cached
   git commit -m "Add PS4 Playtime Companion dashboard and blueprints"
   git remote add origin https://github.com/NirBY/ha-ps-playtime-companion.git
   git push -u origin main
   ```

החליפו `YOUR_USERNAME` בשם המשתמש שלכם. אם Git מבקש זהות, הגדירו `git config user.name` ו־`git config user.email` עבור המאגר. התחברו ל־GitHub דרך מנגנון ההתחברות הרגיל; אין להוסיף token לקובץ או לכתובת ה־remote.

החבילה מכילה רק תבניות ודוגמאות כלליות. לפני פרסום התאמות אישיות, עברו על ה־diff: לא לפרסם כתובת HA פרטית, אסימונים, היסטוריית הבית, שמות בני משפחה או גיבויים. `dashboard/rendered.yaml` וקובצי secrets אינם נכללים ב־Git.

## קישורי ייבוא Blueprint

לאחר push, הקישורים יהיו (החליפו את שם המשתמש):

```text
https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/automation/ps4_playtime/enforce.yaml
https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/automation/ps4_playtime/reminders.yaml
https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/script/ps4_playtime/cec_rest.yaml
```

הדביקו כל קישור ב־Settings → Automations & scenes → Blueprints → Import Blueprint. לוח Bubble מיובא דרך Raw configuration editor, ולא דרך מסך Blueprints.

## עדכונים וגרסאות

```powershell
git switch -c improve-dashboard
# Edit files, then run the tests.
python -m unittest discover -s tests -v
git add <changed-files>
git commit -m "Describe the change"
git push -u origin improve-dashboard
```

פתחו Pull Request, עברו על השינויים ומזגו. לפרסום גרסה לאחר המיזוג:

```powershell
git switch main
git pull --ff-only
git tag v0.1.0
git push origin v0.1.0
```

צרו Release ב־GitHub עם הסבר על דרישות ההתקנה והבדיקות. אין צורך בפרסום ב־HACS: זו חבילת תצורה ו־Blueprints. ה־CI המצורף בודק מבנה וקובצי מיפוי, ולא מפעיל מכשירים.

## תרומות

צרפו גרסאות HA/Bubble, התנהגות צפויה ובפועל, שגיאה רלוונטית ללא סודות, ותרחיש שחזור. שינוי ב־CEC יש לבדוק פיזית על החומרה; בדיקת YAML לבדה אינה מוכיחה מצב מנוחה או שימור GoldHEN.
