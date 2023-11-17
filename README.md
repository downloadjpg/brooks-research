
# Description
This script imports all pdfs in the 'Input' folder, expecting them to be in the format from [equineline.com](https://equineline.com).

## Current Status:
The script will run for any number of pdf files, but I've only tested Awesome Again thoroughly. Outputs are regularly put in the Google Drive when I can :D
### Catch rate
Trying to capture every single foal, no matter the race count. Currently at **1,314** total rows for Awesome Again.
This means approximately **5%** of entries are being lost, though I forget what the exact total count is.
  


## Known Issues:
- Many foals contain a country tag, e.g. '(KOR).' This can cause problems down the line if other data sets do/do not contain it.
  - Currently, it breaks a lot of entries as the pattern relies on the birth year being the only thing in parentheses.
- Page breaks introduce many issues. Headers/footers are complicated, and my current method of filtering them out (scanner obj) is slowing everything down by a ton.


## Remaining tasks:
- [ ] Export application
	- [ ] Outputs
		- [ ] Diffs
		- [ ] Statistics
			- [ ] Total catch rate
			- [ ] Individual variable catch rates?
		- [ ] PDF Text dumps
	- [ ] Github Actions
		- [ ] Export and compile to CLI tool, put download link in README.
		- [ ] Rewrite README.
- [ ] Debugging
	- [ ] Page break issues
	- [ ] Header/Subheader issues
  
- [ ] Optimize header/subheader removal
	- [ ] Test regex vs Scanner object
- [ ] Scores (sorry)
