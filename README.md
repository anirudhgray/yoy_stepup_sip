# Investment Growth Calculator

This Python script calculates and visualizes the growth of an investment portfolio over time. It supports various features including plotting growth with different SIP amounts, annual step-ups, and rates of return, as well as summarizing the investment growth in a table format.

## Features
- [x] Calculate Yearly Growth: Compute the portfolio value over time with specified SIP amounts, step-ups, and rates of return.
- [x] Plot Growth: Visualize the growth of the investment portfolio using Matplotlib, with options to customize colors, markers, and save the plot.
- [x] Show Summary: Generate a summary table of the investment growth for different parameters using Rich.

## How to use
```zsh
(>_>) python3 yoy_stepup_sip.py --help
                                                                                                                                                                          
 Usage: yoy_stepup_sip.py [OPTIONS] COMMAND [ARGS]...                                                                                                                     
                                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                         │
│ --help                        Show this message and exit.                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ plot-multiple-growths   Plot the growth of investment portfolio over time with different SIP amounts, step-ups, and rates of return.                                   │
│ show-summary            Show a summary table of investment growth.                                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```zsh
(>_>) python3 yoy_stepup_sip.py plot-multiple-growths --help
                                                                                                                                                                          
 Usage: yoy_stepup_sip.py plot-multiple-growths [OPTIONS]                                                                                                                 
                                                                                                                                                                          
 Plot the growth of investment portfolio over time with different SIP amounts, step-ups, and rates of return.                                                             
                                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --initial-lump-sum        FLOAT    Initial lump sum investment in INR [default: 700000]                                                                                │
│ --sip-amounts             TEXT     Comma-separated list of SIP amounts in INR [default: 70000,120000,250000]                                                           │
│ --step-ups                TEXT     Comma-separated list of annual step-up percentages [default: 0,10,15]                                                               │
│ --rates-of-return         TEXT     Comma-separated list of annual rates of return in percentage [default: 10,14,18]                                                    │
│ --years                   INTEGER  Number of years for the investment [default: 25]                                                                                    │
│ --colors                  TEXT     Comma-separated list of colors for the plots [default: None]                                                                        │
│ --markers                 TEXT     Comma-separated list of markers for the plots [default: None]                                                                       │
│ --save-as                 TEXT     File name to save the plot [default: None]                                                                                          │
│ --help                             Show this message and exit.                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```zsh
python3 yoy_stepup_sip.py show-summary --help
                                                                                                                                                                          
 Usage: yoy_stepup_sip.py show-summary [OPTIONS]                                                                                                                          
                                                                                                                                                                          
 Show a summary table of investment growth.                                                                                                                               
                                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --initial-lump-sum        FLOAT    Initial lump sum investment in INR [default: 700000]                                                                                │
│ --sip-amounts             TEXT     Comma-separated list of SIP amounts in INR [default: 70000,120000,250000]                                                           │
│ --step-ups                TEXT     Comma-separated list of annual step-up percentages [default: 0,10,15]                                                               │
│ --rates-of-return         TEXT     Comma-separated list of annual rates of return in percentage [default: 10,14,18]                                                    │
│ --years                   INTEGER  Number of years for the investment [default: 25]                                                                                    │
│ --help                             Show this message and exit.                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
