import os
import zipfile
import sys
import subprocess
from multiprocessing import Pool, Manager
from tqdm import tqdm

# Color codes
reset = '\033[0m'
red = '\033[31m'
green = '\033[32m'
blue = '\x1b[38;2;40;139;168m'

def clear():
    """Clear the terminal screen based on OS."""
    if os.name == "posix":
        return os.system("clear")
    elif os.name in ("ce", "nt", "dos"):
        return os.system("cls")

def count_lines(file_path):
    """Efficiently count lines in a file without loading it into memory."""
    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        print(f'{red}+{reset} Dictionary file not found.')
        sys.exit(1)
    except Exception as e:
        print(f'{red}+{reset} Error reading dictionary file: {e}')
        sys.exit(1)

def read_dictionary_file(dictionary_path):
    """Generator function to yield lines from the dictionary file."""
    try:
        with open(dictionary_path, "r", encoding='latin-1') as dic:
            for line in dic:
                yield line.rstrip('\n')
    except FileNotFoundError:
        print(f'{red}+{reset} Dictionary file not found.')
        sys.exit(1)
    except Exception as e:
        print(f'{red}+{reset} Error reading dictionary file: {e}')
        sys.exit(1)

def test_7z_password(args):
    """Test a password for a .7z file using 7z command."""
    sevenzip_file, password, found_event = args
    if found_event.is_set():
        return None
    try:
        result = subprocess.call(
            f"7z t -p'{password}' '{sevenzip_file}'",
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            shell=True
        )
        if result == 0:
            found_event.set()
            return password
    except Exception:
        pass
    return None

def sevenzip():
    """Brute-force a .7z file using passwords from a dictionary file."""
    print('''
 {}   ___________
    \_____    /__________   _____________         ___________________    _____  _________  ____  __._____________________  
         /   / \____    /  |   \______   \        \_   ___ \______   \  /  _  \ \_   ___ \|    |/ _|\_   _____/\______   \ 
        /   /    __/___/__ |   ||     ___/        /    \  \/|       _/ /  /_\  \/    \  \/|      <   |    __)_  |       _/ 
       /   /      /   /___ |   ||    |      ---   \     \___|    |   \/    |    \     \___|    |  \  |        \ |    |   \ 
      /___/      /_______ \|___||____|             \______  /____|_  /\____|__  /\______  /____|__ \/_______  / |____|_  / 
                         \/                               \/       \/         \/        \/        \/        \/         \/  
 {}
    '''.format(blue, reset))

    sevenzip_file = input('   Enter the exact name of the .7z file ❯  ')
    print('   ')
    dictionary = input('   Enter the exact name of the dictionary file ❯  ')
    print('   ')

    # Count total lines for progress bar
    total_lines = count_lines(dictionary)
    
    # Initialize multiprocessing components
    manager = Manager()
    found_event = manager.Event()
    num_processes = os.cpu_count() or 4  # Use number of CPU cores, default to 4
    chunk_size = 100  # Process passwords in chunks to reduce overhead

    try:
        with Pool(processes=num_processes) as pool, tqdm(total=total_lines, desc="Testing passwords", unit="password") as pbar:
            # Prepare arguments for each password
            passwords = read_dictionary_file(dictionary)
            args = [(sevenzip_file, password, found_event) for password in passwords]
            
            # Process passwords in chunks
            for result in pool.imap_unordered(test_7z_password, args, chunksize=chunk_size):
                pbar.update(1)
                if result:
                    print(f'\n[{green}+{reset}] Password Found! : {result}\n')
                    pool.terminate()
                    return
            print(f'{red}+{reset} Password not found.')
    except KeyboardInterrupt:
        print(f'\n{red}+{reset} Operation cancelled by user.')
        pool.terminate()
    except Exception as e:
        print(f'{red}+{reset} Error during 7z brute-force: {e}')
    finally:
        pool.close()
        pool.join()

def zip():
    """Brute-force a .zip file using passwords from a dictionary file."""
    if os.name == 'posix' and os.getuid() != 0:
        print(f'Execute the script as {red}root{reset}')
        sys.exit(1)

    print('''
 {}           __________   _____________         ___________________    _____  _________  ____  __._____________________  
            \____    /  |   \______   \        \_   ___ \______   \  /  _  \ \_   ___ \|    |/ _|\_   _____/\______   \ 
              __/___/__ |   ||     ___/        /    \  \/|       _/ /  /_\  \/    \  \/|      <   |    __)_  |       _/ 
               /   /___ |   ||    |      ---   \     \___|    |   \/    |    \     \___|    |  \  |        \ |    |   \ 
              /_______ \|___||____|             \______  /____|_  /\____|__  /\______  /____|__ \/_______  / |____|_  / 
                      \/                               \/       \/         \/        \/        \/        \/         \/  
 {}
    '''.format(blue, reset))

    def test_zip_password(args):
        """Test a password for a .zip file."""
        zip_file_path, password, found_event = args
        if found_event.is_set():
            return None
        try:
            with zipfile.ZipFile(zip_file_path) as zip_file:
                zip_file.extractall(pwd=password.encode())
                found_event.set()
                return password
        except Exception:
            pass
        return None

    def zipmain():
        """Main function for ZIP brute-forcing."""
        zipname = input('   Enter the exact name of the .zip file ❯  ')
        print('   ')
        dicname = input('   Enter the exact name of the dictionary file ❯  ')
        print('   ')

        try:
            zipfile.ZipFile(zipname)  # Test if file is valid
        except FileNotFoundError:
            print(f'{red}+{reset} ZIP file not found.')
            return
        except Exception as e:
            print(f'{red}+{reset} Error opening ZIP file: {e}')
            return

        # Count total lines for progress bar
        total_lines = count_lines(dicname)
        
        # Initialize multiprocessing components
        manager = Manager()
        found_event = manager.Event()
        num_processes = os.cpu_count() or 4
        chunk_size = 100

        try:
            with Pool(processes=num_processes) as pool, tqdm(total=total_lines, desc="Testing passwords", unit="password") as pbar:
                # Prepare arguments for each password
                passwords = read_dictionary_file(dicname)
                args = [(zipname, password, found_event) for password in passwords]
                
                # Process passwords in chunks
                for result in pool.imap_unordered(test_zip_password, args, chunksize=chunk_size):
                    pbar.update(1)
                    if result:
                        print(f'\n[{green}+{reset}] Password Found! : {result}\n')
                        pool.terminate()
                        return
                print(f'{red}+{reset} Password not found.')
        except KeyboardInterrupt:
            print(f'\n{red}+{reset} Operation cancelled by user.')
            pool.terminate()
        except Exception as e:
            print(f'{red}+{reset} Error during ZIP brute-force: {e}')
        finally:
            pool.close()
            pool.join()

    zipmain()

def main():
    """Main menu for selecting brute-force option."""
    print('''
 {}
            ___________________    _____  _________  ____  __._____________________  
            \_   ___ \______   \  /  _  \ \_   ___ \|    |/ _|\_   _____/\______   \ 
            /    \  \/|       _/ /  /_\  \/    \  \/|      <   |    __)_  |       _/ 
            \     \___|    |   \/    |    \     \___|    |  \  |        \ |    |   \ 
             \______  /____|_  /\____|__  /\______  /____|__ \/_______  / |____|_  / 
                    \/       \/         \/        \/        \/        \/         \/  
 {}
                                    coded by viic w {}<3{}
    
                ┌──────────────────────────────────────────────────────────┐   
                │             ¿What do you want to Brute-Force?            │   
                ├──────────────────────────────────────────────────────────┤   
                │  [1]   .7z file                                          │   
                │  [2]   .zip file                                         │   
                │  [99]  {}EXIT{}, salirás del programa                    │   
                └──────────────────────────────────────────────────────────┘   
    
    '''.format(blue, reset, red, reset, red, reset))

    choice = input('   Opción ❯  ')
    if choice == '1':
        clear()
        sevenzip()
    elif choice == '2':
        clear()
        zip()
    elif choice == '99':
        clear()
        print(f'  See you soon {red}<3{reset} !')
        sys.exit(0)
    else:
        clear()
        main()

if __name__ == '__main__':
    clear()
    main()

