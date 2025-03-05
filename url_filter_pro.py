import os
import readline
import sys
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Style, init

init()

def display_banner():
    colors = [ Fore.BLUE ]
    banner_lines = [
        "███████╗  ██╗  ██╗  ██████╗  ███████╗ ██╗  ███████╗ ",
        "██╔════╝  ██║  ██║ ██╔═══██╗ ██╔══██╝ ██║  ██╔════╝ ",
        "███████╗  ███████║ ██║   ██║ ███████╗ ██║  ███████╗ ",
        "╚════██║  ██╔══██║ ██║   ██║ ██╔══██║ ██║  ██╔════╝ ",
        "███████║  ██║  ██║ ╚██████╔╝ ██║  ██║ ██║  ██║      ",
        "╚══════╝  ╚═╝  ╚═╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝  "
    ]
    for i, line in enumerate(banner_lines):
        print(colors[i % len(colors)] + line + Style.RESET_ALL)

def get_input_file():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    while True:
        try:
            input_file = input(Fore.CYAN + "Enter input file name: " + Style.RESET_ALL).strip()
            if not input_file:
                print(Fore.RED + "Input file is required." + Style.RESET_ALL)
                continue
            if not os.path.exists(input_file):
                print(Fore.RED + f"File {input_file} does not exist." + Style.RESET_ALL)
                continue
            return input_file
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)

def get_output_file():
    default_output = 'safilter.txt'
    try:
        output_file = input(Fore.CYAN + f"Enter output file name (default: {default_output}): " + Style.RESET_ALL).strip()
        return output_file if output_file else default_output
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

def filter_keyword_based(urls, keywords):
    non_keyword_urls = []
    keyword_urls = []
    for url in urls:
        if any(k in url for k in keywords):
            keyword_urls.append(url)
        else:
            non_keyword_urls.append(url)
    
    keyword_assigned = {}
    selected_urls = set()
    for keyword in keywords:
        for url in keyword_urls:
            if keyword in url:
                if keyword not in keyword_assigned:
                    keyword_assigned[keyword] = url
                    selected_urls.add(url)
                    break
    
    output_urls = non_keyword_urls + list(selected_urls)
    return output_urls, len(non_keyword_urls), len(selected_urls)

def filter_parameter_based(urls):
    param_dict = {}
    for url in urls:
        parsed = urlparse(url)
        query = parsed.query
        params = parse_qs(query)
        for param in params.keys():
            if param not in param_dict:
                param_dict[param] = url
    output_urls = list(param_dict.values())
    return output_urls, len(param_dict)

def filter_keyword_in_params(urls, keywords):
    selected_urls = []
    for url in urls:
        parsed = urlparse(url)
        query = parsed.query
        params = parse_qs(query)
        found = False
        for name, values in params.items():
            if any(k in name for k in keywords):
                found = True
                break
            for v in values:
                if any(k in v for k in keywords):
                    found = True
                    break
            if found:
                break
        if found:
            selected_urls.append(url)
    return selected_urls, len(selected_urls)

def filter_parameter_presence(urls):
    param_urls = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.query:
            param_urls.append(url)
    return param_urls, len(param_urls)

def main():
    try:
        display_banner()
        print(Fore.YELLOW + "\nOptions:")
        print("[1] Keyword-based Filtering")
        print("[2] Parameter-based Filtering")
        print("[3] Keyword-based Filtering in Parameters")
        print("[4] Filter URLs with Parameters")
        print(Style.RESET_ALL)
        
        while True:
            try:
                choice = input(Fore.CYAN + "Select an option (1-4): " + Style.RESET_ALL).strip()
                if choice not in ['1', '2', '3', '4']:
                    print(Fore.RED + "Invalid option. Please choose 1-4." + Style.RESET_ALL)
                else:
                    break
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)

        input_file = get_input_file()
        output_file = get_output_file()
        
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        total_urls = len(urls)
        
        if choice == '1':
            keywords_input = input(Fore.CYAN + "Enter keywords (comma-separated): " + Style.RESET_ALL).strip()
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            if not keywords:
                print(Fore.RED + "No keywords provided. Exiting." + Style.RESET_ALL)
                return
            print(Fore.YELLOW + "Processing keyword-based filtering..." + Style.RESET_ALL)
            output_urls, non_keyword_count, selected_count = filter_keyword_based(urls, keywords)
        elif choice == '2':
            print(Fore.YELLOW + "Processing parameter-based filtering..." + Style.RESET_ALL)
            output_urls, param_count = filter_parameter_based(urls)
        elif choice == '3':
            keywords_input = input(Fore.CYAN + "Enter keywords (comma-separated): " + Style.RESET_ALL).strip()
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            if not keywords:
                print(Fore.RED + "No keywords provided. Exiting." + Style.RESET_ALL)
                return
            print(Fore.YELLOW + "Processing keyword in parameters filtering..." + Style.RESET_ALL)
            output_urls, selected_count = filter_keyword_in_params(urls, keywords)
        elif choice == '4':
            print(Fore.YELLOW + "Filtering URLs with parameters..." + Style.RESET_ALL)
            output_urls, param_count = filter_parameter_presence(urls)
        
        with open(output_file, 'w') as f:
            for url in output_urls:
                f.write(url + '\n')
        
        # Display results in terminal
        print(Fore.GREEN + "\nFilter Results:")
        for url in output_urls:
            print(Fore.WHITE + url)
        
        print(Fore.GREEN + "\nFiltering Summary:")
        print(f"Total URLs analyzed: {total_urls}")
        if choice == '1':
            print(f"Keywords used: {', '.join(keywords)}")
            print(f"Non-keyword URLs kept: {non_keyword_count}")
            print(f"Keyword-based URLs selected: {selected_count}")
        elif choice == '2':
            print(f"Unique parameters found: {param_count}")
        elif choice == '3':
            print(f"Keywords used in parameters: {', '.join(keywords)}")
            print(f"URLs containing keywords in parameters: {selected_count}")
        elif choice == '4':
            print(f"URLs with parameters found: {len(output_urls)}")
        print(f"Total URLs written to {output_file}: {len(output_urls)}")
        print(Style.RESET_ALL)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()