import configparser
import os
import sys

try:
    from sync_my_photos import exif
except ImportError:
    curdir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(curdir, ".."))
    import exif


MonthStrs = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

def load_config():
    """Load from the configuration file "/etc/sync_my_photos.ini" configuration
    variables."""
    local_cfg = None
    config = configparser.ConfigParser()
    config.read(os.path.join("/etc", "sync_my_photos.ini"))
    sections = config.sections()
    for name in sections:
        if name.startswith("Local"):
            local_cfg = config["Local"]
    return local_cfg


def Warn_user(message):
    print("WARNING: %s" % message)
    while True:
        answer = input("Continue? (Y/N)").lower().strip()
        if answer[0] == 'y':
            return
        elif answer[0] == 'n':
            sys.exit(0)

def YesOrNo():
    while True:
        answer = input("(Y/N)").lower().strip()
        if answer[0] == 'y':
            return True
        elif answer[0] == 'n':
            return False

   
def Ask_user(message):
    print("INFO: %s" % message)
    return YesOrNo()


def Ask_rename(old_name, new_name):
    print("RENAME: %s to %s?" % (old_name, new_name))
    if YesOrNo():
        os.rename(old_name, new_name)
        return True
    return False

count = 0

def process_file(root, year, month, _file):
    global count
    idx = _file.rfind(".")
    if idx >= 0:
        extension = _file[idx:]
        if extension.lower() in (".jpg", ".jpeg"):
            count += 1
            sys.stdout.write("\r%i  " % count)
            pathname = os.path.join(root, _file)
            info = exif.Exif(pathname)
            if info.Year != year:
                print("%s year %d != year %d" % (_file, info.Year, year))
            if info.Month != month:
                print("%s month %d != month %d" % (_file, info.Month, month))
    pass


def check_month_folder_name(root, year, folder):
    """Month folder name should be XXXX_YY_ZZZ or XXXX_Misc"""
    if year is None:
        return None, -1

    idx = folder.find("_")
    if idx < 0:
        Warn_user("Incorrect Folder name '%s', should be either %04i_xx_xxx format or %04i_Misc" % (folder, year, year))
        return None, -1

    if folder[:idx] != "%04i" % year:
        if Ask_user("Incorrect folder name '%s' should start with matching year prefix of '%04i', fix?" % (folder, year)):
            new_name = ("%04i_" % year) + folder[idx:]
            if Ask_rename(os.path.join(root, folder), os.path.join(root, new_name)):
                return new_name, -1

    keep = folder[:idx+1]
    rest = folder[idx+1:]

    idx = rest.find("_")
    if idx < 0:
        if rest != "Misc":
            if rest.lower() == "misc":
                new_name = keep + "Misc"
                if Ask_user("Incorrect folder name '%s' should %s, fix?" % (folder, new_name)):
                    if Ask_rename(os.path.join(root, folder), os.path.join(root, new_name)):
                        return new_name, None
            else:
                Warn_user("Incorrect Folder name '%s', should be either %04i_xx_xxx format or %04i_Misc" \
                        % (folder, year, year))
        return None, 0
    
    month = int(rest[:idx])
    if (month < 1) or (month > 12):
        Warn_user("Month out of range %s, should be between 1 and 12" % rest[:idx])
        return None, 0

    if idx != 2:
        fix = Ask_user("Incorrect folder name '%s' month should be 2 digits, fix?" \
                        % folder)
        raise RuntimeError("TODO")
    keep = keep + rest[:idx+1]
    rest = rest[idx+1:]

    monthStr = rest
    if MonthStrs[month-1] != monthStr:
        if Ask_user("Incorrect folder name '%s' month str should %s not %s, fix?" \
                % (folder, MonthStrs[month-1], monthStr)):
            new_name = keep + MonthStrs[month-1]
            if Ask_rename(os.path.join(root, folder), os.path.join(root, new_name)):
                return new_name, month
    return None, month


def process_month_folder(root, year, folder):
    """Month folder name should be XXXX_YY_ZZZ"""
    new_name, month = check_month_folder_name(root, year, folder)
    if new_name:
        return process_month_folder(root, year, new_name)
    
    month_folder = os.path.join(root, folder)
    files = os.listdir(month_folder)
    for _file in files:
        if _file in (".", ".."):
            pass
        process_file(month_folder, year, month, _file)
            



def process_year_folder(root, folder):
    year = None
    if len(folder) != 4:
        Warn_user("Incorrect Folder name '%s', should be a 4 digit year" % folder)
    else:
        try:
            year = int(folder)
        except ValueError:
            Warn_user("Incorrect Folder name '%s', should be a year" % folder)

    year_folder = os.path.join(root, folder)
    folders = os.listdir(year_folder)
    for folder in folders:
        if folder in (".", ".."):
            pass
        pathname = os.path.join(year_folder, folder)
        if os.path.isdir(pathname):
            process_month_folder(year_folder, year, folder)
        elif folder.lower().endswith(".jpg"):
            process_file(year_folder, year, None, folder)






def run():
    local_cfg = load_config()
    photos_path = local_cfg["photo_path"]
    folders = os.listdir(photos_path)
    for folder in folders:
        if folder in (".", ".."):
            pass
        process_year_folder(photos_path, folder)


if __name__ == "__main__":
    run()
