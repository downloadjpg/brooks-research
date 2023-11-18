
import os
import progressbar
import scripts.text_parser as Parser
import scripts.data_handler as Data
import scripts.writer as Writer
import scripts.messages as Messages


# Argument flags, used globally.
flag_text = False
flag_stats = False
flag_diffs = False 
flag_verbose = False

input_folder = 'input'
output_folder = 'output'

auto_quit = False

def main():
    print(Messages.welcome)

    program_loop = True
    while(program_loop):
        user_input = input("Enter a command: ")
        args = user_input.split()
        if args[0] == 'q':
            raise SystemExit(0)
        elif args[0] == 'run':
            set_flags(args)
            start(args)
        elif args[0] == 'h':
            print(Messages.help)
        elif args[0] == 'horse':
            print(Messages.horse)
        else:
            print("Command not found.")
        if (auto_quit):
            raise SystemExit(0)

def start(args):
    # Gather input files.
    #progressbar.streams.wrap_stderr()
    set_flags(args)
    os.makedirs(os.path.dirname(f'./{output_folder}'), exist_ok=True)
    os.makedirs(os.path.dirname(f'./{output_folder}'), exist_ok=True)
    files = os.listdir(input_folder)
    
    if len(files) == 0:
        print(Messages.no_files)
    log("%d files found in \'%s\'" % (len(files), input_folder))


    # Create a progress bar with a specific width
    pbar = progressbar.ProgressBar(
        term_width=80,
        max_value=len(files),
        max_error=False,
        redirect_stdout=True,
        widgets=[
            progressbar.Bar('=', '[', ']'),
            ' ', progressbar.Percentage(),
            ' ', #progressbar.Variable(name='current_task', format='\t{formatted_value}',width=30)
        ]
    )
    i = 0
    #pbar.variables['current_task'] = 'Initializing'
    #progressbar.streams.flush()
    pbar.start()
    for file in files:
        pbar.update(i)
        process_file(file, pbar)
        i += 1
    pbar.finish()
    print("Done!")
    
def process_file(file, pbar):

    # little macro for updating the progress bar because shit won't work unless i force it to.
    def update_task(task):
        pbar.variables['current_task'] = f'{task} \'{file}\'' 
        progressbar.streams.flush()
        pbar.update(pbar.currval)
        #pbar.update(pbar.currval - 1)

    path = input_folder + '/' + file

    # Read/filter text
    update_task('Parsing')
    text = Parser.extract_body_text(path, pbar)
    # Get data
    update_task('Extracting')
    foal_data = Data.extract_foal_data(text)
    # Write output
    update_task('Extracting')
    output_path = output_folder + '/csv/' + file + '.csv'
    Writer.write_csv(output_path, foal_data)

    # Optional writes
    if (flag_text):
        update_task('Dumping')
        output_path = output_folder + '/txt/' + file + '.txt'
        Writer.write_txt(output_path, text)
    if (flag_stats): # TODO: implement stats!
        update_task('Staticzing')
        return
    
        
    
def log(text):
    if flag_verbose:
        print(text)
    
def set_flags(args):
    global flag_text, flag_stats, flag_diffs, flag_verbose

    flag_text = bool( '-t' in args) or  bool( '--text' in args)
    flag_stats = bool( '-s' in args) or  bool( '--stats' in args)
    flag_diffs = bool( '-d' in args) or  bool( '--diff' in args) 
    flag_verbose = bool('-v' in args) or bool('--verbose' in args)

if __name__ == "__main__":
    main()