# YNAB Wrapped
A (very) quick and dirty Dash app supplying some year end views on my finances that the native YNAB app doesn't supply.

The backend makes a call to the YNAB API and calculates some financial metrics used in feeding the Dash app, saving them locally as a `.csv`. The frontend reads in that `.csv` and builds out a Dash app aggregating those metrics in a way that tells our personal finance story on an annual basis over time. Strictly for personal use; this was not built with modularity in mind.

# Demo
Check out a (purposely obfuscated) demo. 
https://github.com/user-attachments/assets/b0df238e-d8a9-4620-88ac-e8d485d6ed7a

# A Note To Self
Future Kevin: You can run this from the terminal by navigating to your local copy of the repo via `cd` and `ls` and then running `python <local_path_to_ynab_wrapped_here>/ynab_wrapped.py`.
