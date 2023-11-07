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

```
Hotstufanthensome, 2000/01/30, b gelding -- Don't Read My Lips (1991) (SPR=92; CPI=5.8)
equineline.com Product 33P
Awesome Again 09/14/23 16:11:36 EDT
Bay Horse; Mar 29, 1994
Copyright © 2023 The Jockey Club Information Systems, Inc. Page 13 of 336
Turkoman (1982)
(SPR=94; CPI=9.2)
```

```
python
import main
with open('output/test.txt', 'w') as f:
    f.write(main.extract_body_text("input/AwesomeAgain.pdf"))
```

