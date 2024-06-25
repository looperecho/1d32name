# ID32Name
A quick script with a basic terminal CLI, to batch rename `.mp3` files based on their ID3 tags.

## Process
- When prompted, input the directory containing source files e.g:
`/Users/username/path/to/files`  
- A config file `config.json` is stored in `/Users/username/Library/Application Support/id32name`  
    - You can edit the source directory path by editing this file.
    - There is an `example_config.json` in the repo.
- ID3 tags `artist` and `title` will be read for all `.mp3` files in the directory.  

- The files will be renamed as: `Artist - Title`  



>Note: Just using this repo as a backup