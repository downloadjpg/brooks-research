## Hi! 
This is a project to automate filtering horse statistics from a PDF format into a spreadsheet using some simple Python code.

## Specifications:
We are only sampling from horses with 3 or more starts.

### From each PDF we need:
- the name of the foal
- how many starts they had
- the year they were born
- sex
- dam (mother) name
- dam sire (if possible)
- totals (how many win place and shows)
- career length (in years?)

![Diagram of PDF with circled fields.](diagrammed-data.bmp)


# Current Status:
- Trying to capture every single foal, no matter the race count. Currently at **1,314** total rows.
- This means approximately **5%** of entries are being lost, though I forget what the exact total count is.  

## Fields captured: (! = known issue)
- Name (!)
- Birthday 
- Sex 
- Dam name
- Dam year
- Dam SPR 
- Dam CPI
- Dam's sire name (!) 
- Dam's sire year (!)

## Remaining tasks:
- Calculate totals (need an exact definition of these, number of wins, places, and shows?)
- Calculate career length
- Get better capture percentage (ideally 100%!!)
- Test with other PDF files
- Export script into an executable file.

## Known Issues:
- Many foals contain a country tag, e.g. '(KOR).' Unsure if this needs to be removed.
- Haven't separated Dam's sire name from the year, this is the last field before race data so it is tricky.