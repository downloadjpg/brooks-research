# Relevant naming rules
#### (from https://www.jockeyclub.com/pdfs/rule_book.pdf)



The following classes of names are not eligible for use:
1. Names consisting of more than 18 letters (spaces and punctuation marks count as letters);
2. Names consisting entirely of initials such as C.O.D., F.O.B., etc.;
3. Names ending in “filly,” “colt,” “stud,” “mare,” “stallion,” or any similar horse-related term;
4. Names consisting entirely of numbers. Numbers above thirty may be used if they are spelled out;
5. Names ending with a numerical designation such as 17 “2nd” or “3rd,” whether or not such a designation is spelled out;


# Breakdown of the REGEX.
The full pattern for a horse's info, before the table, looks like this: (bold = optional)


\[name\], \[DOB\], **\[color\]** \[gender\] -- \[dam name\] (\[dam year\]) **(SPR=\[Dam SPR\]; CPI=\[Dam CPI\])**

\[Dam Sire Name\] **(Country Code)** (Dam Sire Year)

> [!NOTE]
> Not sure what the newline or whitespace character is, might not matter?


## Examples
```
Ain't She Awesome, 2000/02/14, dk b/ filly -- Primarily (1988) (SPR=98; CPI=10.8)
Lord At War (ARG) (1980)
(SPR=96; CPI=4.3)
```

```
Awesome for Sure, 2000/04/30, ch filly -- Woodsy Meadow (1995) (SPR=86; CPI=2.2)
Meadowlake (1983)
(SPR=62; CPI=0.8)
```