import os 
 import sys 
  
  
 def set_action_output(name: str, value: str): 
     sys.stdout.write(f'::set-output name={name}::{value}\n') 
  
  
 def main(): 
     path = 'Themes'
     extension = '.wptp'
  
     path_count = 0 
     paths = '' 
     for root, dirs, files in os.walk(path): 
         for file in files: 
             if file.endswith(f'{extension}'): 
                 paths = paths + root + '/' + str(file) + ' ' 
                 path_count = path_count + 1 
  
     set_action_output('path_count', path_count) 
     set_action_output('paths', paths)  
  
     f = open('themes.wpdb', 'w')
     f.write(paths, 'w')
     print(paths)

     sys.exit(0) 
  
 if __name__ == "__main__": 
     main()
